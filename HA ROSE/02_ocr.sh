#!/usr/bin/env bash
# STEP 2: make <name>_ocr.pdf and <name>.txt for every PDF in this folder.
#  - removes PDF encryption if present (original kept as *.encrypted.bak)
#  - reuses an existing good text layer (fast); FORCE_OCR=1 forces fresh OCR
#  - otherwise runs ocrmypdf (max 40 min per book); if it hangs/fails but a text
#    layer exists, that text layer is reused
#  - the vernacular index also gets Urdu + Hindi OCR
set -e
cd "$(dirname "$0")"
command -v qpdf >/dev/null || sudo apt install -y qpdf

for f in *.pdf; do
  case "$f" in *_ocr.pdf) continue ;; esac
  v="${f%.pdf}"
  if [ -f "${v}_ocr.pdf" ] && [ -f "${v}.txt" ]; then
    echo "[$v] already done, skipping (delete ${v}_ocr.pdf to redo)"; continue
  fi
  if qpdf --is-encrypted "$f" 2>/dev/null; then
    echo "[$v] PDF is encrypted, decrypting..."
    qpdf --decrypt "$f" "${v}.tmp_decrypted" && mv "$f" "${f}.encrypted.bak" && mv "${v}.tmp_decrypted" "$f"
  fi
  lang=eng
  case "$v" in *vernacular*) lang="eng+urd+hin" ;; esac
  chars=$(pdftotext -f 1 -l 30 "$f" - 2>/dev/null | wc -c)
  if [ -z "$FORCE_OCR" ] && [ "$chars" -gt 3000 ]; then
    echo "[$v] already has a text layer, reusing it"
    cp "$f" "${v}_ocr.pdf"
    pdftotext -layout "$f" "${v}.txt"
  else
    echo "[$v] running OCR, language=$lang (large books can take an hour or more)..."
    rm -f "${v}.txt" "${v}_ocr.pdf"
    set +e
    timeout -k 10 2400 ocrmypdf -l "$lang" --redo-ocr --output-type pdf -j 4 \
      --skip-big 100 --tesseract-timeout 90 \
      --sidecar "${v}.txt" "$f" "${v}_ocr.pdf"
    rc=$?
    if [ $rc -eq 6 ]; then
      timeout -k 10 2400 ocrmypdf -l "$lang" --force-ocr --output-type pdf -j 4 \
        --skip-big 100 --tesseract-timeout 90 \
        --sidecar "${v}.txt" "$f" "${v}_ocr.pdf"
      rc=$?
    fi
    set -e
    if [ $rc -ne 0 ]; then
      pkill gs 2>/dev/null || true; pkill tesseract 2>/dev/null || true
      echo "[$v] ocrmypdf stopped with exit code $rc"
      if [ "$(pdftotext -f 1 -l 30 "$f" - 2>/dev/null | wc -c)" -gt 3000 ]; then
        echo "[$v] using the PDF's existing text layer instead"
        cp "$f" "${v}_ocr.pdf"; pdftotext -layout "$f" "${v}.txt"
      else
        echo "[$v] no usable text layer; skipping this book (send me this message)"
      fi
    fi
  fi
done
ls -l *_ocr.pdf *.txt
