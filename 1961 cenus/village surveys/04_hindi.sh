#!/usr/bin/env bash
# STEP 4: find Hindi/Gaddi poems, translate them (needs ANTHROPIC_API_KEY), write table
#   export ANTHROPIC_API_KEY=sk-ant-...   then   bash 04_hindi.sh
#   bash 04_hindi.sh --detect-only        (no API calls, no key needed)
set -e
cd "$(dirname "$0")"
if [ "$1" != "--detect-only" ] && [ -z "$ANTHROPIC_API_KEY" ]; then
  echo "ANTHROPIC_API_KEY not set. Run:  export ANTHROPIC_API_KEY=sk-ant-..."
  echo "or use:  bash 04_hindi.sh --detect-only"
  exit 1
fi
.venv/bin/python hindi_poems.py "$@"
