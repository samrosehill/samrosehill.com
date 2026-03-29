#!/usr/bin/env python3
"""
generate-thumbnail.py

Generates a branded thumbnail by compositing:
  1. A screenshot of the source PDF's first page (title + abstract area)
  2. A tiffany-blue branded overlay with the article's one-line verdict

Usage:
  python3 scripts/generate-thumbnail.py <slug>          # reads verdict + pdfPath from frontmatter
  python3 scripts/generate-thumbnail.py --all            # generates for all articles with pdfPath set
  python3 scripts/generate-thumbnail.py <slug> <pdf>     # override PDF path

The slug determines the output filename: public/images/reviews/<slug>.png
"""

import sys
import os
import re
import textwrap
import fitz  # PyMuPDF
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = PROJECT_ROOT / "src" / "content" / "reviews"
OUTPUT_DIR = PROJECT_ROOT / "public" / "images" / "reviews"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Thumbnail dimensions
WIDTH = 1280
HEIGHT = 800

# Design tokens
PRIMARY = (10, 186, 181)        # #0ABAB5
PRIMARY_DARK = (7, 144, 140)    # #07908C
ON_PRIMARY = (255, 255, 255)    # white
SURFACE = (249, 249, 251)       # #f9f9fb
ON_SURFACE = (26, 28, 29)       # #1a1c1d
ON_SURFACE_VARIANT = (63, 73, 73)  # #3f4949
PRIMARY_FIXED = (212, 245, 243) # #d4f5f3
OVERLAY_BG = (249, 249, 251, 230)  # semi-transparent surface


def parse_frontmatter(slug: str) -> dict:
    """Read the markdown file for this slug and extract frontmatter."""
    md_path = CONTENT_DIR / f"{slug}.md"
    if not md_path.exists():
        return {}
    text = md_path.read_text()
    match = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        idx = line.find(":")
        if idx == -1:
            continue
        key = line[:idx].strip()
        val = line[idx + 1:].strip().strip('"').strip("'")
        fm[key] = val
    return fm


def render_pdf_page(pdf_path: str, dpi: int = 200) -> Image.Image:
    """Render the first page of a PDF as a PIL Image."""
    doc = fitz.open(pdf_path)
    page = doc[0]
    # Render at high DPI for crisp text
    mat = fitz.Matrix(dpi / 72, dpi / 72)
    pix = page.get_pixmap(matrix=mat)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    doc.close()
    return img


def crop_title_region(page_img: Image.Image) -> Image.Image:
    """Crop the top portion of the page (title + abstract area).
    Takes roughly the top 60% of the page, which typically captures
    journal header, title, authors, and abstract."""
    w, h = page_img.size
    crop_height = int(h * 0.55)
    return page_img.crop((0, 0, w, crop_height))


def try_load_font(names, size):
    """Try loading fonts by name, fall back to default."""
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except (OSError, IOError):
            continue
    return ImageFont.load_default()


