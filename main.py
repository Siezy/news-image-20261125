#!/usr/bin/env python3
"""news-image-20261125: sum up Wednesday 25 November 2026 in one image.

Draws a 1024x1024 newspaper front page with pure-stdlib Python (no
network, no fonts on disk: a 5x7 bitmap font is defined below, and the PNG
encoder is written by hand) and writes it to $MAKEFUN_OUTPUT_DIR/entry.png
(default /output/entry.png). Two runs write the same bytes.

36 stories across 10 regions, every one verified as having happened or
first been reported on Wed 25 Nov 2026 (Reuters, AP, NOS, MLex, Al
Jazeera, DW, SRI, Starlit Daily, WireMinute, Horn Economic Review, ENNW,
CuriousCats). Stories from 22-24 Nov were checked and excluded even when
reported on the 25th. Layout: LAYOUT constant below ("A" frontpage
classic, "B" dense broadsheet, "C" lead-heavy); the submitted file uses
the tournament champion.
"""

import os
import struct
import zlib

W, H = 1024, 1024

# ---------------------------------------------------------------- palette
PAPER = (246, 241, 227)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (30, 48, 88)
GOLD = (201, 162, 39)
RED = (180, 35, 24)
TEAL = (14, 124, 123)
GRAY = (96, 96, 96)
LGRAY = (210, 204, 188)
WHITE = (255, 255, 255)
CARD = (255, 255, 255)

