# GEO Technical SEO Audit — samrosehill.com

**Audit Date:** 1 April 2026
**Site:** https://samrosehill.com
**Framework:** Astro (static site generation)
**Hosting:** Vercel (Sydney edge, syd1)
**Purpose:** Dental professional's personal site — clinical research reviews

---

## Overall Score: 87 / 100

| Category | Score | Max | Status |
|---|---|---|---|
| 1. Crawlability | 14 | 15 | Excellent |
| 2. Indexability | 10 | 12 | Good |
| 3. Security | 9 | 10 | Excellent |
| 4. URL Structure | 7 | 8 | Good |
| 5. Mobile Optimization | 9 | 10 | Excellent |
| 6. Core Web Vitals (est.) | 14 | 15 | Excellent |
| 7. Server-Side Rendering | 15 | 15 | Perfect |
| 8. Page Speed | 9 | 15 | Needs Work |

---

## Pages Audited

1. **Homepage** — https://samrosehill.com
2. **About** — https://samrosehill.com/about
3. **Reviews (Journal)** — https://samrosehill.com/reviews
4. **Sample Article** — https://samrosehill.com/reviews/lithium-disilicate-ten-year-review/

---

## 1. CRAWLABILITY (14/15)

### robots.txt — PASS (5/5)

The robots.txt explicitly welcomes all AI and search crawlers with individual `Allow: /` directives:

| Crawler | Access |
|---|---|
| Googlebot | Allowed |
| Bingbot | Allowed |
| GPTBot (OpenAI) | Allowed |
| ChatGPT-User | Allowed |
| ClaudeBot (Anthropic) | Allowed |
| Claude-Web | Allowed |
| PerplexityBot | Allowed |
| Google-Extended | Allowed |
| Applebot | Allowed |
| Wildcard (*) | Allowed |

**Verdict:** Best-in-class. Every major AI and search crawler is explicitly permitted. The opening comment "Welcome all crawlers including AI systems" is an excellent signal.

### XML Sitemap — PASS (4/5)

- Sitemap index at `/sitemap-index.xml` references `/sitemap-0.xml`
- Contains **21 URLs** covering all pages and review articles
- Properly declared in robots.txt
- **Issue:** No `<lastmod>` dates on any URL. This reduces crawl efficiency because crawlers cannot determine which pages have changed without re-fetching all of them.

### Crawl Depth — PASS (3/3)

All content is reachable within 2 clicks from homepage:
- Homepage (depth 0) -> Reviews listing (depth 1) -> Individual review (depth 2)
- Homepage -> About (depth 1)
- Featured reviews linked directly from homepage (depth 1)

### noindex Directives — PASS (2/2)

- No `noindex` meta tags found on any page
- No `X-Robots-Tag` headers detected
- All pages are freely indexable

### llms.txt — BONUS PASS

An `llms.txt` file is present and well-structured, providing AI systems with a machine-readable site summary, author bio, topic taxonomy, and links to all review articles. This is an excellent GEO signal that most sites lack entirely.

### Findings

| Check | Result |
|---|---|
| robots.txt present | PASS |
| AI crawlers allowed | PASS (all major bots) |
| Sitemap present | PASS |
| Sitemap in robots.txt | PASS |
| Sitemap lastmod dates | FAIL (missing) |
| Crawl depth <= 3 | PASS (max 2) |
| No unintended noindex | PASS |
| llms.txt | PASS (present) |

### Recommendation

- **Add `<lastmod>` dates** to sitemap entries. Astro can generate these from file modification times or frontmatter dates.

---

## 2. INDEXABILITY (10/12)

### Canonical Tags — PASS (4/4)

Every audited page has a proper `<link rel="canonical">` tag:

| Page | Canonical URL |
|---|---|
| Homepage | `https://samrosehill.com/` |
| About | `https://samrosehill.com/about/` |
| Reviews | `https://samrosehill.com/reviews/` |
| Sample Article | `https://samrosehill.com/reviews/lithium-disilicate-ten-year-review/` |

