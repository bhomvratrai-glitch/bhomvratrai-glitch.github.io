from PIL import Image, ImageDraw, ImageFont
import os

width = 1200
height = 630

# Create base image with clean modern gradient
image = Image.new("RGBA", (width, height), (15, 23, 42, 255))
draw = ImageDraw.Draw(image)

# Background subtle gradient effect
for y in range(height):
    r = int(15 + (y / height) * 15)
    g = int(23 + (y / height) * 20)
    b = int(42 + (y / height) * 35)
    draw.line([(0, y), (width, y)], fill=(r, g, b, 255))

# Decorative glow circles
draw.ellipse([850, -100, 1300, 350], fill=(225, 29, 72, 40))
draw.ellipse([-100, 300, 400, 800], fill=(8, 145, 178, 35))

# Logo box
logo_box = [100, 100, 190, 190]
draw.rounded_rectangle(logo_box, radius=20, fill=(225, 29, 72, 255))

# Try loading standard system font or default
try:
    font_bold_huge = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 68)
    font_bold_large = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 52)
    font_medium = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial.ttf", 28)
    font_pill = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 22)
    font_logo = ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", 46)
except Exception:
    font_bold_huge = ImageFont.load_default()
    font_bold_large = ImageFont.load_default()
    font_medium = ImageFont.load_default()
    font_pill = ImageFont.load_default()
    font_logo = ImageFont.load_default()

# Draw TB text inside logo
draw.text((120, 118), "TB", font=font_logo, fill=(255, 255, 255, 255))

# Brand Title next to logo
draw.text((215, 115), "The", font=font_bold_large, fill=(255, 255, 255, 255))
draw.text((315, 115), "Bhom", font=font_bold_large, fill=(244, 63, 94, 255))
draw.text((218, 172), "VERIFIED DEALS & DIGITAL TOOLS", font=font_pill, fill=(148, 163, 184, 255))

# Main Headline
draw.text((100, 245), "Top Shopping Deals, Free HD Video", font=font_bold_huge, fill=(255, 255, 255, 255))
draw.text((100, 325), "Downloader & Expert Buying Guides", font=font_bold_huge, fill=(56, 189, 248, 255))

# Description
desc_text = "Verified 70-90% off Amazon & Flipkart loot drops, 1080p Instagram & YouTube video\nextraction with zero watermarks, and hands-on gadget testing reviews."
draw.text((100, 425), desc_text, font=font_medium, fill=(203, 213, 225, 255))

# Feature Pills at bottom
pills = [
    ("🔥 8,700+ Verified Deals", (251, 100, 27, 40), (251, 146, 60, 255)),
    ("⚡ 1080p Video Extractor", (8, 145, 178, 40), (56, 189, 248, 255)),
    ("📖 Tested Buying Guides", (16, 185, 129, 40), (52, 211, 153, 255)),
    ("✓ 100% Free & Safe", (100, 116, 139, 40), (226, 232, 240, 255)),
]

x_offset = 100
y_pill = 525
for text, bg_color, text_color in pills:
    pill_w = len(text) * 11 + 30
    draw.rounded_rectangle([x_offset, y_pill, x_offset + pill_w, y_pill + 42], radius=21, fill=bg_color, outline=text_color, width=1)
    draw.text((x_offset + 15, y_pill + 10), text, font=font_pill, fill=text_color)
    x_offset += pill_w + 16

# Save PNG
out_path = os.path.join(os.path.dirname(__file__), "..", "og-image.png")
image.convert("RGB").save(out_path, "PNG", quality=95)
print(f"Generated: {out_path} ({os.path.getsize(out_path)} bytes)")
