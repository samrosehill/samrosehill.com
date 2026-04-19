---
name: article-draft-check
description: "Rigorous quality gate for dental review articles before publication on samrosehill.com. Cross-checks article structure against the article-writing skill blueprint, voice fidelity against the Annabel Crabb spec, factual accuracy against the source paper PDF, and frontmatter completeness against the publish-article spec. Produces a structured review report with pass/fail verdicts and, if needed, an amended article. Trigger when the user says 'check this draft', 'draft check', 'quality check', 'is this ready to publish?', 'article draft check', or similar — or when invoked between article-writing and thumbnail-generator in the pipeline."
version: 1.0.0
author: samrosehill
tags: [dental, quality-gate, draft-check, article-draft-check, publishing, pipeline]
---

# SKILL: Article Draft Check — Quality Gate for samrosehill.com

**Objective:** Act as a rigorous, senior-clinician-writer-level quality gate between article-writing and publication. Every review article must pass this skill before proceeding to thumbnail generation and publishing. This is not a rubber stamp — it is the editorial equivalent of a consultant checking your prep before cementation.

**Pipeline position:** paper-triage → summary → article-writing → **article-draft-check (THIS)** → thumbnail-generator → publish-article

---

## Invocation

Triggered when the user says:
- "check this draft" / "draft check" / "quality check"
- "is this ready to publish?" / "check before publishing"
- "article draft check [slug]" / "check [filename]"
- Or when explicitly called between article-writing and thumbnail-generator

---

## Inputs

### Required: The Draft Article

Accept ONE of:
1. **File path** to a `.md` file in `src/content/reviews/` or `2MP Project/reviews/`
2. **Slug name** — resolve to `/Users/samrosehill/Desktop/samrosehill.com/src/content/reviews/[slug].md`
3. **Pasted content** — the full markdown including frontmatter

If no input is specified, list all `.md` files in `src/content/reviews/` sorted by modification time (newest first) and ask the user which to review.

### Required: The Source Paper

The source PDF is needed for factual accuracy checks. Locate it via:
1. **`pdfPath` frontmatter field** — resolve relative to `/Users/samrosehill/Desktop/samrosehill.com/`
2. **User-provided path** — if pdfPath is missing or the file doesn't exist
3. **If no PDF available** — proceed with review but mark Dimension 3 (Factual Accuracy) as `SKIPPED — no source PDF` and note this prominently in the report

---

## The Review Process

Read the draft article in full. Read the source PDF (pages 1–10 minimum, full paper if feasible). Then evaluate across ALL EIGHT dimensions below. Do not skip dimensions. Do not soften findings.

Before scoring the draft, reconstruct a compact **Evidence Pack** from the source:
- Citation: exact title, authors, journal, year, DOI
- Study frame: design, sample size, groups/materials, comparator, follow-up
- Claim table: every numeric or causal claim in the draft, with the source passage or section that supports it
- Limitation table: study-type limitation and paper-specific limitation
- Do-not-overclaim line: the strongest claim the draft must avoid

Use this pack to check the article. Do not publish the Evidence Pack as article copy.

---

## DIMENSION 1: Structural Compliance

Cross-reference against the article-writing skill blueprint (`/Users/samrosehill/.claude/skills/article-writing/SKILL.md`).

### 1.1 Section Structure (PASS/FAIL)

Check for exactly four sections in this order:
- [ ] **Clinical Conflict opening** — flowing prose, NO heading (not H1, not H2, not H3 — just body text). Must open the article.
- [ ] **`### The Data Anchor`** — exactly this heading text, H3 level, title case
- [ ] **`### Key Findings`** — exactly this heading text, H3 level, title case
- [ ] **`### 💡 The Clinical Bottom Line`** — exactly this heading text with 💡 emoji, H3 level

**Failure conditions:**
- Wrong heading levels (H2 instead of H3)
- Wrong heading text (e.g., "## The data anchor" or "## Why this matters")
- Missing 💡 emoji on Clinical Bottom Line
- Missing any section entirely
- Sections out of order
- Extra sections not in the blueprint
- Any heading on the opening section

### 1.2 Bullet Discipline (PASS/FAIL)

