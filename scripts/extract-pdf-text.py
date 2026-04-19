#!/usr/bin/env python3
"""
extract-pdf-text.py

Pre-extract text from journal PDFs so the publication pipeline can read
lightweight .md files instead of token-expensive PDF images.

Usage:
  python3 scripts/extract-pdf-text.py --all              # extract all PDFs missing a .md companion
  python3 scripts/extract-pdf-text.py --all --force       # re-extract all, overwriting existing .md
  python3 scripts/extract-pdf-text.py <path/to/paper.pdf> # extract a single PDF

Output:
  Creates a .md file alongside each PDF with the same basename.
  e.g., CIDR_Lee_cid.70064.pdf → CIDR_Lee_cid.70064.md

  Tables detected via PyMuPDF's find_tables() are appended as markdown tables.
"""

import sys
import argparse
from pathlib import Path

import fitz  # PyMuPDF

PROJECT_ROOT = Path(__file__).resolve().parent.parent
JOURNALS_DIR = PROJECT_ROOT / "2MP Project" / "journals"


def extract_tables(page) -> list[str]:
    """Extract tables from a page as markdown-formatted strings."""
    tables = []
    try:
        found = page.find_tables()
        for table in found.tables:
            data = table.extract()
            if not data or len(data) < 2:
                continue
            # Build markdown table
            headers = data[0]
            # Clean None values
            headers = [str(h) if h else "" for h in headers]
            rows = data[1:]

            md = "| " + " | ".join(headers) + " |\n"
            md += "| " + " | ".join(["---"] * len(headers)) + " |\n"
            for row in rows:
                cells = [str(c) if c else "" for c in row]
                md += "| " + " | ".join(cells) + " |\n"
            tables.append(md)
    except Exception:
        pass  # find_tables() not available or failed — skip
    return tables


def extract_text(pdf_path: Path) -> str:
    doc = fitz.open(str(pdf_path))
    pages = []
    all_tables = []
    for i, page in enumerate(doc):
        pages.append(page.get_text())
        # Extract tables from this page
        tables = extract_tables(page)
        for j, tbl in enumerate(tables, 1):
            all_tables.append(f"Table (page {i + 1}):\n\n{tbl}")
    doc.close()

    text = "\n\n".join(pages)

    # Append structured tables at the end if any were found
    if all_tables:
        text += "\n\n---\n\n## Extracted Tables\n\n"
        text += "\n\n".join(all_tables)

    return text


def process_pdf(pdf_path: Path, force: bool = False) -> str:
    md_path = pdf_path.with_suffix(".md")
    if md_path.exists() and not force:
        return "skipped"
    try:
        text = extract_text(pdf_path)
        if len(text.strip()) < 100:
            return "empty"
        md_path.write_text(text, encoding="utf-8")
        return "ok"
    except Exception as e:
        return f"failed: {e}"


def run_all(force: bool = False):
    pdfs = sorted(JOURNALS_DIR.rglob("*.[pP][dD][fF]"))
    total = len(pdfs)
    ok = 0
    skipped = 0
    empty = 0
    failed = 0

    print(f"Found {total} PDFs in {JOURNALS_DIR}")
    for i, pdf in enumerate(pdfs, 1):
        result = process_pdf(pdf, force)
        if result == "ok":
            ok += 1
        elif result == "skipped":
            skipped += 1
        elif result == "empty":
            empty += 1
            print(f"  EMPTY: {pdf.relative_to(PROJECT_ROOT)}")
        else:
            failed += 1
            print(f"  FAIL:  {pdf.relative_to(PROJECT_ROOT)} — {result}")

        if i % 200 == 0:
            print(f"  Progress: {i}/{total} ({ok} extracted, {skipped} skipped)")

    print(f"\nDone. {ok} extracted, {skipped} skipped, {empty} empty, {failed} failed (of {total} total)")


def main():
    parser = argparse.ArgumentParser(description="Extract text from journal PDFs")
    parser.add_argument("pdf", nargs="?", help="Single PDF path to extract")
    parser.add_argument("--all", action="store_true", help="Extract all PDFs in journals/")
    parser.add_argument("--force", action="store_true", help="Overwrite existing .md files")
    args = parser.parse_args()

    if args.all:
        run_all(args.force)
    elif args.pdf:
        pdf_path = Path(args.pdf)
        if not pdf_path.is_absolute():
            pdf_path = PROJECT_ROOT / pdf_path
        if not pdf_path.exists():
            print(f"Error: {pdf_path} not found")
            sys.exit(1)
        result = process_pdf(pdf_path, args.force)
        md_path = pdf_path.with_suffix(".md")
        if result == "ok":
            print(f"Extracted: {md_path}")
        elif result == "skipped":
            print(f"Already exists: {md_path} (use --force to overwrite)")
        else:
            print(f"Failed: {result}")
            sys.exit(1)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
