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