# ---------------------------------------------------------------- 5x7 font
# Each glyph is 7 rows of 5 bits, written by hand for this entry.
F = {
 'A': ("01110","10001","10001","11111","10001","10001","10001"),
 'B': ("11110","10001","10001","11110","10001","10001","11110"),
 'C': ("01110","10001","10000","10000","10000","10001","01110"),
 'D': ("11110","10001","10001","10001","10001","10001","11110"),
 'E': ("11111","10000","10000","11110","10000","10000","11111"),
 'F': ("11111","10000","10000","11110","10000","10000","10000"),
 'G': ("01110","10001","10000","10111","10001","10001","01111"),
 'H': ("10001","10001","10001","11111","10001","10001","10001"),
 'I': ("01110","00100","00100","00100","00100","00100","01110"),
 'J': ("00111","00010","00010","00010","00010","10010","01100"),
 'K': ("10001","10010","10100","11000","10100","10010","10001"),
 'L': ("10000","10000","10000","10000","10000","10000","11111"),
 'M': ("10001","11011","10101","10101","10001","10001","10001"),
 'N': ("10001","11001","10101","10011","10001","10001","10001"),
 'O': ("01110","10001","10001","10001","10001","10001","01110"),
 'P': ("11110","10001","10001","11110","10000","10000","10000"),
 'Q': ("01110","10001","10001","10001","10101","10010","01101"),
 'R': ("11110","10001","10001","11110","10100","10010","10001"),
 'S': ("01111","10000","10000","01110","00001","00001","11110"),
 'T': ("11111","00100","00100","00100","00100","00100","00100"),
 'U': ("10001","10001","10001","10001","10001","10001","01110"),
 'V': ("10001","10001","10001","10001","10001","01010","00100"),
 'W': ("10001","10001","10001","10101","10101","11011","10001"),
 'X': ("10001","10001","01010","00100","01010","10001","10001"),
 'Y': ("10001","10001","01010","00100","00100","00100","00100"),
 'Z': ("11111","00001","00010","00100","01000","10000","11111"),
 'a': ("00000","00000","01110","00001","01111","10001","01111"),
 'b': ("10000","10000","11110","10001","10001","10001","11110"),
 'c': ("00000","00000","01110","10001","10000","10001","01110"),
 'd': ("00001","00001","01111","10001","10001","10001","01111"),
 'e': ("00000","00000","01110","10001","11111","10000","01110"),
 'f': ("00110","01001","01000","11110","01000","01000","01000"),
 'g': ("00000","01111","10001","10001","01111","00001","01110"),
 'h': ("10000","10000","11110","10001","10001","10001","10001"),
 'i': ("00100","00000","01100","00100","00100","00100","01110"),
 'j': ("00010","00000","00110","00010","00010","10010","01100"),
 'k': ("10000","10000","10010","10100","11000","10100","10010"),
 'l': ("01100","00100","00100","00100","00100","00100","01110"),
 'm': ("00000","00000","11010","10101","10101","10101","10101"),
 'n': ("00000","00000","11110","10001","10001","10001","10001"),
 'o': ("00000","00000","01110","10001","10001","10001","01110"),
 'p': ("00000","11110","10001","10001","11110","10000","10000"),
 'q': ("00000","00000","01111","10001","10001","01111","00001"),
 'r': ("00000","00000","10110","11001","10000","10000","10000"),
 's': ("00000","00000","01111","10000","01110","00001","11110"),
 't': ("01000","01000","11110","01000","01000","01001","00110"),
 'u': ("00000","00000","10001","10001","10001","10011","01101"),
 'v': ("00000","00000","10001","10001","10001","01010","00100"),
 'w': ("00000","00000","10001","10101","10101","10101","01010"),
 'x': ("00000","00000","10001","01010","00100","01010","10001"),
 'y': ("00000","00000","10001","10001","01111","00001","01110"),
 'z': ("00000","00000","11111","00010","00100","01000","11111"),
 '0': ("01110","10001","10011","10101","11001","10001","01110"),
 '1': ("00100","01100","00100","00100","00100","00100","01110"),
 '2': ("01110","10001","00001","00110","01000","10000","11111"),
 '3': ("11110","00001","00001","01110","00001","00001","11110"),
 '4': ("00010","00110","01010","10010","11111","00010","00010"),
 '5': ("11111","10000","11110","00001","00001","10001","01110"),
 '6': ("01110","10000","10000","11110","10001","10001","01110"),
 '7': ("11111","00001","00010","00100","01000","01000","01000"),
 '8': ("01110","10001","10001","01110","10001","10001","01110"),
 '9': ("01110","10001","10001","01111","00001","00001","01110"),
 ' ': ("00000","00000","00000","00000","00000","00000","00000"),
 '.': ("00000","00000","00000","00000","00000","01100","01100"),
 ',': ("00000","00000","00000","00000","01100","00100","01000"),
 ':': ("00000","01100","01100","00000","01100","01100","00000"),
 ';': ("00000","01100","01100","00000","01100","00100","01000"),
 '!': ("00100","00100","00100","00100","00100","00000","00100"),
 '?': ("01110","10001","00001","00110","00100","00000","00100"),
 "'": ("00100","00100","01000","00000","00000","00000","00000"),
 '"': ("01010","01010","01010","00000","00000","00000","00000"),
 '-': ("00000","00000","00000","01110","00000","00000","00000"),
 '–': ("00000","00000","00000","01110","00000","00000","00000"),
 '—': ("00000","00000","00000","11111","00000","00000","00000"),
 '(': ("00010","00100","01000","01000","01000","00100","00010"),
 ')': ("01000","00100","00010","00010","00010","00100","01000"),
 '/': ("00001","00010","00010","00100","01000","01000","10000"),
 '\\': ("10000","01000","01000","00100","00010","00010","00001"),
 '&': ("01100","10010","10100","01000","10101","10010","01101"),
 '%': ("11001","11010","00010","00100","01000","01011","10011"),
 '$': ("00100","01111","10100","01110","00101","11110","00100"),
 '#': ("01010","01010","11111","01010","11111","01010","01010"),
 '@': ("01110","10001","10111","10101","10110","10000","01110"),
 '*': ("00000","10101","01110","11111","01110","10101","00000"),
 '+': ("00000","00100","00100","11111","00100","00100","00000"),
 '=': ("00000","00000","11111","00000","11111","00000","00000"),
 '<': ("00010","00100","01000","10000","01000","00100","00010"),
 '>': ("01000","00100","00010","00001","00010","00100","01000"),
 '_': ("00000","00000","00000","00000","00000","00000","11111"),
 '[': ("01110","01000","01000","01000","01000","01000","01110"),
 ']': ("01110","00010","00010","00010","00010","00010","01110"),
 '°': ("01100","10010","10010","01100","00000","00000","00000"),
 '·': ("00000","00000","00000","00000","01100","01100","00000"),
 '•': ("00000","01110","11111","11111","01110","00000","00000"),
 '×': ("00000","10001","01010","00100","01010","10001","00000"),
 '|': ("00100","00100","00100","00100","00100","00100","00100"),
 '~': ("00000","00000","01001","10110","00000","00000","00000"),
 '^': ("00100","01010","10001","00000","00000","00000","00000"),
 '`': ("01000","00100","00010","00000","00000","00000","00000"),
 '{': ("00010","00100","00100","11100","00100","00100","00010"),
 '}': ("01000","00100","00100","00110","00100","00100","01000"),
 '’': ("00100","00100","01000","00000","00000","00000","00000"),
 '‘': ("01000","01000","00100","00000","00000","00000","00000"),
 '“': ("01010","01010","01010","00000","00000","00000","00000"),
 '”': ("01010","01010","01010","00000","00000","00000","00000"),
}
FALLBACK = F['?']

# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self, w, h, bg):
        self.w, self.h = w, h
        self.px = bytearray(bg * (w * h))

    def put(self, x, y, c):
        if 0 <= x < self.w and 0 <= y < self.h:
            i = (y * self.w + x) * 3
            self.px[i:i + 3] = bytes(c)

    def rect(self, x, y, w, h, c):
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                self.put(xx, yy, c)

    def hline(self, x, y, w, c, t=1):
        self.rect(x, y, w, t, c)

    def vline(self, x, y, h, c, t=1):
        self.rect(x, y, t, h, c)

    def text_w(self, s, scale):
        return sum(6 for _ in s) * scale - scale

    def text(self, s, x, y, scale, c):
        cx = x
        for ch in s:
            g = F.get(ch, FALLBACK)
            for r in range(7):
                row = g[r]
                for cc in range(5):
                    if row[cc] == '1':
                        for dy in range(scale):
                            for dx in range(scale):
                                self.put(cx + cc * scale + dx,
                                         y + r * scale + dy, c)
            cx += 6 * scale
        return cx

    def text_c(self, s, cx, y, scale, c):
        self.text(s, cx - self.text_w(s, scale) // 2, y, scale, c)

    def wrap(self, s, maxw, scale):
        """Greedy word wrap; returns list of lines, each <= maxw px."""
        words, lines, cur = s.split(' '), [], ''
        for wd in words:
            t = wd if not cur else cur + ' ' + wd
            if self.text_w(t, scale) <= maxw or not cur:
                cur = t
            else:
                lines.append(cur)
                cur = wd
        if cur:
            lines.append(cur)
        return lines

    def para(self, s, x, y, maxw, scale, c, lh=None):
        lh = lh if lh is not None else 7 * scale + 2
        yy = y
        for ln in self.wrap(s, maxw, scale):
            self.text(ln, x, yy, scale, c)
            yy += lh
        return yy


def png_bytes(cv):
    def chunk(tag, data):
        c = struct.pack('>I', len(data)) + tag + data
        return c + struct.pack('>I', zlib.crc32(tag + data) & 0xFFFFFFFF)
    raw = b''.join(b'\x00' + bytes(cv.px[y * cv.w * 3:(y + 1) * cv.w * 3])
                   for y in range(cv.h))
    ihdr = struct.pack('>IIBBBBB', cv.w, cv.h, 8, 2, 0, 0, 0)
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR', ihdr)
            + chunk(b'IDAT', zlib.compress(raw, 9)) + chunk(b'IEND', b''))


def write_png(cv, path):
    with open(path, 'wb') as fh:
        fh.write(png_bytes(cv))


