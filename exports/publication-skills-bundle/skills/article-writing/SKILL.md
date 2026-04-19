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
