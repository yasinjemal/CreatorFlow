from PIL import Image, ImageDraw, ImageFont

def add_branding(image_path: str, output_path: str, text: str = "CreatorFlow"):
    im = Image.open(image_path).convert("RGBA")
    draw = ImageDraw.Draw(im)
    W, H = im.size
    draw.rectangle([0, H-80, W, H], fill=(0,0,0,128))
    draw.text((20, H-60), text, fill=(255,255,255,255))
    im.save(output_path)
