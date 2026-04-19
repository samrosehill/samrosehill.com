# Publication Workflow Improvements

This note preserves workflow decisions that should survive outside the chat thread.

## Keep the Voice

The current Annabel Crabb-adapted review voice is a product differentiator for dental research summaries. Preserve it. Improve content quality by making the inputs, evidence checks, and publication mechanics stronger, not by flattening the prose into generic medical SEO copy.

## Content Quality Upgrades

- Triage summaries must be more useful than abstract paraphrases: include study design, sample/materials, comparator, follow-up, main numeric finding, limitation, publishing angle, and a do-not-overclaim warning.
- Use priority scores during triage: evidence strength, clinical relevance, novelty/angle, reader usefulness, and overclaiming risk.
- Prefer manuscript metadata over path metadata. Folder names are useful fallbacks, but the paper text wins when journal/title/year/DOI conflict with the path.
- Create an Evidence Pack before drafting: citation, study frame, 3-5 must-use findings, limitations, and the strongest claim the article must not make.
- Draft review must preserve the established voice while checking every numeric, causal, and study-design claim against the source.
- Treat case reports, retrospective studies, and in-vitro papers with explicit caveats. Do not let a lively sentence become a stronger claim than the paper can carry.
- Add duplicate detection beyond filename: DOI, normalised title, and first-author/year/title combinations.

## Pipeline Reliability Upgrades

- Use `/journal/[slug]` and `/journal` for live verification. `/reviews` is a content directory, not the public route.
- Run a prepublish check before commit when available; otherwise check the same items inline: Astro schema/build compatibility, thumbnail, `pubDate`, DOI/reference line, no H1, body word count, source PDF path, and Substack subtitle length risk.
- Do not future-date reviews unless scheduling is intentional. Future `pubDate` values can make a newly published article look missing or out of order.
- Substack publishing should return `substack_url`, `draft_id`, `published`, `auth_failed`, and any API error. Fail fast if draft creation fails.
- Prefer the live-site Substack method: fetch the deployed article, convert the rendered `.prose` DOM to Substack's editor payload, publish from the authenticated browser session, then capture the final URL.
- After Substack publication, write `substackUrl` into the article frontmatter, commit, and push so the live CTA links to the Substack post.
- Update `paper-tracker.csv` with published status, date, article slug, and Substack URL in notes.
- Use subagents only when the harness supports them and the user has authorised delegation. Otherwise process one article at a time inline, using extracted source text files to keep context manageable.
- Treat the Sci-Hub skill as legacy and out of scope for the local publication pipeline when papers are already present locally.
