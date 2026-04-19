#!/usr/bin/env python3
"""
substack-publisher.py

Prepares samrosehill.com review articles for Substack publishing.
Outputs a JSON payload that can be POSTed to Substack's API.

Usage:
  python3 scripts/substack-publisher.py <slug>                # output JSON payload
  python3 scripts/substack-publisher.py <slug> --js            # output ready-to-run JS for Chrome

The --js flag outputs JavaScript that can be executed in a Chrome tab
on substack.com to create the draft and apply tags using the browser's
existing authenticated session. No cookies file needed.

Pipeline integration:
  1. Python parses markdown, selects tags, builds ProseMirror body
  2. Claude executes the JS output in Chrome (already logged into Substack)
  3. Draft is created + tags applied in ~2 seconds via fetch() calls
"""

import sys
import re
import json
import argparse
import textwrap
import yaml
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONTENT_DIR = PROJECT_ROOT / "src" / "content" / "reviews"
SITE_URL = "https://samrosehill.com"
USER_ID = 159918627

# Tag priority tiers (reused from substack-formatter.py)
TAG_PRIORITY = {
    "prosthodontics": 1, "implantology": 1, "digital dentistry": 1,
    "periodontology": 1, "restorative dentistry": 1,
    "zirconia": 2, "CAD/CAM": 2, "shade matching": 2, "3D printing": 2,
    "lithium disilicate": 2, "dental implants": 2, "soft tissue": 2,
    "colour science": 2, "robot-assisted surgery": 2, "immediate implant placement": 2,
    "systematic review": 3, "ten-year study": 3, "colour stability": 3,
    "surgical accuracy": 3, "dimensional accuracy": 3, "crown survival": 3,
    "peri-implantitis": 3, "crestal bone loss": 3,
}


def parse_frontmatter(filepath):
    """Parse YAML frontmatter and markdown body from a file."""
    text = filepath.read_text(encoding="utf-8")
    match = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", text, re.DOTALL)
    if not match:
        raise ValueError(f"No frontmatter found in {filepath}")
    fm = yaml.safe_load(match.group(1))
    body = match.group(2).strip()
    return fm, body


def select_tags(tags, max_tags=5):
    """Select top N tags by priority tier."""
    sorted_tags = sorted(tags, key=lambda t: TAG_PRIORITY.get(t, 4))
    return sorted_tags[:max_tags]


def parse_inline(text):
    """Convert inline markdown (bold, italic, links) to ProseMirror marks."""
    nodes = []
    # Pattern matches: **bold**, *italic*, [text](url)
    pattern = r'(\*\*(.+?)\*\*|\*(.+?)\*|\[(.+?)\]\((.+?)\))'
    last_end = 0

    for m in re.finditer(pattern, text):
        # Add plain text before this match
        if m.start() > last_end:
            plain = text[last_end:m.start()]
            if plain:
                nodes.append({"type": "text", "text": plain})

        if m.group(2):  # bold
            nodes.append({"type": "text", "text": m.group(2), "marks": [{"type": "strong"}]})
        elif m.group(3):  # italic
            nodes.append({"type": "text", "text": m.group(3), "marks": [{"type": "em"}]})
        elif m.group(4) and m.group(5):  # link
            link_mark = {"type": "link", "attrs": {"href": m.group(5)}}
            link_nodes = parse_inline(m.group(4))
            for node in link_nodes:
                node["marks"] = node.get("marks", []) + [link_mark]
                nodes.append(node)

        last_end = m.end()

    # Add remaining plain text
    if last_end < len(text):
        remaining = text[last_end:]
        if remaining:
            nodes.append({"type": "text", "text": remaining})

    if not nodes:
        nodes.append({"type": "text", "text": text})

    return nodes


def markdown_to_prosemirror(markdown):
    """Convert markdown to ProseMirror document JSON."""
    lines = markdown.split("\n")
    content = []
    i = 0

    while i < len(lines):
        line = lines[i]

        # Heading
        heading_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if heading_match:
            level = len(heading_match.group(1))
            text = heading_match.group(2)
            content.append({
                "type": "heading",
                "attrs": {"level": level},
                "content": parse_inline(text)
            })
            i += 1
            continue

        # Horizontal rule
        if re.match(r'^---\s*$', line):
            content.append({"type": "horizontal_rule"})
            i += 1
            continue

        # Blockquote (collect consecutive > lines)
        if line.startswith('>'):
            quote_lines = []
            while i < len(lines) and lines[i].startswith('>'):
                quote_lines.append(lines[i].lstrip('>').strip())
                i += 1
            quote_text = ' '.join(quote_lines)
            content.append({
                "type": "blockquote",
                "content": [{"type": "paragraph", "content": parse_inline(quote_text)}]
            })
            continue

        # Bullet list
        if re.match(r'^[\*\-]\s+', line):
            items = []
            while i < len(lines) and re.match(r'^[\*\-]\s+', lines[i]):
                item_text = re.sub(r'^[\*\-]\s+', '', lines[i])
                items.append({
                    "type": "list_item",
                    "content": [{"type": "paragraph", "content": parse_inline(item_text)}]
                })
                i += 1
            content.append({"type": "bullet_list", "content": items})
            continue

        # Empty line (skip)
        if not line.strip():
            i += 1
            continue

        # Regular paragraph
        content.append({
            "type": "paragraph",
            "content": parse_inline(line)
        })
        i += 1

    return {"type": "doc", "content": content}


