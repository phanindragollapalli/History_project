#!/usr/bin/env bash
# Steps 1-3 in order (Hindi step 04 is optional and not run here)
set -e
cd "$(dirname "$0")"
bash 01_setup.sh
bash 02_ocr.sh
bash 03_images.sh
echo "Done. Outputs: image_context_output/  *.txt  *_ocr.pdf"
