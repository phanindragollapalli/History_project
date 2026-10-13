#!/usr/bin/env python3
"""
Master Computational Analysis Pipeline

Orchestrates all timeline-specific computational modules:
1. 1881 Punjab Census Analysis (Denzil Ibbetson)
2. 1911-1919 Ethnographic Glossary Analysis (H. A. Rose)
3. 1931 Punjab Census Analysis (Khan Ahmad Hasan Khan)
4. 1961 Village Surveys Micro-Analysis (Brahmaur, Chitrari, Maingal)
5. Visual Figures Generation (Figures 1, 2, and 3 at 300 DPI)
6. Output Validation and Summary Report
"""

import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

# Define the sequence of computational analysis modules across historical periods
TIMELINE_SCRIPTS = [
    ("1881 Punjab Census", HERE / "Punjab 1881, Denzil Ibbetson" / "analysis_1881.py"),
    ("1911-1919 Rose Glossary", HERE / "HA ROSE" / "analysis_rose.py"),
    ("1931 Punjab Census", HERE / "1931 census" / "analysis_1931.py"),
    ("1961 Village Surveys", HERE / "1961 cenus/village surveys" / "analysis_1961.py"),
    ("Harmonized Datasets & Crosswalks", HERE / "build_curated_datasets.py"),
    ("Visual Figures Rendering", HERE / "generate_figures.py")
]

# Execute each analysis module in sequence and verify all research deliverables
def run_master_pipeline():
    print("Running historical computational analysis pipeline (1881-1961)...")

    python_executable = sys.executable

    # Execute timeline modules sequentially in their respective working directories
    for title, script_path in TIMELINE_SCRIPTS:
        print(f"Executing module: {title} ({script_path.name})")
        if not script_path.exists():
            print(f"Error: Script {script_path} not found.")
            sys.exit(1)
        
        result = subprocess.run([python_executable, str(script_path)], cwd=str(script_path.parent if "analysis" in script_path.name else HERE), capture_output=True, text=True)
        if result.returncode != 0:
            print(f"Execution failed for {title}:\n{result.stderr}")
            sys.exit(1)
        else:
            print(result.stdout.strip())
            print(f"Completed {title}.\n")

    # Verify that all expected data records, concordances, and figures exist on disk
    print("Verifying generated analytical deliverables and datasets...")
    
    key_deliverables = [
        # 1881 Imperial Census outputs
        HERE / "Punjab 1881, Denzil Ibbetson" / "output_1881_keyword_summary.csv",
        HERE / "Punjab 1881, Denzil Ibbetson" / "output_1881_concordance.csv",
        HERE / "Punjab 1881, Denzil Ibbetson" / "output_1881_records.csv",
        HERE / "Punjab 1881, Denzil Ibbetson" / "output_1881_passages.csv",
        # 1911-1919 H. A. Rose Ethnographic Glossary outputs
        HERE / "HA ROSE" / "output_rose_keyword_summary.csv",
        HERE / "HA ROSE" / "output_rose_concordance.csv",
        HERE / "HA ROSE" / "output_rose_bias_analysis.csv",
        HERE / "HA ROSE" / "output_rose_terms.csv",
        HERE / "HA ROSE" / "output_rose_passages.csv",
        # 1931 Interwar Census outputs
        HERE / "1931 census" / "output_1931_keyword_summary.csv",
        HERE / "1931 census" / "output_1931_concordance.csv",
        HERE / "1931 census" / "output_1931_chamba_demographics.csv",
        HERE / "1931 census" / "output_1931_records.csv",
        HERE / "1931 census" / "output_1931_passages.csv",
        # 1961 Village-Level Micro-Outputs (Brahmaur, Chitrari, Maingal)
        HERE / "1961 cenus/village surveys" / "output_brahmaur_records.csv",
        HERE / "1961 cenus/village surveys" / "output_brahmaur_passages.csv",
        HERE / "1961 cenus/village surveys" / "output_chitrari_records.csv",
        HERE / "1961 cenus/village surveys" / "output_chitrari_passages.csv",
        HERE / "1961 cenus/village surveys" / "output_maingal_records.csv",
        HERE / "1961 cenus/village surveys" / "output_maingal_passages.csv",
        # 1961 Comparative Concordance & Relative Word Frequencies
        HERE / "1961 cenus/village surveys" / "output_1961_village_normalized_frequencies.csv",
        HERE / "1961 cenus/village surveys" / "output_1961_interaction_concordance.csv",
        # Harmonized Primary Research Datasets & Comparative Matrices
        HERE / "data" / "quantitative_records.csv",
        HERE / "data" / "qualitative_passages.csv",
        HERE / "data" / "terminology_dictionary.csv",
        HERE / "outputs" / "tables" / "economic_relationship_evidence.csv",
        HERE / "outputs" / "tables" / "village_1961_normalized_frequencies.csv",
        HERE / "outputs" / "tables" / "census_comparability_crosswalk.csv",
        # Rendered Visual Figures (300 DPI)
        HERE / "outputs" / "figures" / "fig1_1961_village_mentions_normalized.png",
        HERE / "outputs" / "figures" / "fig2_livestock_ecological_distribution.png",
        HERE / "outputs" / "figures" / "fig3_bipartite_economic_exchange.png"
    ]

    all_exist = True
    for item in key_deliverables:
        rel_path = item.relative_to(HERE)
        if item.exists():
            size_kb = item.stat().st_size / 1024
            print(f" [OK] {rel_path} ({size_kb:.1f} KB)")
        else:
            print(f" [MISSING] {rel_path}")
            all_exist = False

    if all_exist:
        print("\nAll timeline computational analyses and research deliverables are verified.")
    else:
        print("\nWarning: One or more research deliverables were not found.")

if __name__ == '__main__':
    run_master_pipeline()
