#!/usr/bin/env python3
"""Read-only Birdeye token-risk radar.

The radar fetches public market/security data through Birdeye only. It never
loads wallet keys, signs transactions, builds transactions, or submits orders.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_BASE_URL = "https://public-api.birdeye.so"
DEFAULT_CHAIN = "solana"
DEFAULT_LIMIT = 10
DEFAULT_MIN_LIQUIDITY_USD = 1_000.0
DEFAULT_REPORT = Path("birdeye-radar.md")
DEFAULT_JSONL = Path("birdeye-radar.jsonl")
DEFAULT_REQUEST_INTERVAL_SECONDS = 1.1

ENDPOINTS = {
    "new_listing": "/defi/v2/tokens/new_listing",
    "token_market_data": "/defi/v3/token/market-data",
    "token_security": "/defi/token_security",
    "token_trending": "/defi/token_trending",
}


class BirdeyeRadarError(RuntimeError):
    """A safe, operator-facing error that must not include secrets."""


class BirdeyeHttpError(BirdeyeRadarError):
    """HTTP error from Birdeye with status metadata for safe retry handling."""

    def __init__(self, status_code: int, message: str, retry_after_seconds: float | None = None) -> None:
        super().__init__(message)
        self.status_code = status_code
        self.retry_after_seconds = retry_after_seconds


class BirdeyeClient:
    """Rate-limited live Birdeye client that tracks calls without exposing keys."""

    def __init__(
        self,
        *,
        base_url: str,
        api_key: str,
        chain: str,
        timeout_seconds: float,
        request_interval_seconds: float,
    ) -> None:
        self.base_url = base_url
        self.api_key = api_key
        self.chain = chain
        self.timeout_seconds = timeout_seconds
        self.request_interval_seconds = request_interval_seconds
        self.call_count = 0
        self.endpoint_counts: dict[str, int] = {}
        self._last_request_started_at: float | None = None

    def fetch(self, endpoint: str, params: dict[str, str | int | bool | None]) -> dict[str, Any]:
        payload = self._fetch_with_retry(endpoint, params)
        self.call_count += 1
        self.endpoint_counts[endpoint] = self.endpoint_counts.get(endpoint, 0) + 1
        return payload

    def _fetch_with_retry(self, endpoint: str, params: dict[str, str | int | bool | None]) -> dict[str, Any]:
        attempts = 0
        while True:
            if self._last_request_started_at is not None:
                elapsed = time.monotonic() - self._last_request_started_at
                remaining = self.request_interval_seconds - elapsed
                if remaining > 0:
                    time.sleep(remaining)

            self._last_request_started_at = time.monotonic()
            try:
                return fetch_json(
                    base_url=self.base_url,
                    endpoint=endpoint,
                    params=params,
                    api_key=self.api_key,
                    chain=self.chain,
                    timeout_seconds=self.timeout_seconds,
                )
            except BirdeyeHttpError as exc:
                if exc.status_code != 429 or attempts >= 3:
                    raise
                attempts += 1
                retry_after = exc.retry_after_seconds or (5.0 * attempts)
                time.sleep(max(retry_after, self.request_interval_seconds))


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def safe_float(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def first_present(values: dict[str, Any], keys: list[str]) -> Any:
    for key in keys:
        if key in values and values[key] not in (None, ""):
            return values[key]
    return None


def markdown_escape(value: object) -> str:
    return str(value).replace("|", "/").replace("\n", " ")


def request_url(base_url: str, endpoint: str, params: dict[str, str | int | bool | None]) -> str:
    cleaned = {key: value for key, value in params.items() if value is not None}
    encoded = urllib.parse.urlencode({key: str(value).lower() if isinstance(value, bool) else value for key, value in cleaned.items()})
    if not encoded:
        return base_url.rstrip("/") + endpoint
    return f"{base_url.rstrip('/')}{endpoint}?{encoded}"


def parse_retry_after(value: str | None) -> float | None:
    if not value:
        return None
    try:
        return max(0.0, float(value))
    except ValueError:
        return None


def http_error_message(exc: urllib.error.HTTPError) -> str:
    body = exc.read(500).decode("utf-8", errors="replace").strip()
    if not body:
        return f"Birdeye API HTTP error: {exc.code}"
    detail = body
    try:
        payload = json.loads(body)
    except json.JSONDecodeError:
        payload = None
    if isinstance(payload, dict):
        candidate = first_present(payload, ["message", "error", "msg", "detail"])
        if candidate:
            detail = str(candidate)
    return f"Birdeye API HTTP error: {exc.code}; detail: {detail[:240]}"


def fetch_json(
    *,
    base_url: str,
    endpoint: str,
    params: dict[str, str | int | bool | None],
    api_key: str,
    chain: str,
    timeout_seconds: float,
) -> dict[str, Any]:
    request = urllib.request.Request(
        request_url(base_url, endpoint, params),
        headers={
            "accept": "application/json",
            "user-agent": "birdeye-risk-radar/0.1",
            "x-chain": chain,
            "X-API-KEY": api_key,
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        raise BirdeyeHttpError(
            exc.code,
            http_error_message(exc),
            retry_after_seconds=parse_retry_after(exc.headers.get("Retry-After")),
        ) from exc
    except urllib.error.URLError as exc:
        raise BirdeyeRadarError(f"Birdeye API connection error: {exc.reason}") from exc
    except TimeoutError as exc:
        raise BirdeyeRadarError("Birdeye API request timed out") from exc
    except json.JSONDecodeError as exc:
        raise BirdeyeRadarError("Birdeye API returned malformed JSON") from exc

    if payload.get("success") is False:
        raise BirdeyeRadarError("Birdeye API returned success=false")
    return payload


def extract_tokens(payload: dict[str, Any]) -> list[dict[str, Any]]:
    data = payload.get("data", payload)
    if isinstance(data, list):
        return [item for item in data if isinstance(item, dict)]
    if not isinstance(data, dict):
        return []
    for key in ("tokens", "items", "list", "result"):
        value = data.get(key)
        if isinstance(value, list):
            return [item for item in value if isinstance(item, dict)]
    return []


def normalize_token(raw: dict[str, Any], source: str) -> dict[str, Any]:
    address = first_present(raw, ["address", "tokenAddress", "mint", "token_address"])
    if address is None:
        raise BirdeyeRadarError("token record lacks an address")
    liquidity = safe_float(first_present(raw, ["liquidity", "liquidityUSD", "liquidity_usd"]))
    volume_24h = safe_float(first_present(raw, ["volume24hUSD", "v24hUSD", "volumeUSD", "volume_usd_24h"]))
    return {
        "address": str(address),
        "symbol": str(first_present(raw, ["symbol", "tokenSymbol"]) or "unknown"),
        "name": str(first_present(raw, ["name", "tokenName"]) or "unknown"),
        "liquidity_usd": liquidity,
        "volume_24h_usd": volume_24h,
        "rank": first_present(raw, ["rank", "marketCapRank"]),
        "source": source,
        "raw_keys": sorted(raw.keys()),
    }


def merge_token_records(token_lists: list[list[dict[str, Any]]]) -> list[dict[str, Any]]:
    merged: dict[str, dict[str, Any]] = {}
    for tokens in token_lists:
        for token in tokens:
            address = token["address"]
            if address not in merged:
                merged[address] = dict(token)
                continue

            existing = merged[address]
            sources = set(str(existing["source"]).split(","))
            sources.update(str(token["source"]).split(","))
            existing["source"] = ",".join(sorted(sources))
            if existing.get("liquidity_usd") is None and token.get("liquidity_usd") is not None:
                existing["liquidity_usd"] = token["liquidity_usd"]
            if existing.get("volume_24h_usd") is None and token.get("volume_24h_usd") is not None:
                existing["volume_24h_usd"] = token["volume_24h_usd"]
            if existing.get("rank") is None and token.get("rank") is not None:
                existing["rank"] = token["rank"]
    return list(merged.values())


def security_data(payload: dict[str, Any]) -> dict[str, Any]:
    data = payload.get("data", payload)
    return data if isinstance(data, dict) else {}


def security_flag_present(security: dict[str, Any], keys: list[str]) -> bool:
    value = first_present(security, keys)
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() not in ("", "0", "false", "none", "null", "no")
    return value not in (None, 0)


def assess_token(
    token: dict[str, Any],
    security: dict[str, Any] | None,
    *,
    min_liquidity_usd: float,
    trending_addresses: set[str],
) -> dict[str, Any]:
    flags: list[str] = []
    warnings: list[str] = []

    liquidity = token.get("liquidity_usd")
    if liquidity is None:
        warnings.append("missing-liquidity")
    elif liquidity < min_liquidity_usd:
        warnings.append(f"liquidity-below-{int(min_liquidity_usd)}-usd")

    if token["address"] not in trending_addresses:
        warnings.append("not-in-trending-sample")

    if not security:
        warnings.append("missing-security-data")
    else:
        if security_flag_present(security, ["is_scam", "isScam", "fake", "isFake", "honeypot", "isHoneypot"]):
            flags.append("scam-or-honeypot-flag")
        if security_flag_present(security, ["freezeAuthority", "freeze_authority", "freezable", "isFreezable"]):
            flags.append("freeze-authority-present")
        if security_flag_present(security, ["mintAuthority", "mint_authority", "mintable", "isMintable"]):
            flags.append("mint-authority-present")
        if security_flag_present(security, ["mutableMetadata", "mutable_metadata", "isMutable"]):
            warnings.append("mutable-metadata")

        top10_holder_percent = safe_float(first_present(security, ["top10HolderPercent", "top10_holder_percent", "top10HolderRatio"]))
        if top10_holder_percent is not None:
            normalized_percent = top10_holder_percent * 100 if top10_holder_percent <= 1 else top10_holder_percent
            if normalized_percent >= 50:
                flags.append("top10-holders-over-50pct")
            elif normalized_percent >= 25:
                warnings.append("top10-holders-over-25pct")

        sell_tax = safe_float(first_present(security, ["sellTax", "sell_tax", "sellTaxRate"]))
        if sell_tax is not None and sell_tax > 0:
            warnings.append("sell-tax-present")

    if flags:
        classification = "reject"
    elif warnings:
        classification = "research"
    else:
        classification = "watch"

    return {
        "address": token["address"],
        "symbol": token["symbol"],
        "name": token["name"],
        "source": token["source"],
        "liquidity_usd": liquidity,
        "volume_24h_usd": token.get("volume_24h_usd"),
        "classification": classification,
        "risk_flags": flags,
        "warnings": warnings,
    }


def fixture_payloads() -> dict[str, Any]:
    safe_address = "Safe111111111111111111111111111111111111111"
    risky_address = "Risk111111111111111111111111111111111111111"
    return {
        "new_listing": {
            "success": True,
            "data": {
                "tokens": [
                    {
                        "address": safe_address,
                        "symbol": "SAFE",
                        "name": "Fixture Safe",
                        "liquidity": 42_000,
                        "volume24hUSD": 210_000,
                    },
                    {
                        "address": risky_address,
                        "symbol": "RISK",
                        "name": "Fixture Risk",
                        "liquidity": 120,
                        "volume24hUSD": 9_000,
                    },
                ]
            },
        },
        "token_trending": {
            "success": True,
            "data": {
                "tokens": [
                    {
                        "address": safe_address,
                        "symbol": "SAFE",
                        "name": "Fixture Safe",
                        "liquidity": 42_000,
                        "volume24hUSD": 210_000,
                        "rank": 1,
                    }
                ]
            },
        },
        "security": {
            safe_address: {
                "success": True,
                "data": {
                    "freezeAuthority": None,
                    "mintAuthority": None,
                    "mutableMetadata": False,
                    "top10HolderPercent": 0.18,
                    "sellTax": 0,
                },
            },
            risky_address: {
                "success": True,
                "data": {
                    "freezeAuthority": "FreezeAuthority11111111111111111111111",
                    "mintAuthority": "MintAuthority1111111111111111111111111",
                    "mutableMetadata": True,
                    "top10HolderPercent": 0.76,
                    "sellTax": 5,
                },
            },
        },
    }


def collect_fixture_records(min_liquidity_usd: float, timestamp: str | None = None) -> dict[str, Any]:
    fixtures = fixture_payloads()
    new_tokens = [normalize_token(token, "new_listing") for token in extract_tokens(fixtures["new_listing"])]
    trending_tokens = [normalize_token(token, "token_trending") for token in extract_tokens(fixtures["token_trending"])]
    trending_addresses = {token["address"] for token in trending_tokens}
    assessments = [
        assess_token(
            token,
            security_data(fixtures["security"].get(token["address"], {})),
            min_liquidity_usd=min_liquidity_usd,
            trending_addresses=trending_addresses,
        )
        for token in new_tokens
    ]
    return build_record(
        timestamp=timestamp or utc_timestamp(),
        mode="fixture",
        chain=DEFAULT_CHAIN,
        call_count=2 + len(new_tokens),
        endpoint_counts={
            ENDPOINTS["new_listing"]: 1,
            ENDPOINTS["token_trending"]: 1,
            ENDPOINTS["token_security"]: len(new_tokens),
        },
        endpoint_errors=[],
        endpoints=list(ENDPOINTS.values()),
        new_tokens=new_tokens,
        trending_tokens=trending_tokens,
        assessments=assessments,
        qualification_complete=False,
        notes=["Fixture output only. Not live Birdeye evidence."],
    )


def collect_live_records(
    *,
    base_url: str,
    api_key: str,
    chain: str,
    limit: int,
    min_liquidity_usd: float,
    timeout_seconds: float,
    meme_platform_enabled: bool,
    target_call_count: int,
    request_interval_seconds: float,
) -> dict[str, Any]:
    client = BirdeyeClient(
        base_url=base_url,
        api_key=api_key,
        chain=chain,
        timeout_seconds=timeout_seconds,
        request_interval_seconds=request_interval_seconds,
    )
    endpoint_errors: list[dict[str, str | int]] = []
    new_listing_params: dict[str, str | int | bool | None] = {"limit": limit}
    if meme_platform_enabled:
        new_listing_params["meme_platform_enabled"] = True

    new_payload = client.fetch(ENDPOINTS["new_listing"], new_listing_params)
    trending_payload = client.fetch(
        ENDPOINTS["token_trending"],
        {"sort_by": "rank", "sort_type": "asc", "interval": "24h", "offset": 0, "limit": limit},
    )

    new_tokens = [normalize_token(token, "new_listing") for token in extract_tokens(new_payload)]
    trending_tokens = [normalize_token(token, "token_trending") for token in extract_tokens(trending_payload)]
    trending_addresses = {token["address"] for token in trending_tokens}

    candidates = merge_token_records([new_tokens, trending_tokens]) if target_call_count else new_tokens
    security_by_address: dict[str, dict[str, Any]] = {}
    security_unavailable = False
    market_data_by_address: dict[str, dict[str, Any]] = {}
    market_data_unavailable = False
    extra_trending_pages = 0

    def fetch_security_for(token: dict[str, Any]) -> None:
        nonlocal security_unavailable
        if security_unavailable:
            return
        if token["address"] in security_by_address:
            return
        try:
            security_by_address[token["address"]] = client.fetch(
                ENDPOINTS["token_security"],
                {"address": token["address"]},
            )
        except BirdeyeHttpError as exc:
            if exc.status_code not in (401, 403):
                raise
            security_unavailable = True
            endpoint_errors.append(
                {
                    "endpoint": ENDPOINTS["token_security"],
                    "status_code": exc.status_code,
                    "detail": str(exc),
                }
            )

    def fetch_market_data_for(token: dict[str, Any]) -> None:
        nonlocal market_data_unavailable
        if market_data_unavailable:
            return
        if token["address"] in market_data_by_address:
            return
        try:
            market_data_by_address[token["address"]] = client.fetch(
                ENDPOINTS["token_market_data"],
                {"address": token["address"]},
            )
        except BirdeyeHttpError as exc:
            if exc.status_code not in (401, 403):
                raise
            market_data_unavailable = True
            endpoint_errors.append(
                {
                    "endpoint": ENDPOINTS["token_market_data"],
                    "status_code": exc.status_code,
                    "detail": str(exc),
                }
            )

    for token in candidates:
        fetch_security_for(token)
        if target_call_count and client.call_count < target_call_count:
            fetch_market_data_for(token)

    offset = limit
    while target_call_count and client.call_count < target_call_count:
        extra_payload = client.fetch(
            ENDPOINTS["token_trending"],
            {"sort_by": "rank", "sort_type": "asc", "interval": "24h", "offset": offset, "limit": limit},
        )
        extra_trending_pages += 1
        extra_trending_tokens = [
            normalize_token(token, "token_trending")
            for token in extract_tokens(extra_payload)
        ]
        if not extra_trending_tokens:
            break
        trending_tokens = merge_token_records([trending_tokens, extra_trending_tokens])
        trending_addresses = {token["address"] for token in trending_tokens}
        candidates = merge_token_records([candidates, extra_trending_tokens])
        for token in candidates:
            if client.call_count >= target_call_count:
                break
            fetch_security_for(token)
            if client.call_count >= target_call_count:
                break
            fetch_market_data_for(token)
        offset += limit

    assessments = []
    for token in candidates:
        security_payload = security_by_address.get(token["address"])
        assessments.append(
            assess_token(
                token,
                security_data(security_payload) if security_payload is not None else None,
                min_liquidity_usd=min_liquidity_usd,
                trending_addresses=trending_addresses,
            )
        )

    return build_record(
        timestamp=utc_timestamp(),
        mode="live",
        chain=chain,
        call_count=client.call_count,
        endpoint_counts=client.endpoint_counts,
        endpoint_errors=endpoint_errors,
        endpoints=list(ENDPOINTS.values()),
        new_tokens=new_tokens,
        trending_tokens=trending_tokens,
        assessments=assessments,
        qualification_complete=client.call_count >= max(50, target_call_count),
        notes=[
            "Read-only Birdeye calls only.",
            "Qualification for the Sprint 4 listing requires at least 50 successful API calls before submission.",
            f"Live requests were rate-limited to at most one call every {request_interval_seconds:.2f} seconds.",
            f"Extra trending pages fetched for call target: {extra_trending_pages}.",
            "Token-security data is used when the current API package permits it; otherwise tokens remain research-only.",
        ],
    )


def build_record(
    *,
    timestamp: str,
    mode: str,
    chain: str,
    call_count: int,
    endpoint_counts: dict[str, int],
    endpoint_errors: list[dict[str, str | int]],
    endpoints: list[str],
    new_tokens: list[dict[str, Any]],
    trending_tokens: list[dict[str, Any]],
    assessments: list[dict[str, Any]],
    qualification_complete: bool,
    notes: list[str],
) -> dict[str, Any]:
    return {
        "timestamp_utc": timestamp,
        "mode": mode,
        "chain": chain,
        "call_count": call_count,
        "endpoint_counts": endpoint_counts,
        "endpoint_errors": endpoint_errors,
        "endpoints": endpoints,
        "new_token_count": len(new_tokens),
        "trending_token_count": len(trending_tokens),
        "assessments": assessments,
        "qualification_complete": qualification_complete,
        "notes": notes,
    }


def render_report(record: dict[str, Any]) -> str:
    qualification = "complete" if record["qualification_complete"] else "incomplete"
    lines = [
        "# Birdeye Risk Radar",
        "",
        "Read-only token-risk radar output. This is not a trade recommendation.",
        "",
        "## Run Summary",
        "",
        f"- Time UTC: `{record['timestamp_utc']}`",
        f"- Mode: `{record['mode']}`",
        f"- Chain: `{record['chain']}`",
        f"- Birdeye call count: `{record['call_count']}`",
        f"- Sprint 4 call qualification: `{qualification}`",
        f"- Endpoints: {', '.join(f'`{endpoint}`' for endpoint in record['endpoints'])}",
        f"- Endpoint call counts: {', '.join(f'`{endpoint}`={count}' for endpoint, count in sorted(record['endpoint_counts'].items()))}",
        "",
        "## Notes",
        "",
    ]
    lines.extend(f"- {note}" for note in record["notes"])
    if record["endpoint_errors"]:
        lines.extend(["", "## Endpoint Blockers", ""])
        lines.extend(
            f"- `{item['endpoint']}` returned HTTP {item['status_code']}: {markdown_escape(item['detail'])}"
            for item in record["endpoint_errors"]
        )
    lines.extend(
        [
            "",
            "## Token Assessments",
            "",
            "| Symbol | Name | Source | Address | Liquidity USD | Volume 24h USD | Class | Flags | Warnings |",
            "| --- | --- | --- | --- | --- | --- | --- | --- | --- |",
        ]
    )
    for item in record["assessments"]:
        flags = ", ".join(item["risk_flags"]) or "none"
        warnings = ", ".join(item["warnings"]) or "none"
        lines.append(
            "| "
            + " | ".join(
                markdown_escape(value)
                for value in [
                    item["symbol"],
                    item["name"],
                    item["source"],
                    item["address"],
                    item["liquidity_usd"] if item["liquidity_usd"] is not None else "unknown",
                    item["volume_24h_usd"] if item["volume_24h_usd"] is not None else "unknown",
                    item["classification"],
                    flags,
                    warnings,
                ]
            )
            + " |"
        )
    lines.extend(
        [
            "",
            "## Risk Rule",
            "",
            "Reject means do not trade. Research means inspect further before any strategy can be written. Watch means no critical flag in this sample only.",
            "",
        ]
    )
    return "\n".join(lines)


def write_jsonl(path: Path, record: dict[str, Any]) -> None:
    with path.open("w", encoding="utf-8") as handle:
        handle.write(json.dumps({"type": "run_summary", **{key: value for key, value in record.items() if key != "assessments"}}, sort_keys=True) + "\n")
        for assessment in record["assessments"]:
            handle.write(json.dumps({"type": "token_assessment", **assessment}, sort_keys=True) + "\n")


def write_outputs(report_path: Path, jsonl_path: Path, record: dict[str, Any]) -> None:
    report_path.write_text(render_report(record), encoding="utf-8")
    write_jsonl(jsonl_path, record)


def run_self_test() -> None:
    record = collect_fixture_records(DEFAULT_MIN_LIQUIDITY_USD, timestamp="2026-05-13T00:00:00Z")
    assessments = {item["symbol"]: item for item in record["assessments"]}
    if record["call_count"] != 4:
        raise BirdeyeRadarError("fixture call-count self-test failed")
    if assessments["SAFE"]["classification"] != "watch":
        raise BirdeyeRadarError("safe fixture classification self-test failed")
    if assessments["RISK"]["classification"] != "reject":
        raise BirdeyeRadarError("risky fixture classification self-test failed")
    report = render_report(record)
    if "Fixture output only" not in report or "Reject means do not trade" not in report:
        raise BirdeyeRadarError("report rendering self-test failed")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Build a read-only Birdeye token-risk radar report.")
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--chain", default=DEFAULT_CHAIN)
    parser.add_argument("--api-key-env", default="BIRDEYE_API_KEY")
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT, help="tokens per Birdeye list call; Birdeye docs allow 1..20")
    parser.add_argument("--min-liquidity-usd", type=float, default=DEFAULT_MIN_LIQUIDITY_USD)
    parser.add_argument("--timeout", type=float, default=20.0)
    parser.add_argument("--target-call-count", type=int, default=0, help="minimum live Birdeye calls to collect before writing outputs")
    parser.add_argument("--request-interval-seconds", type=float, default=DEFAULT_REQUEST_INTERVAL_SECONDS)
    parser.add_argument("--meme-platform-enabled", action="store_true")
    parser.add_argument("--fixture", action="store_true", help="write deterministic fixture output without network calls")
    parser.add_argument("--report", type=Path, default=DEFAULT_REPORT)
    parser.add_argument("--jsonl", type=Path, default=DEFAULT_JSONL)
    parser.add_argument("--self-test", action="store_true", help="run local fixture tests and exit")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    try:
        if args.self_test:
            run_self_test()
            print("self-test ok")
            return 0
        if not 1 <= args.limit <= 20:
            raise BirdeyeRadarError("limit must be between 1 and 20")
        if args.target_call_count < 0:
            raise BirdeyeRadarError("target-call-count must be zero or greater")
        if args.request_interval_seconds < 0:
            raise BirdeyeRadarError("request-interval-seconds must be zero or greater")

        if args.fixture:
            record = collect_fixture_records(args.min_liquidity_usd)
        else:
            api_key = os.environ.get(args.api_key_env)
            if not api_key:
                raise BirdeyeRadarError(f"{args.api_key_env} is required for live Birdeye calls; use --fixture for offline verification")
            record = collect_live_records(
                base_url=args.base_url,
                api_key=api_key,
                chain=args.chain,
                limit=args.limit,
                min_liquidity_usd=args.min_liquidity_usd,
                timeout_seconds=args.timeout,
                meme_platform_enabled=args.meme_platform_enabled,
                target_call_count=args.target_call_count,
                request_interval_seconds=args.request_interval_seconds,
            )

        write_outputs(args.report, args.jsonl, record)
        print(
            json.dumps(
                {
                    "mode": record["mode"],
                    "report": str(args.report),
                    "jsonl": str(args.jsonl),
                    "call_count": record["call_count"],
                    "qualification_complete": record["qualification_complete"],
                    "token_assessments": len(record["assessments"]),
                },
                sort_keys=True,
            )
        )
    except BirdeyeRadarError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
