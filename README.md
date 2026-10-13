# History Project: Changing Patterns of Occupation and Economic Interdependence in Chamba (1881–1961)

## How to Run the Project

### 1. End-to-End Pipeline Execution (Recommended)
To execute all four timeline modules, generate harmonized datasets in `data/`, render publication figures in `outputs/figures/`, and verify all 23 deliverables with a single command:

```bash
# Direct Python:
python3 master_analysis_pipeline.py

# Or via uv package runner:
uv run --with pandas,matplotlib,seaborn python3 master_analysis_pipeline.py
```

### 2. Running Individual Timeline Modules
Each timeline script can also be executed independently from the root or within its folder:

* **1881 Punjab Census:**
  ```bash
  python3 "Punjab 1881, Denzil Ibbetson/analysis_1881.py"
  ```
* **1911–1919 H. A. Rose Glossary:**
  ```bash
  python3 "HA ROSE/analysis_rose.py"
  ```
* **1931 Punjab Census:**
  ```bash
  python3 "1931 census/analysis_1931.py"
  ```
* **1961 Village Surveys (Brahmaur, Chitrari, Maingal):**
  ```bash
  python3 "1961 cenus/village surveys/analysis_1961.py"
  ```

### 3. Harmonization and Figure Rendering
To generate harmonized crosswalks and render visual figures separately:
```bash
# Harmonize records into data/ and outputs/tables/:
python3 build_curated_datasets.py

# Render Figures 1, 2, and 3 at 300 DPI:
python3 generate_figures.py
```