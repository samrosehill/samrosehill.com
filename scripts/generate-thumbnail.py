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

# Thumbnail dimensions (1.91:1 — optimal for LinkedIn + Substack)
WIDTH = 1200
HEIGHT = 630

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
    strip_width = 360
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

    # One-line verdict — dynamically sized to fill the strip width
    verdict = fm.get("verdict", "")
    padding_x = 36
    max_text_width = strip_width - (padding_x * 2)

    # Find the optimal font size: try sizes from large to small,
    # pick the largest where all wrapped lines fit within max_text_width
    font_paths = [
        "/System/Library/Fonts/Supplemental/Georgia Bold.ttf",
        "/System/Library/Fonts/Supplemental/Georgia.ttf",
    ]

    best_font_size = 28  # minimum
    best_wrapped = [verdict]
    best_font = None

    for size in range(56, 26, -2):
        test_font = try_load_font(font_paths, size)
        # Wrap by measuring actual pixel width
        words = verdict.split()
        lines = []
        current = ""
        for word in words:
            test_line = f"{current} {word}".strip()
            bbox = draw.textbbox((0, 0), test_line, font=test_font)
            if bbox[2] - bbox[0] > max_text_width and current:
                lines.append(current)
                current = word
            else:
                current = test_line
        if current:
            lines.append(current)

        # Check all lines fit and we don't have too many lines
        all_fit = all(
            (draw.textbbox((0, 0), line, font=test_font)[2] -
             draw.textbbox((0, 0), line, font=test_font)[0]) <= max_text_width
            for line in lines
        )
        max_lines = 4 if size >= 40 else 5
        if all_fit and len(lines) <= max_lines:
            best_font_size = size
            best_wrapped = lines
            best_font = test_font
            break

    if best_font is None:
        best_font = try_load_font(font_paths, best_font_size)

    line_height = int(best_font_size * 1.3)

    # Vertically center the text block between the divider and bottom branding
    text_block_height = len(best_wrapped) * line_height
    top_zone = 80       # below the divider
    bottom_zone = 70    # above bottom branding
    available_height = HEIGHT - top_zone - bottom_zone
    text_start_y = top_zone + (available_height - text_block_height) // 2

    for i, line in enumerate(best_wrapped):
        draw.text(
            (padding_x, text_start_y + i * line_height),
            line,
            fill=ON_PRIMARY,
            font=best_font,
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
