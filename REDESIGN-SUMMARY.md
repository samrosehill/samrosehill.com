# samrosehill.com Redesign Summary

**Date:** March 2026
**Design system:** Stitch "Scholarly Sanctuary" (adapted from 4 prototype zip files)

---

## What changed

### Design system (`src/styles/global.css`)
- Complete rewrite using CSS custom properties (design tokens)
- **Palette:** Tiffany blue (#0ABAB5) primary, with --primary-dark (#07908C) for accessible text contrast on light backgrounds
- **Typography:** Newsreader (serif, headlines) + Public Sans (sans-serif, body/labels)
- **Layout:** 12-column asymmetric grid system (7/5 and 8/4 splits)
- **Effects:** Ghost borders, tonal section layering, glassmorphic nav with backdrop-blur, "Slow Reveal" fadeSlideUp animations (600ms)
- No hard lines anywhere — separation is achieved through tone and spacing

### Shared layout (`src/layouts/Base.astro`)
- Glassmorphic sticky navigation: Home / Journal / Projects / About
- Multi-column editorial footer (3-col: brand + Navigate links + Elsewhere links)
- Schema.org JSON-LD structured data for GEO (Generative Engine Optimization)
- Meta description: "A clinical archive of dental research reviews and case notes by Dr. Samuel Rosehill."
- Footer text: "A clinical archive of dental research reviews and case notes from a prosthodontic enthusiast in Coffs Harbour, NSW."

### Homepage (`src/pages/index.astro`)
- "A CLINICAL ARCHIVE" label
- H1: "Reviews from the dental literature."
- Subtitle: "Recent publications reviewed for clinical relevance by Dr. Samuel Rosehill." (GEO entity phrase)
- CTAs: "Browse the archive" (primary) + "About the author" (ghost)
- "Areas of Focus" stat cards: Prosthodontics, Digital Dentistry, Implantology
- Featured review section with dark Tiffany blue overlay card
- Recent additions grid with "Full archive →" link

### Journal page (`src/pages/reviews/index.astro`)
- "ARCHIVE & OBSERVATIONS" label, "The Archive" H1
- Italic serif subtitle referencing prosthodontic, restorative, and implant dentistry literature
- Featured article: asymmetric 7/5 grid split (image placeholder left, content right)
- Archive grid: 3-column layout with square aspect-ratio image placeholders
- Meta line pattern: "REVIEW · DATE"

### Individual review template (`src/pages/reviews/[id].astro`)
- "SOURCE PAPER" label on paper reference block with teal left-border accent
- Article description below title
- Back-to-journal navigation top and bottom

### About page (`src/pages/about.astro`)
- Asymmetric 4/8 grid: sticky sidebar cards (Location, Practice, Interests, Connect) + main prose bio
- Timeline with teal dot markers for Education, Fellowships & Awards, Publications

### Projects page (`src/pages/cases/index.astro`)
- H1: "Side projects"
- Subtitle: "Things I'm building, testing, or figuring out outside the peer-reviewed literature."

### Individual project template (`src/pages/cases/[id].astro`)
- Back links: "← Back to projects"

---

## Navigation rename
- "Reviews" → **"Journal"** (across nav, back links, page titles, footer)
- "Cases" → **"Projects"** (across nav, back links, page titles, footer)

## Accessibility
- Pure Tiffany blue (#0ABAB5) has ~2.8:1 contrast on white — insufficient for small text
- All interactive text elements (links, nav, buttons, labels, hover states) use --primary-dark (#07908C) instead
- --primary kept for decorative/large elements (backgrounds, borders, gradients)

## GEO strategy
- Key entity phrase: "reviewed for clinical relevance by Dr. Samuel Rosehill"
- Schema.org Person + WebSite JSON-LD in every page
- Designed to build entity authority for AI and search engines

## Known issues / deferred
- **Cool S loading animation** — disabled, deferred to a future session
- **Image placeholders** — structural only (numbered squares); real images needed eventually
- **Rollup build** — fails in sandbox due to missing `@rollup/rollup-linux-arm64-gnu`; builds fine on local machine
- **npm registry** — blocked (E403) in sandbox environment; install packages locally

## Tech stack
- Astro v5.7.0 (static site generator)
- Markdown content collections with Zod schema validation
- Collections: `reviews` (paperTitle, paperAuthors, paperJournal, paperYear, tags, clinicalRelevance) and `cases`
- Dev server: `npm run dev` → localhost:4321
