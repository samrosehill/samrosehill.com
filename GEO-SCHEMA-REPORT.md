# GEO Schema & Structured Data Audit Report

**Site:** samrosehill.com
**Audit Date:** 1 April 2026
**Framework:** Astro (static SSG) deployed on Vercel
**Pages Audited:** 4

---

## Overall Score: 78 / 100

| Criterion | Max | Score | Status |
|---|---|---|---|
| Organization/Person schema completeness | 15 | 13 | GOOD |
| sameAs links (5+ platforms) | 15 | 6 | NEEDS WORK |
| Article schema with author details | 10 | 9 | GOOD |
| Business-type-specific schemas | 10 | 8 | GOOD |
| WebSite + SearchAction | 5 | 3 | NEEDS WORK |
| BreadcrumbList on inner pages | 5 | 4 | GOOD |
| JSON-LD format | 5 | 5 | PASS |
| Server-rendered not JS-injected | 10 | 10 | PASS |
| speakable property | 5 | 5 | PASS |
| Valid JSON + valid types | 10 | 10 | PASS |
| knowsAbout property | 5 | 5 | PASS |
| No deprecated schemas | 5 | 5 | PASS |

---

## Page-by-Page Analysis

### 1. Homepage (https://samrosehill.com)

**JSON-LD Blocks Found: 2**

#### Block 1 -- Person (site-wide, from Base layout)

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "Dr. Samuel Rosehill",
  "givenName": "Samuel",
  "familyName": "Rosehill",
  "honorificPrefix": "Dr.",
  "jobTitle": "Dentist",
  "description": "A clinical archive of dental research reviews...",
  "url": "https://samrosehill.com",
  "worksFor": { "@type": "Dentist", ... },
  "alumniOf": [ ... ],
  "knowsAbout": [ ... ],
  "sameAs": [ ... ]
}
```

**Validation:**
- PASS: Valid @context and @type
- PASS: name, givenName, familyName, honorificPrefix present
- PASS: jobTitle present
- PASS: url present and correct
- PASS: worksFor uses correct Dentist type with PostalAddress
- PASS: alumniOf with CollegeOrUniversity types
- PASS: knowsAbout with 7 relevant topics
- PASS: sameAs array present
- MISSING: image property (headshot/photo)
- MISSING: email or telephone
- MISSING: hasCredential for formal qualifications
- ISSUE: sameAs has only 3 links (LinkedIn, Ethical Dental profile, Substack) -- should be 5+

#### Block 2 -- WebSite

```json
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Dr. Samuel Rosehill",
  "url": "https://samrosehill.com",
  "description": "A clinical archive of dental research reviews...",
  "author": { "@type": "Person", "name": "Dr. Samuel Rosehill", "url": "..." }
}
```

**Validation:**
- PASS: Valid @context and @type
- PASS: name, url, description present
- PASS: author linked
- MISSING: potentialAction with SearchAction -- required for sitelinks search box in AI results
- MISSING: @id for cross-referencing with other schemas

**Microdata / RDFa:** None detected.

---

### 2. About Page (https://samrosehill.com/about)

**JSON-LD Blocks Found: 2**

#### Block 1 -- Person (inherited from Base layout)

Same as homepage Person block. See above.

#### Block 2 -- ProfilePage

```json
{
  "@context": "https://schema.org",
  "@type": "ProfilePage",
  "mainEntity": { "@type": "Person", "name": "Dr. Samuel Rosehill", "url": "..." },
  "url": "https://samrosehill.com/about",
  "name": "About Dr. Samuel Rosehill"
}
```

**Validation:**
- PASS: Valid @context and @type
- PASS: mainEntity correctly references Person
- PASS: url and name present
- MISSING: dateCreated, dateModified
- MISSING: BreadcrumbList schema (this is an inner page)
- ISSUE: mainEntity Person is thin -- could use @id reference to the full Person block rather than duplicating a minimal version

---

### 3. Reviews Index (https://samrosehill.com/reviews)

**JSON-LD Blocks Found: 2**

#### Block 1 -- Person (inherited from Base layout)

Same as homepage. See above.

#### Block 2 -- CollectionPage

```json
{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "Dental Research Reviews",
  "description": "Recent publications from the prosthodontic...",
  "url": "https://samrosehill.com/reviews",
  "author": { "@type": "Person", "name": "Dr. Samuel Rosehill", "url": "..." }
}
```

**Validation:**
- PASS: Valid @context and @type
- PASS: name, description, url, author present
- MISSING: BreadcrumbList schema (this is an inner page)
- MISSING: mainEntity with ItemList of review articles
- MISSING: numberOfItems or hasPart for AI discovery of collection size

---

### 4. Sample Article (https://samrosehill.com/reviews/digital-guided-occlusal-adjustment)

**JSON-LD Blocks Found: 3**

#### Block 1 -- Person (inherited from Base layout)

Same as homepage. See above.

#### Block 2 -- Article

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Grinding With a GPS: Computer-Guided Occlusal Adjustment Goes Digital",
  "description": "A fully digital workflow for occlusal adjustment...",
  "datePublished": "2026-03-31",
  "dateModified": "2026-03-31",
  "author": { "@type": "Person", "name": "...", "url": "...", "jobTitle": "Dentist" },
  "publisher": { "@type": "Person", "name": "...", "url": "..." },
  "mainEntityOfPage": { "@type": "WebPage", "@id": "..." },
  "articleSection": "Dental Research Reviews",
  "keywords": "occlusal adjustment, digital dentistry, ...",
  "about": {
    "@type": "ScholarlyArticle",
    "name": "...",
    "author": "Zhang, Y. et al.",
    "isPartOf": { "@type": "Periodical", "name": "..." },
    "datePublished": "2026"
  },
  "speakable": {
    "@type": "SpeakableSpecification",
    "cssSelector": [".article__desc", ".clinical-relevance__text"]
  }
}
```

