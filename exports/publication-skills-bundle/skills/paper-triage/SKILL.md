# Skill: paper-triage

## Purpose

Systematically triage the dental PDF library in `2MP Project/`, maintain a CSV tracker of every paper's status, generate clinical screening summaries, and feed selected papers into the `article-writing` and `publish-article` skills for publication on samrosehill.com.

---

## Invocation

User says something like:
- "paper triage"
- "triage some papers"
- "what papers are ready to review?"
- "show me my paper tracker"
- "triage 10 papers from COIR"

---

## Paths (always use these exact paths)

```
PROJECT_ROOT   = /Users/samrosehill/Desktop/samrosehill.com
PAPERS_ROOT    = PROJECT_ROOT/2MP Project
JOURNALS_DIR   = PAPERS_ROOT/journals
TRACKER_CSV    = PAPERS_ROOT/paper-tracker.csv
SELECTED_DIR   = PAPERS_ROOT/selected
REVIEWS_SRC    = PROJECT_ROOT/src/content/reviews
DRAFTS_DIR     = PAPERS_ROOT/reviews
```

---

## On Every Invocation — Pre-flight Checklist

1. **Check for tracker** — does `paper-tracker.csv` exist?
   - No → run **Phase 1: Initialize** first, then continue
   - Yes → skip to step 2

2. **Scan for new PDFs** — find all `.pdf`/`.PDF` files recursively under `JOURNALS_DIR` that are NOT already in the tracker. Add any new ones as `unreviewed` rows (append to CSV). Report count of new additions.

3. **Display dashboard:**
   ```
   ── Paper Tracker ─────────────────────────────────────
   Unreviewed:   XXXX
   Summarised:    XXX
   Selected:       XX
   Passed:         XX
   Published:      XX
   Total:        XXXX
   ──────────────────────────────────────────────────────
   ```

