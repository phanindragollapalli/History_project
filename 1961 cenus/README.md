# 1961 Census: Village Survey Monographs

## Overview
This directory contains the archival records, OCR text extractions, and computational analysis for the 1961 Census of India Village Survey monographs for Chamba District, Himachal Pradesh:
* **Monograph No. 5: Brahmaur** (Alpine Valley, ~7,000 ft)
* **Monograph No. 10: Chitrari** (Terraced Basin, ~5,800 ft)
* **Monograph No. 27: Maingal** (Sub-Himalayan Forest, ~4,000 ft)

All primary monograph PDFs, searchable OCR transcripts, preprocessing scripts, and analysis code are located in the subdirectory:
[`1961 cenus/village surveys/`](village%20surveys/)

---

## Quick Start (How to Run)

To run the complete data processing and computational analysis:

```bash
# 1. Navigate to the village surveys subdirectory:
cd "1961 cenus/village surveys"

# 2. Run the main preprocessing pipeline (OCR, image context, text setup):
bash run_all.sh

# 3. Check for Hindi / Devanagari text:
bash 04_hindi.sh --detect-only

# 4. If Hindi detected, translate via Anthropic API:
export ANTHROPIC_API_KEY=sk-ant-your-key-here
bash 04_hindi.sh

# 5. Generate word histograms:
bash 05_histogram.sh

# 6. Run the computational micro-analysis:
python3 analysis_1961.py
```

For the complete file index, detailed outputs breakdown, and troubleshooting guide, see the dedicated [Village Surveys README](village%20surveys/README.md).