All canonicals use HTTPS and the non-www domain consistently.

### Duplicate Content — GOOD (4/6)

**HTTP -> HTTPS:** PASS. HTTP requests receive a `308 Permanent Redirect` to HTTPS.

**www -> non-www:** INCONCLUSIVE. `https://www.samrosehill.com` returned no response within timeout (likely DNS not configured for www, which is acceptable for a non-www canonical site but should be verified).

**Trailing Slashes:** MINOR ISSUE. Both `/about` and `/about/` return HTTP 200 with identical content and identical canonical tags (pointing to the trailing-slash version). While the canonical tag is consistent, serving the same content at two URLs without a redirect is suboptimal. Astro's default `trailingSlash` behavior is in play here.

### Pagination — PASS (2/2)

The reviews listing page displays all articles on a single page (17 reviews). No pagination required at current scale. No orphaned `rel="next"` / `rel="prev"` tags found.

### Findings

| Check | Result |
|---|---|
| Canonical tags present | PASS (all pages) |
| Canonical HTTPS | PASS |
| Canonical non-www | PASS |
| HTTP -> HTTPS redirect | PASS (308) |
| www -> non-www redirect | INCONCLUSIVE (DNS timeout) |
| Trailing slash consistency | MINOR ISSUE (dual 200s) |
| Pagination | PASS (N/A) |

### Recommendations

- **Configure `trailingSlash: "always"` in astro.config.mjs** and set up a Vercel redirect rule so that non-trailing-slash URLs 301 to trailing-slash versions. This eliminates duplicate content signals.
- **Verify www DNS:** Confirm whether `www.samrosehill.com` resolves. If it does, add a redirect to the non-www version.

---

## 3. SECURITY (9/10)

### HTTPS — PASS (3/3)

- Valid TLS certificate served by Vercel
- HTTP -> HTTPS redirect via 308 Permanent Redirect
- HSTS header: `strict-transport-security: max-age=63072000` (2 years) — excellent max-age value

### Security Headers — GOOD (6/7)

| Header | Value | Status |
|---|---|---|
| Strict-Transport-Security | `max-age=63072000` | PASS |
| X-Content-Type-Options | `nosniff` | PASS |
| X-Frame-Options | `DENY` | PASS |
| Referrer-Policy | `strict-origin-when-cross-origin` | PASS |
| Permissions-Policy | `camera=(), microphone=(), geolocation=()` | PASS |
| Content-Security-Policy | Not set | FAIL |

All headers are configured via `vercel.json` and applied consistently across all routes (`/(.*)`).

### Findings

| Check | Result |
|---|---|
| HTTPS enforced | PASS |
| HSTS | PASS (2-year max-age) |
| X-Content-Type-Options | PASS |
| X-Frame-Options | PASS |
| Referrer-Policy | PASS |
| Permissions-Policy | PASS |
| Content-Security-Policy | FAIL (missing) |

### Recommendation

- **Add a Content-Security-Policy header.** For a static Astro site, a restrictive CSP is straightforward. Example:
  ```
  default-src 'self'; style-src 'self' 'unsafe-inline'; img-src 'self' data:; script-src 'self'
  ```
  This is the only missing security header. Adding it would achieve a perfect score.

---

## 4. URL STRUCTURE (7/8)

### Clean URLs — PASS (3/3)

All URLs follow a clean, human-readable pattern:
- `/reviews/lithium-disilicate-ten-year-review/`
- `/about/`
- `/cases/`

No query parameters, session IDs, or file extensions in any URL.

### Logical Hierarchy — PASS (3/3)

```
/                           (homepage)
/about/                     (author profile)
/reviews/                   (article listing)
/reviews/{article-slug}/    (individual review)
/cases/                     (case studies)
```

Clean two-level hierarchy. Slugs are descriptive and keyword-rich.

### Redirect Chains — PASS (1/1)

No redirect chains detected. HTTP -> HTTPS is a single-hop 308.

### Parameter Handling — MINOR (0/1)

No parameter handling detected (no `rel="canonical"` stripping of query params, no robots.txt Disallow for parameter URLs). This is low-risk for a static site but worth noting.