4. **Ask what to do** (unless the user's original message already specified):
   - [T] Triage a batch (default 10)
   - [S] Show selected papers awaiting full review
   - [P] Progress report by journal
   - [W] Write a full article for a selected paper
   - [Q] Quit

---

## Phase 1 — Initialize (first run only)

### Step 1: Scan all PDFs

```python
find JOURNALS_DIR -name "*.pdf" -o -name "*.PDF"
```

For each file, parse metadata from filename where possible:
- Pattern `Author_YYYY_slug.pdf` → extract `author`, `year`, `slug`
- Pattern `ABBREV_Author_YYYY_slug.pdf` → extract journal from abbreviation, `author`, `year`, `slug`
- Anything else → set `author=unknown`, `year=unknown`, `slug=unknown`

Journal from path: extract the folder name immediately under `journals/` as the `journal` field.

### Step 2: Write CSV

Create `paper-tracker.csv` with these columns (in order):

```
filepath, filename, author, year, slug, journal, status, date_cataloged, date_triaged, date_selected, date_published, article_slug, notes
```

- Set `status = unreviewed` for all rows
- Set `date_cataloged = today's date (YYYY-MM-DD)`
- Leave `date_triaged`, `date_selected`, `date_published`, `article_slug`, `notes` empty

### Step 3: Backfill published articles

Read all `.md` files in `REVIEWS_SRC`. For each:
- Extract `paperAuthors` from frontmatter (first author surname)
- Extract `pubDate` from frontmatter
- Search CSV for rows where `author` matches first author surname (case-insensitive)
- If match found: set `status=published`, `article_slug=<slug from filename>`, `date_published=pubDate`
- If no match: add a new row with `filepath=src/content/reviews/<file>`, `status=published`, `article_slug=<slug>`, `notes=no PDF found`

### Step 4: Backfill drafts

Read all `.md` files in `DRAFTS_DIR` (these are in-progress drafts). For each draft:
- Check whether the matched PDF already has `status=published` in the CSV (cross-reference against the published backfill from Step 3)
- If the PDF is already published: **delete the stale draft file** from `DRAFTS_DIR` and do NOT set status to `draft` (it stays `published`)
- If the PDF is NOT published: mark as `status=draft`

This prevents stale drafts from lingering after articles have been published through the pipeline.

### Step 5: Report

```
Initialized paper-tracker.csv
  Total PDFs scanned:  XXXX
  Published (backfilled): XX
  Draft (backfilled):   X
  Unreviewed:          XXXX
```

---

## Phase 2 — Triage

### Input from user

Ask (or infer from message):
1. **Batch size** — default 10
2. **Ordering** — options:
   - `journal:<name>` — papers from a specific journal
   - `year:<YYYY>` — papers from a specific year
   - `keyword:<word>` — slug/filename contains keyword
   - `random` — random sample
   - `oldest` — by year ascending (default if nothing specified)
   - `newest` — by year descending

### For each paper in the batch

1. **Prefer pre-extracted text:** Check if a `.md` file exists alongside the PDF (same directory, same basename, `.md` extension). If yes, read the `.md` file instead of the PDF — this saves significant tokens. If no `.md` exists, read the PDF using pypdf (pages 1–5 max, suppress warnings).
2. Extract:
   - Full paper title
   - Authors (up to 4, then "et al.")
   - Journal name (prefer manuscript text; use path only as fallback)
   - Year
   - DOI
   - Study type (RCT / systematic review / meta-analysis / in vitro / retrospective / case series / case report / expert opinion)
   - Sample size (n = X)
   - Abstract / key findings
3. Update CSV: set `author`, `year`, `slug`, `journal` from extracted data (overwrite `unknown` values). If text and path disagree, trust the source text and add the path-derived value to `notes` as `path journal: [value]`.
4. Assign a screening priority score:
   - Evidence strength: 1–5
   - Clinical relevance: 1–5
   - Novelty / angle: 1–5
   - Reader usefulness: 1–5
   - Overclaiming risk: low / medium / high

Use the score to help the user choose papers, not to replace editorial judgement.

### Display format (for each paper)

```
────────────────────────────────────────────────────────
Paper 1/10: [Author] et al. ([Year])
Title:      [Full paper title]
Journal:    [Journal name]
DOI:        [DOI or "not found"]
Study type: [type]
Sample:     [n = X, description]
Priority:   [publish / maybe / pass] — Evidence [1-5], Clinical [1-5], Novelty [1-5], Reader [1-5], Risk [low/medium/high]

Design:     [study design, groups/materials/intervention/comparator, follow-up]
Result:     [main numeric finding(s), with units and comparison context]
Limit:      [the key limitation or generalisability caveat]
Angle:      [why this is or is not worth publishing for samrosehill.com]
Do not overclaim: [the strongest claim the article must avoid]

[Short factual clinical summary. Plain language, but more detailed than an abstract skim.
Explain what was studied, what was found, why it matters clinically, and why this paper should or should not move forward.
No Annabel Crabb voice here — this is screening only.]
────────────────────────────────────────────────────────
```

After displaying all summaries in the batch:

```
Which papers do you want to select for full review?
Enter numbers (e.g. 1,3,7), "none", or "all":
```

### After user selection

- Selected papers: `status=selected`, `date_selected=today`, copy PDF to `SELECTED_DIR/`
- Unselected papers: `status=summarised`, `date_triaged=today`
- Explicitly rejected (if user says "pass on X"): `status=passed`, add reason to `notes`

---

## Phase 3 — Write Full Article (for a selected paper)

Triggered by user choosing [W] or saying "write the article for X".

1. Display list of `selected` papers from CSV
2. User picks one (or specifies in original message)
3. Read the full PDF (all pages)
4. **Invoke the `article-writing` skill logic** — generate a 400–600 word Annabel Crabb-voice dental review. Follow that skill's structure exactly:
   - No heading for opening Clinical Conflict section
   - Data Anchor section (flowing prose, no bullets)
   - Key Findings (bullets only here)
   - Clinical Bottom Line
   - Author sign-off
   - Reference line
5. Show draft to user for approval
6. On approval: **invoke the `publish-article` skill** — derive slug, write frontmatter, save to `src/content/reviews/`, commit to git, push via SSH
7. Update CSV: `status=published`, `date_published=today`, `article_slug=<slug>`

---

## Phase 4 — Progress Report

Show table of papers by journal:

```
Journal                                          Total  Unrev  Summ  Sel  Pass  Pub
─────────────────────────────────────────────── ────── ────── ───── ──── ───── ────
Clinical Oral Implants Research                   174    170     2    1    0     1
Journal of Oral Rehabilitation                    319    315     3    0    1     0
...
```

Also show: total pipeline progress, time since last triage session, most recent published article.

---

## CSV Update Rules

- **Never delete rows** — only update status fields
- **Always write atomically** — read full CSV, modify in memory, write back
- **Duplicate detection** — if two rows have identical `filename`, identical DOI, near-identical normalised title, or the same first-author/year/title combination (allowing filename suffixes like `_1`), add note `duplicate` and skip during triage unless the user explicitly asks to inspect duplicates
- **Missing file detection** — if a row's `filepath` no longer exists on disk, add note `file missing` but leave status unchanged
- **Date format** — always `YYYY-MM-DD`

---

## Status Transition Rules

```
unreviewed → summarised    (triage: paper read but not selected)
unreviewed → selected      (triage: paper immediately selected)
summarised → selected      (user re-selects a previously summarised paper)
summarised → passed        (user explicitly rejects)
selected   → published     (article written and committed)
any        → published     (manual backfill)
passed     → summarised    (user changes mind, wants to re-evaluate)
```

Never move backwards past `summarised` without explicit user instruction.

---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| PDF is encrypted / no text | Note `encrypted` in CSV, status stays `unreviewed`, skip during triage batch |
| PDF is a duplicate filename | Flag in `notes`, exclude from triage by default |
| Year not extractable | Set `year=unknown`, still triage |
| Journal not in known folder | Use path component as `journal` value, note `unverified journal` |
| Paper is non-dental | Note `not dental` in CSV, set `status=passed` |
| User adds new PDFs to journals/ | Detected on next invocation, added as `unreviewed` |
| Batch larger than remaining unreviewed | Silently cap at available count |

---

## Dependencies

This skill calls into:
- **`article-writing` skill** — for full Crabb-voice review generation (Phase 3)
- **`publish-article` skill** — for frontmatter, git commit, GitHub Desktop push (Phase 3)

Python libraries used at runtime: `pypdf`, `csv`, `pathlib`, `re`, `datetime`, `random`, `shutil`
