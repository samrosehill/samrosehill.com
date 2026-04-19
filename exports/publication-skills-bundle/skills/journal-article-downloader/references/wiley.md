# Wiley Online Library

## Journals
- Journal of Prosthodontics (ISSN 1059-941X / 1532-849X)
- Clinical Implant Dentistry and Related Research — CIDR (ISSN 1523-0899 / 1708-8208)
- Clinical Oral Implants Research — COIR (ISSN 0905-7161 / 1600-0501)
- Journal of Esthetic and Restorative Dentistry — JERD (ISSN 1496-4155 / 1708-8240)
- Journal of Oral Rehabilitation (ISSN 0305-182X)

## Authentication: Shibboleth Institutional Login

Wiley does NOT work with KCL's EZproxy domain rewriting (returns 404). Instead, use Wiley's built-in institutional login which triggers Shibboleth/SAML authentication.

### EZproxy Does NOT Work
```
# THIS FAILS — do not use:
https://onlinelibrary-wiley-com.kcl.idm.oclc.org/  → 404 error
```

### Authentication Flow
1. Navigate to `https://onlinelibrary.wiley.com/`
2. Click "Login / Register" (top right)
3. Click "Institutional Login"
4. Search for "King's College London" in the institution search
5. Select KCL from the results
6. The browser redirects to KCL's Shibboleth IdP login page
7. User enters their KCL credentials (if not already logged in)
8. Redirect back to Wiley with an authenticated session
9. The session persists — articles now show "Access" badges

If the user has recently authenticated with KCL Shibboleth for another publisher (e.g., Elsevier), the Shibboleth session may still be active and steps 6-7 happen automatically.

### PDF URL Pattern

Wiley uses a `pdfdirect` endpoint that returns the actual PDF binary:

```
https://onlinelibrary.wiley.com/doi/pdfdirect/{DOI}?download=true
```

Example:
```
https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/jopr.70007?download=true
```

**Important**: The `/doi/epdf/{DOI}` endpoint is the browser-based PDF viewer (redirects to abstract if not authenticated). Always use `/doi/pdfdirect/` for programmatic download.

### Download Code (Proven Working)

```javascript
window._dlResult = 'pending';
fetch('https://onlinelibrary.wiley.com/doi/pdfdirect/10.1111/jopr.70007?download=true', {credentials: 'include'})
  .then(r => {
    window._dlResult = 'status:' + r.status + ' type:' + r.headers.get('content-type');
    return r.blob();
  })
  .then(blob => {
    window._dlResult = 'size:' + blob.size;
    var blobUrl = URL.createObjectURL(blob);
    var link = document.createElement('a');
    link.href = blobUrl;
    link.download = 'J_Prosthodontics_article.pdf';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(blobUrl);
  })
  .catch(e => { window._dlResult = 'err:' + e.message; });
'fetch started'
```

Then verify: `window._dlResult` → should show `size:` with a number > 100000.

### Batch Download Pattern

For downloading multiple Wiley articles in sequence:

```javascript
// Download article 1
window._wd1 = 'pending';
fetch('https://onlinelibrary.wiley.com/doi/pdfdirect/{DOI1}?download=true', {credentials: 'include'})
  .then(r => r.blob())
  .then(blob => {
    window._wd1 = 'size:' + blob.size;
    var u = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = u; a.download = 'Article1.pdf';
    document.body.appendChild(a); a.click(); document.body.removeChild(a);
    URL.revokeObjectURL(u);
  })
  .catch(e => { window._wd1 = 'err:' + e.message; });
```

Repeat with `_wd2`, `_wd3`, etc. Space requests a few seconds apart.

### DOI Patterns for Wiley Journals
- J Prosthodontics: `10.1111/jopr.XXXXX`
- CIDR: `10.1111/cid.XXXXX`
- COIR: `10.1111/clr.XXXXX`
- JERD: `10.1111/jerd.XXXXX`
- J Oral Rehab: `10.1111/joor.XXXXX`

### Quirks & Notes
- `pdfdirect` with `?download=true` is the key — this returns raw PDF bytes
- The `epdf` endpoint is an HTML viewer, not a direct PDF — avoid it for programmatic download
- Content-type should be `application/pdf` — if you get `text/html`, authentication failed
- Wiley was successfully tested with J Prosthodontics (3 articles downloaded, ~1-2MB each)
- All 5 Wiley journals use the same platform and authentication, so the same workflow applies to all
