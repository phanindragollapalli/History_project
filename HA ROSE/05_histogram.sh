#!/usr/bin/env bash
# STEP 5: word histograms per document + words common to all documents in this folder
set -e
cd "$(dirname "$0")"
[ -d .venv ] || python3 -m venv .venv
.venv/bin/pip install -q matplotlib pandas
.venv/bin/python word_histogram.py "$@"
