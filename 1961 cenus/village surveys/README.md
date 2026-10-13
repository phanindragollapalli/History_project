# 1961 Census Village Surveys (Brahmaur, Chitrari, Maingal)

## Archival Source
* **Source:** *Census of India 1961, Volume XX, Part VI: Himachal Pradesh—A Village Survey*, edited by Ram Chandra Pal Singh (Delhi: Manager of Publications, Government of India).
* **Monographs:**
  * **No. 5: Brahmaur** (`brahmaur.pdf` / `brahmaur.txt`): High alpine Gaddi valley settlement (~7,000 ft; 65,302 searchable words; 99 households, 721 population; 4,484 sheep/goats, 0 buffaloes).
  * **No. 10: Chitrari** (`chitrari.pdf` / `chitrari.txt`): Middle terraced river basin (~5,800 ft; 41,363 searchable words; 79 households, 404 population; 77% Brahmin majority, attached Hali tenancy, Shakti Devi temple).
  * **No. 27: Maingal** (`maingal.pdf` / `maingal.txt`): Sub-Himalayan forested slopes (~4,000 ft; 70,551 searchable words; 40 households, 249 population; 81.5% Muslim Gujjar majority, 217 water buffaloes, commercial ghee trade, Lohar iron barter).

---

## Folder Contents

| File / Subdirectory | Description |
|---|---|
| `brahmaur.pdf`, `chitrari.pdf`, `maingal.pdf` | Primary scanned Census 1961 village monograph volumes. |
| `brahmaur.txt`, `chitrari.txt`, `maingal.txt` | Complete searchable OCR text transcripts of the three monographs. |
| `analysis_1961.py` | **Primary computational micro-analysis script** for all three villages. |
| `run_all.sh` | Shell wrapper for initial setup, OCR, and image extraction. |
| `01_setup.sh`, `02_ocr.sh`, `03_images.sh` | Pipeline stages for environment, OCR, and image extraction. |
| `04_hindi.sh` | Devanagari script detection and LLM translation script. |
| `05_histogram.sh` | Word histogram and frequency counter wrapper. |
| `word_histogram.py` | Lexical frequency counter across the three village texts. |
| `hindi_poems.py` | Folk song and vernacular poetry extractor/translator. |
| `image_context.py` | Photographic plates and material culture illustration extractor. |

---

## How to Run

### Step 1: Open Terminal in the Folder
```bash
cd "1961 cenus/village surveys"
```

### Step 2: Run the Main Preprocessing Pipeline (Setup, OCR, Image Extraction)
```bash
bash run_all.sh
```
*(These village monographs contain traditional Hindi/Gaddi folk songs and Nawala poetry, so Steps 3 and 4 are especially relevant here.)*

### Step 3: Check for Hindi / Devanagari Text
```bash
bash 04_hindi.sh --detect-only
```
If every document shows 0 blocks, skip Step 4.

### Step 4: Translate Hindi / Gaddi Songs via Anthropic API (If Blocks Detected)
If Hindi or Gaddi folk songs were detected, set your API key and run the translation pipeline:
```bash
export ANTHROPIC_API_KEY=sk-ant-your-key-here
bash 04_hindi.sh
```
*Security Note:* Never commit or store your API key inside any code file or zip archive.

### Step 5: Generate Word Histograms and Common Words
```bash
bash 05_histogram.sh
```

### Step 6: Run Historical & Micro-Demographic Computational Analysis
To calculate relative term frequencies per 1,000 words, extract the 1,038 KWIC interaction concordances, and generate village micro-records:
```bash
# Direct Python execution:
python3 analysis_1961.py

# Or via uv package runner:
uv run --with pandas python3 analysis_1961.py
```

---

## Pipeline & Preprocessing Outputs

| Folder / File | Contents |
|---|---|
| `<name>_ocr.pdf`, `<name>.txt` | OCR'd PDF and extracted text for each monograph. |
| `image_context_output/` | Pages with photos/diagrams plus surrounding contextual pages, and a caption table (CSV/XLSX). |
| `hindi_output/` | Extracted Hindi page PDFs, `hindi_poems_table.csv` with corrected Hindi and English translation. |
| `word_histogram_output/` | `words_per_document.csv`, `common_words.csv`, `hist_<doc>.png`, `hist_common_combined.png`, `summary.txt`. |

---

## Generated Analytical Outputs

Running `analysis_1961.py` generates the following files directly in this directory:

### Comparative Outputs
1. **`output_1961_village_normalized_frequencies.csv`**:
   * Term occurrences and normalized frequencies (per 1,000 searchable words) across Brahmaur, Chitrari, and Maingal, controlling for text length differences. Synchronized to `outputs/tables/village_1961_normalized_frequencies.csv`.
2. **`output_1961_interaction_concordance.csv`**:
   * 1,038 verified KWIC concordance windows specifically matching the 12 socio-economic and ritual relationships (`REL_001` through `REL_012`).

### Village-Specific Micro-Datasets
3. **Brahmaur**:
   * `output_brahmaur_records.csv`: 12 verified quantitative records (`REC_001` to `REC_012`) covering caste populations, 4,484 sheep/goats, cattle, the total absence of buffaloes, and agricultural workers.
   * `output_brahmaur_passages.csv`: 5 verified qualitative passages (`PAS_001` to `PAS_005`) covering wage shepherding (*pohal* contracts), climate limits on buffaloes, Sipi weaving, and Nawala ritual feasts.
4. **Chitrari**:
   * `output_chitrari_records.csv`: 7 verified quantitative records (`REC_013` to `REC_019`) covering Brahmin demographic dominance (77%), Bensis, Halis, oxen, sheep, and goats.
   * `output_chitrari_passages.csv`: 4 verified qualitative passages (`PAS_006` to `PAS_009`) covering royal Sasana land grants to Brahmins, attached Hali ploughing, monsoon Gujjar milk trade, and hereditary temple musicians.
5. **Maingal**:
   * `output_maingal_records.csv`: 4 verified quantitative records (`REC_020` to `REC_023`) covering Muslim Gujjars (81.5%), Brahmins, Lohars, and the 217 water buffalo dairy herd.
   * `output_maingal_passages.csv`: 4 verified qualitative passages (`PAS_010` to `PAS_013`) covering spatial hamlet segregation, Lohar *khalian* harvest barter, commercial ghee marketing, and inter-religious coexistence.

All records and passages are aggregated into `data/quantitative_records.csv` and `data/qualitative_passages.csv` by the master pipeline.

---

## Troubleshooting ("If Something Goes Wrong")
* **OCR very slow or stuck:** Check with `top` that `tesseract` is using CPU. Re-running `bash 02_ocr.sh` skips already-completed files.
* **"Input PDF is encrypted":** `02_ocr.sh` removes encryption automatically with `qpdf`.
* **Hindi step says no API key:** Run the `export ANTHROPIC_API_KEY=...` command in the same terminal session before running `bash 04_hindi.sh`.
* **Missing packages for analysis script:** Install pandas or run with `uv run --with pandas python3 analysis_1961.py`.
