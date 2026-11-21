#!/usr/bin/env python3
"""news-image-20261121: draw one image summing up the world news of
Saturday 21 November 2026 and write it to /output/entry.png.

Deterministic: same input, same bytes, every run. No network, no clock,
no randomness. If Pillow is unavailable, copy the bundled entry.png
(same picture) instead.
"""
import os
import shutil
import sys

OUT = sys.argv[1] if len(sys.argv) > 1 else "/output/entry.png"
HERE = os.path.dirname(os.path.abspath(__file__))

# --- the day's news (all first reported on 21 November 2026) -------------
DATE_LINE = "SATURDAY 21 NOVEMBER 2026"
MASTHEAD = "THE WORLD IN ONE PICTURE"

LEAD = {
    "tag": "PERU  ·  EARTHQUAKE",
    "headline": "6.8 QUAKE SHAKES PERU",
    "sub": "Central Peru trembles; Lima residents rush outdoors. "
           "No casualties reported.",
}

STORIES = [
    {
        "tag": "CHINA  ·  SUMMIT",
        "headline": "TRUMP, XI AND PUTIN MEET",
        "sub": "Leaders hold a historic trilateral summit in China.",
        "color": (232, 184, 75),
    },
    {
        "tag": "UKRAINE  ·  WAR",
        "headline": "RUSSIA HITS KYIV BRIDGES",
        "sub": "Missiles strike three bridges; 2 dead, 42 hurt in Kryvyi Rih.",
        "color": (91, 141, 239),
    },
    {
        "tag": "EUROPE  ·  SECURITY",
        "headline": "POLAND SEEKS NATO HELP",
        "sub": "After Russian aircraft breach its airspace.",
        "color": (47, 168, 160),
    },
    {
        "tag": "INDIA  ·  MARKETS",
        "headline": "RECORD CASH INTO INDIA",
        "sub": "\u20b91.22 lakh crore in November \u2014 the biggest monthly "
               "inflow ever.",
        "color": (76, 175, 125),
    },
]

BOTTOM = {
    "tag": "SPORT  ·  CRICKET",
    "headline": "RAHUL COMPLETES THE SENA SET",
    "sub": "First Indian opener with Test centuries in South Africa, England, "
           "New Zealand and Australia \u2014 100 in Wellington.",
    "color": (155, 126, 222),
}

FOOTER = "All stories first reported on 21 November 2026"


def draw():
    from PIL import Image, ImageDraw, ImageFont

    W, H = 1024, 1024
    M = 36  # margin
    BG = (14, 30, 51)
    PANEL = (22, 41, 74)
    GOLD = (232, 184, 75)
    WHITE = (255, 255, 255)
    MUTED = (184, 198, 219)
    RED = (214, 69, 69)

    def font(name, size):
        return ImageFont.truetype(
            "/usr/share/fonts/truetype/dejavu/%s" % name, size)

    f_mast = font("DejaVuSans-Bold.ttf", 27)
    f_date = font("DejaVuSans-Bold.ttf", 54)
    f_lead_head = font("DejaVuSans-Bold.ttf", 62)
    f_lead_sub = font("DejaVuSans.ttf", 29)
    f_tag = font("DejaVuSans-Bold.ttf", 21)
    f_head = font("DejaVuSans-Bold.ttf", 26)
    f_sub = font("DejaVuSans.ttf", 24)
    f_foot = font("DejaVuSans.ttf", 20)

    img = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(img)

    def wrap(text, fnt, max_w):
        lines, cur = [], ""
        for word in text.split(" "):
            trial = (cur + " " + word).strip()
            if fnt.getlength(trial) <= max_w:
                cur = trial
            else:
                if cur:
                    lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return lines

    def text_w(text, fnt):
        return fnt.getlength(text)

    def chip(x, y, label, color):
        pad_x, pad_y = 12, 7
        tw = text_w(label, f_tag)
        th = f_tag.getbbox(label)[3]
        d.rounded_rectangle(
            [x, y, x + tw + 2 * pad_x, y + th + 2 * pad_y + 4],
            radius=6, fill=color)
        d.text((x + pad_x, y + pad_y), label, font=f_tag, fill=(10, 20, 35))
        return th + 2 * pad_y + 4

    # masthead + date
    d.text(((W - text_w(MASTHEAD, f_mast)) / 2, 30), MASTHEAD,
           font=f_mast, fill=GOLD)
    d.text(((W - text_w(DATE_LINE, f_date)) / 2, 66), DATE_LINE,
           font=f_date, fill=WHITE)
    d.rectangle([M, 140, W - M, 144], fill=GOLD)

    # lead story
    chip(M, 164, LEAD["tag"], RED)
    d.text((M, 208), LEAD["headline"], font=f_lead_head, fill=WHITE)
    sub_lines = wrap(LEAD["sub"], f_lead_sub, W - 2 * M)
    y = 292
    for line in sub_lines:
        d.text((M, y), line, font=f_lead_sub, fill=MUTED)
        y += 38
    d.line([M, 382, W - M, 382], fill=(60, 85, 125), width=2)

    # 2x2 grid
    cw = (W - 2 * M - 20) // 2
    ch = 168
    gx = [M, M + cw + 20]
    gy = [400, 588]
    for i, s in enumerate(STORIES):
        x, y0 = gx[i % 2], gy[i // 2]
        d.rounded_rectangle([x, y0, x + cw, y0 + ch], radius=10, fill=PANEL)
        chip(x + 16, y0 + 14, s["tag"], s["color"])
        head_lines = wrap(s["headline"], f_head, cw - 32)
        yy = y0 + 52
        for line in head_lines:
            d.text((x + 16, yy), line, font=f_head, fill=WHITE)
            yy += 34
        sub_lines = wrap(s["sub"], f_sub, cw - 32)
        yy = y0 + 92
        for line in sub_lines:
            d.text((x + 16, yy), line, font=f_sub, fill=MUTED)
            yy += 30

    # bottom strip: sport
    y0 = 776
    d.rounded_rectangle([M, y0, W - M, y0 + 152], radius=10, fill=PANEL)
    chip(M + 16, y0 + 14, BOTTOM["tag"], BOTTOM["color"])
    d.text((M + 16, y0 + 52), BOTTOM["headline"], font=f_head, fill=WHITE)
    sub_lines = wrap(BOTTOM["sub"], f_sub, W - 2 * M - 32)
    yy = y0 + 92
    for line in sub_lines:
        d.text((M + 16, yy), line, font=f_sub, fill=MUTED)
        yy += 30

    # footer
    d.text(((W - text_w(FOOTER, f_foot)) / 2, 952), FOOTER,
           font=f_foot, fill=MUTED)

    return img


def main():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        bundled = os.path.join(HERE, "entry.png")
        os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
        shutil.copyfile(bundled, OUT)
        print("PIL unavailable; copied bundled entry.png to %s" % OUT)
        return
    img = draw()
    os.makedirs(os.path.dirname(OUT) or ".", exist_ok=True)
    img.save(OUT, format="PNG")
    print("wrote %s (%dx%d)" % (OUT, img.width, img.height))


if __name__ == "__main__":
    main()
