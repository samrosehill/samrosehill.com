---
name: thumbnail-generator
description: "Generate a branded thumbnail image for a samrosehill.com dental review article. Composites a screenshot of the source PDF's first page with a tiffany-blue branding strip showing the article's one-line verdict. Trigger when the user says 'generate thumbnail', 'make thumbnail', 'create thumbnail', 'generate image for this article', or similar."
version: 1.1.0
author: samrosehill
tags: [thumbnail, image, dental, publishing, branding]
---

# SKILL: Thumbnail Generator for samrosehill.com

**Objective:** Generate a branded 1200x630 PNG thumbnail for a dental review article by compositing the source paper's first page with a tiffany-blue branding strip.

---

## Prerequisites

- Python 3 with `PyMuPDF` and `Pillow` installed
- The article must exist in `src/content/reviews/[slug].md`
- The article frontmatter must include `verdict` (3-5 word takeaway)
- The article frontmatter must include `pdfPath` (relative path to source PDF)

---

## Thumbnail Design Specification

### Dimensions
- **Output:** 1200 x 630 px (1.91:1 aspect ratio)
- **Why 1.91:1:** Native format for LinkedIn link previews (1200x627) and Substack social previews (1200x630). No cropping when cross-posting.
- **Format:** PNG, optimised

### Layout: Two Panels

| Element | Width | Content |
|---------|-------|---------|
| **Left strip** | 360px | Tiffany blue branding panel |
| **Right panel** | 840px | PDF first page screenshot |

### Left Branding Strip Design

The strip uses the site's primary colour (#0ABAB5) as background and contains three elements stacked vertically:

**1. Top — Author Name (fixed)**
- Text: `DR SAMUEL ROSEHILL`
- Font: Helvetica Neue, 11px, white at 70% opacity
- Position: 36px from left, 36px from top
- Followed by a 1px white divider line at y=65

**2. Middle — Verdict Text (dynamic sizing)**
- Font: Georgia Bold, white
- **Font size is calculated dynamically** — the script tries sizes from 56px down to 28px and picks the largest size where:
  - Every wrapped line fits within the strip width (360px minus 72px padding = 288px usable)
  - Total lines do not exceed 4 (at sizes >= 40px) or 5 (at smaller sizes)
- Line height: 1.3x the font size
- **Vertically centred** between the top divider (y=80) and the bottom branding zone (y=HEIGHT-70)
- This ensures short verdicts like "3x more accurate" render large and punchy, while longer ones like "Design shapes soft tissue" scale down gracefully

**3. Bottom — Site URL (fixed)**
- Text: `samrosehill.com`
- Font: Helvetica Neue, 14px, light teal (#B4EDE9)
- Position: 36px from left, 52px from bottom
- Preceded by a 1px white divider line at y=HEIGHT-70

### Right Panel — PDF Screenshot

- Source: First page of the paper PDF, rendered at 200 DPI via PyMuPDF
- Crop: Top 55% of the page (captures journal header, title, authors, abstract)
- Scaling: Fit to panel width (no horizontal cropping). If taller than panel, crops from bottom. If shorter, white background fills below.
- Seam: 1px tiffany-dark (#07908C) border between strip and panel

### Bottom Accent
- 4px dark tiffany (#07908C) bar across the full width at the bottom edge

---

## Usage

### Single article:
```bash
python3 scripts/generate-thumbnail.py [slug]
```

### All articles:
```bash
python3 scripts/generate-thumbnail.py --all
```

The script reads `verdict` and `pdfPath` from the article's frontmatter automatically. No additional arguments needed.

---

## Output

- **Location:** `public/images/reviews/[slug].png`

---

## Workflow Position

This skill runs **after** `/article-writing` and **before** `/publish-article`:

1. `/article-writing` — produces the article text + verdict
2. **`/thumbnail-generator`** — generates the thumbnail, opens it for user review
3. `/publish-article` — commits the article + approved thumbnail, deploys

## User Approval

After generating the thumbnail, **always**:
1. Open the PNG in Preview (`open public/images/reviews/[slug].png`)
2. Ask the user if they approve the thumbnail
3. If rejected, ask what to change (verdict text, crop, etc.) and regenerate
4. Only proceed to `/publish-article` after explicit approval

---

## Verdict Guidelines

The `verdict` field should be:
- **3-5 words maximum** — must be readable at thumbnail size
- **The punchiest clinical takeaway** — the "should I click?" signal
- **Not a summary** — a verdict, opinion, or key stat

**Good examples:**
- "3x more accurate"
- "Gold standard holds"
- "92% survival at 10 years"
- "ISQ isn't the full story"
- "Design shapes soft tissue"
- "1350°C — stronger crowns"

**Bad examples (too long):**
- "Robotic systems achieve threefold improvements in positioning"
- "The spectrophotometer remains the gold standard for shade matching"

---

## Troubleshooting

- **"No pdfPath in frontmatter"**: Add the `pdfPath` field to the article's markdown file
- **"No verdict in frontmatter"**: Add the `verdict` field — see guidelines above
- **PDF not found**: Check the `pdfPath` is relative to the project root (`/Users/samrosehill/Desktop/samrosehill.com/`)
- **Verdict text too cramped**: Shorten the verdict. The dynamic sizing handles most cases, but verdicts over 5 words may look small.
