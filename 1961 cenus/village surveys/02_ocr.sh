#!/usr/bin/env bash
# STEP 2: make <village>_ocr.pdf and <village>.txt for the three PDFs.
# Each book gets at most 15 minutes of OCR. If ocrmypdf hangs or fails and the PDF
# already has a text layer, that existing text layer is reused instead.
set -e
cd "$(dirname "$0")"

reuse_text_layer () {   # $1 = village
  echo "[$1] using the PDF's existing text layer"
  cp "$1.pdf" "$1_ocr.pdf"
  pdftotext -layout "$1.pdf" "$1.txt"
}

for v in brahmaur chitrari maingal; do
  [ -f "${v}.pdf" ] || { echo "Missing ${v}.pdf in $(pwd)"; exit 1; }
  if [ -f "${v}_ocr.pdf" ] && [ -f "${v}.txt" ]; then
    echo "[$v] already done, skipping (delete ${v}_ocr.pdf to redo)"
    continue
  fi
  echo "[$v] OCR running (max 15 min)..."
  rm -f "${v}.txt" "${v}_ocr.pdf"
  set +e
  timeout -k 10 900 ocrmypdf -l eng+hin --redo-ocr --output-type pdf -j 4 \
    --skip-big 100 --tesseract-timeout 90 \
    --sidecar "${v}.txt" "${v}.pdf" "${v}_ocr.pdf"
  rc=$?
  set -e
  if [ $rc -ne 0 ]; then
    pkill gs 2>/dev/null || true; pkill tesseract 2>/dev/null || true
    echo "[$v] ocrmypdf stopped with exit code $rc"
    chars=$(pdftotext -f 1 -l 30 "${v}.pdf" - 2>/dev/null | wc -c)
    if [ "$chars" -gt 3000 ]; then
      reuse_text_layer "$v"
    else
      echo "[$v] no usable text layer and OCR failed - send me this message"; exit $rc
    fi
  fi
done
ls -l *_ocr.pdf *.txt
