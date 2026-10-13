#!/usr/bin/env python3
"""
For each OCR'd village-survey PDF:
  1. Find pages that contain an image (photograph or line drawing).
  2. Write a new PDF containing every image page plus the page before and after it.
  3. Build a table: one row per image title (caption) with the 5 most frequent
     words on the pages above/below, and Yes/No if any title word appears there.

The scans store text pages as 1-bit CCITT images, so images are found two ways:
  * Photographs are embedded as separate JPEG (DCTDecode) images.
  * Line drawings (jewellery, utensils, house plans...) are printed inside the
    same black-and-white scan as the text. They are found by rendering the page,
    blanking every OCR'd line of real words, and looking for large, dense blobs
    of ink that remain. Table rules are left behind too, but they are sparse
    thin lines, so a minimum ink density filters them out.

Requires: pdfminer.six, pikepdf, pandas, numpy, pillow, and poppler's pdftoppm.
Usage:    python3 image_context.py [pdf ...]
"""

import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd
import pikepdf
from PIL import Image
from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams, LTFigure, LTImage, LTTextContainer, LTTextLine

HERE = Path(__file__).resolve().parent
DEFAULT_PDFS = sorted(p.name for p in HERE.glob("*_ocr.pdf"))   # every *_ocr.pdf in this folder
OUT_DIR = HERE / "image_context_output"

MIN_IMAGE_AREA_FRAC = 0.05   # photo must cover >= 5% of the page
TOP_N = 5
DICT_PATH = Path("/usr/share/dict/words")
# Photo credits printed under captions, e.g. "Courtesy: W. H. Newell"
CREDIT_RE = re.compile(r"tesy|times\s+of\s+india|newell|krishan", re.I)

# Drawing detection (all sizes in PDF points, 72 pt = 1 inch)
RENDER_DPI = 50
CELL_PX = 4                  # pixels per grid cell when looking for ink blobs
CELL_INK_FRAC = 0.06         # a cell is "ink" if >= 6% of its pixels are dark
MIN_FIG_SIDE = 40            # a drawing part is at least 40 x 40 pt
MIN_FIG_DENSITY = 0.2        # ink cells / bbox cells; table rules are ~0.1
MAX_FIG_OCR_COVER = 0.5      # badly OCR'd text (Hindi, italics) still sits in OCR line boxes
MIN_PAGE_FIG_INK = 60        # page needs one drawing with >= 60 ink cells
MERGE_GAP = 15               # join drawing parts closer than this
CAPTION_GAP = 40             # caption must start within this distance below a drawing
NO_CAPTION = "(no caption found)"

STOPWORDS = set("""
a about above after again against all also am an and any are as at be because been
before being below between both but by can could did do does doing down during each
few for from further had has have having he her here hers him his how i if in into is
it its itself just me more most my no nor not now of off on once only or other our out
over own same she should so some such than that the their them then there these they
this those through to too under until up very was we were what when where which while
who whom why will with would you your yours one two three four five six also per may
shall upon thus however etc nil see table total
""".split())


# ---------------------------------------------------------------- PDF parsing
def iter_items(container):
    """Yield every image and text line on a page, descending into figures."""
    for obj in container:
        if isinstance(obj, LTImage):
            yield obj
        elif isinstance(obj, LTFigure):
            yield from iter_items(obj)
        elif isinstance(obj, LTTextContainer):
            for line in obj:
                if isinstance(line, LTTextLine):
                    yield line


def is_photo(img, page_area):
    filt = str(img.stream.get("Filter"))
    if "CCITT" in filt or "DCT" not in filt and "JPX" not in filt:
        return False
    w, h = img.x1 - img.x0, img.y1 - img.y0
    return w * h >= MIN_IMAGE_AREA_FRAC * page_area


def read_pdf(path):
    """Return a list of pages. Line boxes are (x0, top, x1, bottom, text) in
    points measured from the top-left corner of the page."""
    pages = []
    for i, layout in enumerate(extract_pages(str(path), laparams=LAParams()), start=1):
        page_area = layout.width * layout.height
        has_photo, lines = False, []
        for item in iter_items(layout):
            if isinstance(item, LTImage):
                has_photo = has_photo or is_photo(item, page_area)
            else:
                txt = item.get_text().strip()
                if txt:
                    lines.append((item.x0, layout.height - item.y1,
                                  item.x1, layout.height - item.y0, txt))
        pages.append({
            "num": i,
            "width": layout.width,
            "height": layout.height,
            "has_photo": has_photo,
            "drawings": [],
            "lines": lines,
            "text": "\n".join(l[4] for l in lines),
        })
    return pages


# ---------------------------------------------------------------- vocabulary
def tokenize(text):
    return re.findall(r"[a-z]+", text.lower())


