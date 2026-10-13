# 1931 Census, Punjab

Source: Census of India 1931, Punjab (Part I and Vol XVII Part I)

PDFs in this folder: punjab1931_part1.pdf, vol17_1931_part1.pdf (renamed from 1931punjabpart1.pdf and 2015.62732.Census-Of-India-1931-Vol-Xvii-Part-I.pdf)

## How to run

1. Unzip and open a terminal inside the folder:
   ```bash
   unzip "1931 census.zip"
   cd "1931 census"
   ```

2. Run the main pipeline (rename, setup, OCR, image pages):
   ```bash
   bash run_all.sh
   ```
   Note: vol17_1931_part1.pdf is password-protected; the script decrypts it automatically (original kept as `.encrypted.bak`).

3. Check whether the documents contain Hindi / Devanagari text:
   ```bash
   bash 04_hindi.sh --detect-only
   ```
   If every document shows 0 blocks, skip step 4.

4. Only if Hindi was found, translate it (uses the Claude API and costs credit):
   ```bash
   export ANTHROPIC_API_KEY=sk-ant-your-key-here
   bash 04_hindi.sh
   ```
   Never put your API key inside a file or a zip.

5. Word histograms and common words:
   ```bash
   bash 05_histogram.sh
   ```

## Outputs

| Folder / file | Contents |
|---|---|
| `<name>_ocr.pdf`, `<name>.txt` | OCR'd PDF and extracted text for each PDF |
| `image_context_output/` | Pages with photos/diagrams plus the page above and below, and a caption table (CSV/XLSX) |
| `hindi_output/` | Hindi page PDFs, `hindi_poems_table.csv` with corrected Hindi and English translation |
| `word_histogram_output/` | `words_per_document.csv`, `common_words.csv`, `hist_<doc>.png`, `hist_common_combined.png`, `summary.txt` |

## If something goes wrong
- **OCR very slow or stuck:** check with `top` that `tesseract` is using CPU. Re-running `bash 02_ocr.sh` skips finished files.
- **"Input PDF is encrypted":** `02_ocr.sh` removes encryption automatically with `qpdf`.
- **Hindi step says no API key:** run the `export ANTHROPIC_API_KEY=...` line in the same terminal window first.
- **Anything else:** send the full error message to the team chat.
