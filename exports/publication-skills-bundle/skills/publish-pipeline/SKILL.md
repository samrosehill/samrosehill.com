---
name: publish-pipeline
description: "End-to-end orchestrator for the samrosehill.com dental review publishing pipeline. Chains paper-triage, article-writing, article-draft-check, thumbnail-generator, and publish-article into a single guided workflow with user checkpoints at each stage. Supports starting from any stage. Trigger when the user says 'publication workflow', 'run the publication workflow', 'publish pipeline', 'run the pipeline', 'full pipeline', 'start to finish', 'end to end', 'pipeline from [stage]', 'triage and publish', 'process this paper through the pipeline', or 'take this paper all the way to publication'."
version: 1.0.0
author: samrosehill
tags: [orchestration, pipeline, dental, publishing, workflow]
---

# SKILL: Publish Pipeline — End-to-End Article Orchestrator

**Objective:** Orchestrate the full samrosehill.com dental review publishing pipeline — from paper selection through to live publication — as a single guided workflow. User checkpoints exist only at Stage 0 (paper selection), Stage 2 (quality review of drafted articles), and Stage 3 (thumbnail approval). Once the user approves the thumbnail, Stages 4–7 (publication, Substack cross-post, CSV update, and live verification) run automatically with zero further user input.

This skill delegates to five sub-skills. It does not duplicate their logic — it reads each sub-skill's SKILL.md at runtime and follows its instructions at the appropriate stage.

**Current workflow decision:** Preserve the existing Annabel Crabb-adapted article voice. Improve quality by strengthening triage detail, evidence control, factual checks, and publishing automation; do not replace the voice with generic medical SEO prose.

## Execution Discipline

Treat this workflow as an operating procedure, not a loose guideline.

- Do **not** improvise, compress, paraphrase, or "tidy up" required formats, stage rules, checkpoint blocks, or return shapes.
- When a sub-skill specifies an exact display format, output that format directly rather than replacing it with a summary, bullets, or a "cleaner" variant.
- If you notice that your draft output does not match the required structure, stop and correct it before presenting the checkpoint to the user.
- Prefer strict compliance over stylistic judgment. Following the written instructions exactly is more important than brevity or presentation preferences.

---

## Invocation

Triggered when the user says:
- "publication workflow" / "run the publication workflow" / "start the publication workflow"
- "publish pipeline" / "run the pipeline" / "full pipeline"
- "start to finish" / "end to end"
- "orchestrate" / "orchestrate publication"
- "pipeline from [stage name]" (e.g., "pipeline from draft check")
- "triage and publish" / "triage to publish"
- "process this paper through the pipeline"
- "take [PDF/paper] all the way to publication"

---

## Skill Dependencies (read at runtime)

```
PAPER_TRIAGE    = /Users/samrosehill/.claude/skills/paper-triage/SKILL.md
ARTICLE_WRITING = /Users/samrosehill/.claude/skills/article-writing/SKILL.md
DRAFT_CHECK     = /Users/samrosehill/.claude/skills/article-draft-check/SKILL.md
THUMBNAIL_GEN   = /Users/samrosehill/.claude/skills/thumbnail-generator/SKILL.md
PUBLISH_ARTICLE = /Users/samrosehill/.claude/skills/publish-article/SKILL.md
```

At each stage, **read the referenced SKILL.md** and follow its complete instructions. Do not deviate from or abbreviate the sub-skill's specification. If this bundle is running from `exports/publication-skills-bundle`, resolve the same skill names relative to that bundle when the `.claude/skills` paths are unavailable.

**Codex adapter note:** Codex may only use subagents when the user explicitly authorises delegation. If subagents are not available or not authorised, run the same stage sequence inline, preferably one article at a time, and keep the full source text in local files rather than pasting long payloads into the conversation.

---

## Path Constants

```
PROJECT_ROOT    = /Users/samrosehill/Desktop/samrosehill.com
PAPERS_ROOT     = PROJECT_ROOT/2MP Project
JOURNALS_DIR    = PAPERS_ROOT/journals
TRACKER_CSV     = PAPERS_ROOT/paper-tracker.csv
SELECTED_DIR    = PAPERS_ROOT/selected
DRAFTS_DIR      = PAPERS_ROOT/reviews
REVIEWS_SRC     = PROJECT_ROOT/src/content/reviews
THUMBNAILS_DIR  = PROJECT_ROOT/public/images/reviews
THUMBNAIL_SCRIPT = PROJECT_ROOT/scripts/generate-thumbnail.py
SUBSTACK_SCRIPT  = PROJECT_ROOT/scripts/substack-formatter.py
SUBSTACK_PUB     = PROJECT_ROOT/scripts/substack-publisher.py
PREPUBLISH_CHECK = PROJECT_ROOT/scripts/prepublish-check.py
CONTENT_SCHEMA  = PROJECT_ROOT/src/content.config.ts
PIPELINE_STATUS = PAPERS_ROOT/pipeline-status.json
```

---

## Pipeline Overview