def load_dictionary():
    if not DICT_PATH.exists():
        return set()
    return {w.strip().lower() for w in DICT_PATH.read_text(errors="ignore").splitlines()
            if w.strip().isalpha()}


def build_vocab(pages, dictionary):
    """Real words = English dictionary words + words recurring in the book's
    text pages (keeps local names like Gaddi, Gujjar, Brahmaur; drops OCR noise)."""
    counts = Counter(w for p in pages if not p["has_photo"] for w in tokenize(p["text"]))
    local = {w for w, c in counts.items() if c >= 3 and len(w) >= 3}
    return dictionary | local


def norm(word):
    """Light stemming so 'blossoms' matches 'blossom', 'dances' matches 'dance'."""
    for suf in ("ies", "es", "s"):
        if word.endswith(suf) and len(word) - len(suf) >= 3:
            return word[: -len(suf)] + ("y" if suf == "ies" else "")
    return word


def content_words(text, vocab):
    return [w for w in tokenize(text)
            if len(w) >= 3 and w not in STOPWORDS and w in vocab]


def is_real_text(text, vocab):
    """True for a line of body text (words or numbers), False for OCR noise
    read out of a drawing."""
    tokens = [t.lower().strip(".,;:()[]’'\"-—") for t in text.split()]
    tokens = [t for t in tokens if t]
    if not tokens:
        return False
    good = [t for t in tokens
            if (t.isalpha() and t in vocab) or re.fullmatch(r"[\d./-]+", t)]
    return len(good) / len(tokens) >= 0.5


# ---------------------------------------------------------------- drawings
def render_pages(path, tmpdir):
    """Render every page to a small greyscale bitmap; return {page_num: file}."""
    subprocess.run(["pdftoppm", "-r", str(RENDER_DPI), "-gray", str(path),
                    f"{tmpdir}/p"], check=True)
    return {int(f.stem.rsplit("-", 1)[1]): f for f in Path(tmpdir).glob("p-*.pgm")}


def ink_components(grid):
    """Connected components (4-neighbour) of True cells in a 2-D bool array."""
    seen = np.zeros_like(grid)
    comps = []
    for i, j in zip(*np.nonzero(grid)):
        if seen[i, j]:
            continue
        stack, cells = [(i, j)], []
        seen[i, j] = True
        while stack:
            y, x = stack.pop()
            cells.append((y, x))
            for yy, xx in ((y + 1, x), (y - 1, x), (y, x + 1), (y, x - 1)):
                if 0 <= yy < grid.shape[0] and 0 <= xx < grid.shape[1] \
                        and grid[yy, xx] and not seen[yy, xx]:
                    seen[yy, xx] = True
                    stack.append((yy, xx))
        comps.append(cells)
    return comps


def merge_boxes(boxes):
    """Merge [x0, top, x1, bottom, ink] boxes that overlap or nearly touch."""
    boxes = [list(b) for b in boxes]
    merged = True
    while merged:
        merged = False
        for a in range(len(boxes)):
            for b in range(a + 1, len(boxes)):
                A, B = boxes[a], boxes[b]
                if (A[0] - MERGE_GAP < B[2] and B[0] - MERGE_GAP < A[2] and
                        A[1] - MERGE_GAP < B[3] and B[1] - MERGE_GAP < A[3]):
                    boxes[a] = [min(A[0], B[0]), min(A[1], B[1]),
                                max(A[2], B[2]), max(A[3], B[3]), A[4] + B[4]]
                    del boxes[b]
                    merged = True
                    break
            if merged:
                break
    return boxes


def looks_like_table(block):
    """Once their text is blanked, ruled tables leave horizontal rules (rows that
    are mostly ink) but almost no vertical structure. Drawings either have many
    columns with substantial ink, or no rule-like rows at all (e.g. a flute)."""
    rule_rows = (block.mean(axis=1) >= 0.6).sum()
    inked_cols = (block.mean(axis=0) >= 0.4).sum()
    return rule_rows >= 1 and inked_cols <= 4


