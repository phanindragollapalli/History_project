#!/usr/bin/env bash
# STEP 2: make <name>_ocr.pdf and <name>.txt for every PDF in this folder.
# If a PDF already has a good text layer it is reused (fast). To force a fresh OCR:
#   FORCE_OCR=1 bash 02_ocr.sh
set -e
cd "$(dirname "$0")"
command -v qpdf >/dev/null || sudo apt install -y qpdf
for f in *.pdf; do
  case "$f" in *_ocr.pdf) continue ;; esac
  v="${f%.pdf}"
  if [ -f "${v}_ocr.pdf" ] && [ -f "${v}.txt" ]; then
    echo "[$v] already done, skipping (delete ${v}_ocr.pdf to redo)"; continue
  fi
  # Remove encryption first if present (original kept as ${f}.encrypted.bak)
  if qpdf --is-encrypted "$f" 2>/dev/null; then
    echo "[$v] PDF is encrypted, decrypting..."
    qpdf --decrypt "$f" "${v}.tmp_decrypted" && mv "$f" "${f}.encrypted.bak" && mv "${v}.tmp_decrypted" "$f"
  fi
  chars=$(pdftotext -f 1 -l 30 "$f" - 2>/dev/null | wc -c)
  if [ -z "$FORCE_OCR" ] && [ "$chars" -gt 3000 ]; then
    echo "[$v] already has a text layer, reusing it"
    cp "$f" "${v}_ocr.pdf"
    pdftotext -layout "$f" "${v}.txt"
  else
    echo "[$v] running OCR (large books can take an hour or more)..."
    rm -f "${v}.txt"
    set +e
    ocrmypdf -l eng --redo-ocr --output-type pdf -j 4 --skip-big 100 --tesseract-timeout 90 \
      --sidecar "${v}.txt" "$f" "${v}_ocr.pdf"
    rc=$?
    set -e
    if [ $rc -eq 6 ]; then
      ocrmypdf -l eng --force-ocr --output-type pdf -j 4 --skip-big 100 --tesseract-timeout 90 \
        --sidecar "${v}.txt" "$f" "${v}_ocr.pdf"
    elif [ $rc -ne 0 ]; then
      echo "[$v] ocrmypdf failed with exit code $rc"; exit $rc
    fi
  fi
done
ls -l *_ocr.pdf *.txt
