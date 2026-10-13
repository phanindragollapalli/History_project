# 1881 Census of the Punjab (Denzil Ibbetson)

## Archival Source
* **Source:** *Report on the Census of the Panjáb Taken on the 17th of February 1881*, by Denzil Charles Jelf Ibbetson (Calcutta: Central Press, 1883).
* **Volumes:** Six parts spanning the Preface, Results, Operations, Supplemental Tables, Instructions, and Vernacular Index.
* **Geographic Scope:** Imperial Punjab Province and Chamba Princely State.

---

## Folder Contents

| File / Subdirectory | Description |
|---|---|
| `ibbetson1881_*.pdf` | Original scanned archival PDF volumes (Parts 1 to 6). |
| `ibbetson1881_*.txt` | Processed OCR text transcripts extracted from the PDFs. |
| `analysis_1881.py` | **Primary computational analysis script** for the 1881 timeline. |
| `run_all.sh` | Shell wrapper for initial rename, setup, OCR, and image extraction. |
| `00_rename.sh` | File naming standardizer for Ibbetson volume parts. |
| `01_setup.sh`, `02_ocr.sh`, `03_images.sh` | Pipeline stages for environment, OCR, and image extraction. |
| `04_hindi.sh` | Devanagari script detection and LLM translation script. |
| `05_histogram.sh` | Word histogram and frequency counter wrapper. |
| `word_histogram.py` | Term frequency distribution and histogram generator. |
| `hindi_poems.py` | Devanagari script detection and translation utility. |
| `image_context.py` | PDF image and diagram contextual extractor. |

---

## How to Run

### Step 1: Open Terminal in the Folder
```bash
cd "Punjab 1881, Denzil Ibbetson"
```

### Step 2: Run the Main Preprocessing Pipeline (Rename, Setup, OCR, Image Extraction)
```bash
bash run_all.sh
```
*Notes:*
* `00_rename.sh` (called by `run_all.sh`) shortens the original file names.
* The vernacular index is OCR'd with English + Urdu + Hindi language models.
* OCR of the 1881 scans is rougher, especially in tables, so verify critical numbers against the PDFs.
* The Results volume is large; OCR can take an hour or more depending on hardware.

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

### Step 6: Run Historical & Demographic Computational Analysis
To execute term searches, KWIC concordance extraction, and generate timeline-specific records:
```bash
# Direct Python execution:
python3 analysis_1881.py

# Or via uv package runner:
uv run --with pandas python3 analysis_1881.py
```

---

## Pipeline & Preprocessing Outputs

| Folder / File | Contents |
|---|---|
| `<name>_ocr.pdf`, `<name>.txt` | OCR'd PDF and extracted text for each volume part. |
| `image_context_output/` | Pages with photos/diagrams plus surrounding contextual pages, and caption table (CSV/XLSX). |
| `hindi_output/` | Extracted Hindi page PDFs, `hindi_poems_table.csv` with corrected Hindi and English translation. |
| `word_histogram_output/` | `words_per_document.csv`, `common_words.csv`, `hist_<doc>.png`, `hist_common_combined.png`, `summary.txt`. |

---

## Generated Analytical Outputs

Running `analysis_1881.py` generates the following files:

1. **`output_1881_keyword_summary.csv`**:
   * Lexical counts across all six 1881 volumes for key terms (`Gaddi`, `Gujjar`, `Chamba`, `Brahmaur`, `Hali`, `Sipi`, `Lohar`, `Brahman`, `pastoral`, `transhumance`, `begar`).
2. **`output_1881_concordance.csv`**:
   * 718 verified Keyword-in-Context (KWIC) concordance records with a 15-line surrounding context window and line citations.
3. **`output_1881_records.csv`**:
   * Standardized quantitative record (`REC_025`) capturing Chambiali language speakers (104,469 persons) from Table IX (p. 153).
4. **`output_1881_passages.csv`**:
   * Verbatim historical passages (`PAS_014`, `PAS_015`, `PAS_016`) capturing Ibbetson's definition of Gaddi caste boundaries (para 498), trans-Dhaula Dhar transhumance cycles between Kangra and Brahmaur, and regional pastoral proverbs.

These analytical outputs are automatically ingested into `data/` and `outputs/tables/` by `master_analysis_pipeline.py`.

---

## Troubleshooting ("If Something Goes Wrong")
* **OCR very slow or stuck:** Check with `top` that `tesseract` is using CPU. Re-running `bash 02_ocr.sh` skips already-completed files.
* **"Input PDF is encrypted":** `02_ocr.sh` removes encryption automatically with `qpdf`.
* **Hindi step says no API key:** Run the `export ANTHROPIC_API_KEY=...` command in the same terminal session before running `bash 04_hindi.sh`.
* **Missing packages for analysis script:** Install pandas or run with `uv run --with pandas python3 analysis_1881.py`.