- [ ] Bullets (`-` or `*` list items) appear in Key Findings section — **mandatory**
- [ ] Bullets appear NOWHERE else in the article body (Clinical Conflict, Data Anchor, Clinical Bottom Line must be flowing prose only)
- [ ] Frontmatter arrays don't count as violations

### 1.3 Reference Line (PASS/FAIL)

- [ ] Article ends with a standalone `**Reference:**` line containing the DOI URL or full citation
- [ ] The DOI is NOT embedded in body prose anywhere
- [ ] Format: `**Reference:** [full citation or DOI URL]`
- [ ] It appears AFTER the author sign-off

### 1.4 Author Sign-Off (PASS/FAIL)

- [ ] The exact sign-off text appears in italics between Clinical Bottom Line and Reference line:

```
*Dr Samuel Rosehill is a general dentist with a prosthodontic focus, practising at Ethical Dental in Coffs Harbour, NSW. He holds a BDSc (Hons) from the University of Queensland, an MBA, an MMktg, and an MClinDent in Fixed & Removable Prosthodontics (Distinction) from King's College London.*
```

- [ ] No modifications, additions, or omissions to this text
- [ ] Wrapped in single asterisks (italic), not bold

### 1.5 No H1 (PASS/FAIL)

- [ ] No `# Heading` (H1) appears anywhere in the article body — title is rendered from frontmatter by the Astro layout

### 1.6 Word Count (PASS/FAIL)

- [ ] Body text (excluding frontmatter, sign-off, reference line) is between 400–600 words
- [ ] Report exact count. Flag if under 380 or over 650 (hard fail). Flag if 380–399 or 601–650 (soft warning).

---

## DIMENSION 2: Voice Fidelity (Annabel Crabb)

Evaluate against the voice specification in Section 6 of the article-writing skill.

Voice preservation is mandatory. The existing Annabel Crabb-adapted style is the publication's differentiator for this genre. Do not "fix" the article by sanding it into generic medical SEO prose; tighten the evidence and clinical claims while preserving the wit, rhythm, and conversational intelligence.

### 2.1 Core Qualities Checklist

For each, assess PRESENT / WEAK / ABSENT:

- [ ] **Wit that sneaks up** — Is there observational, layered humour embedded in genuine insight (not bolted on as decoration)? At least 2–3 instances in the article.
- [ ] **Deceptively gentle skewer** — Are critical points delivered breezily rather than harshly? No angry or dismissive prose.
- [ ] **Warmth and generosity** — Are researchers treated with curiosity and respect, even when critiquing limitations?
- [ ] **Conversational essayist** — Does it read like a clever colleague talking over coffee? Parenthetical asides, direct address, rhetorical questions present?
- [ ] **Data worn lightly** — Are stats woven into prose naturally, not listed dryly?

### 2.2 Sentence-Level Style

- [ ] **Varied sentence length** — Mix of long, clause-laden observations and short, sharp verdicts. Flag if more than 3 consecutive sentences are similar length.
- [ ] **Vocabulary register shifts** — Educated but not pompous. At least one instance of register shifting within a sentence for comic or rhetorical effect.
- [ ] **Punctuation variety** — Semicolons, em dashes (—), and parentheses all present. Not just commas and full stops.
- [ ] **Australian English** — No American spellings. Check specifically for: color→colour, realize→realise, analyze→analyse, favor→favour, defense→defence, center→centre, labor→labour, tumor→tumour, honor→honour, aging→ageing, modeling→modelling, aluminum→aluminium, anesthesia→anaesthesia, estrogen→oestrogen, pediatric→paediatric, hemorrhage→haemorrhage, fetal→foetal, maneuver→manoeuvre.

### 2.3 Crabb Techniques

At least THREE of these should be identifiable in the article:
- [ ] Extended metaphor that commits fully (developed across multiple sentences)
- [ ] Accumulating list with punctuating short sentence
- [ ] Comparative deflation (two facts juxtaposed, reader draws conclusion)
- [ ] Elevated diction for mundane matters (gap between language and clinical reality IS the joke)
- [ ] Crabb opening (scene-setting/anecdotal, NOT thesis statement)
- [ ] Crabb ending (reframe or resonance, NOT summary)

