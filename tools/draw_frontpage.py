#!/usr/bin/env python3
"""Draw the front page for news-image-20261117: 'THE WORLD TODAY'.

A newspaper front page summing up Tuesday 17 November 2026 in one
1024x1024 image, drawn with PIL (DejaVu / Liberation fonts, both
bundled with the OS). Every story was verified against reporting
dated 17 Nov 2026 (BBC, AP, Reuters, Al Jazeera via daily briefs).

Layout: masthead + date line, lead story (Kerch Bridge) with a drawn
illustration, two right-column stories (Hormuz, Trump in Asia), a row
of three panels (markets, space, Europe), and an 'Also today' strip.

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
    # sky gradient: dusk blue -> pale orange at the horizon
    horizon = y0 + int(h * 0.62)
    for i in range(horizon - y0):
        t = i / max(1, horizon - y0)
        r = int(52 + (232 - 52) * t)
        g = int(72 + (164 - 72) * t)
        b = int(108 + (110 - 108) * t)
        draw.line([(x0, y0 + i), (x1, y0 + i)], fill=(r, g, b))
    # sea
    draw.rectangle([x0, horizon, x1, y1], fill=(38, 62, 88))
    for k in range(4):
        wy = horizon + 12 + k * 14
        draw.arc([x0 + 10 + k * 30, wy, x0 + 90 + k * 30, wy + 12],
                 200, 340, fill=(120, 150, 185), width=2)
    # sun glow low on the horizon, left of the bridge
    draw.ellipse([x0 + 52, horizon - 38, x0 + 96, horizon + 6],
                 fill=(240, 170, 90))
    # bridge deck (left, intact) and right approach
    deck_y = y0 + int(h * 0.52)
    draw.rectangle([x0, deck_y, x0 + int(w * 0.52), deck_y + 10], fill=(24, 24, 24))
    draw.rectangle([x0 + int(w * 0.86), deck_y, x1, deck_y + 10], fill=(24, 24, 24))
    # collapsed span: tilted deck sliding into the water
    cx = x0 + int(w * 0.52)
    draw.polygon([(cx, deck_y + 2), (cx + 150, deck_y + 62),
                  (cx + 150, deck_y + 72), (cx, deck_y + 12)], fill=(40, 40, 40))
    # splash where the span meets the water
    sx, sy = cx + 118, horizon + 6
    for dx, dy, r in [(-16, 0, 12), (0, -8, 16), (16, 0, 12), (0, 6, 10)]:
        draw.ellipse([sx + dx - r, sy + dy - r, sx + dx + r, sy + dy + r],
                     fill=(210, 225, 240))
    # pylons and cables
    for px in (x0 + int(w * 0.18), x0 + int(w * 0.88)):
        draw.rectangle([px - 5, deck_y - 78, px + 5, deck_y], fill=(24, 24, 24))
        draw.line([(px, deck_y - 78), (px - 70, deck_y)], fill=(24, 24, 24), width=2)
        draw.line([(px, deck_y - 78), (px + 70, deck_y)], fill=(24, 24, 24), width=2)
    # smoke plumes hugging the break
    for sx2, sy2, r in [(cx + 28, deck_y - 16, 12), (cx + 46, deck_y - 32, 16),
                        (cx + 64, deck_y - 16, 12)]:
        draw.ellipse([sx2 - r, sy2 - r, sx2 + r, sy2 + r], fill=(110, 110, 110))
    # fire glow at the break
    draw.ellipse([cx - 6, deck_y - 14, cx + 22, deck_y + 14], fill=(240, 120, 40))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- small icons
def draw_tanker(draw, x0, y0, x1, y1):
    h = y1 - y0
    draw.rectangle([x0, y0, x1, y1], fill=(214, 230, 240))
    sea = y0 + int(h * 0.66)
    # sea
    draw.rectangle([x0, sea, x1, y1], fill=(38, 62, 88))
    # hull + containers
    draw.polygon([(x0 + 12, sea), (x1 - 12, sea), (x1 - 30, sea + h - int(h * 0.66) - 4),
                  (x0 + 30, sea + h - int(h * 0.66) - 4)], fill=(24, 24, 24))
    for i, c in enumerate([(178, 34, 34), (28, 58, 96), (200, 160, 40)]):
        draw.rectangle([x0 + 40 + i * 34, sea - 24, x0 + 70 + i * 34, sea - 2],
                       fill=c, outline=INK, width=1)
    # funnel + flame
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


def draw_chart(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(238, 238, 232))
    bars = [(26, 52, (34, 139, 34)), (52, 34, (178, 34, 34)), (40, 62, (34, 139, 34)),
            (62, 30, (178, 34, 34)), (48, 70, (34, 139, 34))]
    bw = (x1 - x0 - 20) // len(bars)
    for i, (up, dn, col) in enumerate(bars):
        bx = x0 + 12 + i * bw
        draw.line([(bx + bw // 2, y0 + 12), (bx + bw // 2, y1 - 12)],
                  fill=INK, width=2)
        top = y0 + 12 + up // 4
        bot = y1 - 14 - dn // 4
        draw.rectangle([bx + 4, top, bx + bw - 4, max(bot, top + 6)],
                       fill=col)
    # chip, top-right corner clear of the bars
    cx, cy = x1 - 30, y0 + 12
    draw.rectangle([cx - 13, cy - 10, cx + 13, cy + 10], fill=INK)
    draw.rectangle([cx - 6, cy - 4, cx + 6, cy + 4], fill=(240, 120, 40))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_rocket(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(180, 210, 235))
    cx = (x0 + x1) // 2
    # rocket body, upright, breaking up
    draw.polygon([(cx - 8, y0 + 10), (cx + 8, y0 + 10), (cx + 14, y0 + 38),
                  (cx - 14, y0 + 38)], fill=(245, 245, 245), outline=INK)
    draw.polygon([(cx - 14, y0 + 38), (cx + 14, y0 + 38), (cx + 10, y0 + 58),
                  (cx - 10, y0 + 58)], fill=(178, 34, 34), outline=INK)
    draw.polygon([(cx - 26, y0 + 50), (cx - 12, y0 + 42), (cx - 10, y0 + 62)],
                 fill=(178, 34, 34))
    draw.polygon([(cx + 26, y0 + 50), (cx + 12, y0 + 42), (cx + 10, y0 + 62)],
                 fill=(178, 34, 34))
    # falling fragment + burst
    fx, fy = x0 + 24, y0 + 46
    draw.polygon([(fx, fy), (fx + 16, fy + 6), (fx + 8, fy + 22), (fx - 6, fy + 12)],
                 fill=(120, 120, 120), outline=INK)
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        draw.line([(cx + 24 + 9 * math.cos(a), y0 + 26 + 9 * math.sin(a)),
                   (cx + 24 + 18 * math.cos(a), y0 + 26 + 18 * math.sin(a))],
                  fill=(240, 120, 40), width=3)
    # smoke trail
    for i, r in enumerate([7, 10, 13]):
        draw.ellipse([cx - r, y1 - 14 - i * 10 - r, cx + r, y1 - 14 - i * 10 + r],
                     fill=(225, 225, 225))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


def draw_eu(draw, x0, y0, x1, y1):
    draw.rectangle([x0, y0, x1, y1], fill=(28, 58, 120))
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    r = min(x1 - x0, y1 - y0) // 2 - 14
    for k in range(12):
        a = math.radians(k * 30 - 90)
        sx, sy = cx + r * math.cos(a), cy + r * math.sin(a)
        draw.ellipse([sx - 4, sy - 4, sx + 4, sy + 4], fill=(255, 210, 60))
    draw.rectangle([x0, y0, x1, y1], outline=INK, width=2)


# ---------------------------------------------------------------- page
def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    d.rectangle([10, 10, W - 11, H - 11], outline=INK, width=3)

    # masthead
    f_mast = font(SERIF, 86)
    d.text(((W - d.textlength("THE WORLD TODAY", font=f_mast)) / 2, 24),
           "THE WORLD TODAY", font=f_mast, fill=INK)
    rule(d, 24, 118, W - 24, 3)
    f_date = font(SANS_B, 21)
    d.text((24, 128), "TUESDAY, 17 NOVEMBER 2026", font=f_date, fill=INK)
    right = "WORLD EDITION  ·  THE DAY IN ONE IMAGE"
    d.text((W - 24 - d.textlength(right, font=f_date), 128), right,
           font=f_date, fill=INK)
    rule(d, 24, 158, W - 24, 2)

    # ---- lead story: Kerch Bridge -------------------------------------
    lx, lw = 24, 628
    y = kicker(d, lx, 172, "UKRAINE  ·  WAR IN EUROPE")
    draw_bridge(d, lx, y, lx + lw, y + 168)
    y = y + 168 + 12
    y = headline(d, lx, y, "UKRAINE STRIKES KERCH BRIDGE AGAIN", 42, lw)
    y += 4
    para(d, lx, y,
         "Second attack in under 24 hours, Kyiv says, as a road span "
         "collapses into the strait. Russian missiles hit two bridges "
         "over the Dnipro in reply.",
         font(SANS, 19), lw, 25)

    # ---- right column --------------------------------------------------
    rx, rw = 676, 324
    y = kicker(d, rx, 172, "MIDDLE EAST  ·  THE GULF")
    draw_tanker(d, rx, y, rx + rw, y + 62)
    y = y + 62 + 8
    y = headline(d, rx, y, "TANKERS HIT BY MINES OFF HORMUZ", 27, rw)
    y += 2
    y = para(d, rx, y,
             "Two ships ablaze; a third US carrier reaches the Gulf.",
             font(SANS, 16), rw, 20)
    rule(d, rx, y + 8, rx + rw, 1)
    y = kicker(d, rx, y + 20, "ASIA  ·  DIPLOMACY")
    draw_route(d, rx, y, rx + rw, y + 40)
    y = y + 40 + 6
    y = headline(d, rx, y, "TRUMP LANDS IN MANILA FOR ASIAN SUMMIT", 27, rw)
    y += 2
    para(d, rx, y,
         "Three-way talks with Xi and Putin set for Thursday at APEC "
         "in Shenzhen.",
         font(SANS, 16), rw, 19)

    # ---- second row ----------------------------------------------------
    rule(d, 24, 584, W - 24, 2)
    panels = [
        ("MARKETS  ·  TECH", draw_chart,
         "NVIDIA REPORTS AFTER HUANG EXIT",
         "First earnings since the chief's resignation. JPMorgan blames "
         "a software bug for Monday's banking outage."),
        ("SPACE", draw_rocket,
         "VULCAN ROCKET FAILS — 40 AMAZON SATELLITES LOST",
         "ULA launcher breaks up minutes after lift-off from Cape "
         "Canaveral."),
        ("EUROPE", draw_eu,
         "FIVE EU STATES PLAN RWANDA RETURN HUB",
         "Estonia to shut every Russia border crossing after a foiled "
         "arson plot."),
    ]
    pxs = [(24, 324), (360, 324), (696, 304)]
    for (kick, icon, head, deck), (px, pw) in zip(panels, pxs):
        y = kicker(d, px, 598, kick)
        icon(d, px, y, px + pw, y + 78)
        y = y + 78 + 10
        y = headline(d, px, y, head, 26, pw)
        y += 2
        para(d, px, y, deck, font(SANS, 16), pw, 21)

    # ---- also today ----------------------------------------------------
    rule(d, 24, 872, W - 24, 2)
    y = kicker(d, 24, 884, "ALSO TODAY")
    y = para(d, 24, y,
             "Houthis say they fired drones at Saudi Arabia's East-West oil "
             "pipeline  ·  Iran fires drones at a US radar site in Bahrain, "
             "its third strike there in days  ·  WHO validates Eritrea's "
             "elimination of trachoma.",
             font(SANS, 16), W - 48, 21)
    rule(d, 24, 972, W - 24, 1)
    f_foot = font(SERIF_R, 15)
    foot = ("All events of Tuesday 17 November 2026 — as reported by BBC, AP, "
            "Reuters and Al Jazeera.")
    d.text(((W - d.textlength(foot, font=f_foot)) / 2, 980), foot,
           font=f_foot, fill=GREY)

    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                       "entry.png")
    out = os.path.normpath(out)
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
