# Changing Patterns of Occupation, Ecological Niches, and Socio-Economic Interdependence in Chamba District (1881–1961)

**A Computational and Historiographical Analysis of Himalayan Agrarian and Pastoral Systems**  
**Course:** Introduction to Historical Analysis (`Intro2Hist` / `HS3.201`)  
**Authors:** Bala Subramanian, Vagdevi Reddy, Phanindra  

---

## 📌 Project Overview

This repository contains the complete computational analysis pipeline, curated datasets, rendered figures, and LaTeX source code for the final research paper investigating how changing patterns of occupation, environmental constraints, and economic interdependence shaped caste and religious relations in the upper Ravi River basin (Brahmaur, Chitrari, and Maingal) of Chamba District, Himachal Pradesh, between 1881 and 1961.

The investigation synthesizes:
1. **Historical Materialism (Marxist Historiography):** Control over productive assets (*dead labour* in land and flocks vs. *living labour*), structural interdependence, extraction of surplus, and subaltern status contestation (*Aryas–Halis*).
2. **The *Annales* School of Environmental History:** *Longue durée* altitudinal relief, physiological ceilings on animal husbandry (cold-induced lactation collapse in water buffaloes), *histoire totale* (shelters, diet, clothing, tools), and *histoire des mentalités* (vernacular oral ballads).
3. **Computational Text Analysis:** Bilingual OCR, regular-expression Keyword-in-Context (KWIC) concordance mining across 2.2+ million words, relative frequency normalization ($/1,000$ words), bipartite network modeling (12 documented exchange links), and qualitative multi-label thematic coding across four benchmark eras (1881, 1911–1919, 1931, and 1961).

---

## 🚀 Quickstart: Reproducing All Results

To replicate all 36 data tables, evidence registers, and high-resolution figures from scratch on any system:

### 1. Clone the Repository
```bash
git clone https://github.com/phanindragollapalli/History_project.git
cd History_project
```

### 2. Set Up Python Virtual Environment
We recommend Python 3.10, 3.11, or 3.12:
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

*(Alternatively, if using `uv`: `uv venv && uv pip install -r requirements.txt`)*

### 3. Run the Master Analysis Pipeline
Execute the single entry-point master script:
```bash
python master_analysis_pipeline.py
```
This automatically executes all 8 computational modules in sequence:
1. `Punjab 1881, Denzil Ibbetson/analysis_1881.py` (1881 Imperial Census text analysis)
2. `HA ROSE/analysis_rose.py` (1911–1919 Ethnographic Glossary analysis)
3. `1931 census/analysis_1931.py` (1931 Interwar Census analysis)
4. `1961 cenus/village surveys/analysis_1961.py` (1961 Village Surveys micro-analysis)
5. `build_curated_datasets.py` (Harmonized datasets and crosswalks)
6. `generate_figures.py` (Renders Figures 1, 2, and 3 at 300 DPI)
7. `audit_and_evidence_register.py` (Audits claims and produces the 45-row Evidence Register)
8. `phase3_computational_analysis.py` (Produces the 4 core Phase 3 analytical tables)

At completion, the pipeline automatically validates that all **36 deliverables** exist on disk.

---

## 📄 Compiling the Final LaTeX Report

The final historical research paper is written in clean, standard LaTeX and saved as **`Phase3_report.tex`**.

### Option A: Local Compilation (via `pdflatex`)
Run `pdflatex` twice (to fully resolve the table of contents and figure cross-references):
```bash
pdflatex -interaction=nonstopmode -halt-on-error Phase3_report.tex
pdflatex -interaction=nonstopmode -halt-on-error Phase3_report.tex
```
The output PDF will be generated as **`Phase3_report.pdf`**.