**Validation:**
- PASS: Valid Article type with all required properties
- PASS: headline, description, datePublished, dateModified present
- PASS: author with Person type including jobTitle
- PASS: publisher present
- PASS: mainEntityOfPage with @id
- PASS: articleSection and keywords present
- PASS: about references ScholarlyArticle source paper (excellent for GEO)
- PASS: speakable with SpeakableSpecification and cssSelector
- MISSING: image property (OG image is set but not in schema)
- MISSING: wordCount
- MISSING: author @id for cross-referencing with site-wide Person
- NOTE: publisher uses Person type (acceptable for personal blog; Organization would be more standard)

#### Block 3 -- BreadcrumbList

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    { "@type": "ListItem", "position": 1, "name": "Home", "item": "https://samrosehill.com" },
    { "@type": "ListItem", "position": 2, "name": "Journal", "item": "https://samrosehill.com/reviews" },
    { "@type": "ListItem", "position": 3, "name": "Grinding With a GPS..." }
  ]
}
```

**Validation:**
- PASS: Valid BreadcrumbList with correct ListItem nesting
- PASS: Sequential position numbers
- PASS: Final item omits "item" URL (correct for current page)
- PASS: All intermediate items have URLs

---

## Detailed Criterion Scoring

### 1. Organization/Person Schema Completeness (13/15)

**What works:**
- Person type used correctly with givenName, familyName, honorificPrefix
- jobTitle, url, description all present
- worksFor with nested Dentist type and PostalAddress
- alumniOf with two CollegeOrUniversity entries

**What is missing (-2pts):**
- No `image` property (photo/headshot). This is a recommended property that AI systems use for knowledge panels
- No `hasCredential` for formal qualifications (MClinDent, BDSc, Fellowships). The about page lists these in HTML but they are not in structured data
- No `@id` identifier for cross-referencing across pages

### 2. sameAs Links (6/15)

**Current sameAs links (3):**
1. LinkedIn: `https://www.linkedin.com/in/sam-rosehill-74905755/`
2. Ethical Dental profile: `https://www.ethical.dental/about-us/dr-sam-rosehill`
3. Substack: `https://samuelrosehill.substack.com`