```
  MAIN CONTEXT (lean orchestrator)
  │
  ├── Stage 0: Triage ✋
  │     └── screening summaries with structured evidence and priority scores
  │
  ├── User selects papers
  │
  ├── FOR EACH article (up to 3 in parallel):
  │     └── PROCESSOR (subagent when authorised): Stages 1-3 combined
  │           ├── Stage 1: Read PDF → write article → save .md
  │           ├── Stage 2: QC check → fix issues → save .md
  │           └── Stage 3: Generate thumbnail
  │           Returns: {slug, verdict, word_count, qc_passed}
  │
  ├── User reviews all articles + thumbnails ✋
  │
  ├── Stage 4: git commit + push (batched, inline)
  │
  ├── FOR EACH article (sequential):
  │     └── Stage 5 — Substack cross-post
  │           Returns: {slug, draft_id, substack_url, published}
  │
  ├── Stage 6: CSV + substackUrl writeback (inline)
  └── Stage 7: Live verification (inline)

  ✋ = user checkpoint
  Subagent contexts are discarded after returning summaries when subagents are used
```

---

## State Tracking

Maintain and display this state block at every checkpoint. Update it as you progress through stages.

```
┌─────────────────────────────────────────────────────┐
│  PIPELINE STATE                                     │
├─────────────────────────────────────────────────────┤
│  Paper:     [Author et al. (Year)]                  │
│  PDF:       [filename.pdf]                          │
│  Slug:      [article-slug]                          │
│  Verdict:   [3-5 word verdict]                      │
│  Site URL:  samrosehill.com/journal/[slug]           │
│  Substack:  [URL or pending/skipped]                 │
│                                                     │
│  Stage 0 — Paper Selection:    [status]             │
│  Stage 1 — Article Writing:    [status]             │
│  Stage 2 — Quality Check:      [status]             │
│  Stage 3 — Thumbnail:          [status]             │
│  Stage 4 — Publication:        [status]             │
│  Stage 5 — Substack Cross-Post:[status]             │
│  Stage 6 — CSV Update:         [status]             │
│  Stage 7 — Live Verification:  [status]             │
└─────────────────────────────────────────────────────┘
```

**Status values:** `PENDING`, `IN PROGRESS`, `COMPLETE`, `SKIPPED (pre-existing)`

For mid-pipeline entry, stages before the entry point are marked `SKIPPED (pre-existing)` — not `COMPLETE` — to indicate they were not validated during this pipeline run.

### Durable Checkpoint Rule

Do not rely on thread memory to remember pipeline progress. Treat the repository history as the durable memory for this workflow.

- Create a checkpoint commit whenever a stage boundary produces tracked artifacts that future sessions may need to reconstruct.
- At minimum, commit separately at these boundaries when tracked files changed:
  - workflow or skill-rule changes
  - Stage 1-3 checkpoint after drafted articles, QC fixes, and thumbnails are ready for review
  - Stage 4 publication commit
  - Stage 5-6 metadata/writeback commit
- If only gitignored files changed at a stage boundary, say explicitly that there is no durable git checkpoint for that stage and summarise the state in the checkpoint message.
- Do not continue into a later stage while assuming an earlier stage will be "remembered" from conversation context alone.
- On explicit resume requests, inspect recent relevant commits as part of reconstructing state; do not depend solely on `PIPELINE_STATUS`.

---

## Browser Preview

At the Stage 1 and Stage 2 checkpoints, **always open the articles in the browser** so the user can see them rendered with full site styling:

1. Check if the Astro dev server is already running (try `curl -s -o /dev/null -w "%{http_code}" http://localhost:4321` or nearby ports)
2. If not running, start it: `npm run dev -- --port 4321` (backgrounded)
3. Open each article in a browser tab: `open http://localhost:[port]/journal/[slug]`
4. Wait for user feedback before proceeding

This is the most accurate preview — it shows the article exactly as it will appear on the live site with the Newsreader/Public Sans typography, Tiffany blue accents, and source paper metadata block.

**Important validation rule:** Do **not** use `file://.../dist/.../index.html` as a visual-rendering check. This site uses root-relative asset paths such as `/_astro/...` and `/images/...`, which do not resolve correctly when a built page is opened directly from the filesystem. That can create false "broken rendering" reports even when the page itself is fine. Prefer `http://localhost:[port]` over `127.0.0.1` when working through browser tooling, and if no HTTP preview is available, report that visual rendering is unverified rather than treating a `file://` preview as authoritative.

---

## Checkpoint Format

At every user checkpoint, display the state block followed by:

```
Options:
  [C] Continue to next stage
  [E] Edit / make changes before continuing
  [R] Redo this stage from scratch
  [Q] Quit pipeline (artifacts saved on disk — resume later with "pipeline from [stage]")
```

Wait for the user's response before proceeding.

---

## Mid-Pipeline Entry

The user can start at any stage. Detect the entry point from their message, then validate prerequisites before proceeding.

| User says | Entry stage | Prerequisites to validate |
|-----------|------------|--------------------------|
| "publication workflow" / "run the publication workflow" / "start the publication workflow" | Stage 0 | None |
| "run the pipeline" / "full pipeline" | Stage 0 | None |
| "write article for [PDF path]" | Stage 1 | PDF file exists at the given path |
| "check and publish [draft path or slug]" | Stage 2 | Draft `.md` exists with valid frontmatter; source PDF locatable via `pdfPath` |
| "pipeline from thumbnail [slug]" | Stage 3 | Article exists at `REVIEWS_SRC/[slug].md` with `verdict` and `pdfPath` fields |
| "publish [slug]" | Stage 4 | Article at `REVIEWS_SRC/[slug].md` AND thumbnail at `THUMBNAILS_DIR/[slug].png` both exist |

