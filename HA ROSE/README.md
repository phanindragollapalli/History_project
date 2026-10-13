# H. A. Rose Ethnographic Glossary (1911–1919)

## Archival Source
* **Source:** *A Glossary of the Tribes and Castes of the Punjab and North-West Frontier Province*, compiled by H. A. Rose based on the census reports of Denzil Ibbetson (1881) and Edward Maclagan (1891).
* **Volumes:**
  * Volume I (`VOL1.md`): Religious history, cults, and folklore.
  * Volume II (`13438.pdf` / `13438.txt`): Castes and tribes A to K (including Gaddi, Gujar, Hali).
  * Volume III (`13664.pdf` / `13664.txt`): Castes and tribes L to Z (including Lohar, Rehara, Sipi).
* **Geographic Scope:** Punjab Hill States, Chamba State, and adjacent Himalayan tracts.

---

## Folder Contents

| File / Subdirectory | Description |
|---|---|
| `13438.pdf`, `13664.pdf` | Scanned archival PDF volumes for Vol II and Vol III. |
| `13438.txt`, `13664.txt` | Complete searchable OCR transcripts of the volumes. |
| `VOL1.md` | Searchable Markdown text transcript of Volume I. |
| `analysis_rose.py` | **Primary computational analysis script** for the Rose ethnographic corpus. |
| `run_all.sh` | Shell wrapper for initial preprocessing and OCR checks. |
| `01_setup.sh`, `02_ocr.sh`, `03_images.sh` | Pipeline stages for environment, OCR, and image extraction. |
| `04_hindi.sh` | Devanagari script detection and LLM translation script. |
| `05_histogram.sh` | Word histogram and frequency counter wrapper. |
| `word_histogram.py` | Lexical frequency distribution and histogram generator. |
| `hindi_poems.py` | Script detection and translation module. |
| `image_context.py` | Contextual extractor for plates, diagrams, and figures. |

---

## How to Run

### Step 1: Open Terminal in the Folder
```bash
cd "HA ROSE"
```

### Step 2: Run the Main Preprocessing Pipeline (Setup, OCR, Image Extraction)
```bash
bash run_all.sh
```
*Note:* These volumes are large (each ~500–900 pages), so OCR can take an hour or more if run from scratch. Check the first lines of each `.txt` to see which volume it is.

### Step 3: Check for Hindi / Devanagari Text
```bash
bash 04_hindi.sh --detect-only
```
If every document shows 0 blocks, skip Step 4.

### Step 4: Translate Hindi Text via Anthropic API (If Blocks Detected)
If Hindi/Devanagari text was found, set your API key and run the translation pipeline:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
bash 04_hindi.sh
```
*Security Note:* Never commit or store your API key inside any code file or zip archive.

### Step 5: Generate Word Histograms and Common Words
```bash
bash 05_histogram.sh
```

### Step 6: Run Historical & Ethnographic Computational Analysis
To execute keyword indexing, colonial bias deconstruction, and qualitative passage extraction:
```bash
# Direct Python execution:
python3 analysis_rose.py

# Or via uv package runner:
uv run --with pandas python3 analysis_rose.py
```

---

## Pipeline & Preprocessing Outputs

| Folder / File | Contents |
|---|---|
| `<name>_ocr.pdf`, `<name>.txt` | OCR'd PDF and extracted text for each volume. |
| `image_context_output/` | Pages with photos/diagrams plus surrounding contextual pages, and a caption table (CSV/XLSX). |
| `hindi_output/` | Extracted Hindi page PDFs, `hindi_poems_table.csv` with corrected Hindi and English translation. |
| `word_histogram_output/` | `words_per_document.csv`, `common_words.csv`, `hist_<doc>.png`, `hist_common_combined.png`, `summary.txt`. |

---

## Generated Analytical Outputs

Running `analysis_rose.py` generates the following structured CSV outputs:

1. **`output_rose_keyword_summary.csv`**:
   * Term occurrence summary across all three Rose volumes for core target communities (`Gaddi`, `Gujjar`, `Sipi`, `Hali`, `Lohar`, `Rehara`, `Chamba`, `Brahmaur`).
2. **`output_rose_concordance.csv`**:
   * 387 verified Keyword-in-Context (KWIC) concordance records with page/line citations.
3. **`output_rose_bias_analysis.csv`**:
   * Qualitative and lexical co-occurrence records identifying colonial bias terms (e.g., `menial`, `lazy`, `indolent`, `theft`, `cattle-lifter`) juxtaposed against pastoral and artisan communities.
4. **`output_rose_terms.csv`**:
   * Systematic critique of 5 key ethnographic categories (`Gaddi`, `Gujar`, `Sipi`, `Hali`, `Rehara`), contrasting Rose's racial/servile framing against 1961 empirical village findings.
5. **`output_rose_passages.csv`**:
   * Coded verbatim passages (`PAS_017`, `PAS_018`, `PAS_019`) documenting the four-tier Gaddi social taxonomy, Sipi craft definitions, and colonial anti-pastoral proverbs.

These analytical outputs are automatically ingested into `data/` and `outputs/tables/` by `master_analysis_pipeline.py`.

---

## Troubleshooting ("If Something Goes Wrong")
* **OCR very slow or stuck:** Check with `top` that `tesseract` is using CPU. Re-running `bash 02_ocr.sh` skips already-completed files.
* **"Input PDF is encrypted":** `02_ocr.sh` removes encryption automatically with `qpdf`.
* **Hindi step says no API key:** Run the `export ANTHROPIC_API_KEY=...` command in the same terminal session before running `bash 04_hindi.sh`.
* **Missing packages for analysis script:** Install pandas or run with `uv run --with pandas python3 analysis_rose.py`.