def find_drawings(page, bitmap_file, vocab):
    """Return drawing boxes (x0, top, x1, bottom) in points, or [] if none."""
    dark = np.array(Image.open(bitmap_file)) < 128
    H, W = dark.shape
    sx, sy = W / page["width"], H / page["height"]

    # Blank out every OCR'd line of real text; what is left is pictures/rules/noise.
    # Also remember where any OCR line (even garbage) was found.
    in_line = np.zeros_like(dark)
    for x0, top, x1, bottom, txt in page["lines"]:
        rows = slice(max(int(top * sy) - 1, 0), int(bottom * sy) + 2)
        cols = slice(max(int(x0 * sx) - 1, 0), int(x1 * sx) + 2)
        in_line[rows, cols] = True
        if is_real_text(txt, vocab):
            dark[rows, cols] = False

    gh, gw = H // CELL_PX, W // CELL_PX
    in_line = in_line[:gh * CELL_PX, :gw * CELL_PX].reshape(gh, CELL_PX, gw, CELL_PX) \
        .mean(axis=(1, 3)) >= 0.5
    ink = dark[:gh * CELL_PX, :gw * CELL_PX].reshape(gh, CELL_PX, gw, CELL_PX) \
        .mean(axis=(1, 3)) >= CELL_INK_FRAC
    grown = ink.copy()                       # dilate by one cell to join strokes
    grown[1:] |= ink[:-1]; grown[:-1] |= ink[1:]
    grown[:, 1:] |= ink[:, :-1]; grown[:, :-1] |= ink[:, 1:]

    parts = []
    for cells in ink_components(grown):
        ys, xs = zip(*cells)
        r0, r1, c0, c1 = min(ys), max(ys) + 1, min(xs), max(xs) + 1
        n_ink = int(ink[r0:r1, c0:c1].sum())
        ocr_cover = (ink & in_line)[r0:r1, c0:c1].sum() / max(n_ink, 1)
        box = [c0 * CELL_PX / sx, r0 * CELL_PX / sy, c1 * CELL_PX / sx, r1 * CELL_PX / sy, n_ink]
        if (box[2] - box[0] >= MIN_FIG_SIDE and box[3] - box[1] >= MIN_FIG_SIDE
                and n_ink / ((r1 - r0) * (c1 - c0)) >= MIN_FIG_DENSITY
                and ocr_cover <= MAX_FIG_OCR_COVER
                and not looks_like_table(ink[r0:r1, c0:c1])):
            parts.append(box)

    figures = merge_boxes(parts)
    if not any(f[4] >= MIN_PAGE_FIG_INK for f in figures):
        return []
    return [tuple(f[:4]) for f in figures]


# ---------------------------------------------------------------- captions
def is_caption_line(text, vocab):
    """A caption is a line made (mostly) of real words, not OCR noise."""
    if CREDIT_RE.search(text):
        return False
    tokens = [t.lower().strip("’'-") for t in text.split()]
    tokens = [re.sub(r"[’']s$", "", t) for t in tokens]          # Gujjar's -> gujjar
    tokens = [t for t in tokens if t and t not in STOPWORDS]     # 'a', 'the' are neutral
    if not tokens:
        return False
    good = [t for t in tokens if t.isalpha() and t in vocab]
    return any(len(t) >= 4 for t in good) and len(good) / len(tokens) >= 0.5


def clean(text):
    return re.sub(r"\s+", " ", text).strip()


def photo_captions(page, vocab):
    """Clean English text lines on a photo page are its captions. Lines that
    sit just below another caption, or start in lowercase, continue it."""
    lines = sorted((l for l in page["lines"] if is_caption_line(l[4], vocab)),
                   key=lambda l: l[1])  # top to bottom
    captions = []
    for x0, top, x1, bottom, txt in lines:
        if captions:
            px0, ptop, px1, pbottom, ptxt = captions[-1]
            close_below = top - pbottom < 0.8 * (pbottom - ptop) and x0 < px1 and x1 > px0
            if close_below or txt[0].islower():
                captions[-1] = (min(x0, px0), ptop, max(x1, px1), bottom, f"{ptxt} {txt}")
                continue
        if txt[0].islower():
            continue  # stray fragment with nothing to attach to
        captions.append((x0, top, x1, bottom, txt))
    return [clean(c[4]) for c in captions]


WORD_SHAPE = re.compile(r"^[(‘'\"]?[A-Za-z][A-Za-z’'\-]*[.,;:)’'\"]*$")


def looks_like_caption(text):
    """Short line of word-shaped tokens. Captions under drawings are often
    local terms (Kulth, Runka, Gharat Chhatta), so no dictionary check here."""
    tokens = [t for t in text.split() if re.search(r"\w", t)]   # drop stray ';' etc.
    if (not 1 <= len(tokens) <= 6 or text.rstrip().endswith("-") or text.isupper()
            or CREDIT_RE.search(text)):
        return False
    words = [t for t in tokens if WORD_SHAPE.match(t)]
    return (text[0].isupper() and len(words) / len(tokens) >= 0.75
            and any(len(w.strip(".,;:()’'\"")) >= 3 for w in words))


