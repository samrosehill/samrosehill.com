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