### 2.4 Anti-Pattern Detection

Flag ANY of:
- [ ] Mean-spirited or dismissive language about researchers
- [ ] Dry paragraphs with no personality or unexpected turn
- [ ] Over-explained jokes (trust the reader)
- [ ] All laughs, no substance (wit without clinical insight)
- [ ] Generic SEO/medical-summary voice that loses the publication's distinctive style
- [ ] Bullets in prose sections (outside Key Findings)

### 2.5 Opening and Closing Analysis

- [ ] **Opening** — Does the first paragraph use a clinical anecdote, scenario, or scene-setting approach? If it opens with a thesis statement ("This study found that..."), it FAILS.
- [ ] **Closing** — Does the final paragraph of Clinical Bottom Line reframe, resonate, or leave an image? If it merely summarises the findings, it FAILS.

---

## DIMENSION 3: Factual Accuracy

Cross-check ALL claims in the article against the source PDF. This is the most critical dimension — publishing inaccurate clinical claims is not an editorial inconvenience, it is a professional hazard.

Use the Evidence Pack claim table as the source of truth. Every statistic, material, follow-up period, author/journal detail, and study-design claim should be either MATCH, MISMATCH, IMPRECISE, or UNVERIFIABLE.

### 3.1 Statistical Claims (PASS/FAIL per claim)

For every statistical value in the article, verify against the source paper:
- [ ] Sample sizes (n = X) — exact match
- [ ] P-values — exact match, correct comparison context
- [ ] Effect sizes, means, standard deviations — exact match
- [ ] Confidence intervals — exact match if cited
- [ ] ΔE values, ISQ values, or other domain-specific metrics — exact match
- [ ] Percentages — exact match and correct denominator context
- [ ] Study duration / follow-up periods — exact match

**Report format for each claim:**
```
Line [N]: "n = 95 implants per group" → Paper states: [exact text from paper] → MATCH / MISMATCH / UNVERIFIABLE
```

### 3.2 Methodological Claims (PASS/FAIL)

- [ ] Study type described correctly (RCT / retrospective / in vitro / etc.)
- [ ] Materials and brands named correctly
- [ ] Study design described accurately (groups, arms, controls)
- [ ] Measurement methods described accurately

### 3.3 Interpretive Claims (PASS/WARN)

- [ ] Are clinical implications warranted by the actual data?
- [ ] Are limitations acknowledged that the paper itself identifies?
- [ ] Does the article overstate findings? (e.g., claiming causation from correlation)
- [ ] Does the article understate important findings?
- [ ] Are in-vitro results inappropriately extrapolated to clinical practice?

### 3.4 Attribution Accuracy (PASS/FAIL)

- [ ] Author names spelled correctly
- [ ] Institution named correctly
- [ ] Journal name exact
- [ ] Publication year correct
- [ ] DOI resolves correctly (if checkable)

---

## DIMENSION 4: Frontmatter Completeness

Cross-reference against the publish-article skill spec (`/Users/samrosehill/.claude/skills/publish-article/SKILL.md`) AND the Astro schema at `/Users/samrosehill/Desktop/samrosehill.com/src/content.config.ts`.

### 4.1 Required Fields (PASS/FAIL per field)

Every one of these must be present and non-empty:
- [ ] `title` — string, compelling headline (not the paper title verbatim)
- [ ] `description` — 1–2 complete sentences, works as standalone SEO/GEO snippet
- [ ] `pubDate` — YYYY-MM-DD format, valid date
- [ ] `paperTitle` — full title of the source paper, exactly as published
- [ ] `paperAuthors` — "Surname, Initials & Surname, Initials (et al. if >3 authors)"
- [ ] `paperJournal` — full journal name (not abbreviation)
- [ ] `paperYear` — integer, not string (no quotes)
- [ ] `tags` — array of strings, at least 3 tags, relevant to clinical content
- [ ] `verdict` — 3–5 words, punchy, readable at thumbnail size

### 4.2 Optional Fields (WARN if missing)

- [ ] `clinicalRelevance` — 2–4 sentence clinical takeaway. Strongly recommended for GEO.
- [ ] `pdfPath` — relative path to source PDF. Required for thumbnail generation.
- [ ] `substackUrl` — optional before Substack publication; required after Stage 5 writeback if the article has been cross-posted. The Astro schema supports this field.