def drawing_captions(page):
    """For each drawing, take the short caption-like lines just below it
    (they may also sit inside the bottom of the drawing's box, since unknown
    words are not blanked out). Lines with another line directly beneath them
    belong to a paragraph and are skipped."""
    lines = page["lines"]

    def in_paragraph(line):
        x0, top, x1, bottom, _ = line
        h = bottom - top
        below = any(o is not line and -0.5 * h <= o[1] - bottom < 0.8 * h
                    and o[0] < x1 and o[2] > x0 for o in lines)
        beside = any(o is not line and o[1] < bottom - h / 2 and o[3] > top + h / 2
                     and (0 <= o[0] - x1 < 2 * h or 0 <= x0 - o[2] < 2 * h) for o in lines)
        return below or beside

    candidates = [l for l in lines if looks_like_caption(l[4]) and not in_paragraph(l)]
    captions = []
    for fx0, ftop, fx1, fbottom in sorted(page["drawings"], key=lambda f: (f[1], f[0])):
        # A box may hold several side-by-side drawings, so keep every caption
        # along its bottom edge, left to right.
        near = [l for l in candidates
                if -30 <= l[1] - fbottom <= CAPTION_GAP
                and fx0 - 20 <= (l[0] + l[2]) / 2 <= fx1 + 20]
        for l in sorted(near, key=lambda l: l[0]):
            title = clean(l[4]).strip(" .,;:")
            if title not in captions:
                captions.append(title)
    return captions


# ---------------------------------------------------------------- outputs
def write_context_pdf(src, image_pages, n_pages, dest):
    keep = sorted({q for p in image_pages for q in (p - 1, p, p + 1) if 1 <= q <= n_pages})
    with pikepdf.open(src) as pdf, pikepdf.new() as out:
        for q in keep:
            out.pages.append(pdf.pages[q - 1])
        out.save(dest)
    return keep


def build_rows(doc_name, pages, vocab):
    by_num = {p["num"]: p for p in pages}
    rows = []
    for page in pages:
        if not (page["has_photo"] or page["drawings"]):
            continue
        n = page["num"]
        neighbours = [by_num[q] for q in (n - 1, n + 1) if q in by_num]
        context = content_words(" ".join(p["text"] for p in neighbours), vocab)
        top = Counter(context).most_common(TOP_N)
        context_norm = {norm(w) for w in context}

        if page["has_photo"]:
            kind, captions = "Photograph", photo_captions(page, vocab)
        else:
            kind, captions = "Drawing", drawing_captions(page)
        for title in captions or [NO_CAPTION]:
            title_words = {norm(w) for w in content_words(title, vocab)} \
                if title != NO_CAPTION else set()
            matched = sorted(title_words & context_norm)
            rows.append({
                "Document": doc_name,
                "Image Page": n,
                "Image Type": kind,
                "Context Pages": ", ".join(str(p["num"]) for p in neighbours),
                "Image Title": title,
                "Top 5 Words (above + below)": ", ".join(f"{w} ({c})" for w, c in top),
                "Title Word in Context": "Yes" if matched else "No",
                "Matched Words": ", ".join(matched),
            })
    return rows


def main(pdf_names):
    OUT_DIR.mkdir(exist_ok=True)
    dictionary = load_dictionary()
    all_rows = []
    for name in pdf_names:
        src = (HERE / name) if not Path(name).is_absolute() else Path(name)
        doc = src.stem.replace("_ocr", "")
        print(f"[{doc}] reading {src.name} ...")
        pages = read_pdf(src)
        vocab = build_vocab(pages, dictionary)

        with tempfile.TemporaryDirectory() as tmp:
            bitmaps = render_pages(src, tmp)
            for page in pages:
                if not page["has_photo"]:
                    page["drawings"] = find_drawings(page, bitmaps[page["num"]], vocab)

        photo_pages = [p["num"] for p in pages if p["has_photo"]]
        drawing_pages = [p["num"] for p in pages if p["drawings"]]
        dest = OUT_DIR / f"{doc}_image_pages.pdf"
        kept = write_context_pdf(src, photo_pages + drawing_pages, len(pages), dest)
        print(f"[{doc}] photo pages:   {photo_pages}")
        print(f"[{doc}] drawing pages: {drawing_pages}")
        print(f"[{doc}] wrote {dest.name} ({len(kept)} pages)")

        all_rows.extend(build_rows(doc, pages, vocab))

    if not all_rows:
        print("\nNo images found in any document; no table written.")
        return
    df = pd.DataFrame(all_rows)
    csv_path = OUT_DIR / "image_context_table.csv"
    df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    try:
        df.to_excel(OUT_DIR / "image_context_table.xlsx", index=False)
    except ImportError:
        pass  # openpyxl not installed; CSV is enough
    print(f"\nTable: {csv_path} ({len(df)} rows)")
    with pd.option_context("display.max_colwidth", 60, "display.width", 200):
        print(df[["Document", "Image Page", "Image Type", "Image Title",
                  "Top 5 Words (above + below)", "Title Word in Context"]].to_string(index=False))


if __name__ == "__main__":
    main(sys.argv[1:] or DEFAULT_PDFS)
