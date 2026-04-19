# Quintessence Publishing

## Journals
- International Journal of Prosthodontics (IJP) — ISSN 0893-2174
- International Journal of Oral & Maxillofacial Implants (IJOMI) — ISSN 0882-2786
- International Journal of Periodontics & Restorative Dentistry (IJPRD) — ISSN 0198-7569

## Authentication: KCL EZproxy (OCLC)

Quintessence uses the standard EZproxy domain rewriting pattern. This is the simplest authentication method.

### EZproxy URL Pattern
```
https://www-quintessence--publishing-com.kcl.idm.oclc.org/
```

The pattern converts `www.quintessence-publishing.com` to `www-quintessence--publishing-com.kcl.idm.oclc.org` (dots become hyphens, hyphens become double-hyphens).

### Authentication Flow
1. Navigate to the EZproxy URL
2. If not already authenticated, the user will be redirected to KCL's login page
3. After login, they are redirected back to the Quintessence site with proxy authentication active
4. The proxy session persists for subsequent requests

### Finding Articles
Navigate to the journal page on the proxied site:
```
https://www-quintessence--publishing-com.kcl.idm.oclc.org/journal/ijp
https://www-quintessence--publishing-com.kcl.idm.oclc.org/journal/ijomi
https://www-quintessence--publishing-com.kcl.idm.oclc.org/journal/ijprd
```

Or use CrossRef API to find DOIs first (see main SKILL.md).

### PDF Download

Once on a proxied article page, the PDF link is typically available as a direct download button. Use the Chrome MCP to:

1. Navigate to the article page via EZproxy
2. Find and click the PDF download link, OR
3. Use the fetch+blob pattern with the proxied PDF URL:

```javascript
window._dlResult = 'pending';
fetch('https://www-quintessence--publishing-com.kcl.idm.oclc.org/[PDF_PATH]', {credentials: 'include'})
  .then(r => r.blob())
  .then(blob => {
    window._dlResult = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'IJP_article_title.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._dlResult = 'err:' + e.message; });
'fetch started'
```

### Quirks & Notes
- EZproxy is the most reliable method for Quintessence — it consistently works
- The proxied site looks and behaves identically to the regular site
- PDF URLs on Quintessence are straightforward direct links (no signed URLs or redirects)
- IJP was the first journal tested and confirmed working with 20 PDFs downloaded successfully
