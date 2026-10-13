#!/usr/bin/env python3
"""
For each OCR'd village-survey PDF:
  1. Find blocks of Hindi / Gaddi (Devanagari) text - folk songs, poems,
     sentence lists - and where each starts and ends.
  2. Send each block to Claude together with the page image(s), with the block
     outlined in red. Claude corrects the noisy OCR, translates it into
     English, and reports the book's own English version if one is printed.
  3. Write a stats table (CSV) and a PDF of the Hindi pages for each book.

Translations are cached in hindi_output/translations_cache.json, so re-running
only pays for blocks that are new or whose OCR text changed.

Requires: everything image_context.py needs, plus the `anthropic` SDK
(installed in ./.venv) and an ANTHROPIC_API_KEY for the translation step.

Usage:
  .venv/bin/python hindi_poems.py                 # detect + translate
  .venv/bin/python hindi_poems.py --detect-only   # no API calls
  .venv/bin/python hindi_poems.py maingal_ocr.pdf # one book
"""

import argparse
import base64
import hashlib
import io
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pandas as pd
import pikepdf
from PIL import Image, ImageDraw

from image_context import DEFAULT_PDFS, HERE, read_pdf

OUT_DIR = HERE / "hindi_output"
CACHE_PATH = OUT_DIR / "translations_cache.json"

MODEL = "claude-opus-5-5"
RENDER_DPI = 150             # page images sent to Claude
MIN_DEVANAGARI = 3           # a Hindi line has at least this many Devanagari chars...
BLOCK_GAP_LINES = 2.5        # ...and joins a block if within 2.5 line heights of it
MIN_GOOD_WORDS = 10          # a block needs this many well-formed Devanagari words...
MIN_GOOD_WORD_FRAC = 0.85    # ...making up most of its Devanagari tokens
PAGE_EDGE_FRAC = 0.25        # blocks this close to a page edge may continue across pages

DEVANAGARI = re.compile("[ऀ-ॿ]")
DEVANAGARI_WORD = re.compile("[ऀ-ॣ॰-ॿ]+")   # excludes Devanagari digits
LATIN = re.compile(r"[A-Za-z]")


# ---------------------------------------------------------------- detection
def is_hindi_line(text):
    """OCR'd Devanagari often has Latin junk mixed in ('तु करहा हैं ATT या'),
    so a line counts as Hindi when Devanagari is at least as common as Latin."""
    dev = len(DEVANAGARI.findall(text))
    return dev >= MIN_DEVANAGARI and dev >= len(LATIN.findall(text))


def is_real_hindi(text):
    """The Hindi OCR also 'reads' dotted leaders, table rules and smudges as
    Devanagari (e.g. 'च्च्ण्म्न्च्न्न्व्', '००००'). Real words are short with few
    conjuncts; junk has long virama chains and repeated letters."""
    words = DEVANAGARI_WORD.findall(text)
    good = [w for w in words if 2 <= len(w) <= 10 and w.count("्") <= 2
            and not re.search(r"(.)\1\1", w)]
    return len(good) >= MIN_GOOD_WORDS and len(good) >= MIN_GOOD_WORD_FRAC * len(words)


def find_blocks(page):
    """Group a page's Hindi lines into blocks: lines in the same column
    (overlapping horizontally) with no big vertical gap between them."""
    lines = sorted((l for l in page["lines"] if is_hindi_line(l[4])), key=lambda l: l[1])
    blocks = []
    for x0, top, x1, bottom, txt in lines:
        h = bottom - top
        for b in blocks:
            if x0 < b["x1"] and x1 > b["x0"] and top - b["bottom"] <= BLOCK_GAP_LINES * h:
                b["lines"].append(txt)
                b["x0"], b["x1"] = min(b["x0"], x0), max(b["x1"], x1)
                b["bottom"] = max(b["bottom"], bottom)
                break
        else:
            blocks.append({"x0": x0, "x1": x1, "top": top, "bottom": bottom, "lines": [txt]})
    blocks = [b for b in blocks if is_real_hindi("\n".join(b["lines"]))]
    for b in blocks:
        b.update(page=page["num"], width=page["width"], height=page["height"])
    return sorted(blocks, key=lambda b: (b["top"], b["x0"]))


def position(block, edge):
    """Human-readable position of a block's top or bottom edge on its page."""
    col = "full width"
    if block["x1"] - block["x0"] < 0.6 * block["width"]:
        centre = (block["x0"] + block["x1"]) / 2
        col = "left column" if centre < block["width"] / 2 else "right column"
    y = block["top"] if edge == "top" else block["bottom"]
    return f"{col}, {round(100 * y / block['height'])}% down"


