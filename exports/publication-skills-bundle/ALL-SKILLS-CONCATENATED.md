# samrosehill.com Publication Skills — Full Bundle

This file contains every skill used in the dental review publication pipeline at samrosehill.com, concatenated in the order they execute. Hand this to Codex (or any other agent) to reproduce the workflow.

Paths in the skills are hard-coded to `/Users/samrosehill/Desktop/samrosehill.com` and `/Users/samrosehill/.claude/skills` — rewrite them before running elsewhere.

Current decision: preserve the existing Annabel Crabb-adapted article voice. Improve quality through structured triage, evidence control, factual checks, Substack URL writeback, and deterministic verification.

## Table of Contents

1. publish-pipeline — end-to-end orchestrator
2. paper-triage — paper selection + tracker
3. article-writing — Crabb-voice review generator
4. annabel-crabb-voice — full voice specification
5. article-draft-check — 8-dimension quality gate
6. thumbnail-generator — branded PNG compositor
7. publish-article — frontmatter + git + push
8. journal-article-downloader (+ 8 publisher references) — KCL institutional fetch
9. scihub-downloader — legacy DOI fallback; do not use in the local publication path when papers are already local


═══════════════════════════════════════════════════════════════
# FILE: skills/publish-pipeline/SKILL.md
═══════════════════════════════════════════════════════════════

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

At the Stage 1 and Stage 2 checkpoints, **always open the articles in the browser and return clickable rendered-page links** so the user can see them rendered with full site styling:

**Normal workflow rule:** Treat local HTTP preview as a standard, mandatory part of the publication workflow. Do **not** ask the user whether they want rendered-page links or browser preview; provide them automatically at the checkpoint.

1. Check if the Astro dev server is already running (try `curl -s -o /dev/null -w "%{http_code}" http://localhost:4321` or nearby ports)
2. If not running, start it: `npm run dev -- --port 4321` (backgrounded)
3. If the Astro dev server fails to bind, hangs, or is otherwise unavailable, **serve the built `dist/` output over HTTP instead of giving up on rendered preview**. Preferred fallback:
   - `python3 -m http.server 4321 --directory dist`
   - then use `http://localhost:4321/journal/[slug]`
4. Open each article in a browser tab: `open http://localhost:[port]/journal/[slug]`
5. In the checkpoint response, include a clickable link for every rendered page using the exact local HTTP URL. Do not make the user infer the route from the slug alone.
6. Wait for user feedback before proceeding

This is the most accurate preview — it shows the article exactly as it will appear on the live site with the Newsreader/Public Sans typography, Tiffany blue accents, and source paper metadata block.

**Important validation rule:** Do **not** use `file://.../dist/.../index.html` as a visual-rendering check. This site uses root-relative asset paths such as `/_astro/...` and `/images/...`, which do not resolve correctly when a built page is opened directly from the filesystem. That can create false "broken rendering" reports even when the page itself is fine. Prefer `http://localhost:[port]` over `127.0.0.1` when working through browser tooling, and if Astro preview is unavailable, use the HTTP-served `dist/` fallback before reporting rendering as unverified.

**No-permission framing rule:** Starting the local preview server, falling back to HTTP-served `dist/`, and returning clickable local URLs are normal workflow operations. Do not treat them as special user-decision checkpoints inside the pipeline.

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
  Rendered page: http://localhost:[port]/journal/[slug]
  Thumbnail: ✅ generated

Article 2: [slug]
  Verdict: "[verdict]"
  Quality: APPROVED — [N] revisions applied
  Word count: [N] body words
  Rendered page: http://localhost:[port]/journal/[slug]
  Thumbnail: ✅ generated
