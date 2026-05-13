# Birdeye Risk Radar

Read-only token-risk radar output. This is not a trade recommendation.

## Run Summary

- Time UTC: `2026-05-13T11:07:44Z`
- Mode: `live`
- Chain: `solana`
- Birdeye call count: `50`
- Sprint 4 call qualification: `complete`
- Endpoints: `/defi/v2/tokens/new_listing`, `/defi/v3/token/market-data`, `/defi/token_security`, `/defi/token_trending`
- Endpoint call counts: `/defi/token_trending`=2, `/defi/v2/tokens/new_listing`=1, `/defi/v3/token/market-data`=47

## Notes

- Read-only Birdeye calls only.
- Qualification for the Sprint 4 listing requires at least 50 successful API calls before submission.
- Live requests were rate-limited to at most one call every 1.25 seconds.
- Extra trending pages fetched for call target: 1.
- Token-security data is used when the current API package permits it; otherwise tokens remain research-only.

## Endpoint Blockers

- `/defi/token_security` returned HTTP 401: Birdeye API HTTP error: 401; detail: Your API key lacks sufficient permissions to access this resource.

## Token Assessments

| Symbol | Name | Source | Address | Liquidity USD | Volume 24h USD | Class | Flags | Warnings |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| WURLDCUN | Wurld Cun | new_listing | 7dYsBHsizX3YFXUETohJ8o92axTPibZLAGJMBRvvPkz5 | 21722.875537856013 | unknown | research | none | not-in-trending-sample, missing-security-data |
| WURLDCUN | Wurld Cun | new_listing | 44EuDbyx1PLekQCwzdsCSCXZs6A9DqBAQBFFc8kuyKih | 94472.85875308585 | unknown | research | none | not-in-trending-sample, missing-security-data |
| YILONG | YILONGMA | new_listing | JAb5ru43W2gb2F7uEZe9s2VG7EjPU3vzSTCsoqPJ7Nw7 | 7557.723395642381 | unknown | research | none | not-in-trending-sample, missing-security-data |
| ElonAir | Elon Air | new_listing | 5PjphW3Nk3PuvywLCwA8KbHeM8KLmJpSqpEZgA22v5jp | 9947.0438171949 | unknown | research | none | not-in-trending-sample, missing-security-data |
| SPAIN | Spain | new_listing | 21MDBnapbJYC1H6Zj3rZFXEisTvXSC3QfFEB5Gi3wgtB | 7565.05245807626 | unknown | research | none | not-in-trending-sample, missing-security-data |
| CHINA | CHINA | new_listing | DZfVmLFbrRXoUxdwASsaF7hTWVPuNjingboAbXtwpmQu | 24722.830657062925 | unknown | research | none | not-in-trending-sample, missing-security-data |
| CHINA | CHINA | new_listing | AVBL3yht6yuWRAJPgYqUT3HM4yd9hav7ziG34uHqkePx | 5673.921191476394 | unknown | research | none | not-in-trending-sample, missing-security-data |
| R.S C0IN | GDOR | new_listing | 6f81SM5ymRtza8BAdyYisUtZTr1fmMaUyhYarP1G5arQ | 7567.321028919327 | unknown | research | none | not-in-trending-sample, missing-security-data |
| JEERC | JAPAN CAT | new_listing | 4VwjFe62LVZSv7Eh6pkayjzKyAbWsPqWmQ8mFXgzpump | 23945.714447075916 | unknown | research | none | not-in-trending-sample, missing-security-data |
| RKC | Red Kitten Crew | new_listing | HMGL6mf5m55BdU3Y4rTy44d1RuB75LMphz62VLeLQ5Wv | 153154.0590894254 | unknown | research | none | not-in-trending-sample, missing-security-data |
| Rockstar | Rockstar Games | new_listing | 21vdLgjsgeATxE9BRTi7BPwpbV383FLsqXy8VMRYpSmK | 8516.97019149313 | unknown | research | none | not-in-trending-sample, missing-security-data |
| Ronaldinu | Ronaldinu | new_listing | ABe61KWwC1SxJRa3F7HxucXaRhvo1sgfpyHHRWBp4eLS | 29708.074668306715 | unknown | research | none | not-in-trending-sample, missing-security-data |
| Wonder Woman | Wonder Woman | new_listing | 4KGYeshg1gDdVjc4MhZLLH628NbdoEUMEnaczRhoewT8 | 2306.9950992033373 | unknown | research | none | not-in-trending-sample, missing-security-data |
| C0IN | ROAF | new_listing | 8b7F6jSPctMQcY8bk5W3fFpiFk45NcYKKS3j6ZQqpVG | 7576.625039757935 | unknown | research | none | not-in-trending-sample, missing-security-data |
| mama | mama | new_listing | 7U8Hcg8UD54tAfbRrXQvN2t6v4ZaswQjgWpjMcotfMEB | 1894.2471054072203 | unknown | research | none | not-in-trending-sample, missing-security-data |
| TESTTT | testtt | new_listing | TYWXZhJ58a3R9HHwegbVSrrLpKHie3RzvVp8GeK4t3s | 0.0 | unknown | research | none | liquidity-below-1000-usd, not-in-trending-sample, missing-security-data |
| $Crew | $Crew | new_listing | 3Zkm9M6u2DChkTfyXZqTa9TJZqyaz8EreFwmfZUPUTQp | 570.4688093132959 | unknown | research | none | liquidity-below-1000-usd, not-in-trending-sample, missing-security-data |
| RUSKGB | RUSKGB | new_listing | D6E6oL8TXfxfiwEGyfJSu8nUHrFs1VYJAWTvmeNPmX4r | 2307.979751529948 | unknown | research | none | not-in-trending-sample, missing-security-data |
| RKC | Red Kitten Crew | new_listing | 7otGW5uHuDTgbez8xBmW8MLJWYkbzxbK6U8AQFLUuNex | 132878.81656498907 | unknown | research | none | not-in-trending-sample, missing-security-data |
| BULL | Bull | new_listing | HCZRHqsjcihh2oKJkwjjJv8Rj4nEN5LbWqw5taJxzJ8R | 0.0 | unknown | research | none | liquidity-below-1000-usd, not-in-trending-sample, missing-security-data |
| fish | rainbowfish | token_trending | CmgJ1PobhUqB7MEa8qDkiG2TUpMTskWj8d9JeZWSpump | 123660.82456827979 | 1718773.30393493 | research | none | missing-security-data |
| AVA | Ava AI | token_trending | DKu9kykSfbN5LBfFXtNNDPaX35o4Fv6vJ9FKk7pZpump | 1224827.4345123707 | 1477221.2422888607 | research | none | missing-security-data |
| MUMU | Mumu the Bull | token_trending | 5LafQUrVco6o7KMz42eqVEJ9LW31StPyGjeeu5sKoMtA | 549605.3764625032 | 259729.91662370175 | research | none | missing-security-data |
| UNOS | United Nations Oil Supply | token_trending | 6QnEB9Ft4oZM55P8tyyhRBi6hr22ZdpbVHu1MWmcaSVk | 141084.04773929212 | 1797487.3233197234 | research | none | missing-security-data |
| FAF | Flash.trade | token_trending | FAFxVxnkzZHMCodkWyoccgUNgVScqMw2mhhQBYDFjFAF | 592247.2834496741 | 133811.42110803546 | research | none | missing-security-data |
| MAGA | Make Aliens Great Again  | token_trending | Hon2rHAiqkcDtUzL5gA2vjXPr7T1MPCK2UT2AHKCpump | 545018.701978097 | 1713682.5610483806 | research | none | missing-security-data |
| pwease | PWEASE | token_trending | CniPCE4b3s8gSUPhUiyMjXnytrEqUrMfSsnbBjLCpump | 520524.1824937507 | 128048.18816265755 | research | none | missing-security-data |
| HANTA | Hantavirus | token_trending | 2tXpgu2DLTsPUf9zFmuZmA4xrYxXKBTpVq9wAM7hzs9y | 688938.8100129934 | 6430648.233271876 | research | none | missing-security-data |
| TRUMP | OFFICIAL TRUMP | token_trending | 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN | 61161674.25440688 | 46371755.202411816 | research | none | missing-security-data |
| SCAM | Scam Altman | token_trending | 6AVAUKa9uxQpruHZUinFECpXEh1usRVtzQWK8N2wpump | 220994.65465484106 | 2728977.5117122848 | research | none | missing-security-data |
| UFD | Unicorn Fart Dust | token_trending | eL5fUxj2J4CiQsmW85k5FG9DvuQjjUoBHoQBi2Kpump | 1404498.9204148788 | 482588.01656689233 | research | none | missing-security-data |
| CARDS | Collector Crypt | token_trending | CARDSccUMFKoPRZxt5vt3ksUbxEFEcnZ3H2pd3dKxYjp | 3067490.202036145 | 3613144.058075472 | research | none | missing-security-data |
| COPPERINU | copper inu | token_trending | 61Wj56QgGyyB966T7YsMzEAKRLcMvJpDbPzjkrCZc4Bi | 463089.73964811524 | 1533557.2808783762 | research | none | missing-security-data |
| CLANKER | CLANKER Robot AI Slur | token_trending | 3qq54YqAKG3TcrwNHXFSpMCWoL8gmMuPceJ4FG9npump | 272524.5722204816 | 400248.9427054847 | research | none | missing-security-data |
| VINE | Vine Coin | token_trending | 6AJcP7wuLwmRYLBNbi825wgguaPsWzPBEHcHndpRpump | 2185277.9962806166 | 1364811.980856625 | research | none | missing-security-data |
| KEVUN | Kevun Wersh | token_trending | DXwcaZ3atb4WfrzDtkR3EcRhkv2rrbzjKLQxyPjNpump | 26425.34899692928 | 958965.9652771462 | research | none | missing-security-data |
| House | Housecoin | token_trending | DitHyRMQiSDhn5cnKMJV2CDDt6sVct96YrECiM49pump | 907347.3279184292 | 326708.23066771077 | research | none | missing-security-data |
| aura | aura | token_trending | DtR4D9FtVoTX2569gaL837ZgrB6wNjj6tkmnX9Rdk9B2 | 2345787.883019247 | 3924203.601541223 | research | none | missing-security-data |
| YILONG | YILONGMA | token_trending | GWqpTt7kwzmEEdLDgZiaiLRQByf3pLJEWAtc9G2RFpdn | 18830.291966643534 | 185896.21511179197 | research | none | missing-security-data |
| ASTEROID | Asteroid The Space Shiba Inu | token_trending | 4UeLCRqARmfb6e6KQijtiktqqXUxbfk6jZng7DhuBAGS | 1471040.6938182649 | 2056589.0897401855 | research | none | missing-security-data |
| RoyalPop | Swatch AP | token_trending | 8TbnsLM72WoHKmVyDqRqEkEuNRGFgA4zbRXQYv6Gpump | 177776.3053236358 | 7540569.459827423 | research | none | missing-security-data |
| ZERA | ZERA | token_trending | 8avjtjHAHFqp4g2RR9ALAGBpSTqKPZR8nRbzSTwZERA | 318299.3547821994 | 251118.81808939672 | research | none | missing-security-data |
| POSITIONS | $positions | token_trending | 7BC22ppHGeCdhpxNVyJMxV51y1qzkAcEd8YXtzX8pump | 91742.00331070433 | 2094707.4847075893 | research | none | missing-security-data |
| Percolator | Percolator | token_trending | 8PzFWyLpCVEmbZmVJcaRTU5r69XKJx1rd7YGpWvnpump | 195072.04657538846 | 117195.16669065595 | research | none | missing-security-data |
| EPIC | EPIC FACE | token_trending | 4XEtVrvHEnik8Gs4b3spWUuwZiJ1tc3fQxBYgvCrpump | 12170.44790495623 | 231797.9744988387 | research | none | missing-security-data |
| BOME | BOOK OF MEME | token_trending | ukHH6c7mMyiWCf1b9pnWe25TSpkDDt3H5pQZgZ74J82 | 12408149.089768814 | 1124075.8198297939 | research | none | missing-security-data |
| DIRECTOR | Truman Show | token_trending | Do6N8m8ssowyAvXs2tkGKkJ8vaNC8H5oRkMdr9shpump | 49263.577853067705 | 453917.411652638 | research | none | missing-security-data |
| DEVIN | SCOTT WU | token_trending | 7gbEP2TAy5wM3TmMp5utCrRvdJ3FFqYjgN5KDpXiWPmo | 102670.85430128133 | 40893.64641434384 | research | none | missing-security-data |
| EITHER | Eitherway | token_trending | HmBdm8vbisABUjkxms6ZUnoaXbfwFM6ymxShWfAENaoi | 777083.4056213851 | 2257474.939885039 | research | none | missing-security-data |
| USOR | U.S Oil | token_trending | USoRyaQjch6E18nCdDvWoRgTo6osQs9MUd8JXEsspWR | 172376.84372164193 | 92210.93881623106 | research | none | missing-security-data |
| Watch | Penis wif Watch | token_trending | Av5RqYc9YYjeU5Lp3jp8ALaHrXvVJdFwjDVDX1vkpump | 34786.62129302857 | 317872.44037999853 | research | none | missing-security-data |
| DISCLOSURE | DISCLOSURE | token_trending | FpBhnZLzHjgPrc69vkimPtHCwN4xoeX3RUhDa3Bpump | 70422.08480969106 | 1572565.2288625683 | research | none | missing-security-data |
| NEAR | NEAR | token_trending | 3ZLekZYq2qkZiSpnSvabjit34tUkjSwD1JFuW9as9wBG | 992183.421810089 | 884121.2779698235 | research | none | missing-security-data |
| UNOS | United Nations Oil Supply | token_trending | 9abVgV5NaZMKtbWJuCSySVfozMXmP1Xr3NRzBkiJ7y2y | 62902.09480370179 | 286569.68594253296 | research | none | missing-security-data |
| PAC | Public Asset Control | token_trending | CaMngTLMQkSRWBCYX2rfc4rJnZChXs1Xex6THzPj7fBi | 62769.51059968803 | 282852.37143947487 | research | none | missing-security-data |
| Mbappe | Dictator Mbappe | token_trending | CQJ3yxLCND48QhRx5bsbfW6VT5LP8T63VtVyoxkcpump | 36971.44462934096 | 226290.38862455043 | research | none | missing-security-data |
| ANDV | Andes Virus | token_trending | jvKtLFLnNGPM7edS9KEpYqPxuY8HPGTZohLFM4Spump | 89313.29143743023 | 1194445.6423826865 | research | none | missing-security-data |
| EYED | Eyed Exchange | token_trending | GpmmQBjXxoppbELykD2PGQ4wwVR74o5sSZXVW6hVpump | 145206.76960110344 | 141114.77928889327 | research | none | missing-security-data |
| ZEC | Zcash | token_trending | A7bdiYdS5GjqGFtxf17ppRHtDKPkkRqbKtR27dxvQXaS | 3582823.6882205023 | 11873344.332345143 | research | none | missing-security-data |
| USMT | Muslim Usmanov | token_trending | 8uhGgd7HBtNNZSVnUAx6T49ofSvmAGVJ1GcWjodFZbEz | 0.4398231390526859 | 1.2912505122984426 | research | none | liquidity-below-1000-usd, missing-security-data |

## Risk Rule

Reject means do not trade. Research means inspect further before any strategy can be written. Watch means no critical flag in this sample only.
