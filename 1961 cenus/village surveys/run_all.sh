#!/usr/bin/env bash
# Runs steps 1-4 in order. Use DETECT_ONLY=1 to skip translation.
set -e
cd "$(dirname "$0")"
bash 01_setup.sh
bash 02_ocr.sh
bash 03_images.sh
if [ -n "$DETECT_ONLY" ] || [ -z "$ANTHROPIC_API_KEY" ]; then
  bash 04_hindi.sh --detect-only
else
  bash 04_hindi.sh
fi
echo "Done. Outputs: image_context_output/  hindi_output/  *.txt  *_ocr.pdf"