# ---------------------------------------------------------------- stories
# (region, headline, detail, source) — verified 25 Nov 2026.
LEADS = [
 ("SPACE",
  "Shenzhou-24 launches, Pakistani first foreign astronaut on Tiangong",
  "Long March 2F lifts off Jiuquan at 08:18 CST. Zeeshan Ali, 40, is the "
  "first Pakistani in orbit and the first foreign astronaut aboard "
  "China's space station.", "Reuters / AP"),
 ("YEMEN",
  "Saudi coalition strikes Hodeidah after Houthis threaten Jeddah",
  "Houthis threaten Jeddah and all Saudi Red Sea ports; the coalition "
  "strikes Hodeidah's operational capabilities after an evacuation "
  "warning.", "Reuters"),
 ("AUSTRALIA",
  "Senate passes Digital Duty of Care, 36-23",
  "Fines up to 5% of global revenue and a private right to sue. The bill "
  "must return to the House before Royal Assent.", "MLex / ACCAN"),
]

REGIONS = [
 ("NORTH AMERICA", NAVY, [
  ("CIA unclassified system breached", "First reported today; unclassified networks only.", "AP"),
  ("Huawei guilty of trade-secrets conspiracy, bank fraud", "US jury convicts the Chinese telecom giant.", "AP"),
  ("Democrats clinch House majority, 259 seats", "Largest Democratic majority since 1990.", "AP"),
  ("Army to detonate 5 tons of lead azide in Iowa", "The explosive is detonated on Wednesday.", "AP"),
  ("Poll: US voters want government to end Iran war", "Regardless of terms, voters tell the poll.", "WireMinute"),
 ]),
 ("LATIN AMERICA", TEAL, [
  ("WHO chief urges end to US fuel blockade on Cuba", "Tedros warns hospitals are running dry.", "AP"),
  ("Brazil reinforces northern border after US strikes", "Troops move after strikes in Venezuela.", "Al Jazeera"),
 ]),
 ("EUROPE", (124, 32, 86), [
  ("Russian strike on Odesa kills 2, injures 3", "A child is among the injured, officials say.", "Reuters"),
  ("US shelves business-deal proposals to end Ukraine war", "Incentives for Moscow are dropped from the plan.", "FT / Reuters"),
  ("Putin: retaliation inevitable as Ukraine hits refineries", "Moscow warns after refinery strikes.", "WireMinute"),
  ("Dutch court keeps binding climate targets", "The state must meet its own climate goals.", "NOS"),
  ("Life sentence sought over Tarwekamp bombing", "Prosecutors ask for life in The Hague case.", "NOS"),
  ("UK police arrest two men after break-in at William's home", "Two held after the royal home break-in.", "SRI"),
 ]),
 ("MIDDLE EAST", RED, [
  ("Iran vows 'all available means' to counter US blockade", "Tehran warns after the blockade is announced.", "SRI"),
  ("Trump officials split over targeting Iran's leaders", "Advisers disagree on striking the leadership.", "WireMinute"),
  ("Iran medicine shortage leaves patients hunting for drugs", "Sanctions bite as pharmacies run empty.", "DW"),
 ]),
 ("AFRICA", (150, 100, 20), [
  ("Nigerian emir suspended after sexual-assault allegation", "The emir is suspended pending an inquiry.", "Starlit"),
  ("Ethiopia offers to host inclusive Sudan peace talks", "Factions back Abiy's initiative.", "Horn Econ."),
 ]),
 ("SOUTH ASIA", (20, 110, 60), [
  ("Pakistan warns of global energy crisis", "Islamabad says prices could spike worldwide.", "SRI"),
  ("Pakistan eyes $1.21bn IMF disbursement next month", "The next tranche is due within weeks.", "WireMinute"),
  ("India: SP offers Congress 26 seats in UP polls", "Seat-sharing talks move ahead.", "CuriousCats"),
  ("Bangladesh opens Invest Bangladesh office in Guangzhou", "Dhaka courts Chinese investors.", "Starlit"),
  ("India bars 'cockroach' drive leader from London flight", "The activist is stopped at the airport.", "SRI"),
 ]),
 ("EAST ASIA", (170, 60, 20), [
  ("Xiamen Airlines orders 50 Boeing 737-8s", "China's airlines keep buying American jets.", "Starlit"),
  ("Asian tech shares slide as AI confidence weakens", "Chip stocks lead the regional fall.", "AP"),
  ("Hong Kong fire, one year on: 168 killed", "The city marks a year since the blaze.", "AP"),
  ("South Korea: Russian jets entered air-defence zone", "Seoul scrambles jets in response.", "SRI"),
 ]),
 ("SOUTHEAST ASIA", (90, 40, 130), [
  ("Indonesia: 25 Nov deadline for VP nominees", "The vote is set for 11 December.", "ENNW"),
  ("Laos graduates from least-developed status", "Vientiane leaves the UN's LDC list.", "ExcellenceGP"),
 ]),
 ("OCEANIA", (10, 90, 110), [
  ("Australia-Solomon Islands security pact signed", "Canberra deepens its Pacific ties.", "AP"),
  ("US envoy: Australia's online safety law limits free speech", "Canberra vows no step back on the law.", "CuriousCats"),
 ]),
 ("SCIENCE & WORLD", GOLD, [
  ("Pope Francis' private diary reveals spiritual crisis", "The diary tells of encounters with the devil.", "AP"),
  ("Landmine toll hits five-year high", "Myanmar and Syria bear the brunt.", "WireMinute"),
 ]),
]

