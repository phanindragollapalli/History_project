import os
import sys
import shutil
import subprocess
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Define base project directories relative to this script
PROJECT_ROOT = Path(__file__).resolve().parent
FIGURES_DIR = PROJECT_ROOT / 'outputs' / 'figures'
TABLES_DIR = PROJECT_ROOT / 'outputs' / 'tables'

# Ensure the destination directories exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Resolve path for 1961 village frequencies; if missing, automatically generate or sync it
norm_csv_path = TABLES_DIR / 'village_1961_normalized_frequencies.csv'
village_local_csv = PROJECT_ROOT / '1961 cenus' / 'village surveys' / 'output_1961_village_normalized_frequencies.csv'

if not norm_csv_path.exists():
    if village_local_csv.exists():
        shutil.copyfile(village_local_csv, norm_csv_path)
    else:
        # Automatically run 1961 village surveys analysis to produce normalized frequency tables
        print("Required 1961 frequencies table not found. Automatically running analysis_1961.py...")
        script_1961 = PROJECT_ROOT / '1961 cenus' / 'village surveys' / 'analysis_1961.py'
        subprocess.run([sys.executable, str(script_1961)], cwd=str(script_1961.parent), check=True)

# Figure 1: Normalized Relative Lexical Frequencies Across 1961 Village Monographs
# This chart compares the textual representation of key social, occupational, and religious terms
# across Brahmaur, Chitrari, and Maingal. Frequencies are normalized per 1,000 searchable words to
# control for differences in monograph length (Brahmaur: 65,302 words; Chitrari: 41,363 words; Maingal: 70,551 words).
df_norm = pd.read_csv(norm_csv_path)

# Select the most analytically significant terms spanning pastoralism, caste groups, and religion
selected_terms = ['Sheep', 'Gaddi', 'Gujjar', 'Buffalo', 'Temple', 'Muslim', 'Nawala / Shiva', 'Brahmin', 'Sipi', 'Hali', 'Lohar']
df_filtered = df_norm[df_norm['category'].isin(selected_terms)].copy()
df_filtered['category'] = pd.Categorical(df_filtered['category'], categories=selected_terms, ordered=True)
df_filtered = df_filtered.sort_values('category')

categories = df_filtered['category'].tolist()
brahmaur_vals = df_filtered['brahmaur_norm_per_1k'].tolist()
chitrari_vals = df_filtered['chitrari_norm_per_1k'].tolist()
maingal_vals = df_filtered['maingal_norm_per_1k'].tolist()

x = np.arange(len(categories))
width = 0.26

plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
fig, ax = plt.subplots(figsize=(14, 7), dpi=300)

rects1 = ax.bar(x - width, brahmaur_vals, width, label='Brahmaur (Alpine Valley, ~7,000 ft)', color='#2b5c8f', edgecolor='black', linewidth=0.8)
rects2 = ax.bar(x, chitrari_vals, width, label='Chitrari (Terraced Basin, ~5,800 ft)', color='#d97724', edgecolor='black', linewidth=0.8)
rects3 = ax.bar(x + width, maingal_vals, width, label='Maingal (Forested Slopes, ~4,000 ft)', color='#2e8b57', edgecolor='black', linewidth=0.8)

ax.set_ylabel('Normalized Frequency (Mentions per 1,000 Searchable Words)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Figure 1: Lexical Representation Across 1961 Village Survey Monographs\nDemonstrating Ecological Altitudinal Ceilings and Caste/Religious Specialization', fontsize=14, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(categories, rotation=35, ha='right', fontsize=11, fontweight='semibold')
ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='#cccccc', fontsize=11, loc='upper right')
ax.set_ylim(0, 3.2)

# Direct data callouts on key peaks to highlight contrasts
for rect in [rects1[0], rects1[1], rects1[4], rects3[2], rects3[3], rects3[5], rects3[7], rects1[8]]:
    height = rect.get_height()
    if height > 0.3:
        ax.annotate(f'{height:.2f}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),
                    textcoords="offset points",
                    ha='center', va='bottom', fontsize=8, fontweight='bold')

# Source attribution and methodological citation
fig.text(0.12, 0.01, 
         'Source: Census of India 1961 Village Survey Monographs Nos. 5 (Brahmaur: 65,302 words), 10 (Chitrari: 41,363 words), and 27 (Maingal: 70,551 words).\nData normalized by total searchable OCR vocabulary to prevent volume-length distortion.', 
         fontsize=8, style='italic', color='#444444')

plt.tight_layout(rect=[0, 0.04, 1, 1])
fig1_path = str(FIGURES_DIR / 'fig1_1961_village_mentions_normalized.png')
plt.savefig(fig1_path, dpi=300)
plt.close()
print(f'Rendered Figure 1: {fig1_path}')