def build_payload(slug):
    """Build the full Substack API payload for an article."""
    filepath = CONTENT_DIR / f"{slug}.md"
    if not filepath.exists():
        print(f"ERROR: No article found at {filepath}", file=sys.stderr)
        sys.exit(1)

    fm, body = parse_frontmatter(filepath)
    title = fm.get("title", "Untitled")
    subtitle = textwrap.shorten(fm.get("description", ""), width=160, placeholder="...")
    tags = fm.get("tags", [])
    selected_tags = select_tags(tags)

    # Convert body to ProseMirror format
    pm_body = markdown_to_prosemirror(body)

    # Append cross-posting byline as pre-built ProseMirror nodes
    # (avoids markdown parsing issues with links inside italic text)
    pm_body["content"].append({"type": "horizontal_rule"})
    pm_body["content"].append({
        "type": "paragraph",
        "content": [
            {"type": "text", "text": "This article was originally published on ", "marks": [{"type": "em"}]},
            {"type": "text", "text": "samrosehill.com", "marks": [
                {"type": "em"},
                {"type": "link", "attrs": {"href": f"{SITE_URL}/journal/{slug}"}}
            ]},
            {"type": "text", "text": ".", "marks": [{"type": "em"}]},
        ]
    })

    draft_payload = {
        "draft_title": title,
        "draft_subtitle": subtitle,
        "draft_body": json.dumps(pm_body),
        "draft_bylines": [{"id": USER_ID, "is_guest": False}],
        "audience": "everyone",
        "section_chosen": True,
        "write_comment_permissions": "everyone",
    }

    return {
        "draft": draft_payload,
        "tags": selected_tags,
        "slug": slug,
        "title": title,
    }


def output_js(payload, draft_only=False):
    """Output JavaScript that creates draft + applies tags via fetch()."""
    draft_json = json.dumps(payload["draft"])
    tags_json = json.dumps(payload["tags"])

    publish_block = ""
    if not draft_only:
        publish_block = """
  // Prepublish check
  await fetch('/api/v1/drafts/' + draft.id + '/prepublish', {credentials: 'include'});
  // Publish
  const publishResp = await fetch('/api/v1/drafts/' + draft.id + '/publish', {
    method: 'POST', credentials: 'include',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({send: true, share_automatically: false})
  });
  result.publish_status = publishResp.status;
  result.publish_response = await publishResp.json().catch(async () => ({text: await publishResp.text()}));
  result.published = publishResp.ok;"""

    js = f"""(async () => {{
  const result = {{}};

  // 1. Create draft
  const draftResp = await fetch('/api/v1/drafts', {{
    method: 'POST', credentials: 'include',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({draft_json})
  }});
  if (!draftResp.ok) {{
    result.create_status = draftResp.status;
    result.create_error = await draftResp.json().catch(async () => ({{text: await draftResp.text()}}));
    return JSON.stringify(result);
  }}
  const draft = await draftResp.json();
  result.draft_id = draft.id;
  result.title = draft.draft_title;

  // 2. Apply tags
  const tags = {tags_json};
  const existingTags = await (await fetch('/api/v1/publication/post-tag', {{credentials: 'include'}})).json();
  result.tags_applied = [];

  for (const tagName of tags) {{
    let tagId;
    const existing = existingTags.find(t => t.name === tagName);
    if (existing) {{
      tagId = existing.id;
    }} else {{
      const created = await (await fetch('/api/v1/publication/post-tag', {{
        method: 'POST', credentials: 'include',
        headers: {{'Content-Type': 'application/json'}},
        body: JSON.stringify({{name: tagName}})
      }})).json();
      tagId = created.id;
    }}
    await fetch('/api/v1/post/' + draft.id + '/tag/' + tagId, {{
      method: 'POST', credentials: 'include'
    }});
    result.tags_applied.push(tagName);
  }}
{publish_block}

  return JSON.stringify(result);
}})()"""
    return js


def main():
    parser = argparse.ArgumentParser(description="Prepare articles for Substack publishing")
    parser.add_argument("slug", nargs="?", help="Article slug to publish")
    parser.add_argument("--draft-only", action="store_true", help="Create draft without publishing")
    parser.add_argument("--js", action="store_true", help="Output JavaScript for Chrome execution")
    parser.add_argument("--json", action="store_true", help="Output raw JSON payload")

    args = parser.parse_args()

    if not args.slug:
        parser.print_help()
        sys.exit(1)

    payload = build_payload(args.slug)

    if args.js:
        print(output_js(payload, draft_only=args.draft_only))
    elif args.json:
        print(json.dumps(payload, indent=2))
    else:
        # Default: output JS
        print(output_js(payload, draft_only=args.draft_only))


if __name__ == "__main__":
    main()
