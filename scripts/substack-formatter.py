#!/usr/bin/env python3
"""
substack-formatter.py

Transforms samrosehill.com review articles into Substack-ready content.
Extracts frontmatter metadata, appends cross-posting byline, and selects
top 5 tags for Substack's tag limit.

Usage:
  python3 scripts/substack-formatter.py <slug>          # format one article
  python3 scripts/substack-formatter.py --all           # format all articles
  python3 scripts/substack-formatter.py --list          # list all slugs with dates

Output: prints metadata summary + formatted body to stdout.
"""

import sys
import os
import re
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = PROJECT_ROOT / "src" / "content" / "reviews"
SITE_URL = "https://samrosehill.com"

# Tag priority tiers for Substack (max 5 tags).
# Broader terms rank higher; ultra-niche terms are deprioritised.
TAG_PRIORITY = {
    # Tier 1 — broad specialties (highest priority)
    "prosthodontics": 1,
    "implantology": 1,
    "digital dentistry": 1,
    "periodontology": 1,
    "restorative dentistry": 1,
    # Tier 2 — materials and techniques
    "zirconia": 2,
    "CAD/CAM": 2,
    "shade matching": 2,
    "3D printing": 2,
    "lithium disilicate": 2,
    "dental implants": 2,
    "soft tissue": 2,
    "colour science": 2,
    "robot-assisted surgery": 2,
    "immediate implant placement": 2,
    # Tier 3 — study types and methods
    "systematic review": 3,
    "ten-year study": 3,
    "colour stability": 3,
    "surgical accuracy": 3,
    "dimensional accuracy": 3,
    "crown survival": 3,
    "peri-implantitis": 3,
    "crestal bone loss": 3,
}
# Everything else defaults to tier 4


def parse_frontmatter(filepath: Path) -> tuple[dict, str]:
    """Parse YAML frontmatter and markdown body from a file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"No frontmatter found in {filepath}")
    fm = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    return fm, body


def select_tags(tags: list[str], max_tags: int = 5) -> list[str]:
    """Select top N tags by priority tier, preserving original order within tiers."""
    def tag_sort_key(tag):
        return TAG_PRIORITY.get(tag, 4)
    sorted_tags = sorted(tags, key=tag_sort_key)
    return sorted_tags[:max_tags]


def format_for_substack(slug: str) -> str:
    """Format a single article for Substack. Returns the full output string."""
    filepath = CONTENT_DIR / f"{slug}.md"
    if not filepath.exists():
        return f"ERROR: No article found at {filepath}"

    fm, body = parse_frontmatter(filepath)

    title = fm.get("title", "Untitled")
    description = fm.get("description", "")
    pub_date = fm.get("pubDate", "unknown")
    tags = fm.get("tags", [])
    selected_tags = select_tags(tags)

    # Build cross-posting byline (appended to bottom)
    # Note: Substack automatically adds a subscribe widget after every published
    # post, so no need to inject one manually.
    byline = (
        f"\n\n---\n\n"
        f"*This article was originally published on "
        f"[samrosehill.com]({SITE_URL}/reviews/{slug}).*"
    )

    formatted_body = body + byline

    # Build output
    output_parts = [
        "=" * 70,
        f"TITLE:    {title}",
        f"SUBTITLE: {description}",
        f"DATE:     {pub_date}",
        f"TAGS:     {', '.join(selected_tags)}",
        f"URL:      {SITE_URL}/reviews/{slug}",
        "=" * 70,
        "",
        formatted_body,
        "",
        "=" * 70,
    ]

    return "\n".join(output_parts)


def list_articles() -> str:
    """List all article slugs with their publication dates."""
    articles = []
    for filepath in sorted(CONTENT_DIR.glob("*.md")):
        fm, _ = parse_frontmatter(filepath)
        slug = filepath.stem
        pub_date = fm.get("pubDate", "unknown")
        title = fm.get("title", "Untitled")
        articles.append((pub_date, slug, title))

    articles.sort(key=lambda x: str(x[0]))

    lines = ["SLUG".ljust(50) + "DATE".ljust(14) + "TITLE"]
    lines.append("-" * 120)
    for pub_date, slug, title in articles:
        lines.append(f"{slug.ljust(50)}{str(pub_date).ljust(14)}{title[:56]}")

    return "\n".join(lines)


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    arg = sys.argv[1]

    if arg == "--list":
        print(list_articles())
    elif arg == "--all":
        slugs = sorted(
            f.stem for f in CONTENT_DIR.glob("*.md")
        )
        # Sort by pubDate for chronological output
        dated = []
        for slug in slugs:
            fm, _ = parse_frontmatter(CONTENT_DIR / f"{slug}.md")
            dated.append((str(fm.get("pubDate", "")), slug))
        dated.sort()

        for _, slug in dated:
            print(format_for_substack(slug))
            print("\n")
    else:
        print(format_for_substack(arg))


if __name__ == "__main__":
    main()
