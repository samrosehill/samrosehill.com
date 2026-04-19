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