### Findings

| Check | Result |
|---|---|
| Clean, readable URLs | PASS |
| Logical hierarchy | PASS |
| No redirect chains | PASS |
| Keyword-rich slugs | PASS |
| Parameter handling | NOT CONFIGURED |

---

## 5. MOBILE OPTIMIZATION (9/10)

### Viewport Meta — PASS (3/3)

All pages include: `<meta name="viewport" content="width=device-width, initial-scale=1.0">`

### Responsive Design — PASS (3/3)

- Single CSS file (`about.DWUHho_S.css`, 12KB) contains responsive styles
- Astro framework outputs semantic HTML with no fixed-width layouts
- No horizontal scroll issues expected

### Tap Targets — ESTIMATED PASS (2/3)

- Navigation links use standard anchor elements with adequate spacing
- Review cards are full-width clickable areas with clear "Read analysis" CTAs
- **Minor concern:** Without live device testing, cannot fully verify all tap target sizes meet the 48x48px minimum. Static analysis suggests compliance.

### Font Sizes — PASS (1/1)

- Base font sizing uses relative units via CSS
- No `font-size` smaller than readable minimums detected in the CSS

### Findings

| Check | Result |
|---|---|
| Viewport meta tag | PASS |
| Responsive CSS | PASS |
| No fixed widths | PASS |
| Tap target sizes | LIKELY PASS |
| Readable font sizes | PASS |

---

## 6. CORE WEB VITALS — Estimated (14/15)

These are estimates based on page architecture analysis. Actual field data from CrUX/PageSpeed Insights is needed for definitive scores.

### LCP (Largest Contentful Paint) — Estimated GOOD (5/5)

- Static HTML served from Vercel's CDN (Sydney edge)
- Main content is pure text (no hero images on most pages)
- Homepage: ~13KB HTML, single 12KB CSS file, 1 script tag
- Review articles: ~15KB HTML with text-heavy content
- **Estimated LCP: < 1.5s** — well within "Good" threshold (< 2.5s)

### INP (Interaction to Next Paint) — Estimated GOOD (5/5)

- Minimal JavaScript (1 `<script>` tag per page)
- No client-side framework hydration
- No event listeners blocking main thread
- **Estimated INP: < 100ms** — well within "Good" threshold (< 200ms)

### CLS (Cumulative Layout Shift) — Estimated GOOD (4/5)

- No web fonts loaded (system font stack implied)
- Images are PNG thumbnails on review cards — **no explicit width/height attributes detected in HTML**, which could cause minor CLS on the reviews listing page when images load
- Article pages are text-dominant with minimal layout shift risk
- **Estimated CLS: < 0.05** for article pages, potentially higher on /reviews/ listing

### Findings

| Metric | Estimate | Threshold | Status |
|---|---|---|---|
| LCP | < 1.5s | < 2.5s | GOOD |
| INP | < 100ms | < 200ms | GOOD |
| CLS | < 0.05 (articles), ~0.05-0.1 (listing) | < 0.1 | GOOD / AT RISK |

### Recommendation

- **Add explicit `width` and `height` attributes to all `<img>` tags** on the reviews listing page to reserve space and prevent CLS when images load.

---

## 7. SERVER-SIDE RENDERING (15/15)

### Raw HTML Analysis — PERFECT

This is the most critical category for GEO (AI crawler discoverability). AI crawlers like GPTBot and ClaudeBot typically do not execute JavaScript, so content must be present in the raw HTML response.

**Test methodology:** Fetched raw HTML via `curl` (no JS execution) for all 4 audited pages.

| Page | Content in Raw HTML? | Result |
|---|---|---|
| Homepage | Full navigation, featured reviews, article snippets, structured data | PASS |
| About | Complete bio, education, fellowships, publications | PASS |
| Reviews | All 17 review cards with titles, summaries, links | PASS |
| Sample Article | Full article text, headings, clinical bottom line, structured data | PASS |

### Framework Confirmation