EXTRA = [  # Candidate B only: 10 more stories from the AP 25 Nov summary
 ("NORTH AMERICA", NAVY, [
  ("Thomas Markle indicted by federal grand jury", "Meghan Markle's father faces federal charges.", "AP"),
  ("Nvidia board under scrutiny after reinstating Huang", "Governance questions follow the CEO's return.", "AP"),
  ("Fort Hood shooter asks court to delay firing squad", "The execution date is challenged.", "AP"),
  ("AI stocks drag US market down again", "The tech sell-off deepens.", "AP"),
  ("CDC director draws doubts from staff, ire from lawmakers", "Trust in the agency is tested.", "AP"),
  ("Pentagon hires contractors to audit base schools", "An audit of military schools begins.", "AP"),
  ("Al Gore to own Tennessee newspaper", "The former VP buys the local paper.", "AP"),
  ("Wind threatens Macy's Thanksgiving Parade balloons", "Gusts could ground the balloons.", "AP"),
  ("Pacific king tides may break records, flood coasts", "Coastal flooding is expected.", "AP"),
 ]),
]

SOURCES_LINE = ("Sources: Reuters - AP - NOS - MLex - ACCAN - FT - Al Jazeera - "
                "DW - SRI - Starlit Daily - WireMinute - Horn Economic Review "
                "- ENNW - CuriousCats - ExcellenceGrandPrix")
N_STORIES = 36
N_STORIES_B = 46


def story_count(regions):
    return sum(len(st) for _, _, st in regions)


def masthead(cv, nstories, nregions):
    x0, x1 = 24, 1000
    cv.hline(x0, 24, x1 - x0, INK, 4)
    cv.text_c("THE WORLD IN ONE DAY", 512, 38, 4, INK)
    cv.text_c("WEDNESDAY, 25 NOVEMBER 2026", 512, 82, 2, RED)
    cv.text_c("%d STORIES  -  %d REGIONS  -  ALL VERIFIED TODAY"
              % (nstories, nregions), 512, 106, 1, GRAY)
    cv.hline(x0, 124, x1 - x0, INK, 4)
    return 136


