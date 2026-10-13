#!/usr/bin/env bash
# STEP 0: give the two PDFs short, simple names (safe to re-run)
cd "$(dirname "$0")"
[ -f 1931punjabpart1.pdf ] && mv -n 1931punjabpart1.pdf punjab1931_part1.pdf
for f in 2015.62732.Census-Of-India-1931-Vol-Xvii-Part-I.pdf; do
  [ -f "$f" ] && mv -n "$f" vol17_1931_part1.pdf
done
ls -l *.pdf
