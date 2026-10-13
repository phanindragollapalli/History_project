# H. A. Rose (13438.pdf, 13664.pdf)

Source: H. A. Rose volumes (glossary of Punjab tribes and castes)

PDFs in this folder: 13438.pdf, 13664.pdf (VOL1.md is ignored by the scripts)

## How to run

1. Unzip and open a terminal inside the folder:
   ```bash
   unzip "HA ROSE.zip"
   cd "HA ROSE"
   ```

2. Run the main pipeline (setup, OCR, image pages):
   ```bash
   bash run_all.sh
   ```
   Note: these volumes are large, so OCR can take an hour or more. Check the first lines of each `.txt` to see which volume it is.

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
