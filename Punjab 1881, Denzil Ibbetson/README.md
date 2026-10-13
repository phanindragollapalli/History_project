# 1881 Census of the Punjab (Denzil Ibbetson)

Source: Census of the Punjab 1881, Denzil Ibbetson, six volumes/parts

PDFs in this folder: ibbetson1881_1_preface.pdf, ibbetson1881_2_results.pdf, ibbetson1881_3_operations.pdf, ibbetson1881_4_suppl_tables_appC.pdf, ibbetson1881_5_instructions_appD.pdf, ibbetson1881_6_vernacular_index.pdf

## How to run

1. Unzip and open a terminal inside the folder:
   ```bash
   unzip "Punjab 1881.zip"
   cd "Punjab 1881, Denzil Ibbetson"
   ```

2. Run the main pipeline (rename, setup, OCR, image pages):
   ```bash
   bash run_all.sh
   ```
   Notes: `00_rename.sh` (called by run_all) shortens the original file names. The vernacular index is OCR'd with English + Urdu + Hindi. OCR of the 1881 scans is rougher, especially in tables, so check numbers against the PDFs. The Results volume is large and OCR can take an hour or more.

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
