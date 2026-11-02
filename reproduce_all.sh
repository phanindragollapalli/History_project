#!/usr/bin/env bash
# ==============================================================================
# Master Reproduction Script: Changing Patterns of Occupation in Chamba (1881–1961)
# Course: Introduction to Historical Analysis (Intro2Hist / HS3.201)
# Authors: Bala Subramanian, Vagdevi Reddy, Phanindra
#
# This single script:
# 1. Detects Python 3 and creates/activates a virtual environment (.venv)
# 2. Installs all required dependencies from requirements.txt
# 3. Executes the full computational analysis pipeline (all 8 historical modules)
# 4. Verifies all 36 data tables, evidence registers, and 300-DPI visual figures
# 5. Compiles the final LaTeX research report (Phase3_report.tex -> Phase3_report.pdf)
# ==============================================================================

set -e

# Terminal text colors
GREEN="\033[0;32m"
BLUE="\033[0;34m"
YELLOW="\033[1;33m"
CYAN="\033[0;36m"
BOLD="\033[1m"
RESET="\033[0m"

echo -e "${CYAN}${BOLD}========================================================================${RESET}"
echo -e "${CYAN}${BOLD}  CHAMBA HISTORICAL COMPUTATIONAL PROJECT (1881–1961): REPRODUCTION SCRIPT${RESET}"
echo -e "${CYAN}${BOLD}========================================================================${RESET}"

# Step 0: Ensure we run from the project root
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$ROOT_DIR"
echo -e "${BLUE}Working directory:${RESET} $ROOT_DIR"

# Step 1: Detect Python
echo -e "\n${YELLOW}[Step 1/5] Checking Python environment...${RESET}"
if command -v python3 &>/dev/null; then
    PYTHON_CMD="python3"
elif command -v python &>/dev/null; then
    PYTHON_CMD="python"
else
    echo -e "${RED}Error: Python 3 was not found on your system PATH.${RESET}"
    exit 1
fi
echo -e "Found Python: $($PYTHON_CMD --version)"

# Step 2: Virtual Environment Setup
echo -e "\n${YELLOW}[Step 2/5] Setting up virtual environment (.venv)...${RESET}"
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment at .venv..."
    $PYTHON_CMD -m venv .venv
fi

# Activate virtual environment
if [ -f ".venv/bin/activate" ]; then
    source .venv/bin/activate
elif [ -f ".venv/Scripts/activate" ]; then
    source .venv/Scripts/activate
fi

VENV_PYTHON="$(which python)"
echo -e "Using virtual environment Python: ${BOLD}$VENV_PYTHON${RESET}"

# Step 3: Install Pinned Dependencies
echo -e "\n${YELLOW}[Step 3/5] Installing/verifying pinned dependencies from requirements.txt...${RESET}"
pip install --quiet --upgrade pip
pip install --quiet -r requirements.txt
echo -e "${GREEN}Dependencies verified successfully.${RESET}"

# Step 4: Run the Complete Master Computational Pipeline
echo -e "\n${YELLOW}[Step 4/5] Executing master analysis pipeline across all benchmark eras...${RESET}"
python master_analysis_pipeline.py

# Step 5: Compile Final LaTeX Report (if pdflatex is available)
echo -e "\n${YELLOW}[Step 5/5] Compiling final research report (Phase3_report.tex)...${RESET}"
if command -v pdflatex &>/dev/null; then
    echo "Running pdflatex (Pass 1 of 2)..."
    pdflatex -interaction=nonstopmode -halt-on-error Phase3_report.tex >/dev/null
    echo "Running pdflatex (Pass 2 of 2 for cross-references & TOC)..."
    pdflatex -interaction=nonstopmode -halt-on-error Phase3_report.tex >/dev/null
    echo -e "${GREEN}Compiled successfully:${RESET} Phase3_report.pdf ($(du -h Phase3_report.pdf | cut -f1))"
else
    echo -e "${YELLOW}Notice: 'pdflatex' not found on PATH.${RESET}"
    echo "You can view the existing Phase3_report.pdf directly or upload Phase3_report.tex to Overleaf."
fi

echo -e "\n${CYAN}${BOLD}========================================================================${RESET}"
echo -e "${GREEN}${BOLD}  ALL RESULTS SUCCESSFULLY REPRODUCED & VERIFIED!${RESET}"
echo -e "${CYAN}${BOLD}========================================================================${RESET}"
echo -e "Primary Deliverables:"
echo -e "  - Final Report PDF:    ${BOLD}Phase3_report.pdf${RESET}"
echo -e "  - Final Report LaTeX:  ${BOLD}Phase3_report.tex${RESET}"
echo -e "  - Audited Tables:      ${BOLD}outputs/tables/${RESET} (5 core CSV files)"
echo -e "  - Rendered Figures:    ${BOLD}outputs/figures/${RESET} (Figures 1, 2, and 3 at 300 DPI)"
echo -e "  - Harmonized Data:     ${BOLD}data/${RESET}"
echo -e "${CYAN}========================================================================${RESET}\n"