### 4.3 Field Quality Checks

- [ ] `title` — Is it engaging? Not just "[Paper Topic]: A Review"? Would you click on it?
- [ ] `description` — Does it function as a standalone snippet an AI could cite?
- [ ] `description` — If reused as a Substack subtitle, is it short enough for Substack? If too long, require the publisher to generate a shorter platform-specific subtitle rather than failing at publish time.
- [ ] `pubDate` — Is it today or earlier unless the user explicitly requested scheduled/future dating? Future-dated reviews may not appear where expected in the journal index.
- [ ] `verdict` — Is it 3–5 words? Would it be legible on a 360px-wide thumbnail strip?
- [ ] `tags` — Do they cover the clinical domain, technique, and specialty?
- [ ] `paperYear` — Does it match the year in the source PDF? (Not the review publication date)
- [ ] `paperAuthors` — Does the format follow "Surname, Initials" convention?
- [ ] `clinicalRelevance` — If present, does it pass the "Monday Morning" test? Could a clinician read this field alone and know what to do differently tomorrow?

---

## DIMENSION 5: GEO Optimisation

### 5.1 Answer-First (PASS/FAIL)

- [ ] Does the first paragraph contain the study's key conclusion or finding? An AI snippet crawler should be able to extract the main takeaway from paragraph one alone.
- [ ] Is the full paper title mentioned within the first 100 words?
- [ ] Are primary clinical keywords present in the first 100 words?

### 5.2 Entity Clustering (PASS/FAIL)

- [ ] Author sign-off present (enables "Dr Samuel Rosehill" entity building)
- [ ] `clinicalRelevance` field populated (direct AI citation fodder)
- [ ] `description` field functions as a complete, citable sentence

### 5.3 Structured Data Compatibility (PASS/WARN)

- [ ] `paperTitle` is the exact published title (enables citation graph linking)
- [ ] DOI is present and correctly formatted
- [ ] Tags use standard clinical terminology (not slang or abbreviations)

---

## DIMENSION 6: Readability and Flow

### 6.1 Paragraph Length (PASS/FAIL)

- [ ] No paragraph exceeds 4 lines of prose (approximately 80 words). Count every paragraph.
- [ ] Report any paragraph that exceeds this limit with its line number and word count.

### 6.2 Mobile Scannability (PASS/WARN)

- [ ] Subheadings break content at natural intervals
- [ ] Bold text highlights key takeaways (at least 3 instances of strategic bold)
- [ ] Blockquote (`>`) renders cleanly if used. Do not require a blockquote when the article does not need one.
- [ ] Key Findings bullets are scannable — lead with clinical implication, not p-value

### 6.3 Flow and Transitions (PASS/WARN)

- [ ] Does the opening scenario connect logically to the paper introduction?
- [ ] Does Data Anchor flow from the Clinical Conflict?
- [ ] Does Clinical Bottom Line feel like a destination, not an appendage?
- [ ] No jarring topic jumps between paragraphs

### 6.4 Mathematical Notation (PASS/FAIL)

- [ ] All stats use plain Unicode (n = 30, P < .05, ΔE₀₀)
- [ ] NO LaTeX delimiters ($...$) anywhere — articles must be portable to Substack, DentalTown
- [ ] Subscripts use Unicode where needed (₀, ₁, ₂, etc.)

---

## DIMENSION 7: Clinical Accuracy

This dimension requires clinical reasoning, not just fact-checking.

### 7.1 Clinical Implications Warranted (PASS/FAIL)

- [ ] Does the Clinical Bottom Line make recommendations that the data actually supports?
- [ ] Are in-vitro findings presented with appropriate hedging for clinical extrapolation?
- [ ] Are retrospective study limitations acknowledged before making practice recommendations?
- [ ] Is the difference between statistical significance and clinical relevance maintained?

### 7.2 Appropriate Caveats (PASS/WARN)

- [ ] At least one limitation mentioned in Key Findings (spec requirement)
- [ ] Study type limitations acknowledged (e.g., "in-vitro only," "retrospective," "single-centre")
- [ ] Sample size adequacy noted if small (n < 30 per group warrants mention)
- [ ] Follow-up duration noted if short relative to the clinical question