def lead_row(cv, y, leads):
    """Lead boxes across the page (2 or 3); returns the y below the row."""
    x0, gap = 24, 12
    n = len(leads)
    w = (976 - gap * (n - 1)) // n
    top = y
    for i, (kick, head, body, src) in enumerate(leads):
        x = x0 + i * (w + gap)
        cv.rect(x, y, w, 140, CARD)
        cv.rect(x, y, w, 3, RED)
        cv.text(kick, x + 10, y + 10, 1, RED)
        yy = cv.para(head, x + 10, y + 26, w - 20, 2, INK, lh=17)
        # body lines only get the space left above the source line
        avail = (y + 118) - (yy + 4)
        max_lines = max(0, avail // 9)
        blines = cv.wrap(body, w - 20, 1)[:max_lines]
        byy = yy + 4
        for ln in blines:
            cv.text(ln, x + 10, byy, 1, GRAY)
            byy += 9
        cv.text(src, x + 10, y + 126, 1, RED)
    return top + 140 + 14


def region_block(cv, x, y, w, name, color, stories, start_no, scale=1):
    """One region block; returns (y below block, next story number)."""
    cv.rect(x, y, w, 24, color)
    cv.text(name, x + 8, y + 6, 1, WHITE)
    n = start_no
    yy = y + 32
    for head, body, src in stories:
        cv.text("%d." % n, x, yy, scale, RED)
        num_w = cv.text_w("%d." % n, scale) + 4
        tx = x + num_w
        tw = w - num_w
        lines = cv.wrap(head, tw, scale)
        yy2 = yy
        for ln in lines[:2]:
            cv.text(ln, tx, yy2, scale, INK)
            yy2 += 10
        det = body + " (" + src + ")"
        for ln in cv.wrap(det, tw, scale)[:2]:
            cv.text(ln, tx, yy2, scale, GRAY)
            yy2 += 10
        yy = yy2 + 8
        n += 1
    return yy + 6, n


def balance_columns(regions, ncol):
    """Greedy balance of region blocks into ncol columns by story count."""
    cols = [[] for _ in range(ncol)]
    loads = [0] * ncol
    for r in sorted(regions, key=lambda t: -len(t[2])):
        i = loads.index(min(loads))
        cols[i].append(r)
        loads[i] += len(r[2])
    # restore the original region order inside each column
    order = {name: k for k, (name, _, _) in enumerate(regions)}
    for c in cols:
        c.sort(key=lambda t: order[t[0]])
    return cols


def footer(cv, nstories):
    y = 986
    cv.hline(24, y, 976, INK, 2)
    cv.text_c(SOURCES_LINE, 512, y + 8, 1, GRAY)
    cv.text_c("THE WORLD IN ONE DAY - 25 NOVEMBER 2026 - %d STORIES"
              % nstories, 512, y + 20, 1, GRAY)


def layout_a(cv):
    """A: frontpage classic - masthead, 3 red leads, 3-column region grid,
    numbers strip."""
    y = masthead(cv, N_STORIES, 10)
    y = lead_row(cv, y, LEADS)
    cols = balance_columns(REGIONS, 3)
    cw, gap = 314, 12
    n = 4
    bottom = y
    for i, col in enumerate(cols):
        x = 24 + i * (cw + gap)
        yy = y
        for name, color, stories in col:
            yy, n = region_block(cv, x, yy, cw, name, color, stories, n)
        bottom = max(bottom, yy)
    # numbers strip
    sy = bottom + 8
    cv.hline(24, sy, 976, INK, 2)
    stats = [("259", "House seats won by Democrats"),
             ("50", "Boeing 737-8s ordered by Xiamen Air"),
             ("5 tons", "of lead azide to be detonated in Iowa"),
             ("36-23", "Senate vote on Australia's duty of care")]
    bw = 244
    for i, (big, small) in enumerate(stats):
        x = 24 + i * bw
        cv.text_c(big, x + bw // 2, sy + 12, 3, RED)
        cv.text_c(small, x + bw // 2, sy + 42, 1, GRAY)
        if i:
            cv.vline(x - 1, sy + 10, 48, LGRAY, 2)
    footer(cv, N_STORIES)
    return cv


def layout_b(cv):
    """B: dense broadsheet - slimmer masthead, 4 columns, 46 stories,
    one-line telegraphic entries."""
    x0, x1 = 24, 1000
    cv.hline(x0, 24, x1 - x0, INK, 4)
    cv.text_c("THE WORLD IN ONE DAY", 512, 36, 3, INK)
    cv.text_c("WEDNESDAY, 25 NOVEMBER 2026  -  %d STORIES  -  10 REGIONS"
              % N_STORIES_B, 512, 70, 1, RED)
    cv.hline(x0, 86, x1 - x0, INK, 4)
    y = lead_row(cv, 98, LEADS)
    regions = REGIONS + EXTRA
    cols = balance_columns(regions, 4)
    cw, gap = 238, 8
    n = 4
    bottom = y
    for i, col in enumerate(cols):
        x = 24 + i * (cw + gap)
        yy = y
        for name, color, stories in col:
            yy, n = region_block(cv, x, yy, cw, name, color, stories, n)
        bottom = max(bottom, yy)
    footer(cv, N_STORIES_B)
    return cv


def rocket(cv, x, y, s):
    """Simple rocket + stars graphic for the hero lead (layout C)."""
    for sx, sy in ((x + 8, y + 6), (x + 150, y + 16), (x + 60, y + 120),
                   (x + 170, y + 96), (x + 24, y + 60)):
        cv.rect(sx, sy, 3, 3, GOLD)
        cv.rect(sx + 1, sy - 3, 1, 9, GOLD)
        cv.rect(sx - 3, sy + 1, 9, 1, GOLD)
    # nose cone
    for dy in range(0, 22, 2):
        w = 4 + dy
        cv.rect(x + 84 - w // 2, y + 6 + dy, w, 2, RED)
    # body
    cv.rect(x + 72, y + 28, 24, 62, WHITE)
    cv.rect(x + 72, y + 28, 24, 4, RED)
    cv.rect(x + 80, y + 48, 8, 8, GOLD)  # window
    # fins
    cv.rect(x + 60, y + 76, 12, 16, RED)
    cv.rect(x + 96, y + 76, 12, 16, RED)
    # flame
    cv.rect(x + 78, y + 90, 12, 12, GOLD)
    cv.rect(x + 81, y + 102, 6, 8, RED)
    cv.text("TIANGONG", x + 44, y + 132, 1, GOLD)
    cv.text("PAKISTAN'S FIRST", x + 30, y + 144, 1, WHITE)


def layout_c(cv):
    """C: lead-heavy - big masthead, hero lead with rocket graphic, then
    two more leads, then a 2-column region list."""
    y = masthead(cv, N_STORIES, 10)
    # hero box
    cv.rect(24, y, 976, 168, NAVY)
    rocket(cv, 40, y + 8, 1)
    cv.text("SPACE", 240, y + 14, 1, GOLD)
    yy = cv.para(LEADS[0][1], 240, y + 30, 700, 3, WHITE, lh=26)
    cv.para(LEADS[0][2], 240, yy + 6, 700, 1, (200, 200, 210), lh=9)
    cv.text(LEADS[0][3], 240, y + 148, 1, GOLD)
    y += 168 + 12
    y = lead_row(cv, y, LEADS[1:])
    # two-column region list
    cols = balance_columns(REGIONS, 2)
    cw, gap = 482, 12
    n = 4
    bottom = y
    for i, col in enumerate(cols):
        x = 24 + i * (cw + gap)
        yy = y
        for name, color, stories in col:
            yy, n = region_block(cv, x, yy, cw, name, color, stories, n)
        bottom = max(bottom, yy)
    footer(cv, N_STORIES)
    return cv


LAYOUT = "A"

LAYOUTS = {"A": layout_a, "B": layout_b, "C": layout_c}


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    cv = Canvas(W, H, PAPER)
    LAYOUTS[LAYOUT](cv)
    path = os.path.join(out_dir, "entry.png")
    write_png(cv, path)
    print("wrote", path, "layout", LAYOUT)


if __name__ == "__main__":
    main()