def detect_poems(pages):
    """Return poems: lists of page-blocks, merged when a block at the bottom
    of one page continues at the top of the next page in the same column."""
    poems = []
    for page in pages:
        for b in find_blocks(page):
            prev = poems[-1][-1] if poems else None
            continues = (
                prev is not None and prev["page"] == b["page"] - 1
                and prev["bottom"] > (1 - PAGE_EDGE_FRAC) * prev["height"]
                and b["top"] < PAGE_EDGE_FRAC * b["height"]
                and b["x0"] < prev["x1"] and b["x1"] > prev["x0"]
            )
            if continues:
                poems[-1].append(b)
            else:
                poems.append([b])
    return poems


# ---------------------------------------------------------------- translation
SYSTEM_PROMPT = """You are an expert in Hindi and in the Pahari dialects of Chamba \
district, Himachal Pradesh (Gaddi, Chambeali, Gujjari). You are helping a history \
student read 1961 Census of India village survey monographs.

You will receive scanned page image(s) with one block of Devanagari text outlined \
in red, plus the noisy OCR text of that block. The OCR often confuses conjuncts and \
replaces Devanagari words with Latin junk, so read the image and treat the OCR only \
as a hint. Work only on the outlined block.

Return:
- hindi_corrected: the block exactly as printed in Devanagari, line breaks kept.
- english_translation: a faithful line-by-line English translation. Keep local \
terms (e.g. chola, gaddan, pohal) in italics-free plain text with a short gloss in \
brackets the first time.
- book_english_version: if the page itself prints an English rendering of this \
block (beside or below it), copy it; otherwise an empty string.
- kind: what the block is.
- title: the heading printed for the block (e.g. "विवाह गीत"), or an empty string.
- printed_page: the page number printed on the first page image, or an empty string.
- dialect: your best judgement of the language/dialect.
- notes: words you could not read or are unsure about; empty string if none."""

RESULT_SCHEMA = {
    "type": "object",
    "properties": {
        "kind": {"type": "string",
                 "enum": ["song/poem", "sentence list", "prose", "glossary/terms", "other"]},
        "title": {"type": "string"},
        "printed_page": {"type": "string"},
        "dialect": {"type": "string"},
        "hindi_corrected": {"type": "string"},
        "english_translation": {"type": "string"},
        "book_english_version": {"type": "string"},
        "notes": {"type": "string"},
    },
    "required": ["kind", "title", "printed_page", "dialect", "hindi_corrected",
                 "english_translation", "book_english_version", "notes"],
    "additionalProperties": False,
}


def page_image_b64(pdf, block, tmpdir):
    """Render the block's page and outline the block in red; return base64 PNG."""
    n = block["page"]
    stem = f"{tmpdir}/pg{n}"
    subprocess.run(["pdftoppm", "-r", str(RENDER_DPI), "-png", "-singlefile",
                    "-f", str(n), "-l", str(n), str(pdf), stem], check=True)
    img = Image.open(f"{stem}.png").convert("RGB")
    s = img.width / block["width"]
    pad = 6
    ImageDraw.Draw(img).rectangle(
        [(block["x0"] - pad) * s, (block["top"] - pad) * s,
         (block["x1"] + pad) * s, (block["bottom"] + pad) * s],
        outline=(255, 0, 0), width=4)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return base64.standard_b64encode(buf.getvalue()).decode()


