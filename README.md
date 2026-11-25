# news-image-20261125 — The World in One Day

[![make.fun · news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/Siezy/news-image-20261125/rank.svg)](https://make.fun/bounty/news-image-20261125/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/Siezy/news-image-20261125/reward.svg)](https://make.fun/bounty/news-image-20261125?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261125)

A make.fun entry for **news-image-20261125**: "Sum up 25 November's world
news in one image."

`main.py` (Python 3.13, standard library only) draws a 1024x1024
newspaper-style front page and writes it to `$MAKEFUN_OUTPUT_DIR/entry.png`
(default `/output/entry.png`). It runs with no network and is fully
deterministic: two runs produce byte-identical output. The 5x7 bitmap font
and the PNG encoder are written by hand inside the file.

## The day: Wednesday 25 November 2026

36 stories across 10 regions — 3 red leads plus 33 numbered region
stories, every one with its source. Each story was verified as having
happened, or first been reported, on 25 November 2026 (sources: Reuters,
AP, NOS, MLex, ACCAN, FT, Al Jazeera, DW, SRI, Starlit Daily, WireMinute,
Horn Economic Review, ENNW, CuriousCats, ExcellenceGrandPrix). Stories
from 22–24 November were checked and excluded even when they were
reported on the 25th.

Leads: Shenzhou-24 launches with the first Pakistani astronaut aboard
Tiangong; the Saudi coalition strikes Hodeidah after the Houthis threaten
Jeddah; Australia's Senate passes the Digital Duty of Care bill, 36–23.

## How it was built

Three candidate layouts were rendered from the same program and compared
pairwise against the winning front-page template (masthead with the day,
red leads, region columns, 35+ numbered stories with sources, zero
narrative padding) and the judge criteria (names the day, breadth, clarity
from the image alone, faithful/no hype, craft legible at ~300px):

- **A — frontpage classic (CHAMPION, submitted):** masthead, 3 red leads,
  3-column region grid, "by the numbers" strip. Clean, fills the page,
  closest to the winner template.
- **B — dense broadsheet:** 46 stories in 4 columns. Rejected: duplicate
  region headers and ~280px of empty paper at the bottom.
- **C — lead-heavy:** hero lead with a drawn rocket. Rejected: the region
  list overflows the 1024px page and collides with the footer.