### Option B: Compiling on Overleaf
1. Create a new blank project on [Overleaf](https://www.overleaf.com/).
2. Upload `Phase3_report.tex` to the project root.
3. Upload the `outputs/figures/` folder containing the three PNG figures:
   - `outputs/figures/fig1_1961_village_mentions_normalized.png`
   - `outputs/figures/fig2_livestock_ecological_distribution.png`
   - `outputs/figures/fig3_bipartite_economic_exchange.png`
4. Click **Recompile**. The document will compile cleanly in 19 pages with zero errors.

---

## 📂 Repository Structure

```
History_project/
├── Phase3_report.pdf                 # Final 19-page research paper (compiled PDF)
├── Phase3_report.tex                 # Final research paper source code (LaTeX)
├── master_analysis_pipeline.py       # Master script running all 8 analysis modules
├── audit_and_evidence_register.py    # Audits claims and compiles the master evidence register
├── phase3_computational_analysis.py  # Generates Phase 3 comparative tables and coding
├── generate_figures.py               # Generates high-resolution figures (300 DPI)
├── build_curated_datasets.py         # Harmonizes raw concordance outputs into data/
├── requirements.txt                  # Pinned Python dependencies for reproducibility
│
├── outputs/
│   ├── figures/                      # Rendered 300-DPI visual figures
│   │   ├── fig1_1961_village_mentions_normalized.png
│   │   ├── fig2_livestock_ecological_distribution.png
│   │   └── fig3_bipartite_economic_exchange.png
│   └── tables/                       # Audited research tables and crosswalks
│       ├── final_evidence_register.csv        # 45 audited evidence claims (13 columns)
│       ├── comparative_village_economy.csv    # Comparative demographic and livestock profile
│       ├── exchange_network_edges.csv         # 12 documented socio-economic exchange links
│       ├── classification_crosswalk_1881_1961.csv # Longitudinal classification crosswalk
│       └── thematic_coding_passages.csv       # 20 passages coded across 9 themes
│
├── data/                             # Harmonized timeline datasets
│   ├── quantitative_records.csv      # Demographic and livestock records
│   ├── qualitative_passages.csv      # Mined qualitative excerpts
│   └── terminology_dictionary.csv    # Vernacular and administrative dictionary
│
├── Punjab 1881, Denzil Ibbetson/     # 1881 Census raw text, scripts, and outputs
├── HA ROSE/                          # 1911–1919 Glossary raw text, scripts, and outputs
├── 1931 census/                      # 1931 Census raw text, scripts, and outputs
├── 1961 cenus/village surveys/       # 1961 Village Monographs (Brahmaur, Chitrari, Maingal)
│
├── docs/                             # Course lecture slides and plan documents (ignored)
│   ├── Lectures 8 9 10 - Marxist History, Intro2Hist M2026.pdf
│   ├── Lectures 11-13, Annales Historiography, Intro2Hist M2026.pdf
│   ├── Phase_3_Execution_Plan_Updated.md
│   └── phase3_plan.md
│
├── Research_Question.pdf             # Phase 1 submission deliverable
└── History_Analysis.pdf              # Phase 2 submission deliverable
```

---

## 📊 Key Research Findings

1. **Environmental Altitudes Imposed Absolute Biological Ceilings (*Longue Durée*):**
   Water buffaloes (*Bubalus bubalis*) suffered severe cold-induced lactation collapse (dropping by 55.6% from 9 to 4 seers/day) in alpine Brahmaur ($\sim$7,000 ft), permanently barring dairy transhumance into the highlands and securing the Gaddi monopoly over sheep pastoralism, while commercial dairy production was confined to sub-Himalayan Maingal ($\sim$4,000 ft).
2. **Asymmetrical Labour Divisions Sustained Caste Hierarchy (*Dead vs. Living Labour*):**
   Dominant proprietors who monopolized accumulated surplus (*dead labour* in land and flocks) were structurally dependent on subordinate *living labour*: Sipis in Brahmaur maintained an indispensable tripartite monopoly as wage shepherds (*pohals* receiving cash and a 2–4% lamb share dividend), master tweed weavers (*rachh* looms), and *Nawala* ritual drummers; attached Halis in Chitrari tilled Brahmin lands under purity taboos while mobilizing as *Aryas–Halis*; and Lohars in Maingal were paid through customary unhusked grain sheaves (*khalian*).
3. **Complementary Ecological Niches Grounded Religious Co-Existence:**
   In Maingal, 203 Muslim Gujjars (81.5%) in forest *kothas* grazed buffaloes while Hindu Brahmins farmed valley terraces, trading dung manure, draft bullocks, and water rights without land competition.
4. **Multi-Tiered Economies:**
   Cash contracts, customary non-monetary jajmani barter, ritual perquisites, and commercial bazaar sales functioned concurrently rather than displacing one another.
