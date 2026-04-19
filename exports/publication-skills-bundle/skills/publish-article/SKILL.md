---
name: publish-article
description: "Publish a dental review article to samrosehill.com. Takes a completed article (from the article-writing skill or user-provided content) and publishes it to the live site by creating the correct markdown file, committing to git, and pushing via SSH to trigger Vercel deployment. Trigger when the user says 'publish this', 'publish to the site', 'add this to the site', 'post this article', or similar."
version: 1.0.0
author: samrosehill
tags: [publishing, astro, dental, content, vercel, github]
---

# SKILL: Publish Article to samrosehill.com

**Objective:** Take a completed dental review article and publish it to samrosehill.com via the GitHub → Vercel pipeline.

---

## Site Publishing Facts

- **Site:** samrosehill.com — Astro static site
- **Content directory:** `/Users/samrosehill/Desktop/samrosehill.com/src/content/reviews/`
- **Routing:** Automatic — filename becomes the journal URL slug (e.g., `zirconia-bonding-study.md` → `samrosehill.com/journal/zirconia-bonding-study`)
- **Deploy pipeline:** Commit to git → `git push origin main` (SSH) → Vercel auto-deploys (takes ~1–2 minutes)

---

## Step 1: Derive the Slug

Generate a URL-friendly slug from the article title:
- Lowercase, hyphen-separated
- Remove special characters and punctuation
- Keep it short but descriptive (4–7 words max)
- Example: "Can Your Phone Camera Replace a Spectrophotometer?" → `phone-camera-vs-spectrophotometer`

---

## Step 2: Build the Frontmatter

Every review file requires this exact frontmatter schema:

```yaml
---
title: "Article headline — as written"
description: "1–2 sentence summary for SEO/GEO. Should be a complete sentence that works as a standalone snippet."
pubDate: YYYY-MM-DD
paperTitle: "Full title of the source paper, exactly as published"
paperAuthors: "Surname, Initials & Surname, Initials (et al. if >3 authors)"
paperJournal: "Full journal name"
paperYear: YYYY
tags: ["tag1", "tag2", "tag3"]
clinicalRelevance: "2–4 sentence clinical take-away. What does this mean for practice? Written in plain, confident clinical language."
verdict: "3–5 word punchy takeaway for thumbnail display"
pdfPath: "relative/path/to/source-paper.pdf"
---
```

**Required fields:** title, description, pubDate, paperTitle, paperAuthors, paperJournal, paperYear, tags, verdict
**Optional fields:** clinicalRelevance (include whenever possible — it improves GEO), pdfPath (relative path to source PDF — required for thumbnail generation), substackUrl (leave absent until the Substack post is published, then write it back and redeploy)

**pubDate:** Use today's date unless the user specifies otherwise. Do not future-date an article unless the user explicitly wants scheduled publication; future-dated reviews can sort ahead of newly published work on the journal index.

Do not add unsupported frontmatter fields for platform-specific publishing. If Substack needs a shorter subtitle than the site `description`, generate it in the Substack publish step or a publish manifest, not in review frontmatter unless `src/content.config.ts` has been updated to allow it.

---

## Step 3: Format the Article Body

The markdown body follows the article-writing skill structure:
- Opening prose (no heading) — the Clinical Conflict
- `### The Data Anchor` section
- `### Key Findings` section (bullets permitted here only)
- `### 💡 The Clinical Bottom Line` section
- Author sign-off (italicised, see Step 3a below)
- `**Reference:** https://doi.org/XXXXXXX` as the final line (standalone, not in body prose)

**Do not add a top-level H1** — the title is rendered from frontmatter by the layout.

### Step 3a: Author Sign-Off (GEO Entity Building)

Every article must include this exact sign-off in italics, placed between the Clinical Bottom Line and the Reference line:

```
*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*
```

This is mandatory for GEO entity clustering — it builds the author's identity profile across AI search platforms.

---

## Step 4: Write the File

Create the file at:
```
/Users/samrosehill/Desktop/samrosehill.com/src/content/reviews/[slug].md
```

---

## Step 5: Commit to Git

**Note:** The thumbnail should already exist at `public/images/reviews/[slug].png` — it is generated via the `/thumbnail-generator` skill *before* publishing. If it doesn't exist, ask the user to run the thumbnail generator first.

Run:
```bash
git add src/content/reviews/[slug].md public/images/reviews/[slug].png
git commit -m "feat: add review — [article title]"
```

Working directory: `/Users/samrosehill/Desktop/samrosehill.com`

---

## Step 6: Push to Origin

Push the commit directly via SSH:

```bash
git push origin main
```

Confirm to the user:

> "Article committed and pushed. Vercel will have it live within 1–2 minutes at `samrosehill.com/journal/[slug]`."

---

## Validation Checklist

Before committing, verify:
- [ ] All required frontmatter fields are present (including `verdict`)
- [ ] Thumbnail generated at `public/images/reviews/[slug].png`
- [ ] `pubDate` is in `YYYY-MM-DD` format
- [ ] `pubDate` is today or earlier unless the user explicitly requested a future date
- [ ] `paperYear` is an integer (not a string)
- [ ] `tags` is an array of strings
- [ ] `substackUrl` is absent before Substack publication or a valid Substack URL after cross-post writeback
- [ ] No H1 in the body (title comes from frontmatter)
- [ ] DOI is on a standalone `**Reference:**` line at the end
- [ ] Bullets only appear in Key Findings section
- [ ] Australian English spelling throughout
- [ ] File is saved to the correct directory

---

## Example Complete File

```markdown
---
title: "Can Your Phone Camera Replace a Spectrophotometer?"
description: "Kizilkaya and colleagues test whether standardised digital photography with colour-analysis software can match the spectrophotometer for shade matching — and the answer is complicated."
pubDate: 2026-03-29
paperTitle: "Can Digital Color Applications be an Alternative to Color Spectrophotometers?"
paperAuthors: "Kizilkaya, Kara & İpek"
paperJournal: "International Journal of Prosthodontics"
paperYear: 2026
tags: ["prosthodontics", "shade matching", "digital dentistry", "colour science"]
clinicalRelevance: "The spectrophotometer remains the most internally consistent shade-matching tool. A standardised photograph with a cross-polarised filter and free colour-analysis software can produce reproducible shade data from equipment most clinics already own."
verdict: "Gold standard holds"
pdfPath: "2MP Project/journals/Journal of Prosthodontics/2025/Kizilkaya_2025_can-digital-color-applications-be-an-alternative-t.pdf"
---

There is a particular kind of professional crisis that strikes dentists at the colour-matching stage...

### The Data Anchor

They measured thirty maxillary central incisors...

### Key Findings

- **Finding one** (clinical implication first, p-value second)
- **Finding two**

### 💡 The Clinical Bottom Line

The spectrophotometer isn't going anywhere...

**Reference:** https://doi.org/10.11607/ijp.XXXX
```