**Missing platforms for comprehensive entity recognition (-9pts):**
- No Google Scholar profile
- No ORCID
- No ResearchGate
- No Twitter/X profile
- No Dental Board / AHPRA registration link
- No Wikidata QID
- No YouTube (if applicable)
- No IADR profile

AI systems use sameAs links as the primary mechanism for entity disambiguation and authority verification. With only 3 links, the entity graph is thin. A minimum of 5 platforms is recommended; 8+ is ideal for healthcare professionals.

### 3. Article Schema with Author Details (9/10)

**What works:**
- Full Article schema on every review page
- Author Person with name, url, and jobTitle
- Publisher specified
- datePublished and dateModified present
- articleSection and keywords for topic classification
- about references the source ScholarlyArticle (excellent for AI citation chains)

**What is missing (-1pt):**
- No `image` property in Article schema (OG image exists but is not mirrored in JSON-LD)
- No `@id` cross-references between Article author and site-wide Person

### 4. Business-Type-Specific Schemas (8/10)

**What works:**
- `Dentist` type used correctly in worksFor
- PostalAddress with locality, region, country
- `ScholarlyArticle` nested inside Article.about for source paper citation
- `Periodical` for journal reference
- `CollectionPage` for the reviews index
- `ProfilePage` for the about page

**What is missing (-2pts):**
- No `MedicalSpecialty` enumeration for prosthodontics
- No `hasOfferCatalog` or `medicalSpecialty` on the Dentist entity
- The Dentist entity could benefit from `@id`, `telephone`, `geo` coordinates

### 5. WebSite + SearchAction (3/5)

**What works:**
- WebSite schema present on homepage with name, url, description, author

**What is missing (-2pts):**
- No `potentialAction` with `SearchAction`. This is required for Google/AI sitelinks search box:
  ```json
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://samrosehill.com/search?q={search_term_string}",
    "query-input": "required name=search_term_string"
  }
  ```
  Note: This requires an actual search page to exist on the site.

### 6. BreadcrumbList on Inner Pages (4/5)

**What works:**
- BreadcrumbList present on all review article pages
- Correct 3-level hierarchy: Home > Journal > Article Title
- Proper ListItem structure with sequential positions

**What is missing (-1pt):**
- No BreadcrumbList on the /about page
- No BreadcrumbList on the /reviews index page

### 7. JSON-LD Format (5/5)

- All structured data uses JSON-LD (not Microdata or RDFa)
- Consistent format across all pages
- Embedded via `<script type="application/ld+json">` tags
- Uses Astro's `set:html={JSON.stringify(...)}` for safe serialization

### 8. Server-Rendered Not JS-Injected (10/10)

- Astro runs in static SSG mode (no `output: 'server'` in config)
- All pages are pre-rendered at build time
- JSON-LD blocks are embedded in the static HTML via Astro template expressions
- No client-side JavaScript is needed to inject structured data
- Verified by inspecting raw HTML from live pages -- all JSON-LD present in initial response

### 9. speakable Property (5/5)

- `speakable` with `SpeakableSpecification` present on all article pages
- Uses `cssSelector` targeting `.article__desc` and `.clinical-relevance__text`
- These selectors correctly point to the article description and clinical relevance summary -- the two most TTS-friendly content blocks

### 10. Valid JSON + Valid Types (10/10)

- All JSON-LD blocks parse as valid JSON
- All @type values are valid Schema.org types:
  - Person, WebSite, ProfilePage, CollectionPage, Article, BreadcrumbList, ListItem
  - Dentist, PostalAddress, CollegeOrUniversity
  - ScholarlyArticle, Periodical, SpeakableSpecification, WebPage
- No typos or malformed properties detected
- Correct nesting of nested types

### 11. knowsAbout Property (5/5)

- Present in site-wide Person schema with 7 specific topics:
  - Prosthodontics, Dental Implantology, Digital Dentistry, Shade Matching, 3D Printing in Dentistry, Guided Implant Surgery, Biomaterials
- Topics are specific and relevant to the site content
- Propagated to every page via the Base layout

### 12. No Deprecated Schemas (5/5)

