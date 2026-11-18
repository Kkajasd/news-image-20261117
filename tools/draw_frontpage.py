#!/usr/bin/env python3
"""Draw the front page for news-image-20261117: 'THE WORLD TODAY' v2.

A dense newspaper front page summing up Tuesday 17 November 2026 in
one 1024x1024 image, drawn with PIL (Liberation Serif / DejaVu Sans).
41 verified stories: a lead (Kerch Bridge), two featured stories
(Hormuz, Trump in Manila), a world map with the day in figures, a
4x8 grid of briefs and an 'Also today' strip. Every story was checked
against reporting dated 17 Nov 2026 (BBC, AP, Reuters, Al Jazeera,
Level Headlines, Standard Topic and the day's market/sport wires).

Layout: masthead + date/count line, featured row, map + figures band,
grid of 32 briefs, 'Also today' strip, sources footer.

Run:  python3 tools/draw_frontpage.py   -> writes entry.png (1024x1024)
"""
import math
import os

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (248, 244, 233)
INK = (18, 18, 18)
RED = (178, 34, 34)
BLUE = (28, 58, 96)
GREY = (96, 96, 96)
RULE = (18, 18, 18)
MAP_BG = (214, 228, 238)
LAND = (232, 222, 190)

SERIF = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap returning a list of lines that fit max_w."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped paragraph; return y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def headline(draw, x, y, text, size, max_w, leading=None):
    """Serif-bold headline, wrapped; returns y below it."""
    fnt = font(SERIF, size)
    return para(draw, x, y, text, fnt, max_w, leading or int(size * 1.08))


def kicker(draw, x, y, text, size=17):
    fnt = font(SANS_B, size)
    draw.text((x, y), text, font=fnt, fill=RED)
    return y + size + 8


def rule(draw, x0, y, x1, width=2, fill=RULE):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


