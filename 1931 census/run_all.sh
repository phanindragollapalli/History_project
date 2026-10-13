#!/usr/bin/env bash
# Steps 0-3 in order (Hindi step skipped; run 04_hindi.sh yourself if wanted)
set -e
cd "$(dirname "$0")"
bash 00_rename.sh
bash 01_setup.sh
bash 02_ocr.sh
bash 03_images.sh
echo "Done. Outputs: image_context_output/  *.txt  *_ocr.pdf"