**If prerequisites are missing:** Report exactly what is needed and ask the user to provide it. Do not silently drop back to an earlier stage.

### Generic Invocation Rule

If the user opens a new session and says only "publication workflow", "run the publication workflow", "run the pipeline", or similar generic pipeline language, interpret that as **start a new publication workflow pipeline from Stage 0 now**.

Do **not** treat a generic invocation as implied permission to resume the most recent incomplete pipeline run. Resume is only the default when the user explicitly says they want to resume, continue the previous run, finish an incomplete pipeline, or names a specific in-progress slug/draft.

### Regression Guard: Do Not Misclassify Housekeeping as a Pipeline Run

When the user gives a generic pipeline invocation, do **not** inspect local git diffs, `substackUrl` writebacks, tracker CSV deltas, `pipeline-status.json`, or recently modified review files and then decide that the "real" task is to finish Stage 5/6/7 housekeeping for earlier articles.

Those signals may describe leftover state from a previous session, but they do **not** override the user's intent. A generic publication-workflow request means: launch a **new** pipeline from Stage 0 unless the user explicitly asked to resume or supplied a concrete slug/draft/stage.

In particular:
- Do **not** infer that uncommitted `substackUrl` changes are the requested workflow.
- Do **not** infer that recently edited review files are the requested workflow.
- Do **not** skip Stage 0 just because completed or partially completed articles exist locally.
- Do **not** treat "run the publication workflow" as permission to decide that the only work left is final metadata writeback.

---

## Pipeline Checkpoint File

The pipeline persists progress to `PIPELINE_STATUS` so that interrupted runs can be resumed in a new session.

### On Pipeline Start (before any stage)

First classify the invocation:

- **Generic new-run invocation:** "publication workflow", "run the publication workflow", "run the pipeline", "full pipeline", "start to finish", "end to end"
- **Explicit resume invocation:** "resume", "continue previous pipeline", "pick up where we left off", "finish the incomplete run", or equivalent
- **Specific mid-pipeline invocation:** user names a slug, stage, draft, or article path

For a **generic new-run invocation**, do **not** interrupt the flow with a resume chooser just because `PIPELINE_STATUS` contains incomplete runs. Start a fresh Stage 0 triage run immediately. You may note incomplete runs briefly after triage begins if useful, but they are informational only and must not block the new pipeline.

Only when the user makes an **explicit resume invocation** should you read `PIPELINE_STATUS` and display incomplete runs like this:

```
┌─────────────────────────────────────────────────────┐
│  INCOMPLETE PIPELINE RUNS                           │
├─────────────────────────────────────────────────────┤
│  1. [slug] — stopped at Stage 5 (Substack)          │
│     Started: 2026-04-04 10:30                       │
│  2. [slug] — failed at Stage 4 (Publish)            │
│     Started: 2026-04-03 14:00                       │
└─────────────────────────────────────────────────────┘
```

Then ask the user:
- **[R] Resume** — continue from the next incomplete stage
- **[S] Start fresh** — reset that article's progress and re-run
- **[N] New article** — ignore incomplete runs and start a new pipeline

### Updating the Checkpoint File

After **each stage completes**, update `PIPELINE_STATUS` by running:

```bash
cd PROJECT_ROOT
python3 -c "
import json, datetime, pathlib
path = pathlib.Path('2MP Project/pipeline-status.json')
try:
    data = json.loads(path.read_text())
except:
    data = {'articles': {}}
slug = '[SLUG]'
if slug not in data['articles']:
    data['articles'][slug] = {
        'paper': '[AUTHOR et al. (YEAR)]',
        'pdf': '[FILENAME]',
        'slug': slug,
        'verdict': '[VERDICT]',
        'started': datetime.datetime.now().isoformat(),
        'stages': {}
    }
data['articles'][slug]['stages']['[STAGE_KEY]'] = 'complete'
data['articles'][slug]['updated'] = datetime.datetime.now().isoformat()
path.write_text(json.dumps(data, indent=2))
"
```

Replace `[SLUG]`, `[AUTHOR et al. (YEAR)]`, `[FILENAME]`, `[VERDICT]`, and `[STAGE_KEY]` with actual values. Stage keys are: `0_select`, `1_write`, `2_check`, `3_thumbnail`, `4_publish`, `5_substack`, `6_csv`, `7_verify`.

### On Stage Failure

If a stage fails (error, auth issue, user quits), mark it as `failed` instead of `complete`:
```python
data['articles'][slug]['stages']['[STAGE_KEY]'] = 'failed'
```

### On Pipeline Completion (Stage 7 done)

Keep the record in the file — it serves as a publication log. Do not delete completed entries.

---

## Stage 0: Paper Selection (Triage → Screen → Select)

**Delegate to:** `PAPER_TRIAGE` skill

**Entry criteria:** User has invoked the pipeline without specifying a paper or draft.

**Default behaviour:** When the pipeline is invoked without specifying a paper, draft, or stage — always start by triaging a fresh batch of 10 unreviewed papers immediately. Do NOT present a menu of options (triage vs. process existing drafts vs. review selected papers). Just start triaging with defaults (batch size 10, no journal filter, no year filter). The user can interrupt or redirect if they want something different.

This stage has three sub-steps: triage a batch, present screening summaries, then the user manually selects which paper(s) to take forward.

### Step 0a: Triage Pre-flight

