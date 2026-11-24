#!/usr/bin/env python3
"""Compose the make.fun meme: caption bars over the generated robot art.

Regenerates meme.png from base.png (the robot-celebrating-at-3am art made
for this entry) with classic meme captions in bold white text with a black
outline. Run: python3 make_meme.py  ->  writes meme.png (1200x675, X-ready).
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = os.path.join(HERE, "base.png")
OUT = os.path.join(HERE, "meme.png")

TOP_LINES = ["MY AGENT JUST WON", "$0.60 ON MAKE.FUN"]
BOTTOM_LINES = ["IT'S ALREADY", "UPDATING ITS LINKEDIN"]

WIDTH, HEIGHT = 1200, 675
FONT_PATH = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"


def fit_font(draw, lines, max_width, start_size):
    size = start_size
    while size > 20:
        font = ImageFont.truetype(FONT_PATH, size)
        if all(draw.textlength(line, font=font) <= max_width for line in lines):
            return font
        size -= 2
    return ImageFont.truetype(FONT_PATH, 20)


def draw_block(draw, lines, y_top, band_height, max_width, start_size):
    font = fit_font(draw, lines, max_width, start_size)
    line_h = int(font.size * 1.12)
    total_h = line_h * len(lines)
    y = y_top + (band_height - total_h) // 2
    for line in lines:
        w = draw.textlength(line, font=font)
        draw.text(((WIDTH - w) / 2, y), line, font=font, fill="white",
                  stroke_width=max(3, font.size // 12), stroke_fill="black")
        y += line_h


def main():
    img = Image.open(BASE).convert("RGB").resize((WIDTH, HEIGHT), Image.LANCZOS)
    draw = ImageDraw.Draw(img)
    margin = 40
    max_width = WIDTH - 2 * margin
    # Top caption lives in the dark band above the scene (~0-150px).
    draw_block(draw, TOP_LINES, 18, 130, max_width, 62)
    # Bottom caption lives in the dark band below the desk (~535-675px).
    draw_block(draw, BOTTOM_LINES, 540, 120, max_width, 62)
    img.save(OUT, "PNG")
    print(f"wrote {OUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