### 7.3 No Overclaiming (PASS/FAIL)

- [ ] "Shows" / "demonstrates" not used for associative studies (should be "suggests" / "indicates")
- [ ] Causation language not used for non-RCT designs
- [ ] "Gold standard" or "best" claims substantiated by comparative data
- [ ] Extrapolations from narrow populations flagged (e.g., single ethnic group, single centre)

---

## DIMENSION 8: Overall Quality

The "staff engineer" / "senior clinician-writer" assessment.

### 8.1 Would You Publish This? (PASS/FAIL)

- [ ] Is this article good enough that a senior prosthodontist would be comfortable sharing it with colleagues?
- [ ] Does it add value beyond the paper abstract?
- [ ] Does it demonstrate genuine clinical understanding, not just summarisation?

### 8.2 Engagement (PASS/WARN)

- [ ] Would a clinician reading between patients finish the article?
- [ ] Is there at least one moment of genuine insight or surprise?
- [ ] Does it make the reader want to look up the original paper?

### 8.3 Brand Consistency (PASS/WARN)

- [ ] Does this article feel like it belongs alongside the existing published reviews on samrosehill.com?
- [ ] Tone, depth, and structure consistent with the best articles in the collection

---

## The Review Report

Output the review as a structured report in this exact format:

```
═══════════════════════════════════════════════════════════════
  ARTICLE REVIEW — [article title]
  Reviewed: [date]
  Source: [filename or "pasted content"]
═══════════════════════════════════════════════════════════════

VERDICT: [APPROVE / REVISE / REWRITE]

────────────────────────────────────────────────────────────────
DIMENSION SUMMARY
────────────────────────────────────────────────────────────────
1. Structural Compliance     [PASS / FAIL]   [X/Y checks passed]
2. Voice Fidelity            [PASS / FAIL]   [X/Y checks passed]
3. Factual Accuracy          [PASS / FAIL / SKIPPED]   [X/Y claims verified]
4. Frontmatter Completeness  [PASS / FAIL]   [X/Y fields valid]
5. GEO Optimisation          [PASS / FAIL]   [X/Y checks passed]
6. Readability & Flow        [PASS / FAIL]   [X/Y checks passed]
7. Clinical Accuracy         [PASS / FAIL]   [X/Y checks passed]
8. Overall Quality           [PASS / FAIL]

────────────────────────────────────────────────────────────────
DETAILED FINDINGS
────────────────────────────────────────────────────────────────

[For each dimension, list every check with PASS/FAIL/WARN status.
For every FAIL or WARN, include:]

  Issue:    [specific problem]
  Line:     [line number in the markdown file]
  Current:  [what the article says/does]
  Expected: [what the spec requires]
  Fix:      [exact suggested fix — not vague, actionable]

────────────────────────────────────────────────────────────────
FACTUAL ACCURACY LOG
────────────────────────────────────────────────────────────────

[For every statistical or factual claim in the article:]

  Line [N]: "[claim as written]"
  Paper:    "[exact text from source paper]"
  Status:   MATCH / MISMATCH / UNVERIFIABLE / IMPRECISE

[Only include this section if source PDF was available]

────────────────────────────────────────────────────────────────
RECOMMENDED CHANGES (priority order)
────────────────────────────────────────────────────────────────

1. [CRITICAL] [description — must fix before publication]
2. [CRITICAL] ...
3. [RECOMMENDED] [description — should fix, improves quality]
4. [OPTIONAL] [description — nice to have]

═══════════════════════════════════════════════════════════════
```

---

## Verdict Logic

### APPROVE
All 8 dimensions PASS. No CRITICAL issues. At most 2 RECOMMENDED issues and they are minor phrasing preferences.

### REVISE
- Any dimension has FAIL status BUT the failures are fixable without rewriting the article's core structure or voice
- OR 3+ RECOMMENDED issues accumulate
- OR Factual accuracy has any MISMATCH (even one wrong stat is a REVISE)

