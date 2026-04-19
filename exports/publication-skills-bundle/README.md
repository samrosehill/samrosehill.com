# samrosehill.com Publication Skills Bundle

Complete export of the Claude Code skills used in the dental review publication workflow at samrosehill.com. Intended for porting the workflow to Codex or any other agent harness.

## What's in here

```
publication-skills-bundle/
├── README.md                              ← this file
├── publication-workflow-improvements.md   ← durable decisions and next improvements
├── ALL-SKILLS-CONCATENATED.md             ← every skill in one file (easiest to paste)
└── skills/
    ├── publish-pipeline/SKILL.md          ← end-to-end orchestrator
    ├── paper-triage/SKILL.md              ← Stage 0: paper selection + tracker CSV
    ├── article-writing/SKILL.md           ← Stage 1: write the 400–600 word review
    ├── article-draft-check/SKILL.md       ← Stage 2: 8-dimension quality gate
    ├── thumbnail-generator/SKILL.md       ← Stage 3: branded PNG compositor
    ├── publish-article/SKILL.md           ← Stage 4: frontmatter + git push
    ├── annabel-crabb-voice/SKILL.md       ← voice specification (referenced by article-writing)
    ├── journal-article-downloader/
    │   ├── SKILL.md                       ← KCL institutional download workflow
    │   └── references/
    │       ├── aaid.md                    ← per-publisher auth + download patterns
    │       ├── elsevier.md
    │       ├── jstage.md
    │       ├── korean-oa.md
    │       ├── quintessence.md
    │       ├── springer-oa.md
    │       ├── wiley.md
    │       └── wolters-kluwer.md
    └── scihub-downloader/SKILL.md         ← legacy fallback DOI fetcher; do not use in the local publication path
```

## Pipeline flow

```
Stage 0  paper-triage          scan PDFs, structured triage brief, user selects
Stage 1  article-writing       write Crabb-voice 400–600 word review
Stage 2  article-draft-check   QC gate (structure, voice, factual, frontmatter)
Stage 3  thumbnail-generator   python3 scripts/generate-thumbnail.py [slug]
Stage 4  publish-article       git add + commit + push origin main
Stage 5  Substack cross-post via authenticated browser/API flow
Stage 6  paper-tracker.csv update + substackUrl frontmatter writeback
Stage 7  live verification (website + Substack)
```

`publish-pipeline/SKILL.md` orchestrates all of the above. It reads the sub-skill SKILL.md files at runtime and follows their instructions verbatim — no logic is duplicated.

## Hard-coded paths

Every skill uses absolute macOS paths rooted at:

```
PROJECT_ROOT = /Users/samrosehill/Desktop/samrosehill.com
SKILLS_ROOT  = /Users/samrosehill/.claude/skills
```

Before running this bundle under Codex on another machine, search-and-replace these two prefixes, plus the Substack automation specifics if those aren't needed.

## External dependencies the skills assume

- **Python 3** with `PyMuPDF`, `Pillow`, `pypdf`
- **Astro** static site at `PROJECT_ROOT` with content collection at `src/content/reviews/`
- **Scripts** at `PROJECT_ROOT/scripts/`:
  - `generate-thumbnail.py` — called by thumbnail-generator
  - `extract-pdf-text.py` — called by publish-pipeline before launching article subagents
  - `substack-publisher.py` — called by Stage 5
  - `substack-formatter.py` — HTML transform for Substack
- **Tracker CSV** at `PROJECT_ROOT/2MP Project/paper-tracker.csv`
- **Git remote** pushable via SSH to trigger Vercel auto-deploy
- **Chrome MCP** for Stage 5 Substack cross-post. In Claude this may be the Chrome/javascript tool; in Codex use Chrome DevTools MCP `evaluate_script`.
- **Context-isolation subagents** for Stages 1–3 and Stage 5 when the harness supports them and the user has authorised delegation. If porting to a harness without subagents, run the same templates inline one article at a time.

## Voice spec

`article-writing/SKILL.md` contains a compact voice section, but the full Annabel Crabb voice specification — including the deep-dive technique catalogue — lives in `annabel-crabb-voice/SKILL.md`. The article-writing skill references it implicitly. Use both together when writing articles.

Current decision: preserve this voice as a core product requirement. Quality improvements should strengthen triage, evidence control, claim checking, and publishing reliability without flattening the prose into generic medical SEO copy.

## Porting notes for Codex

1. The skills are plain Markdown — no `.claude` metadata, no tool bindings. Codex can read them as system prompts, reference docs, or chain-of-thought scaffolds.
2. Sub-skill invocation pattern: `publish-pipeline` tells the agent to literally **read** another `SKILL.md` at runtime. Preserve that pattern — it keeps each stage's spec authoritative and prevents drift.
3. User checkpoints are critical and explicit. Don't remove them during porting unless the user asks for fully autonomous mode.
4. The `article-draft-check` skill is a hard quality gate with 8 dimensions and must fail closed — an agent that skips it will ship inaccurate clinical claims.
5. Do not use the Sci-Hub skill for the local publication workflow when papers are already present in the project root or `2MP Project/`.
