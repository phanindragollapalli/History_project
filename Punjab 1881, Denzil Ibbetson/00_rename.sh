#!/usr/bin/env bash
# STEP 0: give the six 1881 PDFs short names without spaces/commas (safe to re-run)
cd "$(dirname "$0")"
rename_one () {   # $1 = glob pattern, $2 = new name
  for f in $1; do
    [ -f "$f" ] && mv -n -- "$f" "$2" && echo "renamed -> $2"
  done
}
shopt -s nullglob
rename_one "*Preface*.pdf"                  ibbetson1881_1_preface.pdf
rename_one "*Results*.pdf"                  ibbetson1881_2_results.pdf
rename_one "*Operations*.pdf"               ibbetson1881_3_operations.pdf
rename_one "*Supplementary*.pdf"            ibbetson1881_4_suppl_tables_appC.pdf
rename_one "*Instructions*.pdf"             ibbetson1881_5_instructions_appD.pdf
rename_one "*Vernacular*.pdf"               ibbetson1881_6_vernacular_index.pdf
ls -l *.pdf
