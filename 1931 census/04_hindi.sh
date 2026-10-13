#!/usr/bin/env bash
# STEP 4 (OPTIONAL): Hindi block detection/translation. The 1931 reports are mostly
# English, so this is usually not needed.
#   bash 04_hindi.sh --detect-only      (free)
#   export ANTHROPIC_API_KEY=sk-ant-... ; bash 04_hindi.sh   (translates)
set -e
cd "$(dirname "$0")"
if [ "$1" != "--detect-only" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "Set ANTHROPIC_API_KEY first, or use --detect-only"; exit 1
fi
.venv/bin/python hindi_poems.py "$@"
