# 1931 Census of India (Punjab & Chamba State)

## Archival Source
* **Source:** *Census of India, 1931, Volume XVII: Punjab, Part I—Report*, by Khan Ahmad Hasan Khan (Lahore: Civil and Military Gazette Press, 1933).
* **Volumes:**
  * `vol17_1931_part1.pdf` / `.txt`: Main provincial narrative and analytical report (Volume XVII).
  * `punjab1931_part1.pdf` / `.txt`: Census report tables and state-level returns.
* **Geographic Scope:** Imperial Punjab Province, Punjab Hill States Agency, and Chamba Princely State.

---

## Folder Contents

| File / Subdirectory | Description |
|---|---|
| `punjab1931_part1.pdf`, `vol17_1931_part1.pdf` | Scanned archival PDF reports. |
| `punjab1931_part1.txt`, `vol17_1931_part1.txt` | Complete searchable OCR transcripts. |
| `analysis_1931.py` | **Primary computational analysis script** for the 1931 interwar census. |
| `run_all.sh` | Shell wrapper for decryption, setup, and OCR. |
| `01_setup.sh`, `02_ocr.sh`, `03_images.sh` | Pipeline stages for environment, OCR, and image extraction. |
| `04_hindi.sh` | Devanagari script detection and LLM translation script. |
| `05_histogram.sh` | Word histogram and frequency counter wrapper. |
| `word_histogram.py` | Frequency distribution and histogram generator. |
| `hindi_poems.py` | Script detection and API translation module. |
| `image_context.py` | Diagram, map, and plate extractor. |

---

## How to Run

### Step 1: Open Terminal in the Folder
```bash
cd "1931 census"
```

### Step 2: Run the Main Preprocessing Pipeline (Rename, Setup, OCR, Image Extraction)
```bash
bash run_all.sh
```
*Note:* `vol17_1931_part1.pdf` is password-protected; the script decrypts it automatically with `qpdf` (original backup saved as `.encrypted.bak`).

### Step 3: Check for Hindi / Devanagari Text
```bash
bash 04_hindi.sh --detect-only
```
If all documents show 0 blocks, skip Step 4.

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
To scan the text corpus, extract macro-demographic returns for Chamba State, and generate KWIC concordances:
```bash
# Direct Python execution:
python3 analysis_1931.py

# Or via uv package runner:
uv run --with pandas python3 analysis_1931.py
```

---

## Pipeline & Preprocessing Outputs

| Folder / File | Contents |
|---|---|
| `<name>_ocr.pdf`, `<name>.txt` | OCR'd PDF and extracted text for each PDF volume. |
| `image_context_output/` | Pages with photos/diagrams plus surrounding contextual pages, and a caption table (CSV/XLSX). |
| `hindi_output/` | Extracted Hindi page PDFs, `hindi_poems_table.csv` with corrected Hindi and English translation. |
| `word_histogram_output/` | `words_per_document.csv`, `common_words.csv`, `hist_<doc>.png`, `hist_common_combined.png`, `summary.txt`. |

---

## Generated Analytical Outputs

Running `analysis_1931.py` generates the following research files:

1. **`output_1931_keyword_summary.csv`**:
   * Lexical counts across 1931 reports for target occupational and social terms (`Chamba`, `Gaddi`, `Gujjar`, `pastoral`, `earners`, `working_dependents`, `non_working_dependents`, `Hali`, `Lohar`, `Brahman`).
2. **`output_1931_concordance.csv`**:
   * 560 verified Keyword-in-Context (KWIC) concordance records with page and line citations.
3. **`output_1931_chamba_demographics.csv`**:
   * 28 extracted demographic records specific to Chamba State detailing occupied houses, total population, rural density, and dependency ratios.
4. **`output_1931_records.csv`**:
   * Standardized quantitative record (`REC_024`) from Sub Table X (p. 112) recording 30,665 occupied houses and 146,870 total inhabitants across Chamba State (4.79 persons per dwelling).
5. **`output_1931_passages.csv`**:
   * Verbatim passage (`PAS_020`) providing the macro-demographic context of mountainous hamlet dispersion in Chamba State.

These analytical outputs are automatically ingested into `data/` and `outputs/tables/` by `master_analysis_pipeline.py`.

---

## Troubleshooting ("If Something Goes Wrong")
* **OCR very slow or stuck:** Check with `top` that `tesseract` is using CPU. Re-running `bash 02_ocr.sh` skips already-completed files.
* **"Input PDF is encrypted":** `02_ocr.sh` removes encryption automatically with `qpdf`.
* **Hindi step says no API key:** Run the `export ANTHROPIC_API_KEY=...` command in the same terminal session before running `bash 04_hindi.sh`.
* **Missing packages for analysis script:** Install pandas or run with `uv run --with pandas python3 analysis_1931.py`.