# Figure 2: Livestock Composition and Ecological Ceilings Across Study Villages (1961)
# Demonstrates the strict environmental constraints governing animal husbandry:
# High-altitude Brahmaur relies overwhelmingly on transhumant sheep and goats (4,484 head),
# whereas water buffaloes are entirely absent due to severe winter cold and lactation drop (PAS_002).
# Conversely, water buffaloes are concentrated exclusively in sub-Himalayan Maingal (217 head).
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

villages = ['Brahmaur (~7,000 ft)\nHigh Alpine Valley', 'Chitrari (~5,800 ft)\nTerraced River Basin', 'Maingal (~4,000 ft)\nSub-Himalayan Forest']
sheep_goats = [4484, 123, 275]
buffaloes = [0, 0, 217]
cattle_bullocks = [477, 155, 126]

x = np.arange(len(villages))
width = 0.25

r1 = ax.bar(x - width, sheep_goats, width, label='Sheep & Goats (Pastoral Transhumance)', color='#4682b4', edgecolor='black', linewidth=0.8)
r2 = ax.bar(x, buffaloes, width, label='Water Buffaloes (Forest Dairying)', color='#8b0000', edgecolor='black', linewidth=0.8)
r3 = ax.bar(x + width, cattle_bullocks, width, label='Cattle / Draft Bullocks (Terrace Plowing)', color='#daa520', edgecolor='black', linewidth=0.8)

ax.set_ylabel('Total Livestock Count (Head of Cattle/Flock)', fontsize=12, fontweight='bold', labelpad=10)
ax.set_title('Figure 2: Livestock Ecology and Altitudinal Ceilings in Chamba District (1961)\nComplete Absence of Water Buffaloes in Brahmaur vs. Concentration in Sub-Himalayan Maingal', fontsize=13, fontweight='bold', pad=15)
ax.set_xticks(x)
ax.set_xticklabels(villages, fontsize=11, fontweight='semibold')
ax.legend(frameon=True, facecolor='#f8f9fa', edgecolor='#cccccc', fontsize=10, loc='upper right')

for rects in [r1, r2, r3]:
    for rect in rects:
        h = rect.get_height()
        if h > 0:
            ax.annotate(f'{h}',
                        xy=(rect.get_x() + rect.get_width() / 2, h),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=9, fontweight='bold')

fig.text(0.12, 0.01,
         'Source: Dataset A (quantitative_records.csv), Records REC_007, REC_010, REC_017, REC_023.\nHistorical Explanation: Extreme alpine winter cold causes severe lactation collapse in water buffaloes (dropping from 9 to 4 seers/day, PAS_002), restricting them to lower elevations.',
         fontsize=8, style='italic', color='#444444')

plt.tight_layout(rect=[0, 0.05, 1, 1])
fig2_path = str(FIGURES_DIR / 'fig2_livestock_ecological_distribution.png')
plt.savefig(fig2_path, dpi=300)
plt.close()
print(f'Rendered Figure 2: {fig2_path}')


# Figure 3: Bipartite Interaction Network and Socio-Economic Exchange Matrix (1961)
# Models the reciprocal economic, ritual, and ecological relationships connecting distinct
# social groups (left column) to specialized services and exchange institutions (right column).
# Crucially, Sedentary Hindu Villagers serve as the core agrarian counterparty for attached ploughing,
# customary tool repair (khalian), dairy purchases, and field penning fertilization.
fig, ax = plt.subplots(figsize=(15, 8.5), dpi=300)
ax.axis('off')

# Title and subtitle explaining the analytical scope
ax.text(0.5, 0.97, 'Figure 3: Matrix of Socio-Economic Interdependence Across Study Villages (1961)', 
        fontsize=15, fontweight='bold', ha='center')
ax.text(0.5, 0.93, 'Empirical Bipartite Mapping of Hereditary Caste Services, Customary Barter, and Commercial Exchange', 
        fontsize=11, style='italic', ha='center', color='#555555')

# Left Column: Social Actors and Occupational Communities
actors = [
    ('Gaddi Flock Owners\n(Rajput / Brahmin)', '#2b5c8f', 0.83),
    ('Sipi Artisans\n(Weavers / Drummers)', '#4682b4', 0.69),
    ('Hali Attached Labourers\n(Aryas - Halis)', '#d97724', 0.55),
    ('Lohar Blacksmiths\n(Iron Tool Artisans)', '#8b0000', 0.41),
    ('Sedentary Hindu Villagers\n(Terraced Cultivators)', '#2e8b57', 0.27),
    ('Muslim Gujjars\n(Buffalo Pastoralists)', '#006400', 0.13)
]