- No deprecated types used
- No deprecated properties detected
- All types and properties are current Schema.org vocabulary
- Uses modern `datePublished` (not deprecated `dateCreated` for articles)
- Uses `mainEntityOfPage` correctly

---

## Cross-Reference & Nesting Analysis

### Entity Consistency

The Person entity is defined identically on every page via the Base layout. This is good for consistency but creates redundancy. A better approach would be to use `@id` references:

**Current approach:** Full Person object duplicated on every page (4+ times per page load across the site).

**Recommended approach:** Define the canonical Person once with an `@id`, then reference it:
```json
// In Base layout:
{ "@type": "Person", "@id": "https://samrosehill.com/#person", "name": "Dr. Samuel Rosehill", ... }

// In Article author:
{ "author": { "@id": "https://samrosehill.com/#person" } }
```

### Missing Cross-References

- Article.author does not reference the site-wide Person via @id
- ProfilePage.mainEntity does not reference the site-wide Person via @id
- WebSite.author does not reference the site-wide Person via @id
- No @graph structure to bundle all entities per page

---

## Priority Fixes (Ranked by GEO Impact)

### P0 -- Critical (Do First)

1. **Add more sameAs links (current: 3, target: 6+)**
   - Add Google Scholar profile URL
   - Add ORCID if available
   - Add AHPRA dental registration link
   - Add any other professional directory profiles
   - Impact: sameAs is the primary signal AI systems use for entity disambiguation

2. **Add `image` to Person schema**
   - Professional headshot URL
   - AI systems use this for knowledge panel construction
   ```json
   "image": "https://samrosehill.com/images/dr-samuel-rosehill.jpg"
   ```

### P1 -- High Priority

3. **Add `@id` identifiers for entity cross-referencing**
   - Person: `"@id": "https://samrosehill.com/#person"`
   - WebSite: `"@id": "https://samrosehill.com/#website"`
   - Reference these @ids in Article.author, ProfilePage.mainEntity, etc.

4. **Add `image` to Article schema**
   - Mirror the OG image into the JSON-LD:
   ```json
   "image": "https://samrosehill.com/images/reviews/digital-guided-occlusal-adjustment.png"
   ```

5. **Add BreadcrumbList to /about and /reviews pages**
   - /about: Home > About
   - /reviews: Home > Journal

### P2 -- Medium Priority

6. **Add SearchAction to WebSite schema** (requires building a search page first)

7. **Add `hasCredential` to Person schema**
   ```json
   "hasCredential": [
     { "@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "MClinDent Fixed & Removable Prosthodontics", "recognizedBy": { "@type": "CollegeOrUniversity", "name": "King's College London" } },
     { "@type": "EducationalOccupationalCredential", "credentialCategory": "degree", "name": "BDSc (Hons)", "recognizedBy": { "@type": "CollegeOrUniversity", "name": "University of Queensland" } }
   ]
   ```

8. **Add `memberOf` for fellowships**
   ```json
   "memberOf": [
     { "@type": "Organization", "name": "Pierre Fauchard Academy" },
     { "@type": "Organization", "name": "International College of Dentists" }
   ]
   ```

### P3 -- Nice to Have

9. **Add `wordCount` to Article schema** for content depth signaling
10. **Add `MedicalSpecialty` to Dentist entity**
11. **Consider @graph structure** to bundle all entities per page into a single JSON-LD block
12. **Add `dateCreated`/`dateModified` to ProfilePage**

---

## Summary

The site has a solid structured data foundation. The Person schema is comprehensive with knowsAbout, alumniOf, and worksFor. Article pages have excellent schema including speakable, source paper references via ScholarlyArticle, and BreadcrumbList. All data is properly server-rendered via Astro's static build.

The two biggest gaps are: (1) only 3 sameAs links where 5+ are needed for strong entity recognition by AI systems, and (2) no @id cross-referencing between entities across pages. Fixing these two issues would likely push the score into the high 80s.

The site uses no deprecated schemas, all JSON is valid, and the implementation pattern (Base layout + page-specific slots) is clean and maintainable.
