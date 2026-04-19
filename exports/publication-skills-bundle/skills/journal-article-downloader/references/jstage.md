# J-STAGE (Japan Science and Technology Information Aggregator, Electronic)

## Journals
- Dental Materials Journal — DMJ (ISSN 0287-4547)
- Journal of Prosthodontic Research — JPR (ISSN 1883-1958)

## Platform
Both journals are hosted on J-STAGE: `https://www.jstage.jst.go.jp/`

## Authentication: Mostly Open Access

Most articles on J-STAGE are open access. J-STAGE is Japan's primary electronic journal platform operated by the Japan Science and Technology Agency (JST). Dental journals on the platform typically provide free full-text access.

For any paywalled articles, try the EZproxy DOI resolver:
```
https://doi-org.kcl.idm.oclc.org/{DOI}
```

## Article URL Patterns

**Dental Materials Journal:**
```
https://www.jstage.jst.go.jp/article/dmj/{volume}/{issue}/{article_id}/_article
```

**Journal of Prosthodontic Research:**
```
https://www.jstage.jst.go.jp/article/jpr/{volume}/{issue}/{article_id}/_article
```

## PDF URL Patterns

J-STAGE provides direct PDF access:
```
https://www.jstage.jst.go.jp/article/dmj/{volume}/{issue}/{article_id}/_pdf
```

Or with the full DOI-based URL. The `_pdf` suffix on the article URL typically returns the PDF.

## Download Approach

**Method 1: Direct navigation to PDF URL**
```javascript
window._jsDl = 'pending';
fetch('https://www.jstage.jst.go.jp/article/dmj/{vol}/{issue}/{id}/_pdf/-char/en')
  .then(r => r.blob())
  .then(blob => {
    window._jsDl = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'DMJ_article.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._jsDl = 'err:' + e.message; });
'fetch started'
```

**Method 2: Navigate and click**
1. Navigate to the article page
2. Find the "PDF" link (usually prominent on J-STAGE article pages)
3. Click to download

## Finding Articles

```javascript
Promise.all([
  fetch('https://api.crossref.org/journals/0287-4547/works?rows=3&sort=published&order=desc').then(r=>r.json()),
  fetch('https://api.crossref.org/journals/1883-1958/works?rows=3&sort=published&order=desc').then(r=>r.json())
]).then(results => {
  window._dmjArticles = JSON.stringify(results[0].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
  window._jprArticles = JSON.stringify(results[1].message.items.map(i => ({t:(i.title||[''])[0].substring(0,60), doi:i.DOI, url:(i.resource||{}).primary?.URL||''})));
});
```

## Quirks & Notes
- J-STAGE is generally very accessible with minimal barriers — open access, no authentication needed
- The `/_pdf/-char/en` suffix on article URLs gives the English PDF directly — **confirmed working**
- Successfully downloaded DMJ article: 3.8MB PDF via fetch+blob with `/_pdf/-char/en` pattern
- No `{credentials: 'include'}` needed since articles are open access
- J-STAGE has good CrossRef integration so DOIs resolve reliably
- DMJ and JPR are published by Japanese dental societies (Japanese Society for Dental Materials and Devices, and Japan Prosthodontic Society respectively)
- Article URL pattern from CrossRef: `https://www.jstage.jst.go.jp/article/dmj/{vol}/{issue}/45_{article_id}/_article`
- PDF URL pattern: replace `/_article` with `/_pdf/-char/en`