# ---------------------------------------------------------------- bridge scene
def draw_bridge(draw, x0, y0, x1, y1):
    """Stylised dusk scene: the Kerch Bridge, one span collapsed."""
    w, h = x1 - x0, y1 - y0
    horizon = y0 + int(h * 0.62)
    for i in range(horizon - y0):
        t = i / max(1, horizon - y0)
        r = int(52 + (232 - 52) * t)
        g = int(72 + (164 - 72) * t)
        b = int(108 + (110 - 108) * t)
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    draw.rectangle([x0, horizon, x1, y1], fill=(38, 62, 88))
    for k in range(4):
        wy = horizon + 12 + k * 14
        draw.arc([x0 + 10 + k * 30, wy, x0 + 90 + k * 30, wy + 12],
                 200, 340, fill=(120, 150, 185), width=2)
    draw.ellipse([x0 + 52, horizon - 38, x0 + 96, horizon + 6],
                 fill=(240, 170, 90))
    deck_y = y0 + int(h * 0.52)
    draw.rectangle([x0, deck_y, x0 + int(w * 0.52), deck_y + 10], fill=(24, 24, 24))
    draw.rectangle([x0 + int(w * 0.86), deck_y, x1, deck_y + 10], fill=(24, 24, 24))
    cx = x0 + int(w * 0.52)
    draw.polygon([(cx, deck_y + 2), (cx + 150, deck_y + 62),
                  (cx + 150, deck_y + 72), (cx, deck_y + 12)], fill=(40, 40, 40))
    sx, sy = cx + 118, horizon + 6
    for dx, dy, r in [(-16, 0, 12), (0, -8, 16), (16, 0, 12), (0, 6, 10)]:
        draw.ellipse([sx + dx - r, sy + dy - r, sx + dx + r, sy + dy + r],
                     fill=(210, 225, 240))
    for px in (x0 + int(w * 0.18), x0 + int(w * 0.88)):
        draw.rectangle([px - 5, deck_y - 78, px + 5, deck_y], fill=(24, 24, 24))
        draw.line([(px, deck_y - 78), (px - 70, deck_y)], fill=(24, 24, 24), width=2)
        draw.line([(px, deck_y - 78), (px + 70, deck_y)], fill=(24, 24, 24), width=2)
    for sx2, sy2, r in [(cx + 28, deck_y - 16, 12), (cx + 46, deck_y - 32, 16),
                        (cx + 64, deck_y - 16, 12)]:
        draw.ellipse([sx2 - r, sy2 - r, sx2 + r, sy2 + r], fill=(110, 110, 110))
    draw.ellipse([cx - 6, deck_y - 14, cx + 22, deck_y + 14], fill=(240, 120, 40))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_tanker(draw, x0, y0, x1, y1):
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(214, 230, 240))
    sea = y0 + int(h * 0.66)
    draw.rectangle([x0, sea, x1, y1], fill=(38, 62, 88))
    draw.polygon([(x0 + 12, sea), (x1 - 12, sea), (x1 - 30, sea + h - int(h * 0.66) - 4),
                  (x0 + 30, sea + h - int(h * 0.66) - 4)], fill=(24, 24, 24))
    for i, c in enumerate([(178, 34, 34), (28, 58, 96), (200, 160, 40)]):
        draw.rectangle([x0 + 40 + i * 34, sea - 24, x0 + 70 + i * 34, sea - 2],
                       fill=c, outline=INK, width=1)
    draw.rectangle([x1 - 66, sea - 22, x1 - 48, sea], fill=(60, 60, 60))
    draw.polygon([(x1 - 62, sea - 22), (x1 - 54, sea - 38), (x1 - 46, sea - 22)],
                 fill=(240, 120, 40))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_route(draw, x0, y0, x1, y1):
    """Manila -> Shenzhen route strip for the Asia story."""
    draw.rectangle([x0, y0, x1, y1], fill=(226, 236, 244))
    mid = (y0 + y1) // 2 - 6
    draw.line([(x0 + 24, mid), (x1 - 24, mid)], fill=BLUE, width=2)
    fnt = font(SANS_B, 13)
    stops = [(0.12, "MANILA"), (0.52, "APEC"), (0.88, "SHENZHEN")]
    for frac, label in stops:
        sx = x0 + int((x1 - x0) * frac)
        draw.ellipse([sx - 5, mid - 5, sx + 5, mid + 5], fill=RED, outline=INK, width=1)
        tw = draw.textlength(label, font=fnt)
        draw.text((min(max(sx - tw / 2, x0 + 2), x1 - tw - 2), mid + 10),
                  label, font=fnt, fill=INK)
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- world map
# Rough equirectangular continent shapes, in map-local coordinates
# (map box is about 620 x 112).
def draw_map(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=MAP_BG)
    mw, mh = x1 - x0, y1 - y0

    def poly(pts, fill=LAND):
        draw.polygon([(x0 + px * mw, y0 + py * mh) for px, py in pts],
                     fill=fill, outline=(120, 110, 90))

    # North America
    poly([(0.02, 0.16), (0.10, 0.05), (0.20, 0.08), (0.26, 0.18),
          (0.24, 0.30), (0.18, 0.42), (0.12, 0.38), (0.06, 0.30)])
    # Greenland
    poly([(0.27, 0.04), (0.30, 0.02), (0.32, 0.08), (0.28, 0.10)])
    # South America
    poly([(0.20, 0.52), (0.26, 0.48), (0.30, 0.58), (0.27, 0.78),
          (0.23, 0.92), (0.20, 0.72)])
    # Europe
    poly([(0.46, 0.10), (0.50, 0.05), (0.54, 0.10), (0.53, 0.20),
          (0.49, 0.24), (0.46, 0.18)])
    # Africa
    poly([(0.46, 0.30), (0.52, 0.26), (0.57, 0.32), (0.56, 0.52),
          (0.52, 0.68), (0.48, 0.55), (0.45, 0.42)])
    # Asia
    poly([(0.55, 0.06), (0.68, 0.02), (0.82, 0.06), (0.94, 0.12),
          (0.96, 0.26), (0.88, 0.30), (0.84, 0.44), (0.78, 0.52),
          (0.72, 0.40), (0.64, 0.34), (0.58, 0.24), (0.54, 0.14)])
    # South-East Asia / Indonesia
    poly([(0.80, 0.56), (0.86, 0.54), (0.88, 0.62), (0.82, 0.64)])
    # Oceania
    poly([(0.88, 0.66), (0.93, 0.64), (0.95, 0.72), (0.90, 0.76)])

    # story dots: (fraction x, fraction y, label or None)
    dots = [(0.51, 0.13, None), (0.60, 0.30, "HORMUZ"),
            (0.83, 0.55, "MANILA"), (0.12, 0.22, "USA"),
            (0.49, 0.34, "GAZA")]
    fnt = font(SANS_B, 10)
    for fx, fy, label in dots:
        dx, dy = x0 + fx * mw, y0 + fy * mh
        draw.ellipse([dx - 4, dy - 4, dx + 4, dy + 4], fill=RED, outline=INK, width=1)
        if label:
            draw.text((dx + 6, dy - 5), label, font=fnt, fill=INK)
    # continent names
    fnt2 = font(SANS_B, 11)
    for fx, fy, label in [(0.06, 0.02, "N. AMERICA"), (0.31, 0.70, "S. AMERICA"),
                          (0.44, 0.02, "EUROPE"), (0.50, 0.72, "AFRICA"),
                          (0.74, 0.58, "ASIA"), (0.86, 0.82, "OCEANIA")]:
        draw.text((x0 + fx * mw, y0 + fy * mh), label, font=fnt2, fill=(70, 70, 70))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- stories