Astro generates **fully static HTML at build time** (SSG). There is zero client-side rendering dependency. The single `<script>` tag per page is for non-critical functionality (likely Astro's island architecture with no hydrated islands detected).

### Structured Data in Raw HTML — PASS

All JSON-LD structured data is embedded directly in the HTML `<head>`:
- Person schema (site-wide)
- WebSite / CollectionPage / ProfilePage / Article schema (page-specific)
- BreadcrumbList (article pages)
- ScholarlyArticle references (article pages)
- SpeakableSpecification (article pages)

### Findings

| Check | Result |
|---|---|
| Main content in raw HTML | PASS (all pages) |
| No JS dependency for content | PASS |
| Structured data in raw HTML | PASS |
| Headings in raw HTML | PASS |
| Internal links crawlable | PASS |
| Images referenced in HTML | PASS |

**This is a perfect score.** Astro's SSG approach is ideal for GEO. Every piece of content that an AI crawler needs is available without JavaScript execution.

---

## 8. PAGE SPEED (9/15)

### TTFB (Time to First Byte) — ESTIMATED GOOD (3/3)

- Vercel CDN with edge caching (`x-vercel-cache: HIT`)
- Served from Sydney edge node (syd1) — close to Australian users
- Static assets with immutable cache headers
- **Estimated TTFB: < 100ms** for cached responses

### Page Weight — NEEDS WORK (2/4)

| Page | HTML Size | CSS | Total (excl. images) |
|---|---|---|---|
| Homepage | 13.4 KB | 12.2 KB | ~25.6 KB |
| About | 12.4 KB | 12.2 KB | ~24.6 KB |
| Reviews | — | 12.2 KB | < 30 KB |
| Sample Article | 15.5 KB | 12.2 KB | ~27.7 KB |

**HTML + CSS is extremely lean.** However, image weight is a concern:

| Metric | Value | Status |
|---|---|---|
| Total review images (17 PNGs) | ~3.9 MB | HEAVY |
| Average image size | 229 KB | NEEDS OPTIMIZATION |
| Largest image | 395 KB (platform-switching) | TOO LARGE |
| Smallest image | 124 KB (half-vs-full) | ACCEPTABLE |

### Image Optimization — FAIL (1/4)

**Critical issues:**
1. **All images are PNG format** — these are thumbnail composites of journal article first pages. WebP or AVIF would reduce sizes by 40-70%.
2. **No Astro `<Image>` component detected** — images appear to be served as raw PNGs from `/public/images/` rather than processed through Astro's built-in image optimization pipeline.
3. **No `<img>` tags found in homepage HTML** — images may be loaded via CSS backgrounds or are on subpages only, but the reviews listing page should be checked.
4. **Image cache headers are weak** — `cache-control: public, max-age=0, must-revalidate` on image files means browsers must revalidate on every visit. Static images should have long cache times.

### Compression — PASS (2/2)

- Brotli compression active (`content-encoding: br`) on HTML responses
- Static assets served compressed

### Caching — NEEDS WORK (1/2)

| Asset Type | Cache-Control | Status |
|---|---|---|
| HTML pages | `public, max-age=0, must-revalidate` | APPROPRIATE (dynamic) |
| CSS (hashed) | `public, max-age=31536000, immutable` | EXCELLENT |
| Images (static) | `public, max-age=0, must-revalidate` | POOR |

Astro hashes CSS filenames (`about.DWUHho_S.css`) enabling immutable caching. Images in `/public/` are not hashed, so they get default Vercel caching (no long-term cache). This forces unnecessary revalidation.

### CDN — PASS (included above)

Vercel's global CDN is active. `x-vercel-cache: HIT` confirms edge caching. Sydney edge node serves Australian users with minimal latency.

### Findings

| Check | Result |
|---|---|
| TTFB | PASS (< 100ms est.) |
| HTML weight | PASS (< 16KB) |
| CSS weight | PASS (12KB, single file) |
| JS weight | PASS (minimal) |
| Image format | FAIL (PNG only, no WebP/AVIF) |
| Image sizes | FAIL (avg 229KB) |
| Image optimization pipeline | FAIL (no Astro Image) |
| Brotli/Gzip compression | PASS |
| CSS caching | PASS (immutable) |
| Image caching | FAIL (max-age=0) |
| CDN active | PASS |

### Recommendations

1. **Convert images to WebP** (or better, use Astro's `<Image>` component for automatic format negotiation). Expected savings: 40-60% per image.
2. **Add image cache headers in vercel.json:**
   ```json
   {
     "source": "/images/(.*)",
     "headers": [
       { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
     ]
   }
   ```
3. **Add explicit `width` and `height` to `<img>` elements** to prevent layout shift and enable browser lazy-loading.
4. **Consider adding `loading="lazy"`** to below-the-fold images.

---

## IndexNow Protocol — NOT CONFIGURED

- No IndexNow key file found at `/.well-known/indexnow`
- No IndexNow key file found at root level

IndexNow enables instant notification to Bing and Yandex when content changes. For a site that publishes new reviews regularly, this would accelerate indexing.

### Recommendation

Add IndexNow support. Vercel does not natively support IndexNow, but it can be implemented via:
1. A static key file in `/public/.well-known/`
2. A post-deploy webhook or edge function that pings the IndexNow API

---

## Summary of Issues by Priority

### Critical (Fix Immediately)

*None.* The site has no critical technical SEO or GEO issues.

### High Priority

| Issue | Category | Impact |
|---|---|---|
| Images served as unoptimized PNGs | Page Speed | Adds ~3.9MB total weight; slow on mobile |
| No image cache headers | Page Speed | Unnecessary revalidation on every visit |
| Missing Content-Security-Policy | Security | Only missing security header |

### Medium Priority

| Issue | Category | Impact |
|---|---|---|
| No sitemap `<lastmod>` dates | Crawlability | Crawlers cannot detect changed pages |
| Trailing slash dual-200 responses | Indexability | Minor duplicate content signal |
| No IndexNow | Crawlability | Slower Bing/Yandex indexing |

### Low Priority

| Issue | Category | Impact |
|---|---|---|
| No explicit image dimensions in HTML | Core Web Vitals | Minor CLS risk on listing page |
| No `loading="lazy"` on images | Page Speed | Minor FCP impact |

---

## What This Site Does Well

1. **SSR/SSG is perfect.** Astro generates fully static HTML. Every AI crawler gets complete content without JS execution. This is the single most important GEO technical factor, and it scores 15/15.

2. **AI crawler access is best-in-class.** robots.txt explicitly allows GPTBot, ClaudeBot, PerplexityBot, and all major crawlers. Combined with the llms.txt file, this site is exceptionally well-prepared for AI discoverability.

3. **Structured data is comprehensive.** Person, Article, ScholarlyArticle, BreadcrumbList, CollectionPage, ProfilePage, SpeakableSpecification, and WebSite schemas are all present and correctly implemented.

4. **Security headers are nearly complete.** Five of six recommended headers are configured via vercel.json. Only CSP is missing.

5. **Page weight (excluding images) is exceptional.** Sub-30KB total for HTML + CSS with no JS framework overhead. This is as lean as a production site can get.

6. **Canonical tags and meta descriptions** are present and correct on every page.

7. **Open Graph and Twitter Card tags** are present on all pages, with article-specific images on review pages.

---

## Appendix: Raw Header Dump (Homepage)

```
HTTP/2 200
accept-ranges: bytes
access-control-allow-origin: *
age: 711
cache-control: public, max-age=0, must-revalidate
content-type: text/html; charset=utf-8
etag: "dd4dd119e6e1f3633fa69c0dd965775f"
permissions-policy: camera=(), microphone=(), geolocation=()
referrer-policy: strict-origin-when-cross-origin
server: Vercel
strict-transport-security: max-age=63072000
x-content-type-options: nosniff
x-frame-options: DENY
x-vercel-cache: HIT
content-length: 13394
```

---

*Generated by GEO Technical Audit — 1 April 2026*