def generate_thumbnail(slug: str, pdf_path_override: str = "") -> str:
    """Generate a composite thumbnail from a PDF and save it."""

    # --- Stage 0: Get article metadata ---
    fm = parse_frontmatter(slug)

    # Resolve PDF path: CLI override > frontmatter > error
    pdf_path = pdf_path_override
    if not pdf_path:
        pdf_path_fm = fm.get("pdfPath", "")
        if pdf_path_fm:
            pdf_path = str(PROJECT_ROOT / pdf_path_fm)
        else:
            print(f"Error: No pdfPath in frontmatter for {slug}")
            return ""

    if not os.path.exists(pdf_path):
        print(f"Error: PDF not found: {pdf_path}")
        return ""

    verdict = fm.get("verdict", "")
    if not verdict:
        print(f"Warning: No verdict in frontmatter for {slug} — strip will be empty")

    # --- Stage 1: PDF screenshot ---
    page_img = render_pdf_page(pdf_path, dpi=200)
    title_region = crop_title_region(page_img)

    # --- Stage 2: Build the composite ---
    thumb = Image.new("RGB", (WIDTH, HEIGHT), SURFACE)
    draw = ImageDraw.Draw(thumb)

    # Load fonts
    font_brand = try_load_font([
        "/System/Library/Fonts/Supplemental/Helvetica Neue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ], 14)
    font_label = try_load_font([
        "/System/Library/Fonts/Supplemental/Helvetica Neue.ttc",
        "/System/Library/Fonts/Helvetica.ttc",
    ], 11)
    font_title = try_load_font([
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/Library/Fonts/Georgia Bold.ttf",
    ], 28)
    font_title_small = try_load_font([
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
    ], 24)

    # Layout
    strip_width = 380
    paper_area_width = WIDTH - strip_width
    paper_area_height = HEIGHT

    # Resize PDF crop to fit within the right panel without cropping
    tr_w, tr_h = title_region.size
    # Fit (not fill) — scale so the entire width is visible
    scale = paper_area_width / tr_w
    new_w = int(tr_w * scale)
    new_h = int(tr_h * scale)
    title_region_resized = title_region.resize((new_w, new_h), Image.LANCZOS)

    # If the resized image is shorter than the panel, place it top-aligned
    # on a white background; if taller, crop from the bottom (keeps title visible)
    paper_crop = Image.new("RGB", (paper_area_width, paper_area_height), (255, 255, 255))
    paste_y = 0
    if new_h > paper_area_height:
        # Crop from bottom — keep the top (title + abstract)
        title_region_resized = title_region_resized.crop((0, 0, new_w, paper_area_height))
    paper_crop.paste(title_region_resized, (0, paste_y))

    # Paste paper screenshot on the right
    thumb.paste(paper_crop, (strip_width, 0))

    # --- Left branding strip ---
    draw.rectangle([(0, 0), (strip_width, HEIGHT)], fill=PRIMARY)

    # Top section: author name
    draw.text((36, 36), "DR SAMUEL ROSEHILL", fill=(255, 255, 255, 180), font=font_label)

    # Thin divider
    draw.line([(36, 65), (strip_width - 36, 65)], fill=(255, 255, 255, 60), width=1)

    # One-line verdict — large, bold, vertically centered
    verdict = fm.get("verdict", "")
    padding_x = 36
    max_text_width = strip_width - (padding_x * 2)

    font_verdict = try_load_font([
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
    ], 44)
    font_verdict_small = try_load_font([
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
    ], 36)

    # Wrap — at 44px Georgia Bold, ~8 chars per line in 308px
    chars_per_line = int(max_text_width / 20)
    wrapped = textwrap.wrap(verdict, width=chars_per_line)

    if len(wrapped) > 5:
        font_used = font_verdict_small
        chars_per_line = int(max_text_width / 16)
        wrapped = textwrap.wrap(verdict, width=chars_per_line)
        line_height = 46
    else:
        font_used = font_verdict
        line_height = 56

    # Vertically center
    text_block_height = len(wrapped) * line_height
    available_height = HEIGHT - 160
    text_start_y = 80 + (available_height - text_block_height) // 2

    for i, line in enumerate(wrapped):
        draw.text(
            (padding_x, text_start_y + i * line_height),
            line,
            fill=ON_PRIMARY,
            font=font_used,
        )

    # Bottom branding: samrosehill.com
    draw.line([(36, HEIGHT - 70), (strip_width - 36, HEIGHT - 70)],
              fill=(255, 255, 255, 60), width=1)
    draw.text((36, HEIGHT - 52), "samrosehill.com", fill=(180, 237, 233), font=font_brand)

    # Bottom accent bar across full width
    draw.rectangle([(0, HEIGHT - 4), (WIDTH, HEIGHT)], fill=PRIMARY_DARK)

    # Subtle 1px border at the seam
    draw.line([(strip_width, 0), (strip_width, HEIGHT)],
              fill=PRIMARY_DARK, width=1)

    # Save
    output_path = OUTPUT_DIR / f"{slug}.png"
    thumb.save(str(output_path), "PNG", optimize=True)
    print(f"Generated: {output_path}")
    return str(output_path)


if __name__ == "__main__":
    args = sys.argv[1:]

    if not args:
        print("Usage: python3 scripts/generate-thumbnail.py <slug> [pdf_path]")
        print("       python3 scripts/generate-thumbnail.py --all")
        sys.exit(1)

    if "--all" in args:
        # Generate for all articles that have pdfPath in frontmatter
        files = [f for f in CONTENT_DIR.iterdir() if f.suffix == ".md"]
        for f in sorted(files):
            slug = f.stem
            fm = parse_frontmatter(slug)
            if fm.get("pdfPath"):
                generate_thumbnail(slug)
            else:
                print(f"Skipping {slug} — no pdfPath in frontmatter")
    elif len(args) == 1:
        # Single slug — read everything from frontmatter
        generate_thumbnail(args[0])
    elif len(args) == 2:
        # slug + pdf path override
        generate_thumbnail(args[0], pdf_path_override=args[1])
    else:
        # Multiple slugs
        for slug in args:
            generate_thumbnail(slug)
