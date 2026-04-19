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
