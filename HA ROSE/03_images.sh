#!/usr/bin/env bash
# STEP 3: image/diagram pages (+ page above and below) and caption table
set -e
cd "$(dirname "$0")"
.venv/bin/python image_context.py
