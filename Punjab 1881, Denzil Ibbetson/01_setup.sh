#!/usr/bin/env bash
# STEP 1: install tools + Python environment (run once)
set -e
cd "$(dirname "$0")"
sudo apt update
sudo apt install -y ocrmypdf tesseract-ocr tesseract-ocr-eng poppler-utils qpdf python3-venv tesseract-ocr-urd tesseract-ocr-hin
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q -U pip
.venv/bin/pip install -q -U pdfminer.six pikepdf pandas numpy pillow openpyxl anthropic
echo "Setup done."