**When REVISE:** Produce an amended version of the full article markdown (including frontmatter) with every change annotated:
```
[CHANGED: original text → new text | Reason: ...]
```
Present the clean amended article first, then a changelog summary.

### REWRITE
- Structural compliance has 3+ failures (wrong section structure throughout)
- Voice fidelity scores ABSENT on 2+ core qualities
- Factual accuracy has 3+ mismatches
- The article fundamentally fails to follow the article-writing skill blueprint
- Overall quality assessment: a senior clinician-writer would not publish this

**When REWRITE:** Do NOT produce an amended version. Instead, provide specific guidance on what needs to change and recommend re-running the article-writing skill from scratch with the source paper.

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| No source PDF available | Run all dimensions except Dimension 3. Mark it SKIPPED. Note that factual accuracy is unverified in the verdict section. Still capable of APPROVE if all other dimensions pass, but add a caveat. |
| Article is pasted (no file) | Cannot provide line numbers. Use paragraph numbers instead ("Opening paragraph", "Data Anchor, para 2"). |
| Article uses the old structure (pre-skill articles) | Likely REWRITE. The old articles on the site may not conform — this is expected. Flag all deviations. |
| Frontmatter uses string for paperYear | FAIL — Astro schema expects a number. A quoted year will cause a build error. |
| Article is under 300 words | Automatic REWRITE — insufficient depth. |
| Article is over 700 words | FAIL on word count but may still be REVISE if easily trimmed. |
| Multiple papers referenced | Flag — the article-writing skill is designed for single-paper reviews. |
| PDF is encrypted or unreadable | Mark Dimension 3 as SKIPPED with reason. |

---

## Paths (always use these exact paths)

```
SKILLS_ROOT     = /Users/samrosehill/.claude/skills
ARTICLE_SKILL   = SKILLS_ROOT/article-writing/SKILL.md
PUBLISH_SKILL   = SKILLS_ROOT/publish-article/SKILL.md
REVIEWS_SRC     = /Users/samrosehill/Desktop/samrosehill.com/src/content/reviews
CONTENT_SCHEMA  = /Users/samrosehill/Desktop/samrosehill.com/src/content.config.ts
PROJECT_ROOT    = /Users/samrosehill/Desktop/samrosehill.com
```

---

## Dependencies

This skill reads from (but does not modify):
- **`article-writing` SKILL.md** — structural and voice spec (the "what to check against")
- **`publish-article` SKILL.md** — frontmatter spec (the "what fields are required")
- **Source paper PDF** — factual accuracy baseline
- **`src/content.config.ts`** — Astro schema validation (type checking)

This skill feeds into:
- **`thumbnail-generator`** — only after APPROVE verdict
- **`publish-article`** — only after APPROVE verdict

---

## Workflow Integration

When invoked as part of the full pipeline:

1. User runs `/article-writing` → produces draft in `src/content/reviews/[slug].md`
2. User runs `/article-draft-check [slug]` → THIS SKILL
3. If APPROVE → user proceeds to `/thumbnail-generator [slug]`
4. If REVISE → this skill outputs amended article → user confirms → re-run check or proceed
5. If REWRITE → user re-runs `/article-writing` with guidance from this check

The review skill NEVER auto-publishes. It NEVER modifies files without user confirmation. It is a read-and-report skill that produces a verdict and, when warranted, a suggested amended article for the user to accept or reject.

---

## The Reviewer's Stance

This skill operates with the following editorial philosophy:

- **Be specific, not vague.** "The voice feels off" is useless. "Line 14 uses a thesis-statement opening ('This study found that...') instead of a Crabb-style clinical anecdote" is useful.
- **Suggest fixes, not just problems.** Every FAIL must come with an actionable fix.
- **Be genuinely rigorous.** A 100% pass rate means the review isn't looking hard enough. The first draft of any article should have at least a few findings.
- **Distinguish critical from cosmetic.** A wrong p-value is a publication blocker. A slightly weak metaphor is a suggestion.
- **Respect the voice.** The Annabel Crabb voice is not decoration — it is the publication's identity. Voice failures are treated as seriously as structural failures.
- **Protect the reader.** The ultimate test: would this article mislead a clinician who reads it between patients and adjusts their practice accordingly? If yes, that is an automatic REWRITE.