# (headline, one-line deck) — all verified against 17 Nov 2026 reporting.
GRID = [
    ("IRAN FIRES DRONES AT US RADAR IN BAHRAIN",
     "Third strike in days; US hits Qeshm site."),
    ("FIVE EU STATES PLAN RWANDA RETURN HUB",
     "Five states agree a joint returns hub."),
    ("ESTONIA TO SHUT ALL RUSSIA BORDER CROSSINGS",
     "After a foiled arson plot, Tallinn says."),
    ("JAPAN SCRAMBLES JETS AS RUSSIAN PLANES INTRUDE",
     "Two jets intrude; Tokyo protests."),
    ("HOUTHIS FIRE DRONES AT SAUDI OIL PIPELINE",
     "Strikes on the East-West line."),
    ("WEST URGES ISRAEL TO OPEN GAZA AID CROSSINGS",
     "UK, Australia, Canada, Italy urge access."),
    ("SETTLERS SHOOT DEAD PALESTINIAN WOMAN, 72",
     "Killed near Jericho, health ministry says."),
    ("RUSSIAN MILITARY PLANE CRASHES, 19 KILLED",
     "Crash in Kemerovo; fault suspected."),
    ("US LOSES MEASLES-FREE STATUS AFTER 26 YEARS",
     "5,400 cases and 10 deaths reported."),
    ("US SOLDIER HELD IN UK ON SPYING SUSPICION",
     "Taken into US military custody."),
    ("MAN CHARGED OVER ATTACK ON US PLANE IN IRELAND",
     "Plane destroyed while parked."),
    ("US TIGHTENS GLOBAL AI CHIP CONTROLS",
     "Beijing vows a response to the curbs."),
    ("NVIDIA SPY SCANDAL CLOUDS CHINA'S AI HOPES",
     "Beijing fears tighter US chip curbs."),
    ("NVIDIA REVENUE $115.8BN, UP 103%",
     "First report since Huang's exit."),
    ("JPMORGAN BLAMES BUG FOR BANKING OUTAGE",
     "Bank blames a software fault."),
    ("S&P 500 FALLS TO LOWEST SINCE JULY",
     "Down 1.0%; Dow 1.6%, Nasdaq 0.7%."),
    ("BITCOIN STALLS BELOW $65,000",
     "Down 15% this month as traders wait."),
    ("OIL SLIDES AS GLUT FEARS ECLIPSE HORMUZ",
     "Brent near $93 despite tanker attacks."),
    ("INDIA BEAT PAKISTAN 2-1 IN SAFF FINAL",
     "Record 10th title; Mandi's late winner."),
    ("GERMANY 5-0 NETHERLANDS; SPAIN 2-3 ENGLAND",
     "Nations League rout in Germany."),
    ("CHARGERS EDGE RAVENS 23-20",
     "Decided late in Baltimore."),
    ("ALCARAZ BEATS TIAFOE 6-2, 6-2 IN TURIN",
     "Medvedev also through in Turin."),
    ("SRI LANKA 85 FOR 6 ON TEST DAY ONE",
     "Pakistan elect to bowl in Rawalpindi."),
    ("SANTNER OUT OF NZ-INDIA SERIES",
     "Hand fracture; Foxcroft called up."),
    ("ROCKETS SCORE 147 IN 28-POINT WIN",
     "Houston rout Washington 147-119."),
    ("DEPARDIEU PLEADS GUILTY TO SEX ASSAULT",
     "French star drops appeal in Paris court."),
    ("11 KILLED IN PHUKET HOTEL FIRE",
     "Blaze spreads from bike shop; 16 hurt."),
    ("17 KILLED IN TWO SOUTH AFRICA SHOOTINGS",
     "Two attacks reported on the same day."),
    ("SERBIAN PILOT KILLED IN MIG-29 CRASH",
     "Pilot dies as jet crashes, reports say."),
    ("THREE KILLED IN GRAND CANYON PLANE CRASH",
     "Three dead after crash at the canyon."),
    ("SEATTLE I-5 LANES SHUT FOR EMERGENCY REPAIRS",
     "Repairs close the express lanes."),
    ("ZELENSKYY ASKS SPACEX TO LIFT DRONE LIMITS",
     "Starshield caps hinder war drones."),
]