def translate(client, pdf, poem, tmpdir):
    import anthropic

    ocr = "\n".join(line for b in poem for line in b["lines"])
    content = []
    for b in poem:
        content.append({"type": "text", "text": f"PDF page {b['page']}:"})
        content.append({"type": "image", "source": {
            "type": "base64", "media_type": "image/png",
            "data": page_image_b64(pdf, b, tmpdir)}})
    content.append({"type": "text", "text": f"OCR text of the outlined block:\n{ocr}"})

    kwargs = dict(
        model=MODEL,
        max_tokens=16000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
        output_config={"effort": "high",
                       "format": {"type": "json_schema", "schema": RESULT_SCHEMA}},
    )
    try:
        try:
            # Preferred: with the server-side fallback beta (needs a recent SDK).
            response = client.beta.messages.create(
                **kwargs, betas=["server-side-fallback-2026-07-01"], fallbacks="default")
        except TypeError:
            # Older SDK without the beta arguments: plain call.
            try:
                response = client.messages.create(**kwargs)
            except TypeError:
                # Older SDK without output_config: ask for JSON in the prompt.
                kwargs.pop("output_config")
                kwargs["system"] = (SYSTEM_PROMPT + "\n\nReply with ONLY a JSON object "
                                    "with keys: " + ", ".join(RESULT_SCHEMA["required"]) + ".")
                response = client.messages.create(**kwargs)
    except anthropic.AuthenticationError:
        raise SystemExit("Claude API: authentication failed - set ANTHROPIC_API_KEY.")
    except anthropic.APIStatusError as e:
        return {"notes": f"API error {e.status_code}: {e.message}"}
    except anthropic.APIConnectionError:
        return {"notes": "API connection error"}

    if response.stop_reason == "refusal":
        return {"notes": "Claude declined to process this block"}
    if response.stop_reason == "max_tokens":
        return {"notes": "Response cut off (max_tokens)"}
    text = next(b.text for b in response.content if b.type == "text")
    text = re.sub(r"^```(?:json)?|```$", "", text.strip(), flags=re.M).strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"notes": "Could not parse model reply: " + text[:300]}


# ---------------------------------------------------------------- outputs
def write_pages_pdf(src, page_nums, dest):
    with pikepdf.open(src) as pdf, pikepdf.new() as out:
        for n in page_nums:
            out.pages.append(pdf.pages[n - 1])
        out.save(dest)


def load_cache():
    return json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("pdfs", nargs="*", default=DEFAULT_PDFS)
    ap.add_argument("--detect-only", action="store_true",
                    help="find Hindi blocks without calling the Claude API")
    args = ap.parse_args()

    OUT_DIR.mkdir(exist_ok=True)
    cache = load_cache()
    client = None
    if not args.detect_only:
        import anthropic
        client = anthropic.Anthropic()

    rows = []
    for name in args.pdfs:
        src = HERE / name if not Path(name).is_absolute() else Path(name)
        doc = src.stem.replace("_ocr", "")
        print(f"[{doc}] reading {src.name} ...")
        poems = detect_poems(read_pdf(src))
        pages = sorted({b["page"] for poem in poems for b in poem})
        if pages:
            write_pages_pdf(src, pages, OUT_DIR / f"{doc}_hindi_pages.pdf")
        print(f"[{doc}] {len(poems)} Hindi blocks on pages {pages}")

        with tempfile.TemporaryDirectory() as tmp:
            for i, poem in enumerate(poems, start=1):
                first, last = poem[0], poem[-1]
                ocr = "\n".join(line for b in poem for line in b["lines"])
                key = f"{doc}:{first['page']}:" + hashlib.sha1(ocr.encode()).hexdigest()[:12]

                result = cache.get(key, {})
                if client and not result.get("english_translation"):
                    print(f"[{doc}] translating block {i}/{len(poems)} "
                          f"(page {first['page']}) ...")
                    result = translate(client, src, poem, tmp)
                    cache[key] = result
                    CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False, indent=1))

                rows.append({
                    "Document": doc,
                    "Block": f"{doc}-{i:02d}",
                    "Kind": result.get("kind", ""),
                    "Title": result.get("title", ""),
                    "Start Page (PDF)": first["page"],
                    "Start Page (printed)": result.get("printed_page", ""),
                    "Starts At": position(first, "top"),
                    "End Page (PDF)": last["page"],
                    "Ends At": position(last, "bottom"),
                    "Lines": sum(len(b["lines"]) for b in poem),
                    "First Line (OCR)": first["lines"][0],
                    "Last Line (OCR)": last["lines"][-1],
                    "Dialect": result.get("dialect", ""),
                    "Hindi (OCR)": ocr,
                    "Hindi (corrected)": result.get("hindi_corrected", ""),
                    "English Translation": result.get("english_translation", ""),
                    "Book's Own English Version": result.get("book_english_version", ""),
                    "Notes": result.get("notes", ""),
                })

    if not rows:
        print("\nNo Hindi blocks found; no table written.")
        return
    df = pd.DataFrame(rows)
    csv_path = OUT_DIR / "hindi_poems_table.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")  # BOM so Excel shows Devanagari
    print(f"\nTable: {csv_path} ({len(df)} blocks)")
    with pd.option_context("display.max_colwidth", 40, "display.width", 200):
        print(df[["Block", "Start Page (PDF)", "Starts At", "End Page (PDF)", "Ends At",
                  "Lines", "Kind", "First Line (OCR)"]].to_string(index=False))


if __name__ == "__main__":
    sys.exit(main())