# Right Column: Exchange Media, Reciprocal Services, and Customary Jajmani Barter
exchanges = [
    ('Wage Shepherding (Pohal Contract)\n[Free meals + wool + 2-4 sheep/100 + Rs. 2/mo]', '#333333', 0.83),
    ('Textile Processing & Garments\n[Chola tailoring, pattu/gardu tweed weaving]', '#333333', 0.71),
    ('Ritual Nawala Drummers & Sacrificial Meat\n[Dholak playing in exchange for sheep neck (ghardi)]', '#333333', 0.59),
    ('Attached Ploughing & Harvest Tenancy\n[Agricultural labor bypassing high-caste plough taboos]', '#333333', 0.47),
    ('Iron Implement Manufacture & Maintenance\n[Repairs rewarded via non-monetary khalian grain shares]', '#333333', 0.35),
    ('High-Fat Buffalo Dairy & Forest Manure\n[Commercial ghee marketing & seasonal alpine milk sale]', '#333333', 0.21),
    ('Overnight Field Penning (Tarkals)\n[Pastoral sheep manure fertilization for arable cereals]', '#333333', 0.08)
]

# Render community actor nodes on the left side
for name, col, y_pos in actors:
    bbox_props = dict(boxstyle='round,pad=0.55', facecolor=col, edgecolor='black', linewidth=1.2, alpha=0.92)
    ax.text(0.18, y_pos, name, fontsize=10, fontweight='bold', color='white', ha='center', va='center', bbox=bbox_props)

# Render exchange service nodes on the right side
for name, col, y_pos in exchanges:
    bbox_props = dict(boxstyle='square,pad=0.55', facecolor='#f5f6f8', edgecolor='#555555', linewidth=1.1)
    ax.text(0.80, y_pos, name, fontsize=9.5, fontweight='semibold', color='#222222', ha='center', va='center', bbox=bbox_props)

# Verified historical exchange ties connecting actors to their corresponding economic practices
# Includes explicit reciprocal connections for Sedentary Hindu Villagers (actor index 4)
links = [
    # Gaddi Flock Owners: contractual wage herding (Pohal) and ecological fallow penning
    (0, 0, 0.00, 0.00, 'REL_001', '#2b5c8f', 0.45, 0.00),
    (0, 6, -0.015, 0.01, 'REL_004 (Flock Transit)', '#2b5c8f', 0.42, 0.03),
    
    # Sipi Artisans: woolen textile processing and ritual Nawala drumming
    (1, 1, 0.00, 0.00, 'REL_002', '#4682b4', 0.45, 0.00),
    (1, 2, -0.01, 0.01, 'REL_003', '#4682b4', 0.46, 0.01),
    
    # Hali Attached Labourers: attached agricultural tenancy bypassing high-caste plough taboos
    (2, 3, 0.00, 0.01, 'REL_005 (Labour)', '#d97724', 0.44, 0.02),
    
    # Lohar Blacksmiths: tool manufacture and repairs rewarded by khalian grain
    (3, 4, 0.00, 0.01, 'REL_008 (Craft)', '#8b0000', 0.44, 0.01),
    
    # Sedentary Hindu Villagers: central agrarian counterparties in agricultural labour, craft barter, dairy, and manuring
    (4, 3, 0.02, -0.01, 'REL_005 (Brahmin Tenancy)', '#2e8b57', 0.50, -0.02),
    (4, 4, 0.01, -0.01, 'REL_008 (Khalian Barter)', '#2e8b57', 0.49, -0.01),
    (4, 5, -0.005, 0.01, 'REL_006 / REL_010', '#2e8b57', 0.47, 0.00),
    (4, 6, -0.02, -0.01, 'REL_004 (Terrace Penning)', '#2e8b57', 0.52, -0.04),
    
    # Muslim Gujjars: dairy production, buffalo dung, and draft bullock exchange
    (5, 5, 0.01, -0.01, 'REL_006 / REL_009 / REL_010', '#006400', 0.40, 0.01),
]

# Draw directional flow arrows with offset midpoints to prevent visual collision
for a_idx, e_idx, dy_start, dy_end, lbl, c, x_mid, dy_mid in links:
    y_start = actors[a_idx][2] + dy_start
    y_end = exchanges[e_idx][2] + dy_end
    
    # Draw arrow from actor to exchange node
    ax.annotate('', xy=(0.59, y_end), xytext=(0.32, y_start),
                arrowprops=dict(arrowstyle='->', color=c, lw=1.8, alpha=0.85, shrinkA=4, shrinkB=4))
    
    # Annotate relationship identifier along the connection line
    y_mid = (y_start + y_end) / 2 + dy_mid
    ax.text(x_mid, y_mid, lbl, fontsize=7.5, fontweight='bold', color=c, ha='center', va='center',
            bbox=dict(boxstyle='round,pad=0.22', facecolor='white', edgecolor=c, lw=0.75, alpha=0.92))

# Archival source citation and verification lineage
fig.text(0.10, 0.02,
         'Source: Dataset B (qualitative_passages.csv) and Relational Matrix (economic_relationship_evidence.csv).\nVerification Chain: Primary Census Page -> Verbatim Text Passage -> Coded Actors & Exchange Medium -> Historical Matrix.',
         fontsize=8, style='italic', color='#555555')

plt.tight_layout()
fig3_path = str(FIGURES_DIR / 'fig3_bipartite_economic_exchange.png')
plt.savefig(fig3_path, dpi=300)
plt.close()
print(f'Rendered Figure 3: {fig3_path}')
