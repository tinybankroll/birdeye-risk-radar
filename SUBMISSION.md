# Birdeye Risk Radar Submission Draft

Status: repository pushed; X/Superteam submission pending.

Reason: Superteam should see the standalone project only, not the operating
workspace that produced it. This packet contains the scanner, live evidence,
and submission copy without wallet files or operating-state files.

## Listing

- Listing: Birdeye Data 4-Week BIP Competition - Sprint 4
- Source: https://superteam.fun/earn/listing/birdeye-data-4-week-bip-competition-sprint-4
- Prize target: 500 USDC plus Birdeye API credits
- Required before submission: at least 50 Birdeye API calls, project name, GitHub link, X post link, and endpoint summary

## Project

Project name: Birdeye Risk Radar.

Description:

Birdeye Risk Radar is a read-only Solana token-risk scanner for small-bankroll
operators. It pulls new listings, compares them with trending tokens, enriches
candidates with market data, and classifies each token as reject, research, or
watch. The first live output is deliberately conservative: it refuses to
recommend trades and keeps all candidates research-only when token-security
data is unavailable.

## Endpoints Used

- `GET /defi/v2/tokens/new_listing`
- `GET /defi/token_trending`
- `GET /defi/v3/token/market-data`
- `GET /defi/token_security` attempted, but the current API package returned HTTP 401 for insufficient permissions.

## Current Evidence

- `tools/birdeye_radar.py` exists and is read-only.
- `python3 tools/birdeye_radar.py --self-test` passes with deterministic fixture data.
- `birdeye-radar.jsonl` records live mode, 50 successful calls, and 60 token assessments.
- `birdeye-radar.md` records the `/defi/token_security` HTTP 401 package-permission blocker and keeps all candidates research-only.

## Ready Submission Fields

Project title:

Birdeye Risk Radar

Public project link:

https://github.com/tinybankroll/birdeye-risk-radar

X progress post link:

Blocked until the prepared post is published from the controlled X account.

Endpoint summary:

The tool uses Birdeye new listings as one candidate source, token trending as a
demand/context source, and token market data as an enrichment source. It
attempts token security as the risk gate when package access permits it. With
the current key, token security returns HTTP 401, so the live report
conservatively classifies every candidate as research-only and does not produce
trade recommendations.

Other submission notes:

Birdeye Risk Radar is a read-only Solana token-risk scanner for small-bankroll
operators. It generated a live Markdown report and JSONL evidence log with 50
successful Birdeye API calls and 60 token assessments. No wallet key was
loaded, no transaction was built, and no trade recommendation was emitted.

## X Post Draft

Built Birdeye Risk Radar for Birdeye Data Sprint 4: a read-only Solana
token-risk scanner.

Live run: 50 Birdeye API calls, 60 research-only token assessments, no wallet
signing.

https://github.com/tinybankroll/birdeye-risk-radar

@birdeye_data #BirdeyeAPI

## Submission Blockers

- X post link: publish the draft from the controlled account, then record the URL.
- Superteam Earn identity: submit through the listing manually or provide an agent API key and human payout-claim path.
- Optional stronger scoring: upgrade or replace the Birdeye key if `/defi/token_security` access is required before submission.

## Risk Statement

This is not a trading bot and does not submit transactions. It is a pre-trade
safety filter. Any live trading would require a separate strategy, entry rule,
exit rule, position sizing rule, fee/slippage estimate, execution guard, and
ledger path.
