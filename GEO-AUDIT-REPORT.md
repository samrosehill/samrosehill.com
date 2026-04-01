# GEO Audit Report: samrosehill.com

**Audit Date:** 1 April 2026
**URL:** https://samrosehill.com
**Business Type:** Publisher (Clinical Dental Review Archive)
**Pages Analyzed:** 21

---

## Executive Summary

**Overall GEO Score: 46/100 (Poor) --> 59/100 (Fair) after fixes deployed today**

samrosehill.com has genuinely strong content fundamentals -- expert-authored clinical reviews with high statistical density, consistent article structure, and excellent source attribution. However, prior to today's fixes the site was nearly invisible to AI systems due to missing foundational infrastructure: no robots.txt, no sitemap, no llms.txt, no Article schema, no OG tags, and no canonical URLs. Today's deployment addresses the critical technical and schema gaps, lifting the score from Poor to Fair, with a clear path to Good (75+) through content-level and brand authority improvements.

### Score Breakdown (Pre-Fix / Post-Fix)

| Category | Pre-Fix | Post-Fix | Weight | Weighted (Post) |
|---|---|---|---|---|
| AI Citability | 62/100 | 62/100 | 25% | 15.5 |
| Brand Authority | 38/100 | 38/100 | 20% | 7.6 |
| Content E-E-A-T | 74/100 | 76/100 | 20% | 15.2 |
| Technical GEO | 48/100 | 78/100 | 15% | 11.7 |
| Schema & Structured Data | 18/100 | 68/100 | 10% | 6.8 |
| Platform Optimization | 25/100 | 25/100 | 10% | 2.5 |
| **Overall GEO Score** | **~46/100** | | | **~59/100** |

---

## What Was Fixed Today

### Critical Infrastructure (deployed to production)

1. **robots.txt** -- Created with explicit Allow directives for GPTBot, ClaudeBot, PerplexityBot, Google-Extended, and all major AI crawlers
2. **sitemap-index.xml** -- Added @astrojs/sitemap integration; auto-generates at build time
3. **llms.txt** -- Auto-generated from content collection at build time; lists all 17 review articles with titles and URLs; updates automatically when new articles are published
4. **Article schema (JSON-LD)** -- Added to every review page with: headline, description, datePublished, author (Person), publisher, articleSection, keywords, about (ScholarlyArticle linking to source paper), and speakable specification
5. **BreadcrumbList schema** -- Added to every review page (Home > Journal > Article Title)
6. **WebSite schema** -- Added to homepage
7. **CollectionPage schema** -- Added to /reviews/ archive
8. **ProfilePage schema** -- Added to /about/ page
9. **Enhanced Person schema** -- Added knowsAbout (7 expertise areas), university URLs, honorificPrefix, givenName, familyName, practice URL
10. **Open Graph meta tags** -- og:type, og:title, og:description, og:url, og:site_name, og:image on all pages
11. **Twitter Card meta tags** -- summary_large_image with title, description, image on all pages
12. **Canonical URLs** -- Added to all pages via Astro.url
13. **Heading hierarchy fix** -- Converted H3 to H2 in all 17 review article markdown files (was H1 > H3, now correct H1 > H2)
14. **Head slot architecture** -- Added named `<slot name="head" />` to Base.astro for page-specific schema injection

---

## Remaining Issues

### High Priority (Fix Within 1 Week)

1. **Expand sameAs links on Person schema** -- Currently only 2 links (LinkedIn, practice profile). AI entity resolution needs 5+ links. Create and link:
   - ORCID profile
   - Google Scholar profile
   - ResearchGate profile (if applicable)

2. **Add author headshot to Person schema** -- `image` property is missing. Add a professional photo to `/public/images/` and reference it in the schema.

3. **Add cross-links between related reviews** -- Zero internal cross-linking between articles. The digital surgery, robot-assisted surgery, and surgical guide articles share obvious topical overlap. Add a "Related Reviews" component at the bottom of each article.

4. **Add explicit question framing before answer blocks** -- Articles answer implicit clinical questions but never state them. Adding a visible "Clinical Question" element before Key Findings would dramatically improve AI citation likelihood.

### Medium Priority (Fix Within 1 Month)

5. **Build tag archive pages** -- Tags exist in frontmatter but don't generate browsable pages. Creating /reviews/tags/[tag]/ pages builds topical cluster structure.

6. **Add privacy policy and clinical disclaimer** -- Missing legal pages are a trust gap for YMYL health content.

7. **Improve self-containment of Key Findings bullets** -- Add brief parenthetical definitions when using abbreviations within individual bullets.

8. **Add textbook citation details** -- The co-authored textbook is mentioned without title, ISBN, or publisher. Make it verifiable.

9. **Add images/diagrams to articles** -- Zero images in article body content.

### Low Priority (Optimize When Possible)

10. **Build external brand presence** -- YouTube channel, Reddit engagement in dental subreddits, contribute to Wikipedia dental articles.

11. **Add dateModified tracking** -- Currently dateModified = datePublished for all articles.

12. **Standardize data presentation as tables** -- Some articles use inline prose for numerical comparisons where tables would be more extractable.

