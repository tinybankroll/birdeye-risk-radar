# Winner Benchmark

Status: local product surface built; submission paused until public link or walkthrough exists.

Decision: Birdeye Risk Radar has moved beyond the CLI/report packet, but it is
not ready for Sprint 4 submission until the static app is reviewer-visible.
Prior winners shipped public product surfaces with immediate utility, clear
positioning, and stronger presentation.

## Sources Checked

| Source | Evidence |
| --- | --- |
| Sprint 1 listing: https://superteam.fun/earn/listing/birdeye-data-4-week-bip-competition-sprint-1 | Winner: Idris Ahmed; 46 submissions; evaluation metrics include community support, product utility, technical depth, and presentation. |
| Sprint 2 listing: https://superteam.fun/earn/listing/birdeye-data-4-week-bip-competition-sprint-2 | Winner: Estar Kunmi; 35 submissions; winner project link: `https://lurq-sol.vercel.app/`. |
| Sprint 3 listing: https://superteam.fun/earn/listing/birdeye-data-4-week-bip-competition-sprint-3 | Winner: Idris Ahmed; 43 submissions; winner profile references the Sprint 3 win. |
| LURQ winner app: https://lurq-sol.vercel.app/ | Live product surface with signal feed, confidence score, wallet/holder metrics, Telegram alerts, Birdeye links, and a clear thesis: wallet accumulation before price moves. |
| Hall of Rugs app: https://hall-of-rugs.vercel.app/ | Public themed web app with token autopsy concept, 6 endpoint claim, verdict engine, shareable obituaries, and direct explanation of why it wins. |
| Birdeye competition listing: https://superteam.fun/earn/listing/birdeye-data-4-week-bip-competition-sprint-4 | Requires 50 API calls and evaluates community support, utility, technical depth, and presentation equally. |

## What Prior Winners Signal

| Dimension | Winner Pattern | Current State | Gap |
| --- | --- | --- | --- |
| Product surface | Public, live web app | CLI plus Markdown/JSONL report | Build UI. |
| User value | Concrete workflow: signals, autopsies, alerts | Static research-only assessment table | Add interactive workflow and clear decisions. |
| Data depth | Multiple endpoint story and derived metrics | New listings, trending, market data; security blocked | Add fallback risk scoring and document endpoint coverage. |
| Presentation | Strong name, thesis, copy, shareable link | Sparse repo/readme | Improve narrative, screenshots, demo flow. |
| Community | X posts and engagement are part of scoring | X post not published | Publish only after demo is worth sharing. |
| Technical proof | Live app backed by API calls | Live API evidence exists but not productized | Wire live evidence into app/demo. |

## Revised Product Direction

Positioning: a public "token triage desk" for small-wallet Solana operators.

The product should answer three questions quickly:

1. Is this token safe enough to research?
2. Is anything happening now that makes it worth watching?
3. What exact data made the scanner reject, research, or watch it?

## Required Before Submission

- Build a public web UI, not just a CLI report. Local static UI exists in `index.html`.
- Show live cards for token candidates with:
  - price,
  - liquidity,
  - 24h volume,
  - source signal,
  - watch/research/reject status,
  - missing-data warnings,
  - Birdeye token link.
- Add a token detail/autopsy view.
- Add a "why this verdict" explanation per token.
- Add a static/demo fallback so reviewers see the product even when API quota or package access fails.
- Add a screenshot or short demo section to `README.md`.
- Publish one X post only after the public demo is live and useful.
- Submit only after the GitHub link, X link, and endpoint summary all point to the standalone product.

## Technical Upgrade Plan

1. Convert the repo to a small web app. Done locally with static HTML/CSS/JS.
2. Reuse `birdeye-radar.jsonl` as seed data for static demo mode. Done through `tools/build_demo_data.py`.
3. Add live refresh through `tools/birdeye_radar.py` or a small API endpoint when `BIRDEYE_API_KEY` is available.
4. Render summary metrics: total assessed, reject/research/watch counts, missing security count, strongest candidates. Done.
5. Render token cards with stable risk labels and copyable token addresses. Partially done; addresses are visible and Birdeye links are present.
6. Render token detail pages or expandable rows with the exact scoring reasons. Done as a selected-token detail panel.
7. Add presentation polish: product name, concise thesis, endpoint disclosure, not-financial-advice safety note. Partially done.
8. Re-run live evidence after UI exists.
9. Update submission copy and X draft to show the web app, not the CLI.

## No-Submit Rule

Do not submit to Superteam until the project has a public working app URL or a
high-quality walkthrough demo. A GitHub repo with a CLI and report is below the
observed winner bar.
