---
name: scihub-downloader
description: "Download academic papers from Sci-Hub using browser automation. Use this skill when the user wants to bulk download papers via Sci-Hub, fetch paywalled articles using Sci-Hub, or acquire PDFs by DOI through Sci-Hub. Triggers: 'sci-hub', 'scihub', 'download papers from sci-hub', 'get papers from sci-hub', 'fetch from scihub'."
version: 1.0.0
author: samrosehill
tags: [papers, download, sci-hub, academic, browser-automation]
allowed-tools: Read, Write, Bash, Glob, Grep, mcp__Claude_in_Chrome__tabs_context_mcp, mcp__Claude_in_Chrome__tabs_create_mcp, mcp__Claude_in_Chrome__tabs_close_mcp, mcp__Claude_in_Chrome__navigate, mcp__Claude_in_Chrome__find, mcp__Claude_in_Chrome__computer, mcp__Claude_in_Chrome__read_page, mcp__Claude_in_Chrome__get_page_text, mcp__Claude_in_Chrome__javascript_tool, mcp__Claude_in_Chrome__form_input
---

# Sci-Hub Paper Downloader

Download academic papers from Sci-Hub by DOI using Chrome browser automation.

## Prerequisites

- Chrome browser open with Claude in Chrome extension connected
- A JSON file containing papers with DOI fields (e.g., `papers-to-acquire.json`)
- A target download folder for PDFs

## Input

The skill reads from a JSON array of paper objects. Each object should have at minimum:
- `doi` — the DOI string (e.g., `"10.1186/s40359-020-00423-3"`)
- `pmid` — PubMed ID (used for tracking)
- `first_author` — for filename generation
- `year` — for filename generation
- `title` — for filename generation

Default input file: `/Users/samrosehill/Desktop/Dental Personality Research/papers-to-acquire.json`
Default download target: `/Users/samrosehill/Desktop/Dental Personality Research/papers/downloads/`

## Workflow

For each paper with a DOI that has not already been downloaded:

### Step 1: Navigate to Sci-Hub
Navigate the browser tab to `https://sci-hub.st` (primary mirror).
Fallback mirrors: `https://sci-hub.ru`, `https://sci-hub.ren`

### Step 2: Enter DOI
- Find the search/input box on the Sci-Hub homepage
- Clear any existing text
- Type/paste the DOI into the search box
- Press Enter or click the search/open button

### Step 3: Check Result
- Wait 2-3 seconds for the page to load
- Take a screenshot to assess the result
- Check the page for one of three outcomes:
  1. **Paper found**: PDF is displayed or a download link/button is visible
  2. **Not found**: Page says "article not found" or is empty
  3. **Captcha**: Page shows a captcha challenge

### Step 4: Download (if found)
Use JavaScript to extract the PDF URL from the page. Sci-Hub stores it in a meta tag:

```javascript
// Extract PDF URL from meta tag
var meta = document.querySelector('meta[name="citation_pdf_url"]');
var pdfPath = meta ? meta.getAttribute('content') : null;
pdfPath;
```

If the PDF path is found, construct the full URL (prepend `https://sci-hub.st` if path is relative) and trigger a download:

```javascript
// Download the PDF via blob fetch
var pdfUrl = 'https://sci-hub.st' + pdfPath;
window._dlStatus = 'fetching';
fetch(pdfUrl)
  .then(function(r) { return r.blob(); })
  .then(function(blob) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = 'FILENAME.pdf';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
    window._dlStatus = 'done:' + blob.size;
  })
  .catch(function(e) { window._dlStatus = 'error:' + e.message; });
'started';
```

Then check `window._dlStatus` after a few seconds to confirm download completed.

### Step 5: Handle failures
- **Not found**: Log the DOI as unavailable on Sci-Hub and move to next paper
- **Captcha**: If a captcha appears, take a screenshot. The user may need to solve it manually. After solving, retry the current DOI.
- **Error**: Log and move on

### Step 6: Return to homepage and repeat
Navigate back to `https://sci-hub.st` and process the next DOI.

## File Naming Convention

Downloaded files should be named: `{Surname}_{Year}_{FirstFourTitleWords}.pdf`

Where:
- `Surname` = last name of first author (alphanumeric only)
- `Year` = 4-digit publication year
- `FirstFourTitleWords` = first 4 words of title (alphanumeric, underscored)

Example: `Lewis_2020_The_big_five_personality.pdf`

## After Download

Once a PDF lands in `~/Downloads/`, move it to the target download folder with the correct filename.

## Tracking

After processing, report:
- Total papers attempted
- Successfully downloaded
- Not found on Sci-Hub
- Captcha blocks
- Other errors

## Rate Limiting

Use natural browser interaction pace. No need for artificial delays — the browser page load time provides natural spacing. If captchas start appearing frequently, slow down and consider switching mirrors.

## Mirror Rotation

If one mirror becomes unresponsive or starts blocking:
1. `https://sci-hub.st` (primary)
2. `https://sci-hub.ru` (fallback 1)
3. `https://sci-hub.ren` (fallback 2)
