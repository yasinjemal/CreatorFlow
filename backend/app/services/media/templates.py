from __future__ import annotations
from PIL import Image, ImageDraw, ImageFont
from typing import Tuple


def generate_thumbnail(output_path: str, size: Tuple[int, int] = (1280, 720), title: str = "CreatorFlow", subtitle: str = ""):
    w, h = size
    im = Image.new("RGB", size, color=(15, 15, 15))
    draw = ImageDraw.Draw(im)
    # Title box
    draw.rectangle([40, h//2 - 120, w - 40, h//2 + 120], fill=(255, 255, 255))
    # Text
    try:
        title_font = ImageFont.truetype("arial.ttf", 72)
        subtitle_font = ImageFont.truetype("arial.ttf", 36)
    except Exception:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
    draw.text((60, h//2 - 40), title, fill=(0, 0, 0), font=title_font)
    if subtitle:
        draw.text((60, h//2 + 30), subtitle, fill=(0, 0, 0), font=subtitle_font)
    im.save(output_path)