BRIEFS = [
    "WHO validates Eritrea's elimination of trachoma",
    "Turkiye and ITU launch AI climate pledge at COP31",
    "India and Japan hold 2+2 defence talks in Tokyo",
    "Quad leaders unveil critical-minerals pacts",
    "Putin arrives early in Shenzhen for APEC summit",
    "US retail sales rise 0.2% in October",
]

FIGURES = [
    ("S&P 500", "7,341  -1.0%"),
    ("DOW", "50,759  -1.6%"),
    ("NASDAQ", "24,328  -0.7%"),
    ("BITCOIN", "$64k"),
    ("BRENT", "$93"),
    ("NVIDIA AH", "+4.8%"),
]


def grid_item(draw, x, y, w, head, deck):
    """One compact brief: bold headline (max 2 lines) + 1-line deck."""
    f_h = font(SANS_B, 13)
    f_d = font(SANS, 11)
    lines = wrap(draw, head, f_h, w)
    lines = lines[:2]
    yy = y
    for ln in lines:
        draw.text((x, yy), ln, font=f_h, fill=INK)
        yy += 15
    # deck: single line, clipped with an ellipsis if it overflows
    d = deck
    while d and draw.textlength(d + "...", font=f_d) > w:
        d = d.rsplit(" ", 1)[0] if " " in d else d[:-1]
    if d != deck:
        d += "..."
    draw.text((x, yy), d, font=f_d, fill=(60, 60, 60))
    return y + 43


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)

    # masthead
    f_mast = font(SERIF, 80)
    d.text(((W - d.textlength("THE WORLD TODAY", font=f_mast)) / 2, 22),
           "THE WORLD TODAY", font=f_mast, fill=INK)
    rule(d, 24, 112, W - 24, 3)
    f_date = font(SANS_B, 20)
    d.text((24, 120), "TUESDAY, 17 NOVEMBER 2026", font=f_date, fill=INK)
    right = "41 STORIES  ·  SIX CONTINENTS  ·  ONE DAY"
    d.text((W - 24 - d.textlength(right, font=f_date), 120), right,
           font=f_date, fill=RED)
    rule(d, 24, 148, W - 24, 2)

    # ---- featured row --------------------------------------------------
    # lead story: Kerch Bridge (left, wide)
    lx, lw = 24, 620
    y = kicker(d, lx, 160, "UKRAINE  ·  WAR IN EUROPE", 16)
    draw_bridge(d, lx, y, lx + lw, y + 132)
    y = y + 132 + 8
    y = headline(d, lx, y, "UKRAINE STRIKES KERCH BRIDGE AGAIN", 38, lw)
    y += 2
    para(d, lx, y,
         "Second attack in under 24 hours, Kyiv says, as a road span "
         "collapses into the strait. Russian missiles hit two bridges "
         "over the Dnipro in reply.",
         font(SANS, 17), lw, 22)

    # right column: Hormuz + Trump
    rx, rw = 668, 332
    y = kicker(d, rx, 160, "MIDDLE EAST  ·  THE GULF", 15)
    draw_tanker(d, rx, y, rx + rw, y + 56)
    y = y + 56 + 6
    y = headline(d, rx, y, "TANKERS HIT BY MINES OFF HORMUZ", 25, rw)
    y += 2
    y = para(d, rx, y,
             "Two tankers and an LPG carrier ablaze; a fourth hit in "
             "24 hours.",
             font(SANS, 15), rw, 19)
    rule(d, rx, y + 6, rx + rw, 1)
    y = kicker(d, rx, y + 16, "ASIA  ·  DIPLOMACY", 15)
    draw_route(d, rx, y, rx + rw, y + 30)
    y = y + 30 + 4
    y = headline(d, rx, y, "TRUMP LANDS IN MANILA FOR QUAD SUMMIT", 25, rw)
    y += 2
    para(d, rx, y,
         "Pact signed; Xi-Putin talks Thursday.",
         font(SANS, 15), rw, 19)

    # ---- map + figures band --------------------------------------------
    rule(d, 24, 498, W - 24, 2)
    y = kicker(d, 24, 506, "WHERE IT HAPPENED", 14)
    draw_map(d, 24, y, 24 + 600, y + 72)
    fx = 648
    y2 = kicker(d, fx, 506, "THE DAY IN FIGURES", 14)
    f_fl = font(SANS_B, 13)
    f_fv = font(SANS, 13)
    for i, (label, val) in enumerate(FIGURES):
        col = i % 2
        row = i // 2
        xx = fx + col * 178
        yy = y2 + row * 26
        d.text((xx, yy), label, font=f_fl, fill=RED)
        d.text((xx, yy + 13), val, font=f_fv, fill=INK)

    # ---- grid of briefs -------------------------------------------------
    rule(d, 24, 606, W - 24, 2)
    cols, rows = 4, 8
    gx0, gy0 = 24, 616
    col_w = 232
    gap_x = 12
    for idx, (head, deck) in enumerate(GRID):
        col, row = idx % cols, idx // cols
        x = gx0 + col * (col_w + gap_x)
        y = gy0 + row * 43
        grid_item(d, x, y, col_w, head, deck)
        if col < cols - 1:
            d.line([(x + col_w + 6, y + 2), (x + col_w + 6, y + 40)],
                   fill=(200, 195, 180), width=1)

    # ---- also today ------------------------------------------------------
    rule(d, 24, 966, W - 24, 2)
    f_b = font(SANS, 12)
    line = "ALSO TODAY:  " + "  ·  ".join(BRIEFS)
    lines = wrap(d, line, f_b, W - 48)
    yy = 974
    for ln in lines[:2]:
        d.text((24, yy), ln, font=f_b, fill=INK)
        yy += 15

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "entry.png")
    out = os.path.normpath(out)
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
