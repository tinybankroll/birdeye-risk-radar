# Birdeye Risk Radar

Read-only Solana token-risk radar for small-bankroll operators.

Birdeye Risk Radar pulls fresh listings, trending tokens, and market data from
Birdeye, then produces a conservative research-only report. It is designed as a
pre-trade safety filter: when token-security data is unavailable, candidates
stay research-only.

## Evidence

- `birdeye-radar.md`: live report from the qualification run.
- `birdeye-radar.jsonl`: evidence log with 50 successful Birdeye calls and
  60 token assessments.
- `SUBMISSION.md`: prepared Superteam submission fields and X post draft.

## Run

Fixture mode:

```bash
python3 tools/birdeye_radar.py --self-test
python3 tools/birdeye_radar.py --fixture --report birdeye-radar.md --jsonl birdeye-radar.jsonl
```

Live mode requires `BIRDEYE_API_KEY` in the environment:

```bash
python3 tools/birdeye_radar.py \
  --report birdeye-radar.md \
  --jsonl birdeye-radar.jsonl \
  --limit 20 \
  --target-call-count 50 \
  --request-interval-seconds 1.25
```

## Safety

- No wallet secret is included.
- The radar is read-only.
- It does not load wallet keys, sign transactions, build transactions, or
  submit orders.
- Any trading action would require a separate strategy, execution guard, and
  ledger path.