1. Read and follow the paper-triage SKILL.md instructions
2. Run the pre-flight checklist (check tracker exists, scan for new PDFs, display dashboard)
3. **Immediately proceed to Step 0b** using defaults (batch size 10, random or oldest-first ordering). Do NOT ask the user for triage preferences — just start screening papers.

### Step 0b: Batch Screening (default 10 papers)

1. Pull a batch of **10 unreviewed papers** from the tracker (or the user's requested batch size)
2. For each paper in the batch:
   - **Prefer pre-extracted text:** Check if a `.md` file exists alongside the PDF (same directory, same basename, `.md` extension). If yes, read the `.md` file instead of the PDF — this saves significant tokens. If no `.md` exists, fall back to reading the PDF (pages 1–5).
   - Extract: full title, authors, journal, year, DOI, study type, sample size. Prefer the manuscript text over folder names when journal metadata conflicts with the path.
   - Write a structured plain-language clinical screening summary: design, main numeric result, limitation, publishing angle, do-not-overclaim warning, and priority score. No Annabel Crabb voice here — this is factual screening only.
3. Display all 10 summaries in the triage format specified by the paper-triage skill:

**Non-deviation rule for Stage 0:** Reproduce the triage summary block below as written for each paper. Do **not** replace it with recommendation bullets, shortlist notes, or any condensed alternative format.

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

[Short factual clinical summary]
────────────────────────────────────────────────────────
```

4. Update the CSV tracker: set extracted metadata for each paper, mark triaged papers as `status=summarised`, `date_triaged=today`

### Step 0c: Manual Selection

After displaying all summaries, ask:

> "Which papers do you want to select for full review? Enter numbers (e.g. 1,3,7), 'none', or 'all':"

Wait for the user's response. Then:
- **Selected papers:** `status=selected`, `date_selected=today`, copy PDF to `SELECTED_DIR/`
- **Unselected papers:** remain as `status=summarised`
- **Explicitly rejected** (if user says "pass on X"): `status=passed`, add reason to `notes`

**Automatic article processing:** Once the user confirms their selection, **immediately begin processing articles**. Do NOT ask which paper to process first or wait for further confirmation unless the environment cannot safely process the selected batch.

**CONTEXT ISOLATION — CRITICAL:** To minimise token usage, run each article's heavy processing (PDF reading, article writing, quality checking, and thumbnail generation) inside a dedicated subagent when subagents are available and authorised. If not, process one article at a time inline and use the extracted `.md` source text as the main working artifact. The orchestrator should avoid pasting full PDFs or full article drafts into the conversation.

For each selected paper, launch a **Sonnet subagent** using the prompt template in the "Per-Article Subagent Templates" section below when authorised. You may run up to 3 subagents in parallel if multiple papers are selected and the user has approved delegation. Otherwise, process sequentially with the same stage requirements.

**Exit criteria:** All selected papers have articles written, quality-checked, and thumbnails generated on disk. The CSV tracker shows each paper as `status=selected`.

**Checkpoint (after ALL per-article subagents complete):**

Display the state block showing the result for each article, then open all articles in the browser and all thumbnails in Preview. Present results as:

```
Article 1: [slug]
  Verdict: "[verdict from subagent]"
  Quality: APPROVED — [N] revisions applied
  Word count: [N] body words
  Thumbnail: ✅ generated

Article 2: [slug]
  Verdict: "[verdict]"
  Quality: APPROVED — [N] revisions applied
  Word count: [N] body words
  Thumbnail: ✅ generated
```

Then ask:
> "All [N] articles have been drafted, quality-checked, and thumbnails generated. They're open in your browser and Preview. Options: [C] Approve all — proceed to publish, [E] Request changes to specific articles, [Q] Quit pipeline."

If any subagent reported a quality failure:
> "Article [slug] could not pass quality review after [N] revisions. Please review manually."

**State produced:** `selected_pdf_paths[]`, `paper_authors[]`, `paper_years[]`, `paper_titles[]`, `slugs[]`, `verdicts[]`, `quality_verdicts[]`

---

## Stages 1–3: Per-Article Subagent Processing

Stages 1 (Article Writing), 2 (Quality Check), and 3 (Thumbnail Generation) are **combined into a single processing unit per article**. In Claude Code this is a subagent invocation. In Codex, use a subagent only when the user has explicitly authorised delegation; otherwise run the same sequence inline for one article at a time.

**The main orchestrator MUST NOT:**
- Read full source PDFs inline when a `.md` source text extraction is available
- Hold full article text in the conversation context longer than needed
- Generate or paste large Substack JavaScript payloads into the conversation

**The main orchestrator MUST:**
- Assign each article a Crabb opening strategy (check last 3–5 published articles for variety)
- Derive the slug from the paper metadata before launching the subagent
- Derive the text file path: replace the PDF's `.pdf` extension with `.md`. If the `.md` file exists, pass it as SOURCE TEXT. If not, run `python3 scripts/extract-pdf-text.py <pdf_path>` first to create it.
- Build an Evidence Pack before drafting: citation, study frame, 3–5 must-use findings, limitations, and a do-not-overclaim line
- Pass the complete subagent prompt from the template below when using subagents, or apply the same requirements inline when not using subagents
- Collect or produce the lightweight result summary
- Open the resulting articles in the browser for user review

**Subagent model:** Use `sonnet` for all per-article subagents when subagents are authorised. Sonnet is ~5x cheaper per token and sufficient for article writing and QC.

See the "Per-Article Subagent Templates" section below for the exact prompt to use.

---

## Stage 4: Publication

**Delegate to:** `PUBLISH_ARTICLE` skill

**Entry criteria:** Article file at `REVIEWS_SRC/[slug].md` and thumbnail at `THUMBNAILS_DIR/[slug].png` both exist and are user-approved.

**Work:**
1. Read and follow the publish-article SKILL.md instructions
2. Run the validation checklist (all required frontmatter fields, no H1, Australian English, etc.)
3. If `scripts/prepublish-check.py` exists, run `python3 scripts/prepublish-check.py [slug]` and fix any failures before committing. If it does not exist, perform the same checks inline: Astro schema/build compatibility, thumbnail exists, `pubDate` not future-dated unless intentional, description/Substack subtitle length risk, DOI/reference line, no H1, body word count, and source PDF path.
4. Stage and commit both files:
   ```bash
   cd PROJECT_ROOT
   git add src/content/reviews/[slug].md public/images/reviews/[slug].png
   git commit -m "feat: add review — [article title]"
   ```

5. **Push to origin** via SSH to trigger deployment:
   ```bash
   git push origin main
   ```
   SSH authentication is configured — this should succeed automatically with no user interaction.

6. **Clean up stale draft:** If a draft file exists in `DRAFTS_DIR` for this paper (matched by author/slug), delete it. The canonical article now lives in `REVIEWS_SRC` — the draft is no longer needed.

**Exit criteria:** Git commit pushed to origin via SSH. No stale draft remains in `DRAFTS_DIR`. The article will be live at `samrosehill.com/journal/[slug]` within 1–2 minutes.

**No checkpoint** — proceed directly to Stage 5.

**State produced:** `commit_hash`, `published_url`

---

## Stage 5: Substack Cross-Post (API Method)

**Entry criteria:** Git commit created successfully in Stage 4. Article exists at `REVIEWS_SRC/[slug].md`. A Chrome tab must be open and logged into `samuelrosehill.substack.com`.

**Codex preflight:** In Codex, verify that Chrome DevTools MCP is connected before doing any Stage 5 work. The required execution route is Chrome DevTools MCP `evaluate_script` against the authenticated Substack tab. If DevTools MCP is unavailable, stop immediately and tell the user Stage 5 cannot proceed until it is enabled. Do not substitute AppleScript, cookie replay, remote-debugging workarounds, or giant bookmarklet payloads unless the workflow is explicitly revised to allow that fallback.

**CONTEXT ISOLATION:** Do not paste giant Substack JavaScript payloads into the main conversation. Prefer a small browser-side API script that fetches the already-deployed article from `https://samrosehill.com/journal/[slug]`, converts the rendered `.prose` DOM to Substack's editor format, and publishes via the authenticated browser session. If using subagents, keep the generated payload inside the subagent and return only the result fields.

**For each article**, run the "Substack Cross-Post Template" from the templates section below. Process articles sequentially (not in parallel) to avoid Substack API rate limits.

**If auth fails** (401 or unauthenticated response): The browser session may have expired. Tell the user to refresh the Substack page in Chrome and retry.

**Exit criteria:** All articles published live on Substack with title, subtitle, body content, tags, cross-posting byline, and a captured `substack_url`.

**No checkpoint** — proceed directly to Stage 6.

**State produced:** `substack_published`, `substack_draft_id`, `substack_url` (per article)

---

## Stage 6: CSV and Substack URL Writeback (Automatic)

**No user checkpoint** — this is automatic housekeeping.

**Entry criteria:** Substack cross-post completed (Stage 5) or explicitly skipped.

**Work:**
1. Read `TRACKER_CSV`
2. Find the row matching the source PDF
3. Update: `status=published`, `date_published=[today YYYY-MM-DD]`, `article_slug=[slug]`
4. If Stage 5 produced `substack_url`, append or update the row `notes` with `substack: [substack_url]`
5. If Stage 5 produced `substack_url`, add `substackUrl: "[substack_url]"` to `REVIEWS_SRC/[slug].md` frontmatter. The Astro schema supports this field.
6. Commit and push the `substackUrl` writeback so the live site CTA points to the Substack post:
   ```bash
   cd PROJECT_ROOT
   git add src/content/reviews/[slug].md
   git commit -m "chore: link Substack post for [short article name]"
   git push origin main
   ```
7. Write the updated CSV back

**Exit criteria:** CSV updated. If `substack_url` exists, review frontmatter includes `substackUrl` and the writeback commit has been pushed. If no matching CSV row is found, note this but do not halt — the article is already published.

---

## Stage 7: Live Verification (Automatic)

**No user checkpoint** — this is automatic post-deployment QA.

**Entry criteria:** Git push completed (Stage 4), Substack post published or explicitly skipped (Stage 5), and `substackUrl` writeback pushed if applicable (Stage 6). Poll the live site rather than relying on a fixed sleep: check every 20–30 seconds until `https://samrosehill.com/journal/[slug]` returns 200 and contains the expected title or until 5 minutes have elapsed.

**Work:**

For each published article, verify both the live website and the Substack post:

### 7a: Website Verification

1. Navigate to `https://samrosehill.com/journal/[slug]` in the browser
2. Check that the page loads successfully (not 404)
3. Verify the following against the source markdown:
   - **Title** renders correctly
   - **Verdict** appears in the metadata block
   - **Author sign-off** is present at the bottom
   - **Reference DOI link** is present and clickable
   - **Thumbnail image** loads (check `<img>` for `/images/reviews/[slug].png`)
   - **Structural headings** are present: "The Data Anchor", "Key Findings", "The Clinical Bottom Line"
   - **No obvious rendering issues**: broken markdown, raw HTML, missing sections
4. Check the journal index page at `https://samrosehill.com/journal` to confirm the new article appears in the listing, unless the article was intentionally future-dated. If it does not appear and `pubDate` is in the future, report this as a date/scheduling issue rather than a rendering failure.

### 7b: Substack Verification

1. Navigate to the published Substack post URL
2. Confirm the post is live with the correct title
3. **Run the empty paragraph check on the published HTML:**
   ```javascript
   const body = document.querySelector('.body.markup') || document.querySelector('[class*="body"]');
   const emptyP = Array.from(body.querySelectorAll('p')).filter(p => p.textContent.trim() === '');
   // emptyP.length MUST be 0
   ```
   If `emptyP.length > 0`: this is a **FAIL** — the post has line spacing artifacts. Go back to the editor, run the cleanup script, wait for auto-save, and recheck. If cleanup cannot fix it (ProseMirror re-inserts empty paragraphs), report to user for manual fix.
4. Visually verify by scrolling through the published post:
   - **Title and subtitle** match the article frontmatter
   - **Body content** is present (not empty or truncated)
   - **Headings** render correctly (Data Anchor, Key Findings, Clinical Bottom Line)
   - **No excessive blank lines** between paragraphs — paragraphs should have single normal spacing only
   - **Blockquote** renders with left border if the source article uses a blockquote
   - **Cross-posting byline** is present at the bottom ("originally published on samrosehill.com")
   - **Tags** are applied (check Settings panel)
   - **No formatting artifacts** from ProseMirror injection (double spacing, missing bold, broken lists)

### Verification Report

Display results as a checklist:

```
┌─────────────────────────────────────────────────────────────┐
│  VERIFICATION REPORT — [slug]                               │
├─────────────────────────────────────────────────────────────┤
│  WEBSITE (samrosehill.com/journal/[slug])                   │
│    ✅/❌ Page loads (not 404)                                │
│    ✅/❌ Title renders correctly                             │
│    ✅/❌ Verdict displayed                                   │
│    ✅/❌ Thumbnail image loads                               │
│    ✅/❌ Structural headings present                         │
│    ✅/❌ Author sign-off present                             │
│    ✅/❌ Reference DOI link present                          │
│    ✅/❌ Appears on /journal index                           │
│                                                             │
│  SUBSTACK (published post)                                  │
│    ✅/❌ Post exists with correct title                      │
│    ✅/❌ Body content present                                │
│    ✅/❌ Headings render correctly                           │
│    ✅/❌ Zero empty paragraphs in published HTML             │
│    ✅/❌ No excessive line spacing (visual check)            │
│    ✅/❌ Cross-posting byline present                        │
│    ✅/❌ Tags applied                                        │
│    ✅/❌ No formatting artifacts                             │
└─────────────────────────────────────────────────────────────┘
```

### Auto-Fix and Retry (up to 3 attempts)

If any check fails, attempt to diagnose and fix the issue before reporting to the user. Track `verification_attempt` (starts at 1, max 3).

**Fixable issues and remediation:**

| Failure | Fix |
|---------|-----|
| Page returns 404 | Vercel may still be deploying — wait 60 seconds and recheck. If still 404 after 3 attempts, check that the slug matches the filename exactly. |
| Title/verdict/headings missing or wrong | Edit the source markdown at `REVIEWS_SRC/[slug].md`, commit, and push the fix. Wait for redeployment (~90s), then recheck. |
| Thumbnail not loading | Verify the file exists at `THUMBNAILS_DIR/[slug].png`. If missing, regenerate it. If present but not loading, check the `<img>` src path. Commit and push any fix. |
| Article missing from /journal index | May be a build cache issue — wait 60s and recheck. If persistent, check that frontmatter `pubDate` is not in the future. |
| Substack body empty or truncated | Re-open the Substack post editor, clear the body, and re-inject the HTML. Save/publish again. |
| Substack empty paragraphs in published HTML | This is the most common Substack issue. The published HTML contains empty `<p>` elements that create double spacing. Fix: go to editor, run the ProseMirror cleanup script (targeting `ProseMirror-trailingBreak` and all empty `<p>` elements), wait for auto-save (5+ seconds), then verify the published page. If cleanup doesn't persist (ProseMirror re-inserts empties), the only reliable fix is to select all body content, delete it, and re-type/re-paste the content manually paragraph by paragraph. |
| Substack formatting artifacts (empty lines) | Re-open the post editor and run the ProseMirror cleanup JavaScript. Save/publish again. |
| Substack tags missing | Re-open Settings panel and add the missing tags. Save/publish again. |
| Substack cross-posting byline missing | Re-open the post editor, append the byline HTML, and save/publish again. |
| Substack title/subtitle wrong | Re-open the post editor and correct the title/subtitle fields. Save/publish again. |

**Retry flow:**
1. Run all checks
2. If any fail: diagnose the root cause, apply the fix from the table above
3. Increment `verification_attempt`
4. Re-run **only the failed checks** (not all checks)
5. If still failing and `verification_attempt < 3`: repeat from step 2
6. If all checks now pass: proceed to Pipeline Complete
7. If `verification_attempt >= 3` and checks still fail: halt and report to user:
   > "Verification failed after 3 fix attempts. The following issues remain: [list]. Please review manually."
   Include a screenshot of each remaining failure.

**Exit criteria:** All checks pass (within 3 attempts), or persistent failures reported to user after 3 fix attempts.

**State produced:** `verification_passed` (boolean), `verification_attempt` (1–3), `verification_failures` (list, if any)

---

## Pipeline Complete

After Stage 7, display the final state block with all stages marked COMPLETE, then:

```
═══════════════════════════════════════════════════════════════
  PIPELINE COMPLETE
═══════════════════════════════════════════════════════════════

  Article:    [title]
  Live URL:   samrosehill.com/journal/[slug]
  Thumbnail:  public/images/reviews/[slug].png
  Substack:   Published at samuelrosehill.substack.com
  Verified:   ✅ Website and Substack checks passed
═══════════════════════════════════════════════════════════════
```

---

## Subagent Policy — Context Isolation

**Design principle:** The main orchestrator context must remain lean. Heavy processing (PDF reading, article writing, QC cross-checking, Substack publishing) should run in dedicated subagents when the harness supports them and the user has authorised delegation. If not, run the same steps inline one article at a time using extracted source text files.

**What stays in the main context:**
- Stage 0: Triage (screening summaries are short; user needs to see them all at once to select)
- Stage 4: Git commit/push (single batched operation, lightweight)
- Stage 6: CSV update (lightweight)
- Stage 7: Live verification (curl checks, lightweight)
- All user checkpoints and state tracking

**What runs in per-article subagents:**
- Stages 1-3 combined: Article writing + QC + thumbnail (one subagent per article, Sonnet model)
- Stage 5: Substack cross-post (one subagent per article, Sonnet model) when subagents are authorised; otherwise run it inline with a compact browser-side script

**Parallelism:**
- Stage 0 triage: up to 10 subagents in parallel only when the harness permits it and the user has approved delegation
- Stages 1-3: up to 3 per-article subagents in parallel only when authorised
- Stage 5: sequential (one at a time, to avoid Substack API rate limits)

**The main orchestrator MUST NOT:**
- Read full source PDFs inline when extracted source text exists
- Hold full article markdown text in the conversation
- Generate or hold Substack JS payloads in the conversation
- Skip QC because subagents are unavailable

---

## Per-Article Subagent Templates

### Stages 1-3 Combined: Write + QC + Thumbnail

Use this exact prompt template for each article's subagent. Replace all `[PLACEHOLDERS]` with actual values. Use `model: sonnet`.

```
Process this dental paper through Stages 1-3 of the samrosehill.com publication pipeline.
Working directory: /Users/samrosehill/Desktop/samrosehill.com

SOURCE TEXT: [FULL_TXT_PATH]
SOURCE PDF: [FULL_PDF_PATH]
SLUG: [SLUG]
OPENING STRATEGY: [ASSIGNED_CRABB_OPENING_STRATEGY]

TOKEN EFFICIENCY: Read the SOURCE TEXT file (.md) for all article content and factual cross-checking.
Do NOT read the SOURCE PDF — it is only needed by the thumbnail script in Stage 3.

═══════════════════════════════════════════════
STAGE 1 — ARTICLE WRITING
═══════════════════════════════════════════════

MANDATORY: Read /Users/samrosehill/.claude/skills/article-writing/SKILL.md in full.
This file is your COMPLETE writing specification — every instruction is a hard requirement.
Do not skip, abbreviate, or deviate from any section.

1. Read the SOURCE TEXT file (the .md file, NOT the PDF).
2. Create an Evidence Pack for yourself: citation, study frame, 3-5 must-use findings, limitations, and do-not-overclaim line.
3. Write the article following every requirement in the skill file while preserving the established Annabel Crabb-adapted voice.
4. Use the assigned opening strategy above. Do NOT use a "[day of the week] + operatory" formula.
5. Pay special attention to the CRITICAL REQUIREMENTS section — these are historically missed.

Save to: /Users/samrosehill/Desktop/samrosehill.com/src/content/reviews/[SLUG].md

═══════════════════════════════════════════════
STAGE 2 — QUALITY CHECK & FIX
═══════════════════════════════════════════════

MANDATORY: Read /Users/samrosehill/.claude/skills/article-draft-check/SKILL.md in full.
This is your MANDATORY quality gate — not reference material. Every dimension applies.

1. Check the article against ALL 8 dimensions in the draft-check skill.
2. Fix ALL failures — do not leave any FAIL or MISMATCH unresolved.
3. After fixing, re-read the draft-check skill and verify compliance again.
4. Up to 3 revision cycles. Save the corrected file after each cycle.

═══════════════════════════════════════════════
STAGE 3 — THUMBNAIL
═══════════════════════════════════════════════

Run: cd /Users/samrosehill/Desktop/samrosehill.com && python3 scripts/generate-thumbnail.py [SLUG]

═══════════════════════════════════════════════
RETURN (as your final message, this exact format):
═══════════════════════════════════════════════

slug: [SLUG]
verdict: [verdict from frontmatter]
title: [title from frontmatter]
word_count: [body words, excluding frontmatter/sign-off/reference]
qc_verdict: APPROVE or REVISE or FAILED
revisions_applied: [count]
issues_fixed: [brief comma-separated list, or "none"]
thumbnail: generated or failed
factual_accuracy: verified or unverifiable
```

### Stage 5: Substack Cross-Post Template

Use this prompt for each article's Substack step. If using a subagent, use `model: sonnet`; otherwise run the same steps inline.

```
Cross-post a dental review article to Substack via the API.
Working directory: /Users/samrosehill/Desktop/samrosehill.com

SLUG: [SLUG]

STEPS:
1. Confirm the live article is deployed:
   https://samrosehill.com/journal/[SLUG]

2. Prefer the live-site method:
   - In the authenticated Chrome tab, execute a compact browser-side script that fetches `https://samrosehill.com/journal/[SLUG]`
   - Parse the returned HTML
   - Extract the article title, description, tags, and rendered `.prose` body
   - Convert the rendered body DOM to the Substack editor/ProseMirror payload
   - Append the cross-posting byline linking back to the live site
   - Create and publish the Substack post

3. If using `scripts/substack-publisher.py`, it must fail fast if draft creation fails and must return a short result object. It must not continue to tag or publish an undefined draft:
   cd /Users/samrosehill/Desktop/samrosehill.com && python3 scripts/substack-publisher.py [SLUG]

4. Use a Substack-specific subtitle if the site description is too long. Do not add unsupported subtitle fields to Astro frontmatter unless the schema has been updated.

5. The Chrome tab at samuelrosehill.substack.com is already open and authenticated.
   Execute only the compact browser-side script in the Chrome tab using the available JavaScript evaluation tool.

6. Capture the draft/post id, publish status, final post URL, and any API error. If the API returns 401, report auth_failed=true.

RETURN (as your final message, this exact format):

slug: [SLUG]
draft_id: [ID from API response]
substack_url: [published Substack URL, or empty]
published: true or false
auth_failed: true or false
api_error: [empty or exact API error summary]
```

---

## Error Handling

| Error | Response |
|-------|----------|
| PDF unreadable / encrypted | Report the error. Suggest the user check the file. Halt at current stage. |
| Python script failure (thumbnail) | Display the error output. Check that PyMuPDF and Pillow are installed (`pip3 install PyMuPDF Pillow`). Retry once. |
| Git commit failure | Display the git error. Do not attempt to resolve automatically — report and halt. |
| Missing frontmatter fields | Report which fields are missing. Offer to populate them before continuing. |
| Source PDF not found via pdfPath | Ask the user to provide the correct path. Do not skip factual accuracy checks. |
---

## Edge Cases

| Situation | Handling |
|-----------|----------|
| User quits mid-pipeline | Display state block with completed stages. Tell user they can resume with "pipeline from [next stage]" and the slug or draft path. |
| Draft already exists for selected paper | Detect at Stage 1 entry. Ask: "A draft already exists at [path]. Use existing draft (skip to Stage 2) or write a new one?" |
| Article already published for this paper | Detect via CSV tracker or by checking `REVIEWS_SRC`. Warn: "This paper has already been published as [slug]. Continue anyway (creates a duplicate) or pick a different paper?" |
| Thumbnail already exists for this slug | Detect at Stage 3 entry. Ask: "A thumbnail already exists at [path]. Regenerate or use existing?" |
| Quality check SKIPPED factual accuracy | Proceed but add a warning: "Factual accuracy was not verified (no source PDF). The article may contain unchecked claims." |
| Multiple papers selected from triage | If subagents are authorised, process up to 3 in parallel through Stages 1-3 and then publish sequentially. If subagents are not authorised, process one at a time and continue to the next selected paper automatically after the previous article completes unless the user stops the run. |
| User provides draft not in expected directory | Accept any valid `.md` file path. Do not require it to be in `REVIEWS_SRC` or `DRAFTS_DIR`. |
| Frontmatter uses string for paperYear | Flag as error — Astro schema expects a number. Fix before proceeding. |
| Substack subtitle too long | Generate a shorter Substack-only subtitle in the publish step and retry. Do not modify the site description unless it is also a poor site snippet. |
| Article missing from journal index | Check `pubDate` first. Future-dated articles sort ahead or may create confusion; report the exact date and only change it if the user wants immediate publication. |

---

## Dependencies

This skill orchestrates (reads and delegates to):
- **paper-triage** — paper selection and CSV tracking
- **article-writing** — draft article generation
- **article-draft-check** — 8-dimension quality gate
- **thumbnail-generator** — branded thumbnail image creation
- **publish-article** — git commit and deploy instructions
- **substack-formatter.py** (`PROJECT_ROOT/scripts/substack-formatter.py`) — transforms article markdown into Substack-ready HTML with tag selection
- **substack-publisher.py** (`PROJECT_ROOT/scripts/substack-publisher.py`) — publishes via the authenticated Substack browser/API flow when available
- **prepublish-check.py** (`PROJECT_ROOT/scripts/prepublish-check.py`) — optional deterministic preflight; if absent, perform the checklist inline

Browser automation tools used at runtime (Stage 5): authenticated Chrome with JavaScript evaluation capability. In Claude, this may be `javascript_tool`; in Codex, use Chrome DevTools MCP `evaluate_script`. If Chrome DevTools MCP is not connected in Codex, halt Stage 5 and report the blocker instead of improvising with substitute control paths.

Python libraries used at runtime (via sub-skills): `PyMuPDF`, `Pillow`, `pypdf`