---

## Category Deep Dives

### AI Citability (62/100)

**Strengths:** Consistent article structure (Data Anchor, Key Findings, Clinical Bottom Line) creates predictable, extractable content blocks. Statistical density is high (78/100) -- articles consistently include specific measurements with p-values. The clinicalRelevance frontmatter field is a hidden gem containing highly citable 2-3 sentence summaries.

**Weaknesses:** Opening narrative paragraphs dilute signal-to-noise ratio. No explicit question-answer framing. Self-containment is weak (58/100) -- many passages assume context from earlier sections.

### Brand Authority (38/100)

**Strengths:** Strong personal credentials (PFA Fellow, ICD Fellow, MClinDent KCL). Good Australian directory coverage (Whitecoat 4.66 stars, Birdeye 5.0 stars with 107 reviews, ThreeBestRated selection). DentEvents speaker profile. LinkedIn with 500+ connections.

**Weaknesses:** Significant "credentials-to-visibility gap" — impressive qualifications are almost entirely self-reported with minimal independent digital corroboration. No Wikipedia entity, no ORCID, no Google Scholar, no PubMed-indexed publications, no ResearchGate. Zero Reddit mentions. The Dental Graduate Handbook (co-authored, distributed to all Australian dental graduates) lacks discoverable ISBN/publisher web presence. ethical.dental does not link to samrosehill.com. AI models encountering "Dr. Samuel Rosehill" can identify a Coffs Harbour dentist but cannot confidently cite as a prosthodontics authority.

### Content E-E-A-T (74/100)

**Strengths:** Exceptional expertise signals (21/25) -- MClinDent with Distinction from KCL is top-tier. Trustworthiness is strong (20/25) -- DOI-linked citations and limitations disclosure on every article. Authentically human voice with consistent clinical perspective.

**Weaknesses:** Authoritativeness held back by limited external validation (15/25). No ORCID or Google Scholar. Missing privacy policy and editorial disclosure.

### Technical GEO (~78/100 post-fix)

**Strengths (after today's fixes):** robots.txt welcomes all AI crawlers. Sitemap auto-generates. llms.txt auto-generates. Canonical URLs on all pages. OG and Twitter meta tags. Astro SSG delivers static HTML (no JS rendering issues for AI crawlers). HTTPS confirmed.

**Remaining gaps:** No structured error pages. No performance optimization auditing done.

### Schema & Structured Data (~68/100 post-fix)

**Strengths (after today's fixes):** Person schema with knowsAbout and university URLs. Article schema with speakable, ScholarlyArticle citation linking, and keywords on all 17 review pages. BreadcrumbList on reviews. WebSite, CollectionPage, ProfilePage schemas.

**Remaining gaps:** sameAs has only 2 links (needs 5+). No image property on Person. No hasCredential property.

### Platform Optimization (~25/100)

**Assessment:** Minimal presence on platforms AI models train on and cite. No YouTube, no Reddit engagement, no Wikipedia entity. LinkedIn profile exists but is not heavily active.

---

## Quick Wins (Implement This Week)

1. Create ORCID profile and add to sameAs array in Base.astro Person schema
2. Add professional headshot to Person schema (image property)
3. Link Google Scholar profile in sameAs
4. Add 2-3 "Related Reviews" links at bottom of each article
5. Add clinical disclaimer page (/disclaimer)

## 30-Day Action Plan

### Week 1: Entity Resolution
- [ ] Create ORCID profile
- [ ] Create/link Google Scholar profile
- [ ] Add headshot to site and Person schema
- [ ] Expand sameAs to 5+ links
- [ ] Add textbook ISBN/publisher to About page

### Week 2: Content Structure
- [ ] Add "Related Reviews" component to article template
- [ ] Add explicit clinical question framing to 5 highest-traffic articles
- [ ] Convert inline numerical comparisons to tables where appropriate

### Week 3: Trust & Legal
- [ ] Create privacy policy page
- [ ] Create clinical disclaimer page
- [ ] Add editorial methodology statement to About page
- [ ] Add conflict of interest disclosure

### Week 4: Topical Authority
- [ ] Build tag archive pages (/reviews/tags/[tag]/)
- [ ] Identify and fill content gaps in prosthodontic topic coverage
- [ ] Begin external presence building (Reddit, YouTube)

---

## Appendix: Files Modified

| File | Change |
|---|---|
| `public/robots.txt` | New -- AI crawler directives |
| `astro.config.mjs` | Added @astrojs/sitemap integration |
| `src/pages/llms.txt.ts` | New -- auto-generated llms.txt from content collection |
| `src/layouts/Base.astro` | Enhanced Person schema, added OG/Twitter/canonical, head slot |
| `src/pages/reviews/[id].astro` | Added Article + BreadcrumbList schema, OG image |
| `src/pages/index.astro` | Added WebSite schema |
| `src/pages/reviews/index.astro` | Added CollectionPage schema |
| `src/pages/about.astro` | Added ProfilePage schema |
| `src/content/reviews/*.md` (x17) | Fixed H3 to H2 heading hierarchy |