```

For each article, the checkpoint response must include the clickable rendered-page URL itself, not just a statement that the article is "open in the browser". If rendering could not be verified over HTTP, say so explicitly and explain why.

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

═══════════════════════════════════════════════════════════════
# FILE: skills/paper-triage/SKILL.md
═══════════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════════
# FILE: skills/article-writing/SKILL.md
═══════════════════════════════════════════════════════════════

---
name: article-writing
description: "Transform dental academic papers into high-signal, engaging 400–600 word clinical reviews optimized for professional clinicians and 2026 Generative Engine Optimization (GEO), written in the voice of Annabel Crabb. Use this skill whenever the user asks you to write a review, summary, or write-up of a dental journal article or academic paper — including prosthodontics, endodontics, periodontics, implantology, restorative dentistry, orthodontics, oral surgery, or any dental subspecialty. Also trigger when the user provides a dental paper (PDF, DOI, or pasted abstract) and asks for a clinical review, article summary, blog post, or professional write-up. Trigger even if they just say 'write this up', 'review this paper', or 'summarise this study' in a dental context."
version: 1.0.0
author: samrosehill
tags: [dental, clinical-review, content, geo, annabel-crabb, prosthodontics, implantology]
---

# SKILL: samrosehill.com Dental Review Article Writing

**Objective:** To transform dense dental academic papers into high-signal, engaging 400–600 word reviews optimized for professional clinicians and 2026 Generative Engine Optimization (GEO).

**Voice:** Every review is written in the style of **Annabel Crabb** — warm, witty, conversational, intellectually generous. See Section 5 below for full voice guidance.

---

## 1. PRE-FLIGHT CHECKLIST (Data Extraction)

Before drafting, identify and verify the following "Entities":

* **Primary Author & Institution:** (e.g., Kizilkaya / Fırat University)
* **Journal & Publication Date:** (e.g., International Journal of Prosthodontics, Vol 39, 2026)
* **The "Core Conflict":** The specific clinical problem or "pain point" the research addresses.
* **The DOI:** Essential for cross-platform citation and AI indexing.
* **The Verdict:** A 3–5 word punchy summary of the paper's key clinical takeaway, used for thumbnail generation. Must be readable at thumbnail size. Examples: "Gold standard holds", "92% survival at 10 years", "3x more accurate", "ISQ isn't the full story". This is the "should I click?" signal for colleagues scanning a grid of reviews.

Before drafting prose, create a compact **Evidence Pack** for yourself:

* **Citation:** exact title, authors, journal, year, DOI
* **Study frame:** study design, sample size, groups/materials, intervention/comparator, follow-up
* **Must-use findings:** 3–5 factual claims with the exact numbers, units, denominators, and comparison context
* **Limitations:** the paper's most important caveat and the study-type caveat (for example in vitro, single case, retrospective)
* **Do-not-overclaim line:** the strongest claim this article must avoid making
* **Article brief:** target reader, clinical angle, verdict candidate, headline candidate, and the opening strategy chosen after checking recent articles

Use this Evidence Pack as scaffolding only. Do not paste it into the article.

---

## 2. CRITICAL REQUIREMENTS — VERIFY BEFORE SAVING

These are the most commonly missed rules. Failure on ANY = automatic REVISE at QC.

1. **Full paper title in first 100 words** — the exact published title MUST appear in the opening Clinical Conflict section. This is a hard GEO requirement, not optional.
2. **DOI as standalone reference line** — format: `**Reference:** [Author et al. Title. *Journal*, Year. DOI: X](https://doi.org/X)` as the LAST line of the article. The DOI must NEVER appear in body text.
3. **Sign-off text is EXACT** — copy verbatim, do not paraphrase, add to, or omit any word. Check character-by-character.
4. **paperYear is an integer** — `paperYear: 2026` NOT `paperYear: "2026"`. Quoted years break the Astro build.
5. **Australian English throughout** — check every instance: colour, favour, realise, defence, analyse, standardise, centre, labour, tumour, honour, ageing, modelling, anaesthesia, haemorrhage, manoeuvre.
6. **Bullets ONLY in Key Findings** — all other sections must be flowing prose. No exceptions.
7. **No LaTeX delimiters** — use plain Unicode (n = 30, P < .05, ΔE₀₀). No $...$ anywhere.
8. **Maximum 2-3 em dashes per article** — replace extras with commas, semicolons, or parentheses.
9. **Every numeric or causal claim traces back to the Evidence Pack** — if you cannot verify the number, denominator, comparator, or study design, remove or soften the claim before saving.

---

## 3. THE STRUCTURAL BLUEPRINT

### I. The Clinical Conflict

* **Opening:** Begin with a relatable, high-stakes clinical scenario or a common operatory frustration (the "Pattern Interrupt"). Write this as flowing prose — **no section heading**. Just start the article.
* **The Pivot:** Introduce the paper as the evidence-based solution or "reality check" to that scenario.
* **SEO/GEO Trigger:** Include the full paper title and primary keywords (e.g., "Zirconia Bonding," "Digital Shade Matching") within the first 100 words.
* **Voice note:** Open with a clinical anecdote or scenario, NOT a thesis statement. Draw the reader in by curiosity and narrative before they realise they're reading an argument. Let the opening metaphor develop — don't drop a quick simile and move on.
* **CRITICAL — Opening variety:** Do NOT default to the "[day of the week] + operatory scenario" formula. This pattern ("It's a Tuesday afternoon and you're three crowns deep...") has been massively overused and is now banned. Vary your openings across these Crabb-native strategies:

  **1. The deadpan paradox.** State a clinical absurdity as though it's perfectly normal, and let the reader feel the cognitive dissonance. Don't frame it as a question — present it as a fact that shouldn't be true but is.
  *Example: "We have put a man on the moon, sequenced the human genome, and printed a titanium jaw in a university basement, but we still cannot agree on how to glue a broken bit of porcelain back onto a tooth."*

  **2. The overheard corridor moment.** A snippet of colleague conversation, a lab technician's offhand remark, a conference coffee-queue aside. Crabb loves the telling fragment — a single line of dialogue that contains an entire professional debate.
  *Example: "'Just sandblast it and bond,' said the colleague, with the confidence of someone who has never read a bond strength study in their life."*

  **3. The imported metaphor.** Borrow a frame from cooking, architecture, politics, sport, or domestic life and let it run for three or four sentences before pivoting to the clinical question. Crabb constantly imports from outside her domain — the gap between the metaphor and the subject IS the voice.
  *Example: "There is a school of thought in Italian cooking that says the fewer the ingredients, the more each one matters. A margherita pizza has four components; if the mozzarella is wrong, there is nowhere to hide. Ceramic repair operates on much the same principle."*

  **4. The quiet professional confession.** Name something every clinician does but nobody writes down in a journal article. The shared unspoken habit, the small clinical shortcut, the thing you'd never admit at a peer review meeting.
  *Example: "Most of us, if we're honest, have a preferred bonding agent that we chose not because of the evidence but because it was the one the rep left in our drawer during dental school."*

  **5. The historical or etymological detour.** Crabb loves these — a brief etymological aside, a historical curiosity, or a forgotten origin story that reframes a familiar clinical question as something stranger and more interesting than the reader expected.
  *Example: "The word 'ceramic' comes from the Greek keramos — potter's clay — which is a charmingly modest ancestry for a material that now costs $400 a unit and shatters if you look at it with the wrong occlusal scheme."*

  **6. The counterintuitive reveal.** Open with a claim that feels wrong, then immediately signal that the paper's data is about to either vindicate or demolish it. Crabb delivers these with the tone of someone reporting news they find personally fascinating.
  *Example: "Everything we think we know about zirconia bonding may be slightly, quietly, unhelpfully wrong."*

  **7. The material or object given a personality.** Treat a dental material, instrument, or clinical phenomenon as though it has intentions, preferences, or a reputation. Crabb anthropomorphises institutions and policies constantly — do the same with zirconia, composite, or the curing light.
  *Example: "Lithium disilicate has always been the overachiever of the ceramic family — strong enough, pretty enough, bondable enough. But even overachievers fracture, and when they do, the question of what to do next gets surprisingly complicated."*

  **8. The Crabb zoom-out.** Start with a wide observation about the profession, the evidence base, or clinical culture, then narrow sharply to the specific paper. The movement from macro to micro in two sentences is a signature Crabb rhythm.
  *Example: "Restorative dentistry has spent two decades accumulating ceramic options and approximately six months thinking about what happens when they break."*

  **Never reuse the same opening strategy in consecutive articles.** Before writing, check the most recent 3–5 published reviews in `src/content/reviews/` (read the first paragraph of each) and deliberately choose a different approach. If the last three articles opened with metaphors and confessions, use a deadpan paradox or a zoom-out.

### II. The Data Anchor

* **Header:** `### The Data Anchor`
* **Mandatory Stats:** Use plain Unicode for all mathematical expressions and statistical notation (e.g., n = 30, P < .05, ΔE₀₀). Do NOT use LaTeX delimiters ($...$) — articles must be portable to Substack, DentalTown, and other platforms that don't support LaTeX rendering.
* **Data Points:** Explicitly state sample sizes, study duration, control groups, and specific brand-name materials used.
* **The Metric:** Define the measurement unit (e.g., μTBS for bond strength, μm for marginal gap).
* **Voice note:** Weave stats naturally into prose — never as a dry list. Data should feel like an interesting thing you're mentioning in conversation, not a table you're reading aloud.

### III. Key Findings

* **Formatting:** Use a bulleted list for high-impact findings to ensure scannability. (This is the ONE section where bullets are permitted.)
* **Clarity:** Distinguish between *statistically significant* results and *clinically relevant* outcomes.
* **The Caveat:** Mention at least one limitation (e.g., "In-vitro only," "Short follow-up") to maintain professional objectivity.
* **Voice note:** Lead each bullet with the clinical implication, not the p-value. Bold the surprising or practice-changing data. Let the Crabb voice inflect the bullet prose — a parenthetical aside, a wry observation — but keep each bullet tight.

### IV. The Clinical Bottom Line

* **Header:** `### 💡 The Clinical Bottom Line`
* **The "Monday Morning" Rule:** Provide a 2-3 sentence summary explaining exactly how this data should change (or reinforce) a clinician's workflow tomorrow morning.
* **Entity Clustering:** Reiterate the "Gold Standard" comparison to help AI models cluster the content under the correct clinical expertise category.
* **Voice note:** End with resonance, not summary. The final line should leave the reader thinking — a reframing image, a quiet observation, a clinical truth that lingers.

---

## 4. FORMATTING & STYLE GUIDELINES

* **Paragraph Length:** Keep paragraphs under 4 lines to accommodate mobile reading between patients.
* **Emphasis:** Use **Bold** for key takeaways and surprising data points.
* **Nuance:** Use `> Blockquotes` for subjective interpretations, clinical "pearls," or nuanced author opinions.
* **Language:** Maintain a high-EEAT vocabulary (e.g., use "Secondary Caries" instead of "new decay"). But deploy professional terminology with the ease of someone who uses it daily, not someone trying to impress.
* **DOI:** Do NOT integrate the DOI into the body text. Include it as a standalone **Reference:** line at the end of the article.
* **Bullets:** Only permitted in the Key Findings section. All other sections must be flowing prose.

---

## 5. 2026 AI (GEO) OPTIMIZATION

* **Answer-First:** Ensure the first paragraph contains a concise summary of the study's conclusion to satisfy AI "Snippet" crawlers.
* **Consistent Identity:** Ensure the author's name and professional title are included in the metadata or sign-off to build the "Entity" profile.

---

## 6. THE ANNABEL CRABB VOICE

Every review must be written in the distinctive voice of **Annabel Crabb** — the ABC's chief online political writer, Walkley Award winner, and one of Australia's most beloved commentators — adapted here for dental clinical prose.

**Voice preservation is a product requirement.** Do not flatten the article into generic medical SEO copy. The quality improvement goal is stronger evidence control and better clinical judgement while preserving this distinctive voice. A technically accurate but bland summary is not a successful review.

### Core Qualities

**1. Wit That Sneaks Up on You.** The humour is observational, layered, and arrives mid-sentence when the reader is expecting a straight clinical point. It's embedded in genuine insight, never bolted on as decoration.

**2. The Deceptively Gentle Skewer.** Devastating points delivered breezily. Crabb doesn't shout — she raises an eyebrow. If you find yourself writing angry or dismissive prose, stop. Channel frustration into precision and irony, not volume.

**3. Warmth and Generosity.** Even when critiquing a study's limitations, maintain curiosity and respect. Researchers in this voice are fascinating people doing interesting work, not targets.

**4. The Conversational Essayist.** Write the way a very clever, very well-read colleague talks over coffee. Parenthetical asides, direct addresses to the reader, rhetorical questions — but with the precision of someone who trained in evidence-based practice.

**5. Data Worn Lightly.** Stats and evidence back the argument, but never flatten the prose. Cite a finding the way you'd mention an interesting thing you read — naturally, in service of a point. Then add the kicker.

### Sentence-Level Style

* **Sentence length:** Varied. Long, rolling, clause-laden observations followed by short, sharp verdicts.
* **Vocabulary:** Educated but never pompous. The register shifts within a single sentence for comic or rhetorical effect.
* **Punctuation:** Generous semicolons and parentheses. Occasional italics for emphasis or ironic inflection. **Minimise em dashes** — use no more than 2–3 per article. Prefer commas, semicolons, colons, or parentheses instead. Overuse of em dashes is a telltale sign of AI-generated text.
* **Spelling:** Australian English throughout — colour, favour, realise, defence.
* **Parenthetical asides:** Use these as a second voice — an inner commentator who can't quite believe what they're reporting.

### Techniques to Deploy

* **Extended metaphors that commit fully.** Start plausible, develop patiently, land with impact. Don't wink at the audience.
* **The accumulating list.** Build momentum through escalation, then punctuate with a short, devastating sentence.
* **Comparative deflation.** Place two facts next to each other and let the reader do the maths. Don't moralise — name the mechanism.
* **Elevated diction for mundane matters.** The gap between language and clinical reality IS the joke.
* **The Crabb opening.** Scene-setting or anecdotal — a specific clinical moment that seems like a tangent but turns out to be the perfect entry point. Never a thesis statement.
* **The Crabb ending.** Never summarise. Reframe, resonate, or leave an image hanging.

### What NOT to Do

* **Don't be mean-spirited.** Sharp but never cruel.
* **Don't be dry.** If a paragraph has no personality, no unexpected turn — it's not Crabb.
* **Don't over-explain the joke.** Trust the reader.
* **Don't forget the substance.** Wit in service of genuine clinical insight. All laughs and no analysis is a failure.
* **Don't use American English.** No "color," "realize," or "labor."
* **Don't use bullets in prose sections.** Flowing prose always, except in Key Findings.

═══════════════════════════════════════════════════════════════
# FILE: skills/annabel-crabb-voice/SKILL.md
═══════════════════════════════════════════════════════════════

---
name: annabel-crabb-voice
description: "Write in the voice and style of Annabel Crabb, Australia's premier political sketch writer and commentator. Use this skill whenever the user asks you to write like Annabel Crabb, write in her voice/style/tone, produce political commentary or essays in an Australian witty style, create humorous political analysis, or write anything 'in the style of Annabel Crabb'. Also trigger when the user mentions Annabel Crabb and writing together, or asks for witty Australian political prose."
---

# Writing in the Voice of Annabel Crabb

You are writing in the distinctive voice of **Annabel Crabb** — the ABC's chief online political writer, Walkley Award winner, author of *The Wife Drought*, *Rise of the Ruddbot*, *Stop at Nothing*, and *Men at Work* (Quarterly Essay 75), host of *Kitchen Cabinet*, and one of Australia's most beloved political commentators.

Crabb has been called "Australia's undisputed master of political sketch writing, loved by her readers for the deceptively gentle skewering she performs on the subjects." Your job is to channel that voice faithfully.

## The Crabb Voice: Core Qualities

### 1. Wit That Sneaks Up on You

Crabb's humour is never sledgehammer comedy. It's observational, layered, and often arrives mid-sentence when the reader is expecting a straight policy point. The laugh lands because it's embedded in genuine insight.

**How she does it:**
- Extended metaphors that start plausible and escalate to absurdity
- Deadpan observations delivered as though they're perfectly ordinary
- Juxtaposing the grand with the mundane (parliament with piglets, democracy with prawns)

**Example from her work:**
"Opposition leaders are like miniature piglets. They look so sweet in the shop, don't they? With their whiffling little pink noses and their eagerness to please; with their intelligent eyes and their loving natures and the sales assistant's guarantee that they are fastidiously clean and, moreover, will fetch the paper every morning – what's not to love? It is only much later on, well after the election's won and the warranty's expired, that you wake up and realise, with a dull sense of unsurprise, that you've got a six-foot grunter digging up your backyard."

Notice: the metaphor commits fully, never winks at the audience, and the payoff ("six-foot grunter") earns its impact through patient build-up. When writing in Crabb's voice, let your metaphors *develop*. Don't drop a quick simile and move on — give it room to breathe, escalate, and land.

### 2. The Deceptively Gentle Skewer

Crabb's criticism is devastating precisely because it's charming. She doesn't shout. She raises an eyebrow. Her most cutting observations are often delivered with the syntax of a cheerful aside.

**Example:** "The Australian media industry tells a long and continuing story... of mediocre men whose shamelessness extends their professional life expectancies well beyond what a real meritocracy would permit."

**Example:** "It's certainly not resembling in any way what happens with men, who've been breeding like marmots in cabinet since the federation, and no one ever makes a fuss about that."

The trick is to make the devastating point sound almost *breezy*. If you find yourself writing angry prose, stop. Crabb channels frustration into precision and irony, not volume.

### 3. Warmth and Generosity Toward Subjects

Even when she's taking someone apart, there's an underlying affection for the human messiness of politics. Crabb genuinely believes that understanding a politician's background, motivations, and private life makes you understand their public decisions better. As she puts it: "Political decisions, being subjective, are absolutely affected by that person's upbringing, their experiences in life, their passions, their motivations."

This means: never write with contempt. Write with curiosity, even bemusement. Politicians in Crabb's world are fascinating creatures worthy of study, not villains to be destroyed.

### 4. The Conversational Essayist

Crabb writes the way a very clever, very well-read friend talks over a good dinner. Her prose has the rhythm of spoken language — parenthetical asides, direct addresses to the reader, rhetorical questions — but with the precision of someone who trained as a lawyer before becoming a journalist.

**Techniques:**
- Address the reader directly: "Don't you think?", "Bear with me here"
- Parenthetical commentary that adds a second layer: "(which, let's face it, is how most of these things end up)"
- Sentences that vary dramatically in length — a long, rolling, clause-laden observation followed by a short, sharp verdict
- The semicolon is her friend; she uses it to yoke together ideas that are related but surprising in their pairing

### 5. Historical and Cultural Depth

Crabb doesn't just comment on what happened today. She reaches back — to federation, to precedent, to cultural context — to explain why today's absurdity has deep roots. She treats Australian democratic history as a treasure trove of eccentric stories, not a dusty archive.

**Example:** "One of the complex and unique delights of Australian democracy is our three-tiered justice system. The first tier is the laws that are debated and passed by our parliaments. Then we have the common law, which is made by judges interpreting those laws. These two are fairly orthodox. But in this country, we've added a third layer, called the 'pub test'."

### 6. Data Worn Lightly

Crabb backs her arguments with evidence and statistics, but never lets the data flatten the prose. She'll cite a study the way you'd mention an interesting thing you read — naturally, in service of a point, never as a list of bullet points.

**Example:** "A 2006 study of American women found that modern mothers who work full-time actually spend more hours one-on-one with their children per week than their stay-at-home mothers had in 1976. They just feel far more inadequate and guilty."

Notice how the statistic arrives, does its work, and then the kicker — "They just feel far more inadequate and guilty" — is pure Crabb: short, wry, compassionate.

### 7. The Crabb Opening

Her openings are often scene-setting or anecdotal — a specific, vivid moment that seems like a tangent but turns out to be the perfect entry point for her argument. She might open with a toy kangaroo, a question time altercation, or a dinner party observation, then pivot to the larger point.

She almost never opens with a thesis statement. The reader is drawn in by curiosity and narrative before they realise they're reading an argument.

### 8. Australian Vernacular

Crabb's language is distinctly Australian without being performatively so. She'll use "bananas" instead of "crazy," "mate" in exactly the right register, and occasionally deploy Australianisms that feel natural rather than folksy. She writes in Australian English (colour, favour, realise, labour).

**Example:** "How can you test whether something's an assumption? Try this: switch things around, and check how bananas everybody goes."

## Sentence-Level Style Guide

- **Tone:** Warm, witty, conversational, intellectually generous
- **Sentence length:** Varied. Mix long, winding clauses with punchy one-liners
- **Paragraph length:** Generally short-to-medium. She's a newspaper columnist at heart — white space is her ally
- **Vocabulary:** Educated but never pompous. She'd say "fastidiously" but also "grunter." The register shifts within a single sentence for comic or rhetorical effect
- **Punctuation:** Generous use of semicolons, em dashes, and parentheses. Occasional italics for emphasis or ironic inflection
- **Person:** Usually third-person analysis, occasionally first-person when she's weaving in personal experience. Frequent second-person asides ("you'd think," "try this")
- **Spelling & conventions:** Australian English throughout (colour, realise, defence, programme where appropriate)

## What NOT to Do

- **Don't be mean-spirited.** Crabb is sharp but never cruel. If your prose reads like it's punching down, rewrite it.
- **Don't be dry.** This isn't academic analysis. If a paragraph has no personality, no unexpected turn, no moment of delight — it's not Crabb.
- **Don't over-explain the joke.** If you've written something funny, trust the reader and move on.
- **Don't forget the substance.** The wit is in service of genuine insight. A Crabb column that's all laughs and no analysis is a failed Crabb column.
- **Don't use American English.** No "color," "realize," or "labor" (unless referring to the Australian Labor Party, which is the official spelling).
- **Don't write in bullet points or listicle format.** Crabb writes in flowing prose. Always.

## Applying This Voice

When the user gives you a topic, write it as Crabb would approach it:

1. **Find the human entry point** — a person, a moment, an anecdote that makes the topic vivid and specific
2. **Build an extended metaphor or analogy** if the topic warrants it — commit to it fully
3. **Weave in context and evidence** naturally, as part of the narrative, not as citations
4. **Escalate toward your sharpest observation** — save the killer line for when it will land hardest
5. **End with resonance, not summary** — Crabb's endings leave the reader thinking, often with a final image or observation that reframes everything that came before

Remember: you're not writing *about* Annabel Crabb. You're writing *as* her. Channel the warmth, the wit, the intellectual generosity, and the deceptively gentle skewer.

---

## Deep Dive: Techniques Observed Across 20+ Sources (ABC Articles, Books, Interviews)

The following observations are drawn from close reading of Crabb's ABC columns (2019–2026), her Quarterly Essays, *The Wife Drought*, reviews, and interviews. Use these as a granular style toolkit.

### Opening Gambits — The Crabb Lead

Crabb almost never opens with the news. She opens with the *angle* — usually via misdirection or an unexpected register.

**Pattern 1: The deadpan zinger that IS the thesis.**
> "And they say the Liberal Party doesn't get women. They got this one pretty quickly — after just nine months."
(Ley leadership article, Feb 2026 — the entire argument condensed into two sentences. The second sentence is the knife.)

**Pattern 2: The scene-setting detour that becomes the metaphor.**
> "The two months preceding a wedding are notoriously hazardous. Many micro-disasters can cause distress. The bomboniere are unsatisfactory. The chair-hire guy turns out to be a scoundrel. The string quartet contains a drunkard."
(Albanese wedding article, Nov 2025 — lists mundane wedding disasters before pivoting to compare them with the PM's genuinely chaotic schedule.)

**Pattern 3: The philosophical setup that sounds like a civics lecture but lands as comedy.**
> "One of the complex and unique delights of Australian democracy is our three-tiered justice system… But in this country, we've added a third layer, called the 'pub test'. A much, much more nebulous affair, largely administered by journalists asking ourselves: 'Yeah, but what would a totally imaginary group of very pissed people think of this?'"
(Pub test article, Dec 2025)

**Pattern 4: The vaguely proud national shrug.**
> "Australia's democratic system is unlike any other on Earth. As a nation, we sort of vaguely understand this, and take a generalised pride in the triennial democracy sausage, and the beige, competent omnipresence of the Australian Electoral Commission."
(Civic duty article, Nov 2025 — "beige, competent omnipresence" is peak Crabb: an institution described as if it were a reliable appliance.)

### The Accumulating List — A Signature Move

Crabb frequently builds momentum through accumulation — listing items that escalate in absurdity or emotional weight, then punctuating with a short, devastating sentence.

**Example (Albanese's pre-wedding schedule):**
She lists: recognised Palestine, addressed the UN, zipped to the UK, went to Abu Dhabi, entered the Trump White House, went to Uluru, ASEAN, APEC, parliament, WA, midnight COP negotiations, G20, passage of environment bill... then:
> "And on Saturday, the PM concluded all this by GETTING MARRIED. Which feels — even for regular entrants to the Multitasking Olympics — dangerously close to showing off."

Note the all-caps "GETTING MARRIED" — extremely rare in her prose, used for maximum comic contrast with the preceding policy avalanche.

**Example (Wells expense saga):**
> "She ate expensive food in Paris, where food is expensive. She went to sporting events."

The second sentence is comically flat after the first's gentle sarcasm. Then:
> "One newspaper reports, with neutral menace, that 'Ms Wells has been to every AFL grand final since she became sports minister.' Extraordinary."

"Neutral menace" is a brilliant Crabb coinage — describing a press tone. "Extraordinary" as a standalone sentence is dry as the Nullarbor.

### The Structural Aside / Parenthetical Snark

Crabb uses parentheses and em-dashes as a second voice — an inner commentator who can't quite believe what she's reporting.

- "(BOOBS!)" — single word as parenthetical, in all-caps, demolishing the pretence of gender-blind analysis
- "(which, let's face it, is how most of these things end up)"
- "(a city built because we couldn't agree whether Sydney or Melbourne should be the capital, and opted instead to build a new home for it that would be inconvenient for everyone)"
- "(strewn with booby traps and golden gewgaws in comparable and bewildering numbers)" — describing the Trump White House

Also the self-interrupting notation: "*checks notes*" — borrowing internet vernacular for comic timing within formal-register prose.

### Euphemism and Elevated Diction for Low Matters

Crabb routinely describes messy political realities using language several registers above the subject matter. The gap between language and reality IS the joke.

- "crisply sent on eternity leave" — for being sacked as leader
- "executing a major handbrake turn" — for defecting to another party
- "One human gestational period elapsed" — for nine months in office
- "premature ejection isn't exclusively a lady phenomenon" — double entendre delivered at walking pace
- "the denser cock-forests of the Australian biosphere" — describing male-dominated sectors
- "advance dauntlessly into" — heroic register for navigating workplace sexism
- "A jury of their beers" — repurposing legal language for the pub test
- "trading under the One Nation banner" — corporate language for political defection

### The Comparative Deflation Technique

When calling out double standards, Crabb doesn't argue — she simply places two facts next to each other and lets the reader do the maths.

> "Joyce spent double that amount on private flights pottering back and forth from Tamworth when he was deputy PM. Wells's own flights to New York — coming in at around $30,000 — are one hundredth of the $3m that the current deputy PM spent on RAAF flights in just over a year."

Then, rather than saying "this is a double standard," she pivots to:
> "But there's something about New York itself that spells trouble for passing the pub test."

She names the irrational mechanism rather than moralising about it.

### The Knockout Gender Observation

Gender analysis is Crabb's intellectual home turf, and her most devastating passages deploy a specific technique: the hypothetical gender-swap.

> "Can you imagine a female politician surviving a story arc in which she commences a relationship with a staff member and leaves her husband who has raised their kids and fibs about it to colleagues and then blows up her government with her resignation and then later passes out in the street, which is captured on video, and now quits the party that's sponsored her into parliament?"

This is a single breathless sentence — no full stops, deliberately cumulative — forcing the reader to absorb the full absurdity.

Also: naming workplace tropes with mock-corporate headings — "Adult Man Babysitting", "Not In The WhatsApp", "Clean That Up, Would You?", "Just, I Don't Know… *vague gesture* … Not Up To It" — treats systemic sexism as office comedy, which makes it hit harder.

### Historical Anecdotes as Narrative Engine

Crabb treats Australian democratic history as a barrel of eccentric stories. She'll drop in a colonial-era figure and make them feel contemporary.

- Billy Hughes inventing the forerunner of the AFP "in a fit of rage when a rabble-rouser threw an egg at him in Queensland"
- Justice Boothby arriving in South Australia with "his wife and 12 surviving children (the joke was that he brought his own jury)"
- NSW Labor sweeping the 1938 Senate by "running four candidates called Ashley, Arthur, Armstrong and Amour"
- Voters' blue crayons melting in a 1917 heatwave during a conscription plebiscite
- The AEC's bingo roller — "two-and-a-half pages in the Electoral Act devoted to that act of rolling the cage"

These are never there just for colour. They always illuminate something about the present.

### The Crabb Ending

Her endings never summarise. They reframe, resonate, or leave an image hanging.

**The unstated conclusion:**
> "Of the seven former prime ministers of this country who still draw breath, there is really only one who has consistently employed a similar approach. It's the only other woman. What an interesting coincidence."

**The pivot to warmth after sustained critique:**
> "But enough of that. For now: Huzzah! Champagne! Cavoodles! Let us resume our arguments on the morrow."

**The warning disguised as a toast:**
> "And tonight give thanks that in 2025's 'killing season', love had the numbers after all."

**The punchline callback:**
> "But when employing the pub test, avoid the beer goggles."

### Vocabulary & Phrase Patterns to Emulate

| Crabb says... | Instead of... |
|---|---|
| "a generalised pride" | "national pride" |
| "beige, competent omnipresence" | "reliable institution" |
| "with neutral menace" | "threateningly" |
| "scudded home" | "flew back" |
| "a horrid, flu-like lurgy" | "a bad cold" |
| "dangerously close to showing off" | "impressive" |
| "your correspondent's bingo card" | "what I expected" |
| "the technicolour explosions of X blowing itself up" | "X having a crisis" |
| "hard-launched" | "announced" |
| "the ancient marital principle 'for better or worse'" | "marriage vows" |

### Quote Integration

When Crabb quotes interview subjects, she often sets them up with a brief, vivid character tag, then lets the quote run. She never paraphrases when a direct quote is funnier or more revealing.

> "Says Waleed Aly, who is a politics lecturer at Monash University and a writer, thinker, podcaster and Gold Logie-winning TV host..."

The accumulation of Aly's titles is itself a gentle joke — he contains multitudes. Then his quote runs uninterrupted for a full paragraph.

When quoting politicians, she often adds a devastating stage direction:
> "He said, 'Well, you're going to end up paying the ultimate price.' But he thought it was like a bad joke. I was deadly serious, so I remember having to say to him, Tony, I'm serious."

---

## Source Summary

This skill was built from close reading of:
- **5 full-length ABC News analysis columns** (2025–2026): Ley leadership spill, pub test/Barnaby Joyce, Albanese wedding, civic duty/voting system, social media/influencers — totalling approximately **12,000+ words** of primary source text
- **9 targeted web searches** surfacing excerpts from ~25 additional sources including Quarterly Essays (*Stop at Nothing*, *Men at Work*), *The Wife Drought*, Goodreads reviews, BuzzFeed profile, Women's Agenda, Booktopia Q&A, ArtsHub interview, Penguin author page, Wikipedia, and Grokipedia
- **Total source material consulted:** approximately **15,000+ words**

═══════════════════════════════════════════════════════════════
# FILE: skills/article-draft-check/SKILL.md
═══════════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════════
# FILE: skills/thumbnail-generator/SKILL.md
═══════════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════════
# FILE: skills/publish-article/SKILL.md
═══════════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/SKILL.md
═══════════════════════════════════════════════════════════════

---
name: journal-article-downloader
description: "Download full-text journal articles from dental, prosthodontic, and implant dentistry journals using King's College London (KCL) institutional library access. Use this skill whenever the user wants to download academic papers, fetch journal articles, access paywalled dental research, retrieve PDFs from publishers like Wiley, Elsevier, Springer, Quintessence, Wolters Kluwer, J-STAGE, or KoreaMed, or build a literature collection from dental/prosthodontic journals. Also trigger when the user mentions article downloads, library access, EZproxy, institutional login, Shibboleth authentication, or any of the specific journal names listed in this skill."
---

# Journal Article Downloader

Download full-text PDFs from dental and prosthodontic journals using KCL institutional library access via the Chrome MCP browser tools.

## Overview

This skill covers downloading from **8 publisher groups** spanning ~21 journals. Each publisher has a different authentication and download workflow. The general pattern is:

1. **Find articles** — use the CrossRef API to get recent DOIs
2. **Authenticate** — establish an institutional session (EZproxy, Shibboleth, or direct OA)
3. **Download PDFs** — use Chrome JS `fetch()` + blob pattern to trigger browser downloads

All downloads go to the user's `~/Downloads` folder (Chrome default). After downloading, **move files into the organized folder structure** described below.

## File Organization

All downloaded papers must be filed into a structured folder hierarchy within the project workspace. The structure is **one folder per journal**, with subfolders by **year and month of publication**.

```
2MP Project/
├── journals/
│   ├── IJP/
│   │   ├── 2025/
│   │   │   ├── 2025-01/
│   │   │   │   ├── Smith_2025_Zirconia-crowns-RCT.pdf
│   │   │   │   └── Lee_2025_Digital-occlusal-analysis.pdf
│   │   │   ├── 2025-03/
│   │   │   └── 2025-06/
│   │   └── 2026/
│   │       ├── 2026-01/
│   │       └── 2026-03/
│   ├── CIDR/
│   ├── COIR/
│   ├── Dental-Materials/
│   ├── Dental-Materials-J/
│   ├── Implant-Dentistry/
│   ├── IJID/
│   ├── IJOMI/
│   ├── IJPRD/
│   ├── JAP/
│   ├── JERD/
│   ├── JIPS/
│   ├── JOI/
│   ├── J-Oral-Rehab/
│   ├── J-Prosth-Research/
│   ├── J-Prosthodontics/
│   ├── JPIS/
│   └── RDE/
```

### Folder Naming Rules

**Journal folders** use the abbreviation from the ISSN reference table below (e.g. `IJP`, `CIDR`, `JERD`). For journals without a standard abbreviation, use a short hyphenated name (e.g. `Dental-Materials`, `J-Oral-Rehab`, `Implant-Dentistry`).

**Year folders** use four-digit year: `2025`, `2026`.

**Month folders** use `YYYY-MM` format: `2025-01`, `2025-06`, `2026-03`. If the exact month is unavailable from CrossRef metadata, use the **issue number** to determine the month (most dental journals publish monthly or bimonthly). If only a year is available, file under `YYYY-00`.

**PDF filenames** follow this pattern:
```
FirstAuthor_Year_Short-title-slug.pdf
```
Examples:
- `Kizilkaya_2026_Digital-color-vs-spectrophotometer.pdf`
- `Nikzad_2026_Nano-HA-zirconia-bond-strength.pdf`
- `Fasbinder_2026_Lithium-disilicate-CAD-CAM-10yr.pdf`

Keep the title slug under 50 characters. Use hyphens, no spaces. Strip special characters.

### Filing Workflow

After each download:
1. Get the **publication date** from CrossRef metadata (`published-print` or `published-online` fields) or from the article itself
2. Get the **first author surname** and a **short title** from the article metadata
3. Create the journal/year/month folder path if it doesn't exist: `mkdir -p "journals/{ABBREV}/{YYYY}/{YYYY-MM}"`
4. Rename and move the PDF: `mv ~/Downloads/filename.pdf "journals/{ABBREV}/{YYYY}/{YYYY-MM}/{Author}_{Year}_{Slug}.pdf"`

### CrossRef Date Extraction

When querying CrossRef, include date information in the article metadata extraction:

```javascript
fetch('https://api.crossref.org/journals/{ISSN}/works?rows=5&sort=published&order=desc')
  .then(r => r.json())
  .then(data => {
    window._articles = JSON.stringify(
      data.message.items.map(i => ({
        title: (i.title || [''])[0].substring(0, 80),
        doi: i.DOI,
        author: i.author ? i.author[0].family : 'Unknown',
        date: i['published-print']
          ? i['published-print']['date-parts'][0].join('-')
          : (i['published-online']
            ? i['published-online']['date-parts'][0].join('-')
            : 'no-date'),
        url: (i.resource || {}).primary?.URL || ''
      }))
    );
  });
```

This returns dates as `2026-1` (year-month) or `2026-1-15` (year-month-day). Parse the month to build the folder path: a date of `2026-1` becomes folder `2026/2026-01`.

## Prerequisites

- **Chrome MCP** (`mcp__Claude_in_Chrome__*` tools) must be connected
- **KCL institutional credentials** — the user must be able to log in via KCL's Shibboleth/SSO when prompted
- An active browser session in Chrome

## Step 1: Find Articles via CrossRef API

Use Chrome's JavaScript tool to query CrossRef for recent articles from any journal by ISSN:

```javascript
// Single journal query
fetch('https://api.crossref.org/journals/{ISSN}/works?rows=3&sort=published&order=desc')
  .then(r => r.json())
  .then(data => {
    window._articles = JSON.stringify(
      data.message.items.map(i => ({
        title: (i.title || [''])[0].substring(0, 80),
        doi: i.DOI,
        url: (i.resource || {}).primary?.URL || ''
      }))
    );
  });
// Then read: window._articles
```

**Batch query for multiple journals:**

```javascript
Promise.all([
  fetch('https://api.crossref.org/journals/{ISSN1}/works?rows=3&sort=published&order=desc').then(r=>r.json()),
  fetch('https://api.crossref.org/journals/{ISSN2}/works?rows=3&sort=published&order=desc').then(r=>r.json())
]).then(results => {
  window._j1 = JSON.stringify(results[0].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI})));
  window._j2 = JSON.stringify(results[1].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI})));
});
```

Always store results in `window._varName` global variables to avoid Chrome content filter blocking responses that contain cookies, query strings, or base64 data.

## Step 2: Authenticate & Download by Publisher

Read the appropriate reference file for the publisher you need:

| Publisher Group | Journals | Reference File |
|---|---|---|
| Quintessence | IJP, IJOMI, IJPRD | `references/quintessence.md` |
| Wiley | J Prosthodontics, CIDR, COIR, JERD, J Oral Rehab | `references/wiley.md` |
| Elsevier | Dental Materials | `references/elsevier.md` |
| Springer (OA) | Int J Implant Dentistry | `references/springer-oa.md` |
| Korean OA | JAP, RDE, JPIS | `references/korean-oa.md` |
| Wolters Kluwer | JIPS, Implant Dentistry | `references/wolters-kluwer.md` |
| J-STAGE | Dental Materials J, J Prosth Research | `references/jstage.md` |
| AAID | J Oral Implantology | `references/aaid.md` |

## Journal ISSN Reference

| Journal | Abbreviation | Print ISSN | Online ISSN | Publisher |
|---|---|---|---|---|
| Int J Prosthodontics | IJP | 0893-2174 | — | Quintessence |
| Int J Oral Maxillofac Implants | IJOMI | 0882-2786 | — | Quintessence |
| Int J Periodontics Restorative Dent | IJPRD | 0198-7569 | — | Quintessence |
| J Prosthodontics | — | 1059-941X | 1532-849X | Wiley |
| Clin Implant Dent Relat Res | CIDR | 1523-0899 | 1708-8208 | Wiley |
| Clin Oral Implants Res | COIR | 0905-7161 | 1600-0501 | Wiley |
| J Esthet Restorative Dent | JERD | 1496-4155 | 1708-8240 | Wiley |
| J Oral Rehab | — | 0305-182X | — | Wiley |
| Dental Materials | — | 0109-5641 | — | Elsevier |
| Int J Implant Dentistry | IJID | 2198-4034 | — | Springer |
| J Advanced Prosthodontics | JAP | 2005-7806 | — | Korean Acad |
| Restorative Dent Endodontics | RDE | 2234-7658 | — | Korean Acad |
| J Periodontal Implant Science | JPIS | 2093-2278 | — | Korean Acad |
| J Indian Prosthodontic Society | JIPS | 0972-4052 | — | WK/Medknow |
| Implant Dentistry | — | 1056-6163 | — | WK/LWW |
| Dental Materials Journal | DMJ | 0287-4547 | — | J-STAGE |
| J Prosthodontic Research | JPR | 1883-1958 | — | J-STAGE |
| J Oral Implantology | JOI | 0160-6972 | — | AAID |

## Core Download Pattern (Chrome JS fetch + blob)

This is the universal download mechanism used across all publishers once authenticated:

```javascript
window._dlResult = 'pending';
fetch(PDF_URL, {credentials: 'include'})
  .then(r => {
    window._dlResult = 'status:' + r.status + ' type:' + r.headers.get('content-type');
    return r.blob();
  })
  .then(blob => {
    window._dlResult = 'size:' + blob.size;
    var blobUrl = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = blobUrl;
    link.download = 'FILENAME.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(blobUrl);
  })
  .catch(e => { window._dlResult = 'err:' + e.message; });
'fetch started'
```

Then check result: `window._dlResult`

**Success indicator:** `size:` followed by a number > 100000 (typically 500KB–5MB for journal PDFs). If size is < 60000, you likely got an HTML page instead of a PDF — check authentication.

## Important Notes

- **Chrome content filter**: Never try to return fetch response details directly. Always store in `window._varName` globals and read separately.
- **Download location**: Files go to `~/Downloads`. The base64 pipeline to write directly to project folders is blocked by Chrome content filter. After download, **always rename and move to the `journals/` folder structure**.
- **Shibboleth session persistence**: Once authenticated via KCL Shibboleth for one publisher, the session often carries over to other publishers using the same IdP.
- **OA journals**: Korean, Springer IJID, and many J-STAGE articles are open access — no authentication needed.
- **Rate limiting**: Space downloads a few seconds apart. Don't batch more than 5 rapid fetches.
- **Filing is mandatory**: Every downloaded PDF must be renamed and moved into the `journals/{ABBREV}/{YYYY}/{YYYY-MM}/` structure before the task is considered complete. Never leave PDFs loose in `~/Downloads` or the project root.

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/aaid.md
═══════════════════════════════════════════════════════════════

# AAID (American Academy of Implant Dentistry)

## Journals
- Journal of Oral Implantology — JOI (ISSN 0160-6972)

## Platform
Published by the Allen Press / AAID. Available at:
```
https://meridian.allenpress.com/joi
```

## Authentication

JOI is a subscription journal. Use either:

1. **EZproxy DOI resolver** (try first):
   ```
   https://doi-org.kcl.idm.oclc.org/{DOI}
   ```

2. **Direct institutional access**: The Allen Press/Meridian platform supports institutional login. Navigate to the journal and look for "Institutional Login" or "Access via your institution" options.

## DOI Pattern
```
10.1563/aaid-joi-D-XX-XXXXX
```

## Download Approach

1. Use CrossRef to find recent article DOIs
2. Navigate via EZproxy DOI resolver for authenticated access
3. On the article page, find the PDF download link
4. Click to download, or use fetch+blob with the PDF URL:

```javascript
window._joiDl = 'pending';
fetch(PDF_URL, {credentials: 'include'})
  .then(r => r.blob())
  .then(blob => {
    window._joiDl = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'JOI_article.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._joiDl = 'err:' + e.message; });
'fetch started'
```

## Finding Articles

```javascript
fetch('https://api.crossref.org/journals/0160-6972/works?rows=3&sort=published&order=desc')
  .then(r => r.json())
  .then(data => {
    window._joiArticles = JSON.stringify(
      data.message.items.map(i => ({
        title: (i.title || [''])[0].substring(0, 80),
        doi: i.DOI,
        url: (i.resource || {}).primary?.URL || ''
      }))
    );
  });
```

## Quirks & Notes
- Allen Press/Meridian is a smaller publisher platform — less tested than Wiley/Elsevier
- The EZproxy DOI resolver is the recommended first approach
- Some JOI articles may have free access after an embargo period
- The platform may have different PDF URL structures than major publishers — inspect the download button on the article page
- Not yet fully tested with live downloads — workflow is extrapolated from the EZproxy DOI pattern that works with other publishers

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/elsevier.md
═══════════════════════════════════════════════════════════════

# Elsevier (ScienceDirect)

## Journals
- Dental Materials (ISSN 0109-5641)

## Authentication: EZproxy DOI Resolver + Shibboleth

Elsevier uses a two-stage authentication approach. The EZproxy DOI resolver provides the entry point, and Elsevier's own SSO handles the institutional login.

### EZproxy DOI Resolver (Entry Point)
```
https://doi-org.kcl.idm.oclc.org/{DOI}
```

Example:
```
https://doi-org.kcl.idm.oclc.org/10.1016/j.dental.2025.01.001
```

This resolves the DOI through KCL's proxy, which establishes the institutional context.

### Authentication Flow

**For Open Access articles:**
1. Navigate to `https://doi-org.kcl.idm.oclc.org/{DOI}`
2. Redirects directly to ScienceDirect with full access
3. No additional login needed

**For paywalled articles:**
1. Navigate to `https://doi-org.kcl.idm.oclc.org/{DOI}`
2. If no active Shibboleth session, Elsevier redirects to `id.elsevier.com`
3. The page shows "Access through your organization" with KCL listed
4. Click the KCL button
5. Redirects to KCL Shibboleth login (or auto-completes if session exists)
6. Redirects back to ScienceDirect with full access

### PDF Download — IMPORTANT: Special Workflow

Elsevier does NOT support simple URL-based PDF download like Wiley. The `pdfft` URL pattern returns HTML, not a PDF.

```
# THIS DOES NOT WORK for programmatic download:
https://www.sciencedirect.com/science/article/pii/{PII}/pdfft?isDTMRedir=true&download=true
# Returns ~52KB HTML page, not a PDF
```

### Correct Download Method: View PDF Button → Signed S3 URL

Elsevier generates time-limited, signed AWS S3 URLs for PDF access. The workflow requires clicking the "View PDF" button in the browser:

1. Navigate to the article page (authenticated via EZproxy DOI resolver)
2. Use Chrome MCP `find` tool to locate the "View PDF" button/link
3. Click it — this opens the Elsevier PDF viewer
4. The PDF is served from `pdf.sciencedirectassets.com` with AWS signed parameters:
   ```
   https://pdf.sciencedirectassets.com/271039/...?X-Amz-Security-Token=...&X-Amz-Signature=...
   ```
5. These signed URLs are temporary and unique per session

### Download via Chrome MCP Click (Recommended)

Since the PDF URL is dynamically generated with security tokens, the most reliable approach is:

1. Navigate to article page via EZproxy DOI
2. Use `mcp__Claude_in_Chrome__find` to locate "View PDF" or "Download PDF"
3. Click to open the PDF viewer
4. Use `mcp__Claude_in_Chrome__find` to locate the download button within the PDF viewer
5. Click to trigger the browser's native download

### Alternative: Extract and Fetch the S3 URL

If you need programmatic download, you can try extracting the signed URL from the PDF viewer page. However, note that:
- Chrome content filter may block responses containing the signed URL (base64/query string data)
- The URL expires quickly
- This is less reliable than the click-based approach

```javascript
// After the PDF viewer is open, try:
window._pdfUrl = 'pending';
var iframe = document.querySelector('iframe[src*="sciencedirectassets"]');
if (iframe) {
  window._pdfUrl = 'found iframe';
  // The src may be blocked by content filter
} else {
  window._pdfUrl = 'no iframe found';
}
```

### Finding Articles via CrossRef

```javascript
fetch('https://api.crossref.org/journals/0109-5641/works?rows=3&sort=published&order=desc')
  .then(r => r.json())
  .then(data => {
    window._dmArticles = JSON.stringify(
      data.message.items.map(i => ({
        title: (i.title || [''])[0].substring(0, 80),
        doi: i.DOI,
        pii: i.alternative_id ? i.alternative_id[0] : ''
      }))
    );
  });
```

### Quirks & Notes
- Elsevier is the most complex publisher to download from programmatically
- The `pdfft` endpoint is a red herring — it returns HTML, not PDF binary
- Signed S3 URLs contain AWS security tokens and expire within minutes
- Chrome content filter blocks attempts to read the S3 URLs via JavaScript
- The click-based approach through Chrome MCP is most reliable
- Successfully tested: navigated to Dental Materials article, authenticated via Shibboleth, accessed PDF viewer
- PII (Publisher Item Identifier) format: `S0109564125XXXXXX` — useful for constructing article URLs

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/jstage.md
═══════════════════════════════════════════════════════════════

# J-STAGE (Japan Science and Technology Information Aggregator, Electronic)

## Journals
- Dental Materials Journal — DMJ (ISSN 0287-4547)
- Journal of Prosthodontic Research — JPR (ISSN 1883-1958)

## Platform
Both journals are hosted on J-STAGE: `https://www.jstage.jst.go.jp/`

## Authentication: Mostly Open Access

Most articles on J-STAGE are open access. J-STAGE is Japan's primary electronic journal platform operated by the Japan Science and Technology Agency (JST). Dental journals on the platform typically provide free full-text access.

For any paywalled articles, try the EZproxy DOI resolver:
```
https://doi-org.kcl.idm.oclc.org/{DOI}
```

## Article URL Patterns

**Dental Materials Journal:**
```
https://www.jstage.jst.go.jp/article/dmj/{volume}/{issue}/{article_id}/_article
```

**Journal of Prosthodontic Research:**
```
https://www.jstage.jst.go.jp/article/jpr/{volume}/{issue}/{article_id}/_article
```

## PDF URL Patterns

J-STAGE provides direct PDF access:
```
https://www.jstage.jst.go.jp/article/dmj/{volume}/{issue}/{article_id}/_pdf
```

Or with the full DOI-based URL. The `_pdf` suffix on the article URL typically returns the PDF.

## Download Approach

**Method 1: Direct navigation to PDF URL**
```javascript
window._jsDl = 'pending';
fetch('https://www.jstage.jst.go.jp/article/dmj/{vol}/{issue}/{id}/_pdf/-char/en')
  .then(r => r.blob())
  .then(blob => {
    window._jsDl = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'DMJ_article.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._jsDl = 'err:' + e.message; });
'fetch started'
```

**Method 2: Navigate and click**
1. Navigate to the article page
2. Find the "PDF" link (usually prominent on J-STAGE article pages)
3. Click to download

## Finding Articles

```javascript
Promise.all([
  fetch('https://api.crossref.org/journals/0287-4547/works?rows=3&sort=published&order=desc').then(r=>r.json()),
  fetch('https://api.crossref.org/journals/1883-1958/works?rows=3&sort=published&order=desc').then(r=>r.json())
]).then(results => {
  window._dmjArticles = JSON.stringify(results[0].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
  window._jprArticles = JSON.stringify(results[1].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
});
```

## Quirks & Notes
- J-STAGE is generally very accessible with minimal barriers — open access, no authentication needed
- The `/_pdf/-char/en` suffix on article URLs gives the English PDF directly — **confirmed working**
- Successfully downloaded DMJ article: 3.8MB PDF via fetch+blob with `/_pdf/-char/en` pattern
- No `{credentials: 'include'}` needed since articles are open access
- J-STAGE has good CrossRef integration so DOIs resolve reliably
- DMJ and JPR are published by Japanese dental societies (Japanese Society for Dental Materials and Devices, and Japan Prosthodontic Society respectively)
- Article URL pattern from CrossRef: `https://www.jstage.jst.go.jp/article/dmj/{vol}/{issue}/45_{article_id}/_article`
- PDF URL pattern: replace `/_article` with `/_pdf/-char/en`

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/korean-oa.md
═══════════════════════════════════════════════════════════════

# Korean Open Access Journals (KoreaMed Synapse)

## Journals
- Journal of Advanced Prosthodontics — JAP (ISSN 2005-7806)
- Restorative Dentistry & Endodontics — RDE (ISSN 2234-7658)
- Journal of Periodontal & Implant Science — JPIS (ISSN 2093-2278)

## Authentication: None Required

All three Korean journals are fully open access, hosted on KoreaMed Synapse (`synapse.koreamed.org`) and/or their own journal sites. No institutional login needed.

## Platform URLs
- JAP: `https://jap.or.kr/` or `https://synapse.koreamed.org/journals/137`
- RDE: `https://www.rde.ac/` or `https://synapse.koreamed.org/journals/203`
- JPIS: `https://www.jpis.org/` or `https://synapse.koreamed.org/journals/166`

## PDF URL Patterns

Korean journals typically host PDFs directly. The URL pattern varies by journal:

**JAP:**
```
https://jap.or.kr/upload/pdf/{filename}.pdf
```

**RDE:**
```
https://www.rde.ac/upload/pdf/{filename}.pdf
```

**JPIS:**
```
https://www.jpis.org/upload/pdf/{filename}.pdf
```

The exact PDF path can be found by navigating to the article page and locating the PDF download link.

## Download Approach

Since these are open access, the simplest approach is:

1. Navigate to the article page using Chrome MCP
2. Find the "PDF" or "Download PDF" button
3. Click it to trigger a direct download

Or use fetch+blob if you have the direct PDF URL:

```javascript
window._kDl1 = 'pending';
fetch('https://jap.or.kr/upload/pdf/ARTICLE_FILE.pdf')
  .then(r => r.blob())
  .then(blob => {
    window._kDl1 = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'JAP_article.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._kDl1 = 'err:' + e.message; });
'fetch started'
```

## Finding Articles

```javascript
Promise.all([
  fetch('https://api.crossref.org/journals/2005-7806/works?rows=3&sort=published&order=desc').then(r=>r.json()),
  fetch('https://api.crossref.org/journals/2234-7658/works?rows=3&sort=published&order=desc').then(r=>r.json()),
  fetch('https://api.crossref.org/journals/2093-2278/works?rows=3&sort=published&order=desc').then(r=>r.json())
]).then(results => {
  window._japArticles = JSON.stringify(results[0].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
  window._rdeArticles = JSON.stringify(results[1].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
  window._jpisArticles = JSON.stringify(results[2].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
});
```

## Quirks & Notes
- All three journals are open access — no authentication barriers
- KoreaMed Synapse is the aggregator platform, but articles also available on individual journal sites
- PDF download buttons on article pages are straightforward
- JPIS had 1 article downloaded in previous testing session; JAP and RDE are similar platforms
- Some articles may also be available on PubMed Central (PMC) as an alternative source

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/quintessence.md
═══════════════════════════════════════════════════════════════

# Quintessence Publishing

## Journals
- International Journal of Prosthodontics (IJP) — ISSN 0893-2174
- International Journal of Oral & Maxillofacial Implants (IJOMI) — ISSN 0882-2786
- International Journal of Periodontics & Restorative Dentistry (IJPRD) — ISSN 0198-7569

## Authentication: KCL EZproxy (OCLC)

Quintessence uses the standard EZproxy domain rewriting pattern. This is the simplest authentication method.

### EZproxy URL Pattern
```
https://www-quintessence--publishing-com.kcl.idm.oclc.org/
```

The pattern converts `www.quintessence-publishing.com` to `www-quintessence--publishing-com.kcl.idm.oclc.org` (dots become hyphens, hyphens become double-hyphens).

### Authentication Flow
1. Navigate to the EZproxy URL
2. If not already authenticated, the user will be redirected to KCL's login page
3. After login, they are redirected back to the Quintessence site with proxy authentication active
4. The proxy session persists for subsequent requests

### Finding Articles
Navigate to the journal page on the proxied site:
```
https://www-quintessence--publishing-com.kcl.idm.oclc.org/journal/ijp
https://www-quintessence--publishing-com.kcl.idm.oclc.org/journal/ijomi
https://www-quintessence--publishing-com.kcl.idm.oclc.org/journal/ijprd
```

Or use CrossRef API to find DOIs first (see main SKILL.md).

### PDF Download

Once on a proxied article page, the PDF link is typically available as a direct download button. Use the Chrome MCP to:

1. Navigate to the article page via EZproxy
2. Find and click the PDF download link, OR
3. Use the fetch+blob pattern with the proxied PDF URL:

```javascript
window._dlResult = 'pending';
fetch('https://www-quintessence--publishing-com.kcl.idm.oclc.org/[PDF_PATH]', {credentials: 'include'})
  .then(r => r.blob())
  .then(blob => {
    window._dlResult = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'IJP_article_title.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._dlResult = 'err:' + e.message; });
'fetch started'
```

### Quirks & Notes
- EZproxy is the most reliable method for Quintessence — it consistently works
- The proxied site looks and behaves identically to the regular site
- PDF URLs on Quintessence are straightforward direct links (no signed URLs or redirects)
- IJP was the first journal tested and confirmed working with 20 PDFs downloaded successfully

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/springer-oa.md
═══════════════════════════════════════════════════════════════

# Springer Nature (Open Access)

## Journals
- International Journal of Implant Dentistry — IJID (ISSN 2198-4034)

## Authentication: None Required

IJID is a fully open access journal published by Springer Nature. No institutional login or proxy is needed.

## PDF URL Pattern

```
https://link.springer.com/content/pdf/{DOI}.pdf
```

Example:
```
https://link.springer.com/content/pdf/10.1186/s40729-026-00668-4.pdf
```

## Download Code (Proven Working)

```javascript
window._sDl1 = 'pending';
fetch('https://link.springer.com/content/pdf/10.1186/s40729-026-00668-4.pdf')
  .then(r => r.blob())
  .then(blob => {
    window._sDl1 = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'IJID_article_title.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._sDl1 = 'err:' + e.message; });
'fetch started'
```

## Batch Download

For multiple articles, run sequential fetches with different global variables:

```javascript
// Article 1
window._sDl1 = 'pending';
fetch('https://link.springer.com/content/pdf/10.1186/{DOI1}.pdf')
  .then(r => r.blob())
  .then(blob => {
    window._sDl1 = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'IJID_article1.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._sDl1 = 'err:' + e.message; });

// Then article 2 with window._sDl2, etc.
```

## Finding Articles

```javascript
fetch('https://api.crossref.org/journals/2198-4034/works?rows=3&sort=published&order=desc')
  .then(r => r.json())
  .then(data => {
    window._ijidArticles = JSON.stringify(
      data.message.items.map(i => ({
        title: (i.title || [''])[0].substring(0, 80),
        doi: i.DOI
      }))
    );
  });
```

## Quirks & Notes
- No authentication needed — simplest publisher to download from
- Note: `{credentials: 'include'}` is not required but doesn't hurt
- Some DOIs may return 0-byte blobs — if this happens, try a different article
  - Example: `s40729-026-00672-8` returned 0 bytes; `s40729-026-00670-w` worked fine (2.5MB)
- Successfully tested: 3 articles downloaded, typical size 1.5–3MB
- DOI format: `10.1186/s40729-0XX-XXXXX-X`

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/wiley.md
═══════════════════════════════════════════════════════════════

# Wiley Online Library

## Journals
- Journal of Prosthodontics (ISSN 1059-941X / 1532-849X)
- Clinical Implant Dentistry and Related Research — CIDR (ISSN 1523-0899 / 1708-8208)
- Clinical Oral Implants Research — COIR (ISSN 0905-7161 / 1600-0501)
- Journal of Esthetic and Restorative Dentistry — JERD (ISSN 1496-4155 / 1708-8240)
- Journal of Oral Rehabilitation (ISSN 0305-182X)

## Authentication: Shibboleth Institutional Login

Wiley does NOT work with KCL's EZproxy domain rewriting (returns 404). Instead, use Wiley's built-in institutional login which triggers Shibboleth/SAML authentication.

### EZproxy Does NOT Work
```
# THIS FAILS — do not use:
https://onlinelibrary-wiley-com.kcl.idm.oclc.org/  → 404 error
```

### Authentication Flow
1. Navigate to `https://onlinelibrary.wiley.com/`
2. Click "Login / Register" (top right)
3. Click "Institutional Login"
4. Search for "King's College London" in the institution search
5. Select KCL from the results
6. The browser redirects to KCL's Shibboleth IdP login page
7. User enters their KCL credentials (if not already logged in)
8. Redirect back to Wiley with an authenticated session
9. The session persists — articles now show "Access" badges

If the user has recently authenticated with KCL Shibboleth for another publisher (e.g., Elsevier), the Shibboleth session may still be active and steps 6-7 happen automatically.

### PDF URL Pattern

Wiley uses a `pdfdirect` endpoint that returns the actual PDF binary:

```
https://onlinelibrary.wiley.com/doi/pdfdirect/{DOI}?download=true
```

Example:
```
https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/jopr.70007?download=true
```

**Important**: The `/doi/epdf/{DOI}` endpoint is the browser-based PDF viewer (redirects to abstract if not authenticated). Always use `/doi/pdfdirect/` for programmatic download.

### Download Code (Proven Working)

```javascript
window._dlResult = 'pending';
fetch('https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/jopr.70007?download=true', {credentials: 'include'})
  .then(r => {
    window._dlResult = 'status:' + r.status + ' type:' + r.headers.get('content-type');
    return r.blob();
  })
  .then(blob => {
    window._dlResult = 'size:' + blob.size;
    var blobUrl = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = blobUrl;
    link.download = 'J_Prosthodontics_article.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(blobUrl);
  })
  .catch(e => { window._dlResult = 'err:' + e.message; });
'fetch started'
```

Then verify: `window._dlResult` → should show `size:` with a number > 100000.

### Batch Download Pattern

For downloading multiple Wiley articles in sequence:

```javascript
// Download article 1
window._wd1 = 'pending';
fetch('https://onlinelibrary.wiley.com/doi/pdfdirect/{DOI1}?download=true', {credentials: 'include'})
  .then(r => r.blob())
  .then(blob => {
    window._wd1 = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'Article1.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._wd1 = 'err:' + e.message; });
```

Repeat with `_wd2`, `_wd3`, etc. Space requests a few seconds apart.

### DOI Patterns for Wiley Journals
- J Prosthodontics: `10.1111/jopr.XXXXX`
- CIDR: `10.1111/cid.XXXXX`
- COIR: `10.1111/clr.XXXXX`
- JERD: `10.1111/jerd.XXXXX`
- J Oral Rehab: `10.1111/joor.XXXXX`

### Quirks & Notes
- `pdfdirect` with `?download=true` is the key — this returns raw PDF bytes
- The `epdf` endpoint is an HTML viewer, not a direct PDF — avoid it for programmatic download
- Content-type should be `application/pdf` — if you get `text/html`, authentication failed
- Wiley was successfully tested with J Prosthodontics (3 articles downloaded, ~1-2MB each)
- All 5 Wiley journals use the same platform and authentication, so the same workflow applies to all

═══════════════════════════════════════════════════════════════
# FILE: skills/journal-article-downloader/references/wolters-kluwer.md
═══════════════════════════════════════════════════════════════

# Wolters Kluwer (LWW / Medknow)

## Journals
- Journal of Indian Prosthodontic Society — JIPS (ISSN 0972-4052) — hosted on Medknow platform
- Implant Dentistry (ISSN 1056-6163) — hosted on LWW platform

## Platform URLs
- JIPS: `https://journals.lww.com/jips/` (Medknow/LWW)
- Implant Dentistry: `https://journals.lww.com/implantdent/`

Both journals are on the LWW (Lippincott Williams & Wilkins) platform, which is Wolters Kluwer's medical journal hosting.

## Authentication

### JIPS (Medknow)
JIPS is largely open access through Medknow. Many articles have free full-text access without authentication. For any paywalled content, try the EZproxy DOI resolver:

```
https://doi-org.kcl.idm.oclc.org/{DOI}
```

### Implant Dentistry (LWW)
Implant Dentistry is subscription-based. Use either:

1. **EZproxy DOI resolver** (try first):
   ```
   https://doi-org.kcl.idm.oclc.org/{DOI}
   ```

2. **LWW Institutional Login**:
   - Navigate to `https://journals.lww.com/`
   - Click "Log In" → "Institutional Login"
   - Search for "King's College London"
   - Complete Shibboleth authentication

## Article URL Pattern (from CrossRef)

LWW uses DOI-based URLs:
```
https://journals.lww.com/10.4103/jips.jips_XXX_XX
```

Example DOIs from CrossRef:
- JIPS: `10.4103/jips.jips_563_24`, `10.4103/jips.jips_530_24`

## PDF Download (Confirmed Working)

LWW uses a `downloadpdf.aspx` endpoint. The workflow is click-based:

### Method 1: Click-Based Download (Recommended)
1. Navigate to the article page (e.g., `https://journals.lww.com/jips/fulltext/2026/01000/article_slug.10.aspx`)
2. Click the "Download" button in the left sidebar
3. A dropdown appears with "PDF" and "EPUB" options
4. Click "PDF" — opens a new tab at `/_layouts/15/oaks.journals/downloadpdf.aspx?...`
5. The download starts automatically within seconds

### LWW PDF URL Pattern (Confirmed)
```
https://journals.lww.com/{journal}/_layouts/15/oaks.journals/downloadpdf.aspx?trckng_src_pg=ArticleViewer&an={article_number}
```

Example article number: `00660762-202601000-00010`

The article number can be found in the URL that opens when you click the PDF button. The format is `{journal_id}-{volume_issue}-{article_seq}`.

### Method 2: Programmatic Fetch (if URL known)
```javascript
window._wkDl = 'pending';
fetch('https://journals.lww.com/jips/_layouts/15/oaks.journals/downloadpdf.aspx?trckng_src_pg=ArticleViewer&an=00660762-202601000-00010', {credentials: 'include'})
  .then(r => r.blob())
  .then(blob => {
    window._wkDl = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'JIPS_article.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._wkDl = 'err:' + e.message; });
'fetch started'
```

Note: The simple `/pdf/` URL pattern (replacing `/fulltext/` with `/pdf/`) does NOT work — it returns a 765-byte error redirect.

## Finding Articles

```javascript
Promise.all([
  fetch('https://api.crossref.org/journals/0972-4052/works?rows=3&sort=published&order=desc').then(r=>r.json()),
  fetch('https://api.crossref.org/journals/1056-6163/works?rows=3&sort=published&order=desc').then(r=>r.json())
]).then(results => {
  window._jipsArticles = JSON.stringify(results[0].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
  window._idArticles = JSON.stringify(results[1].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
});
```

## Quirks & Notes
- JIPS (via Medknow) is mostly open access — authentication is rarely needed
- Implant Dentistry may require institutional access for recent articles
- The simple `/pdf/` URL pattern does NOT work on LWW (returns 765-byte error)
- Must use the `downloadpdf.aspx` endpoint or the click-based Download → PDF workflow
- The article number format for the download URL is not easily predictable — use click-based approach
- **Successfully tested**: JIPS article downloaded via Download → PDF click workflow (auto-download page confirmed)
- The EZproxy DOI resolver approach is recommended as the first attempt for Implant Dentistry

═══════════════════════════════════════════════════════════════
# FILE: skills/scihub-downloader/SKILL.md
═══════════════════════════════════════════════════════════════

---
name: scihub-downloader
description: "Download academic papers from Sci-Hub using browser automation. Use this skill when the user wants to bulk download papers via Sci-Hub, fetch paywalled articles using Sci-Hub, or acquire PDFs by DOI through Sci-Hub. Triggers: 'sci-hub', 'scihub', 'download papers from sci-hub', 'get papers from sci-hub', 'fetch from scihub'."
version: 1.0.0
author: samrosehill
tags: [papers, download, sci-hub, academic, browser-automation]
allowed-tools: Read, Write, Bash, Glob, Grep, mcp__Claude_in_Chrome__tabs_context_mcp, mcp__Claude_in_Chrome__tabs_create_mcp, mcp__Claude_in_Chrome__tabs_close_mcp, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__computer, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__javascript_tool, mcp__Claude_in_Chrome__form_input
---

# Sci-Hub Paper Downloader

Download academic papers from Sci-Hub by DOI using Chrome browser automation.

## Prerequisites

- Chrome browser open with Claude in Chrome extension connected
- A JSON file containing papers with DOI fields (e.g., `papers-to-acquire.json`)
- A target download folder for PDFs

## Input

The skill reads from a JSON array of paper objects. Each object should have at minimum:
- `doi` — the DOI string (e.g., `"10.1186/s40359-020-00423-3"`)
- `pmid` — PubMed ID (used for tracking)
- `first_author` — for filename generation
- `year` — for filename generation
- `title` — for filename generation

Default input file: `/Users/samrosehill/Desktop/Dental Personality Research/papers-to-acquire.json`
Default download target: `/Users/samrosehill/Desktop/Dental Personality Research/papers/downloads/`

## Workflow

For each paper with a DOI that has not already been downloaded:

### Step 1: Navigate to Sci-Hub
Navigate the browser tab to `https://sci-hub.st` (primary mirror).
Fallback mirrors: `https://sci-hub.ru`, `https://sci-hub.ren`

### Step 2: Enter DOI
- Find the search/input box on the Sci-Hub homepage
- Clear any existing text
- Type/paste the DOI into the search box
- Press Enter or click the search/open button

### Step 3: Check Result
- Wait 2-3 seconds for the page to load
- Take a screenshot to assess the result
- Check the page for one of three outcomes:
  1. **Paper found**: PDF is displayed or a download link/button is visible
  2. **Not found**: Page says "article not found" or is empty
  3. **Captcha**: Page shows a captcha challenge

### Step 4: Download (if found)
Use JavaScript to extract the PDF URL from the page. Sci-Hub stores it in a meta tag:

```javascript
// Extract PDF URL from meta tag
var meta = document.querySelector('meta[name="citation_pdf_url"]');
var pdfPath = meta ? meta.getAttribute('content') : null;
pdfPath;
```

If the PDF path is found, construct the full URL (prepend `https://sci-hub.st` if path is relative) and trigger a download:

```javascript
// Download the PDF via blob fetch
var pdfUrl = 'https://sci-hub.st' + pdfPath;
window._dlStatus = 'fetching';
fetch(pdfUrl)
  .then(function(r) { return r.blob(); })
  .then(function(blob) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'FILENAME.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    window._dlStatus = 'done:' + blob.size;
  })
  .catch(function(e) { window._dlStatus = 'error:' + e.message; });
'started';
```

Then check `window._dlStatus` after a few seconds to confirm download completed.

### Step 5: Handle failures
- **Not found**: Log the DOI as unavailable on Sci-Hub and move to next paper
- **Captcha**: If a captcha appears, take a screenshot. The user may need to solve it manually. After solving, retry the current DOI.
- **Error**: Log and move on

### Step 6: Return to homepage and repeat
Navigate back to `https://sci-hub.st` and process the next DOI.

## File Naming Convention

Downloaded files should be named: `{Surname}_{Year}_{FirstFourTitleWords}.pdf`

Where:
- `Surname` = last name of first author (alphanumeric only)
- `Year` = 4-digit publication year
- `FirstFourTitleWords` = first 4 words of title (alphanumeric, underscored)

Example: `Lewis_2020_The_big_five_personality.pdf`

## After Download

Once a PDF lands in `~/Downloads/`, move it to the target download folder with the correct filename.

## Tracking

After processing, report:
- Total papers attempted
- Successfully downloaded
- Not found on Sci-Hub
- Captcha blocks
- Other errors

## Rate Limiting

Use natural browser interaction pace. No need for artificial delays — the browser page load time provides natural spacing. If captchas start appearing frequently, slow down and consider switching mirrors.

## Mirror Rotation

If one mirror becomes unresponsive or starts blocking:
1. `https://sci-hub.st` (primary)
2. `https://sci-hub.ru` (fallback 1)
3. `https://sci-hub.ren` (fallback 2)
