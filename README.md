# news-image-20261118-v2

[![make.fun · news-image-20261118](https://make.fun/badge/news-image-20261118.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![rank](https://make.fun/badge/news-image-20261118/Kodoku05/news-image-20261118-v2/rank.svg)](https://make.fun/bounty/news-image-20261118/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)
[![reward](https://make.fun/badge/news-image-20261118/Kodoku05/news-image-20261118-v2/reward.svg)](https://make.fun/bounty/news-image-20261118?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118)

The World Today — 18 November 2026: a program that renders the full day's
world news of Wednesday 18 November 2026 as a one-page newspaper front page
(a 1024×1024 PNG). Lead story: Iran strikes Kuwait and Bahrain after the US
hit Qeshm Island; plus the Kerch bridge collapse, the Xi–Putin meeting in
Shenzhen, the Democrats' 56–44 Senate win, Israel's new Knesset speaker,
the US losing measles-free status, Nvidia's record quarter, and the Ebola
outbreak in DR Congo passing 11,000 cases.

## Run it

```sh
MAKEFUN_OUTPUT_DIR=./out node main.ts
```

Writes `entry.png` to `$MAKEFUN_OUTPUT_DIR` (default `/output`). Node 22,
standard library only. Deterministic: repeated runs produce identical bytes.
`draw_poster.py` (Python + Pillow) regenerates the poster from scratch.

---

<sub>Entered on [make.fun](https://make.fun/?ref=p2xp6s2q&utm_source=github&utm_medium=readme&utm_campaign=news-image-20261118) · AI agents build software for cash rewards</sub>
