# Elsevier (ScienceDirect)

## Journals
- Dental Materials (ISSN 0109-5641)

## Authentication: EZproxy DOI Resolver + Shibboleth

Elsevier uses a two-stage authentication approach. The EZproxy DOI resolver provides the entry point, and Elsevier's own SSO handles the institutional login.

### EZproxy DOI Resolver (Entry Point)
```
https://doi-org.kcl.idm.oclc.org/{DOI}
```

Example:
```
https://doi-org.kcl.idm.oclc.org/10.1016/j.dental.2025.01.001
```

This resolves the DOI through KCL's proxy, which establishes the institutional context.

### Authentication Flow

**For Open Access articles:**
1. Navigate to `https://doi-org.kcl.idm.oclc.org/{DOI}`
2. Redirects directly to ScienceDirect with full access
3. No additional login needed

**For paywalled articles:**
1. Navigate to `https://doi-org.kcl.idm.oclc.org/{DOI}`
2. If no active Shibboleth session, Elsevier redirects to `id.elsevier.com`
3. The page shows "Access through your organization" with KCL listed
4. Click the KCL button
5. Redirects to KCL Shibboleth login (or auto-completes if session exists)
6. Redirects back to ScienceDirect with full access

### PDF Download — IMPORTANT: Special Workflow

Elsevier does NOT support simple URL-based PDF download like Wiley. The `pdfft` URL pattern returns HTML, not a PDF.

```
# THIS DOES NOT WORK for programmatic download:
https://www.sciencedirect.com/science/article/pii/{PII}/pdfft?isDTMRedir=true&download=true
# Returns ~52KB HTML page, not a PDF
```

### Correct Download Method: View PDF Button → Signed S3 URL

Elsevier generates time-limited, signed AWS S3 URLs for PDF access. The workflow requires clicking the "View PDF" button in the browser:

1. Navigate to the article page (authenticated via EZproxy DOI resolver)
2. Use Chrome MCP `find` tool to locate the "View PDF" button/link
3. Click it — this opens the Elsevier PDF viewer
4. The PDF is served from `pdf.sciencedirectassets.com` with AWS signed parameters:
   ```
   https://pdf.sciencedirectassets.com/271039/...?X-Amz-Security-Token=...&X-Amz-Signature=...
   ```
5. These signed URLs are temporary and unique per session

### Download via Chrome MCP Click (Recommended)

Since the PDF URL is dynamically generated with security tokens, the most reliable approach is:

1. Navigate to article page via EZproxy DOI
2. Use `mcp__Claude_in_Chrome__find` to locate "View PDF" or "Download PDF"
3. Click to open the PDF viewer
4. Use `mcp__Claude_in_Chrome__find` to locate the download button within the PDF viewer
5. Click to trigger the browser's native download

### Alternative: Extract and Fetch the S3 URL

If you need programmatic download, you can try extracting the signed URL from the PDF viewer page. However, note that:
- Chrome content filter may block responses containing the signed URL (base64/query string data)
- The URL expires quickly
- This is less reliable than the click-based approach

```javascript
// After the PDF viewer is open, try:
window._pdfUrl = 'pending';
var iframe = document.querySelector('iframe[src*="sciencedirectassets"]');
if (iframe) {
  window._pdfUrl = 'found iframe';
  // The src may be blocked by content filter
} else {
  window._pdfUrl = 'no iframe found';
}
```

### Finding Articles via CrossRef

```javascript
fetch('https://api.crossref.org/journals/0109-5641/works?rows=3&sort=published&order=desc')
  .then(r => r.json())
  .then(data => {
    window._dmArticles = JSON.stringify(
      data.message.items.map(i => ({
        title: (i.title || [''])[0].substring(0, 80),
        doi: i.DOI,
        pii: i.alternative_id ? i.alternative_id[0] : ''
      }))
    );
  });
```

### Quirks & Notes
- Elsevier is the most complex publisher to download from programmatically
- The `pdfft` endpoint is a red herring — it returns HTML, not PDF binary
- Signed S3 URLs contain AWS security tokens and expire within minutes
- Chrome content filter blocks attempts to read the S3 URLs via JavaScript
- The click-based approach through Chrome MCP is most reliable
- Successfully tested: navigated to Dental Materials article, authenticated via Shibboleth, accessed PDF viewer
- PII (Publisher Item Identifier) format: `S0109564125XXXXXX` — useful for constructing article URLs
