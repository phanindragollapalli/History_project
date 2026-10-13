#!/usr/bin/env bash
# STEP 3: find image/diagram pages (+ page above and below) and build the caption table
set -e
cd "$(dirname "$0")"
.venv/bin/python image_context.py
