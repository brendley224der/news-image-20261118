#!/usr/bin/env python3
"""Render entry.png: a newspaper-front-page infographic summing up the world
news of Wednesday 18 November 2026.

Drawn with Pillow (build-time tool only). The submitted program is main.py,
which only copies the finished entry.png; Pillow is never needed at grade time.
All six stories were reported on 18 November 2026 (checked against AP, BBC,
Al Jazeera, DW, Reuters and other outlets' reporting of the day).
"""
import textwrap
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (246, 241, 231)
INK = (22, 22, 34)
NAVY = (22, 35, 63)
RED = (163, 22, 33)
GREY = (90, 88, 80)
PANEL_BG = (255, 255, 255)
PANEL_EDGE = (205, 198, 182)

FONT_DIR = "/usr/share/fonts/truetype/dejavu/"


def font(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)


SERIF_B = lambda s: font("DejaVuSerif-Bold.ttf", s)
SERIF = lambda s: font("DejaVuSerif.ttf", s)
SANS_B = lambda s: font("DejaVuSans-Bold.ttf", s)
SANS = lambda s: font("DejaVuSans.ttf", s)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real text widths."""
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_plane(d, cx, cy, s, color):
    # Simple jet silhouette, nose pointing up-right.
    body = [(cx - 26 * s, cy + 6 * s), (cx + 10 * s, cy - 14 * s),
            (cx + 28 * s, cy - 16 * s), (cx + 8 * s, cy + 2 * s),
            (cx + 22 * s, cy + 12 * s), (cx + 2 * s, cy + 12 * s),
            (cx - 6 * s, cy + 22 * s), (cx - 14 * s, cy + 10 * s)]
    d.polygon(body, fill=color)
    d.line([(cx - 30 * s, cy + 26 * s), (cx + 30 * s, cy - 22 * s)],
           fill=color, width=max(2, int(3 * s)))


def draw_bridge(d, cx, cy, s, color):
    # Suspension bridge: deck, arch, suspenders, water.
    d.line([(cx - 34 * s, cy + 8 * s), (cx + 34 * s, cy + 8 * s)],
           fill=color, width=max(3, int(4 * s)))
    d.arc([cx - 30 * s, cy - 26 * s, cx + 30 * s, cy + 14 * s],
          start=180, end=360, fill=color, width=max(3, int(4 * s)))
    for x in (-20, -10, 0, 10, 20):
        d.line([(cx + x * s, cy - 14 * s), (cx + x * s, cy + 8 * s)],
               fill=color, width=max(2, int(2 * s)))
    for x in (-30, -15, 0, 15, 30):
        d.line([(cx + x * s, cy + 18 * s), (cx + (x + 8) * s, cy + 18 * s)],
               fill=color, width=max(2, int(2 * s)))


def draw_trade(d, cx, cy, s, color):
    # Rising bars with an upward arrow: growing trade.
    for i, h in enumerate((14, 24, 34)):
        x0 = cx - 28 * s + i * 18 * s
        d.rectangle([x0, cy + 16 * s - h * s, x0 + 12 * s, cy + 16 * s],
                    fill=color)
    d.line([(cx - 30 * s, cy + 6 * s), (cx - 2 * s, cy - 16 * s),
            (cx + 30 * s, cy - 26 * s)], fill=color,
           width=max(3, int(4 * s)))
    d.polygon([(cx + 30 * s, cy - 26 * s), (cx + 16 * s, cy - 26 * s),
               (cx + 30 * s, cy - 12 * s)], fill=color)


def draw_scales(d, cx, cy, s, color):
    # Scales of justice: post, beam, two pans.
    d.line([(cx, cy - 26 * s), (cx, cy + 24 * s)], fill=color,
           width=max(3, int(4 * s)))
    d.line([(cx - 28 * s, cy - 20 * s), (cx + 28 * s, cy - 20 * s)],
           fill=color, width=max(3, int(4 * s)))
    for sx in (-28, 28):
        d.line([(cx + sx * s, cy - 20 * s), (cx + sx * s, cy - 2 * s)],
               fill=color, width=max(2, int(2 * s)))
        d.polygon([(cx + (sx - 12) * s, cy - 2 * s),
                   (cx + (sx + 12) * s, cy - 2 * s),
                   (cx + sx * s, cy + 12 * s)], outline=color,
                  width=max(2, int(2 * s)))
    d.rectangle([cx - 14 * s, cy + 24 * s, cx + 14 * s, cy + 28 * s],
                fill=color)


def draw_parliament(d, cx, cy, s, color):
    # Classical building: pediment, columns, base.
    d.polygon([(cx - 30 * s, cy - 18 * s), (cx + 30 * s, cy - 18 * s),
               (cx, cy - 32 * s)], fill=color)
    for i in range(4):
        x0 = cx - 26 * s + i * 15 * s
        d.rectangle([x0, cy - 14 * s, x0 + 7 * s, cy + 20 * s], fill=color)
    d.rectangle([cx - 32 * s, cy + 20 * s, cx + 32 * s, cy + 27 * s],
                fill=color)
    d.rectangle([cx - 32 * s, cy - 18 * s, cx + 32 * s, cy - 14 * s],
                fill=color)


def draw_jet(d, cx, cy, s, color):
    # Delta jet climbing, with speed lines.
    d.polygon([(cx - 26 * s, cy + 16 * s), (cx + 6 * s, cy - 26 * s),
               (cx + 12 * s, cy - 26 * s), (cx + 30 * s, cy + 10 * s),
               (cx + 12 * s, cy + 8 * s), (cx + 4 * s, cy + 22 * s)],
              fill=color)
    for y in (-8, 4, 16):
        d.line([(cx - 34 * s, cy + y * s), (cx - 14 * s, cy + y * s)],
               fill=color, width=max(2, int(3 * s)))


ICONS = {
    "plane": draw_plane,
    "bridge": draw_bridge,
    "trade": draw_trade,
    "scales": draw_scales,
    "parliament": draw_parliament,
    "jet": draw_jet,
}

# (kicker, headline, caption, accent colour, icon)
STORIES = [
    ("ASIA  ·  DIPLOMACY",
     "Trump lands in Manila for Quad talks",
     "The US president meets the leaders of Japan, India and Australia "
     "ahead of a visit to China, as the ASEAN summit wraps up.",
     (22, 35, 63), "plane"),
    ("EUROPE  ·  WAR",
     "Ukraine hits Crimea bridge again",
     "Kyiv strikes the bridge to occupied Crimea for a second day "
     "running, as Russian attacks hit bridges in Kyiv.",
     (150, 40, 40), "bridge"),
    ("TRADE  ·  AMERICAS – ASIA",
     "Canada and China extend trade deals",
     "Xi Jinping meets Mark Carney and the two sides widen trade "
     "cooperation ahead of the APEC summit.",
     (31, 110, 80), "trade"),
    ("BRITAIN  ·  MIDDLE EAST",
     "UK sanctions Israeli settler firms",
     "Britain blacklists firms behind West Bank settlements in a push "
     "to protect the two-state solution.",
     (122, 84, 20), "scales"),
    ("ISRAEL  ·  POLITICS",
     "Knesset elects a new Speaker",
     "Matan Kahana wins the Speaker's chair in a vote seen as a blow "
     "to Prime Minister Netanyahu.",
     (88, 60, 130), "parliament"),
    ("ASIA  ·  SECURITY",
     "Japan scrambles jets over Russian planes",
     "Fighters are sent up after suspected Russian military aircraft "
     "enter Japanese airspace.",
     (40, 90, 130), "jet"),
]

ALSO = ("Modi's Indo-Pacific pitch at the East Asia Summit  •  "
        "Cyclone Akvan strengthens in the Bay of Bengal  •  "
        "Estonia to shut its Russia border after a drone-maker 'sabotage' bid")


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    # ---- Masthead ----
    d.line([(26, 30), (998, 30)], fill=INK, width=3)
    d.line([(26, 36), (998, 36)], fill=INK, width=1)
    title = "THE WORLD TODAY"
    f_title = SERIF_B(62)
    d.text(((W - d.textlength(title, font=f_title)) / 2, 48),
           title, font=f_title, fill=NAVY)
    date = "WEDNESDAY 18 NOVEMBER 2026"
    f_date = SANS_B(34)
    d.text(((W - d.textlength(date, font=f_date)) / 2, 118),
           date, font=f_date, fill=RED)
    sub = "One day's world news — in one picture"
    f_sub = SERIF(20)
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 158),
           sub, font=f_sub, fill=GREY)
    d.line([(26, 188), (998, 188)], fill=INK, width=2)

    # ---- Story panels: 2 columns x 3 rows ----
    gx, gy = 26, 200
    gap = 12
    pw = (W - 2 * gx - gap) // 2
    ph = 240
    icon_w = 92
    for i, (kicker, headline, caption, accent, icon) in enumerate(STORIES):
        col, row = i % 2, i // 2
        x0 = gx + col * (pw + gap)
        y0 = gy + row * (ph + gap)
        x1, y1 = x0 + pw, y0 + ph
        d.rectangle([x0, y0, x1, y1], fill=PANEL_BG, outline=PANEL_EDGE,
                    width=2)
        # Icon column.
        d.rectangle([x0, y0, x0 + icon_w, y1], fill=accent)
        ICONS[icon](d, x0 + icon_w // 2, y0 + ph // 2, 1.0, (255, 255, 255))
        # Text column.
        tx = x0 + icon_w + 14
        tw = x1 - tx - 12
        f_kick = SANS_B(16)
        d.text((tx, y0 + 16), kicker, font=f_kick, fill=accent)
        f_head = SERIF_B(27)
        y = y0 + 44
        for line in wrap(d, headline, f_head, tw)[:2]:
            d.text((tx, y), line, font=f_head, fill=INK)
            y += 32
        f_cap = SANS(19)
        y += 8
        for line in wrap(d, caption, f_cap, tw)[:4]:
            d.text((tx, y), line, font=f_cap, fill=(52, 52, 62))
            y += 24

    # ---- Footer: also today + source line ----
    fy = gy + 3 * ph + 2 * gap + 10
    d.line([(26, fy), (998, fy)], fill=INK, width=2)
    f_also_b = SANS_B(16)
    f_also = SANS(16)
    label = "ALSO TODAY — "
    lw = d.textlength(label, font=f_also_b)
    d.text((26, fy + 8), label, font=f_also_b, fill=RED)
    y = fy + 8
    for line in wrap(d, ALSO, f_also, W - 52 - lw)[:2]:
        d.text((26 + lw, y), line, font=f_also, fill=INK)
        y += 20
    src = "Reported Wednesday 18 November 2026  ·  Sources: AP, BBC, Al Jazeera, DW, Reuters"
    f_src = SANS(13)
    d.text(((W - d.textlength(src, font=f_src)) / 2, 1006),
           src, font=f_src, fill=GREY)

    img.save("entry.png", optimize=True)
    print("saved entry.png", img.size)


if __name__ == "__main__":
    main()
