# Birdeye Risk Radar

Read-only Solana token-risk radar for small-bankroll operators.

Birdeye Risk Radar pulls fresh listings, trending tokens, and market data from
Birdeye, then produces a conservative research-only report. It is designed as a
pre-trade safety filter: when token-security data is unavailable, candidates
stay research-only.

## Status

Public preview available. Not submitted yet.

After reviewing prior Birdeye Sprint winners, the original CLI/report packet was
below the winner bar. The repo now includes a static token-triage desk over the
captured live evidence. The static app is pushed to the public repository and
can be reviewed through HTMLPreview:

https://htmlpreview.github.io/?https://github.com/tinybankroll/birdeye-risk-radar/blob/main/index.html

The remaining submission gates are the X post and Superteam submission identity.

## Evidence

- `birdeye-radar.md`: live report from the qualification run.
- `birdeye-radar.jsonl`: evidence log with 50 successful Birdeye calls and
  60 token assessments.
- `index.html`, `styles.css`, `app.js`, `radar-data.js`: static demo desk
  backed by the live evidence log.
- `SUBMISSION.md`: prepared Superteam submission fields and X post draft.
- `WINNER_BENCHMARK.md`: previous-winner benchmark and revised upgrade plan.

## Run

Static demo:

```bash
python3 tools/build_demo_data.py
python3 -m http.server 8787
```

Open `http://127.0.0.1:8787/`.

Validation:

```bash
python3 tools/build_demo_data.py --check
node --check app.js
```

Radar fixture mode:

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

## Submission Gate

The static app is reviewer-visible through HTMLPreview. GitHub Pages is still
preferred, but enabling Pages requires owner/admin permissions not available to
the current local `gh` token.
