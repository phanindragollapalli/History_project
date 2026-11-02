#!/usr/bin/env python3
"""
Phase 3 Part 2: Targeted Computational Analyses Generator

This script implements the four targeted computational analyses specified in the
Phase 3 Execution Plan (Section 5A):
1. Analysis 1: Comparative Village Occupational & Economic Structure (`outputs/tables/comparative_village_economy.csv`)
2. Analysis 2: Economic Interdependence Network Register (`outputs/tables/exchange_network_edges.csv`)
3. Analysis 3: Longitudinal Classification Crosswalk 1881-1961 (`outputs/tables/classification_crosswalk_1881_1961.csv`)
4. Analysis 4: Qualitative Thematic Multi-Label Coding of 20 Passages (`outputs/tables/thematic_coding_passages.csv`)
   and computes the Theme-by-Village analytical distribution matrix.
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

HERE = Path(__file__).resolve().parent
DATA_DIR = HERE / "data"
OUTPUTS_DIR = HERE / "outputs" / "tables"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def generate_analysis_1_comparative_economy():
    """Analysis 1: Comparative Village Occupational & Economic Structure."""
    print("=" * 80)
    print("ANALYSIS 1: COMPARATIVE VILLAGE OCCUPATIONAL & ECONOMIC STRUCTURE")
    print("=" * 80)

    comp_data = [
        # Brahmaur
        {
            'village': 'Brahmaur',
            'sub_tehsil_or_tehsil': 'Brahmaur Sub-Tehsil (Gaderan)',
            'survey_year': 1961,
            'elevation_ft': 7000,
            'ecological_zone': 'High Alpine Valley',
            'total_surveyed_households': 99,
            'total_surveyed_population': 721,
            'community_name': 'Hindu Rajputs',
            'community_households': 55,
            'community_population': 293,
            'community_share_pct': 40.6,
            'dominant_livelihood': 'Agro-Pastoralism (Flock ownership & terrace cultivation)',
            'sheep_and_goat_count': 2364,
            'cattle_count': 101,  # 49 bulls, 52 cows
            'buffalo_count': 0,
            'key_productive_resources': 'Flocks of sheep/goats, terraced arable land, alpine pasture rights (dhars)',
            'labour_relationships': 'Employs Sipis as hired wage-shepherds (pohals); family household farming',
            'modes_of_remuneration': 'Cash wages (Rs. 2/mo), meals, clothing, wool, 2-4% lamb shares'
        },
        {
            'village': 'Brahmaur',
            'sub_tehsil_or_tehsil': 'Brahmaur Sub-Tehsil (Gaderan)',
            'survey_year': 1961,
            'elevation_ft': 7000,
            'ecological_zone': 'High Alpine Valley',
            'total_surveyed_households': 99,
            'total_surveyed_population': 721,
            'community_name': 'Hindu Brahmans',
            'community_households': 48,
            'community_population': 251,
            'community_share_pct': 34.8,
            'dominant_livelihood': 'Priestly Service & Agro-Pastoralism (Flock ownership)',
            'sheep_and_goat_count': 2027,
            'cattle_count': 97,  # 52 bulls, 45 cows
            'buffalo_count': 0,
            'key_productive_resources': 'Temple perquisites (Chaurasi complex), flocks, arable land',
            'labour_relationships': 'Flock owners hiring pohals; sacred officiants at Nawala ceremonies',
            'modes_of_remuneration': 'Sacred fees, food perquisites, flock profits, commercial wool sales'
        },
        {
            'village': 'Brahmaur',
            'sub_tehsil_or_tehsil': 'Brahmaur Sub-Tehsil (Gaderan)',
            'survey_year': 1961,
            'elevation_ft': 7000,
            'ecological_zone': 'High Alpine Valley',
            'total_surveyed_households': 99,
            'total_surveyed_population': 721,
            'community_name': 'Hindu Sipis',
            'community_households': 15,
            'community_population': 119,
            'community_share_pct': 16.5,
            'dominant_livelihood': 'Artisanal Textile Weaving, Wage Shepherding, Ritual Music',
            'sheep_and_goat_count': 93,
            'cattle_count': 41,  # 22 bulls, 19 cows
            'buffalo_count': 0,
            'key_productive_resources': 'Hand shearing scissors (katar), pit frame looms (rachh), dholak drums',
            'labour_relationships': 'Wage shepherds (pohals) for Rajputs/Brahmans; tailors and weavers; Nawala drummers',
            'modes_of_remuneration': 'In-kind wool, meals, clothes, lamb dividends, cash wages (Rs 2/mo), ghardi sacrificial meat'
        },
        {
            'village': 'Brahmaur',
            'sub_tehsil_or_tehsil': 'Brahmaur Sub-Tehsil (Gaderan)',
            'survey_year': 1961,
            'elevation_ft': 7000,
            'ecological_zone': 'High Alpine Valley',
            'total_surveyed_households': 99,
            'total_surveyed_population': 721,
            'community_name': 'Hindu Khatris',
            'community_households': 6,
            'community_population': 28,
            'community_share_pct': 3.9,
            'dominant_livelihood': 'Retail Shopkeeping & Trade',
            'sheep_and_goat_count': 0,
            'cattle_count': 0,
            'buffalo_count': 0,
            'key_productive_resources': 'Bazaar shops, retail goods, trade credit',
            'labour_relationships': 'Commercial exchange with villagers; provision of salt, iron, manufactured wares',
            'modes_of_remuneration': 'Cash sales, barter of wool and grain for store commodities'
        },
        {
            'village': 'Brahmaur',
            'sub_tehsil_or_tehsil': 'Brahmaur Sub-Tehsil (Gaderan)',
            'survey_year': 1961,
            'elevation_ft': 7000,
            'ecological_zone': 'High Alpine Valley',
            'total_surveyed_households': 99,
            'total_surveyed_population': 721,
            'community_name': 'Hindu Reharas',
            'community_households': 3,
            'community_population': 22,
            'community_share_pct': 3.1,
            'dominant_livelihood': 'Silversmithing & Ornaments Manufacture',
            'sheep_and_goat_count': 0,
            'cattle_count': 0,
            'buffalo_count': 0,
            'key_productive_resources': 'Crucibles, blowpipes, metal anvils, silversmithing tools',
            'labour_relationships': 'Fabrication of silver ornaments (chiri, ralu, kanbali) for peasant families',
            'modes_of_remuneration': 'Cash fee per tola silver crafted + retention of metal filings and wedding food gifts'
        },
        {
            'village': 'Brahmaur',
            'sub_tehsil_or_tehsil': 'Brahmaur Sub-Tehsil (Gaderan)',
            'survey_year': 1961,
            'elevation_ft': 7000,
            'ecological_zone': 'High Alpine Valley',
            'total_surveyed_households': 99,
            'total_surveyed_population': 721,
            'community_name': 'Muslims',
            'community_households': 1,
            'community_population': 8,
            'community_share_pct': 1.1,
            'dominant_livelihood': 'Tailoring Service',
            'sheep_and_goat_count': 0,
            'cattle_count': 0,
            'buffalo_count': 0,
            'key_productive_resources': 'Sewing tools',
            'labour_relationships': 'Artisanal tailoring for local residents',
            'modes_of_remuneration': 'Cash fees and piece-rate payments'
        },
        
        # Chitrari
        {
            'village': 'Chitrari',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 5800,
            'ecological_zone': 'Intermediate Terraced River Basin',
            'total_surveyed_households': 79,
            'total_surveyed_population': 404,
            'community_name': 'Hindu Brahmins',
            'community_households': 60,
            'community_population': 311,
            'community_share_pct': 77.0,
            'dominant_livelihood': 'Landed Arable Cultivation & Temple Beneficiaries',
            'sheep_and_goat_count': 123,
            'cattle_count': 155,
            'buffalo_count': 0,
            'key_productive_resources': 'Terraced arable fields, historic royal land endowment from Raja Meru-Varman',
            'labour_relationships': 'High-caste taboos on touching plough; dependent on attached Halis for tillage',
            'modes_of_remuneration': 'Crop shares, rent, temple stipends, purchase of high-dhar Gujjar milk'
        },
        {
            'village': 'Chitrari',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 5800,
            'ecological_zone': 'Intermediate Terraced River Basin',
            'total_surveyed_households': 79,
            'total_surveyed_population': 404,
            'community_name': 'Hindu Rathis / Rajputs',
            'community_households': 6,
            'community_population': 32,
            'community_share_pct': 7.9,
            'dominant_livelihood': 'Terraced Agriculture',
            'sheep_and_goat_count': 18,
            'cattle_count': 16,
            'buffalo_count': 0,
            'key_productive_resources': 'Owner-cultivated terraced plots',
            'labour_relationships': 'Family agricultural labour; reciprocal field assistance',
            'modes_of_remuneration': 'Subsistence crop harvest'
        },
        {
            'village': 'Chitrari',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 5800,
            'ecological_zone': 'Intermediate Terraced River Basin',
            'total_surveyed_households': 79,
            'total_surveyed_population': 404,
            'community_name': 'Hindu Bensis',
            'community_households': 7,
            'community_population': 29,
            'community_share_pct': 7.2,
            'dominant_livelihood': 'Ceremonial Temple Music & Agriculture',
            'sheep_and_goat_count': 12,
            'cattle_count': 10,
            'buffalo_count': 0,
            'key_productive_resources': 'Temple horn/pipes, small arable plots',
            'labour_relationships': 'Piping and drumming at Shakti Devi temple daily worship and annual fairs',
            'modes_of_remuneration': 'Hereditary temple grain stipends and annual collections from villagers'
        },
        {
            'village': 'Chitrari',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 5800,
            'ecological_zone': 'Intermediate Terraced River Basin',
            'total_surveyed_households': 79,
            'total_surveyed_population': 404,
            'community_name': 'Hindu Aryas—Halis',
            'community_households': 2,
            'community_population': 6,
            'community_share_pct': 1.5,
            'dominant_livelihood': 'Attached Agricultural Ploughing & Tenancy',
            'sheep_and_goat_count': 6,
            'cattle_count': 6,
            'buffalo_count': 0,
            'key_productive_resources': 'Wooden ploughs, agricultural labour skills',
            'labour_relationships': 'Attached ploughmen for Brahmin landowners; socio-religious Arya Samaj mobility',
            'modes_of_remuneration': 'Crop-share tenancy, customary maintenance grain, contested service status'
        },

        # Maingal
        {
            'village': 'Maingal',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 4000,
            'ecological_zone': 'Sub-Himalayan Forested Slopes',
            'total_surveyed_households': 40,
            'total_surveyed_population': 249,
            'community_name': 'Muslim Gujjars',
            'community_households': 25,
            'community_population': 203,
            'community_share_pct': 81.5,
            'dominant_livelihood': 'Pastoral Buffalo Dairying & Terrace Maize Cultivation',
            'sheep_and_goat_count': 0,
            'cattle_count': 45,
            'buffalo_count': 217,
            'key_productive_resources': '217 water buffaloes, forest grazing runs, dwelling-byre kothas, crop machans',
            'labour_relationships': 'Forest foraging, milking, ghee production, manure/bullock exchange with Brahmins',
            'modes_of_remuneration': 'Cash ghee sales in Chamba town bazaar; non-monetary manure exchange'
        },
        {
            'village': 'Maingal',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 4000,
            'ecological_zone': 'Sub-Himalayan Forested Slopes',
            'total_surveyed_households': 40,
            'total_surveyed_population': 249,
            'community_name': 'Hindu Brahmins',
            'community_households': 3,
            'community_population': 34,
            'community_share_pct': 13.7,
            'dominant_livelihood': 'Terraced Maize/Wheat Cultivation & Water Mill (Gharat)',
            'sheep_and_goat_count': 21,
            'cattle_count': 32,
            'buffalo_count': 0,
            'key_productive_resources': 'Nucleated arable lands at Maingal proper, water mill on Sila stream',
            'labour_relationships': 'Grain milling; purchase of buffalo manure from Gujjars; draft bullock borrowing',
            'modes_of_remuneration': 'Milling dues (2 seers/maund ground); agricultural grain harvest'
        },
        {
            'village': 'Maingal',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 4000,
            'ecological_zone': 'Sub-Himalayan Forested Slopes',
            'total_surveyed_households': 40,
            'total_surveyed_population': 249,
            'community_name': 'Hindu Lohars',
            'community_households': 2,
            'community_population': 8,
            'community_share_pct': 3.2,
            'dominant_livelihood': 'Blacksmithy (Tool Manufacture/Repair) & Agriculture',
            'sheep_and_goat_count': 0,
            'cattle_count': 6,
            'buffalo_count': 0,
            'key_productive_resources': 'Forge, anvils, hammers, bellows; workshops in Dapaythagot hamlet',
            'labour_relationships': 'Forging and repair of ploughshares, axes, sickles for Gujjars and Brahmins',
            'modes_of_remuneration': 'Customary unhusked grain sheaves (khalian) delivered directly from threshing floors'
        },
        {
            'village': 'Maingal',
            'sub_tehsil_or_tehsil': 'Chamba Tehsil',
            'survey_year': 1961,
            'elevation_ft': 4000,
            'ecological_zone': 'Sub-Himalayan Forested Slopes',
            'total_surveyed_households': 40,
            'total_surveyed_population': 249,
            'community_name': 'Hindu Rajputs',
            'community_households': 1,
            'community_population': 4,
            'community_share_pct': 1.6,
            'dominant_livelihood': 'Terraced Agriculture',
            'sheep_and_goat_count': 0,
            'cattle_count': 2,
            'buffalo_count': 0,
            'key_productive_resources': 'Terraced field plots',
            'labour_relationships': 'Subsistence family farming',
            'modes_of_remuneration': 'Direct harvest produce'
        }
    ]

    df_comp = pd.DataFrame(comp_data)
    out_file = OUTPUTS_DIR / "comparative_village_economy.csv"
    df_comp.to_csv(out_file, index=False)
    print(f"Generated {len(df_comp)} records in {out_file}\n")

def generate_analysis_2_network_edges():
    """Analysis 2: Economic Interdependence Network Register."""
    print("=" * 80)
    print("ANALYSIS 2: ECONOMIC INTERDEPENDENCE NETWORK REGISTER (12 RELATIONSHIPS)")
    print("=" * 80)

    net_edges = [
        {
            'relationship_id': 'REL_001',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Brahmaur',
            'historical_period': '1961',
            'actor_a': 'Gaddi Flock Owner (Malundi)',
            'actor_a_type': 'Upper-Caste Pastoral Landholder (Rajput/Brahman)',
            'actor_b': 'Hired Wage-Shepherd (Pohal)',
            'actor_b_type': 'Lower-Caste Pastoral Labourer (Sipi)',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'High-altitude flock herding, grazing migration across passes',
            'exchange_medium': 'Cash wages (Rs. 2/mo), free food, wool, 2-4% lamb dividends',
            'transaction_category': 'Mixed Contractual (Cash Wage + In-Kind Dividend)',
            'source_title': 'Census of India 1961: Brahmaur',
            'page_or_table_ref': 'p. 44',
            'passage_id': 'PAS_001',
            'historical_significance': 'Demonstrates stratified wage labour emerging within transhumant pastoralism.'
        },
        {
            'relationship_id': 'REL_002',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Brahmaur',
            'historical_period': '1961',
            'actor_a': 'Flock Owners (Rajput/Brahman)',
            'actor_a_type': 'Livestock Owners',
            'actor_b': 'Sipi Artisans (Weavers & Tailors)',
            'actor_b_type': 'Artisanal Service Caste',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Sheep shearing with katar; weaving tweed (pattu), blankets (gardu); tailoring chola/dora',
            'exchange_medium': 'Portion of sheared raw wool, grains, meals',
            'transaction_category': 'Customary In-Kind Barter',
            'source_title': 'Census of India 1961: Brahmaur',
            'page_or_table_ref': 'p. 38',
            'passage_id': 'PAS_004',
            'historical_significance': 'Shows indispensable lower-caste technical monopoly over textile manufacturing.'
        },
        {
            'relationship_id': 'REL_003',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Brahmaur',
            'historical_period': '1961',
            'actor_a': 'Brahman Priest / Peasant Host',
            'actor_a_type': 'High-Caste Sacral Officiant / Householder',
            'actor_b': 'Sipi Musicians (Dholak Drummers)',
            'actor_b_type': 'Low-Caste Ritual Musicians',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Ceremonial drumming during Shaivite Nawala sacrificial feasts',
            'exchange_medium': 'Ghardi (sacrificed sheep neck) and cooked festive meals',
            'transaction_category': 'Customary Ritual Entitlement',
            'source_title': 'Census of India 1961: Brahmaur',
            'page_or_table_ref': 'p. 62',
            'passage_id': 'PAS_005',
            'historical_significance': 'Proves ritual interdependence crossing purity/pollution boundaries in mountain Shaivism.'
        },
        {
            'relationship_id': 'REL_004',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Brahmaur',
            'historical_period': '1961',
            'actor_a': 'Gaddi Shepherds',
            'actor_a_type': 'Transhumant Pastoralists',
            'actor_b': 'Terraced Arable Cultivators',
            'actor_b_type': 'Sedentary Farmers',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Overnight flock penning on fallow fields (tarkals) for dung manure fertilization',
            'exchange_medium': 'Free night shelter, staple food grains, flour',
            'transaction_category': 'Ecological Nutrient Transfer',
            'source_title': 'Census of India 1961: Brahmaur',
            'page_or_table_ref': 'pp. 45-46',
            'passage_id': 'PAS_001',
            'historical_significance': 'Symbiotic agro-pastoral cycle cycling nitrogen from alpine forage into terraced grain crops.'
        },
        {
            'relationship_id': 'REL_005',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Chitrari',
            'historical_period': '1961',
            'actor_a': 'Brahmin Landowners',
            'actor_a_type': 'Landed Temple Beneficiaries (77% pop)',
            'actor_b': 'Halis / Aryas',
            'actor_b_type': 'Attached Ploughmen Tenancy (1.5% pop)',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Field ploughing to circumvent high-caste plough taboos; harvesting labour',
            'exchange_medium': 'Tied crop-share tenancy, land access, maintenance grain',
            'transaction_category': 'Attached Tenancy & Service Barter',
            'source_title': 'Census of India 1961: Chitrari',
            'page_or_table_ref': 'pp. 11-12',
            'passage_id': 'PAS_007',
            'historical_significance': 'Illustrates caste taboos structuring labour, contested via Arya Samaj mobilisation.'
        },
        {
            'relationship_id': 'REL_006',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Chitrari',
            'historical_period': '1961',
            'actor_a': 'Sedentary Hindu Villagers',
            'actor_a_type': 'Agrarian Households',
            'actor_b': 'Nomadic Muslim Gujjars',
            'actor_b_type': 'Transhumant Buffalo Pastoralists',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Supply of high-fat fresh milk and butter during monsoon on high ridges (dhars)',
            'exchange_medium': 'Cash purchase or cereal grain barter',
            'transaction_category': 'Seasonal Pastoral Market Barter / Cash',
            'source_title': 'Census of India 1961: Chitrari',
            'page_or_table_ref': 'p. 45',
            'passage_id': 'PAS_008',
            'historical_significance': 'Direct empirical proof of trans-religious trade between settled Hindus and mobile pastoral Muslims.'
        },
        {
            'relationship_id': 'REL_007',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Chitrari',
            'historical_period': '1961',
            'actor_a': 'Shakti Devi Temple & Cultivators',
            'actor_a_type': 'Temple Shrine & Village Assembly',
            'actor_b': 'Bensi Musicians',
            'actor_b_type': 'Hereditary Temple Pipers & Drummers',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Sacred horn/drum performance at daily morning/evening worship and seasonal fairs',
            'exchange_medium': 'Customary annual grain collections from households + temple endowment stipend',
            'transaction_category': 'Customary Jajmani Sacred Perquisite',
            'source_title': 'Census of India 1961: Chitrari',
            'page_or_table_ref': 'p. 32',
            'passage_id': 'PAS_009',
            'historical_significance': 'Institutionalised temple service caste operating within the sacred village economy.'
        },
        {
            'relationship_id': 'REL_008',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Maingal',
            'historical_period': '1961',
            'actor_a': 'Village Cultivators (Brahmin/Rajput/Gujjar)',
            'actor_a_type': 'Arable Farmers',
            'actor_b': 'Lohar Blacksmiths',
            'actor_b_type': 'Village Iron Artisans',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Fabrication and sharpening of iron ploughshares, sickles, axes, and hoes',
            'exchange_medium': 'Khalian (customary unhusked grain sheaves delivered from threshing floor)',
            'transaction_category': 'Customary Jajmani In-Kind Barter',
            'source_title': 'Census of India 1961: Maingal',
            'page_or_table_ref': 'p. 33, p. 38, p. 40',
            'passage_id': 'PAS_011',
            'historical_significance': 'Definitive evidence of non-monetary jajmani tool maintenance operating in Chamba.'
        },
        {
            'relationship_id': 'REL_009',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Maingal',
            'historical_period': '1961',
            'actor_a': 'Muslim Gujjar Herders',
            'actor_a_type': 'Forest Pastoral Dairy Producers (81.5% pop)',
            'actor_b': 'Urban Bazaar Traders (Chamba Town)',
            'actor_b_type': 'Commercial Merchants & Town Consumers',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Bulk sales of clarified butter (ghee) derived from 217 water buffaloes',
            'exchange_medium': 'Cash currency and credit advances against future deliveries',
            'transaction_category': 'Commercial Market Commodity Sale',
            'source_title': 'Census of India 1961: Maingal',
            'page_or_table_ref': 'p. 14, p. 33',
            'passage_id': 'PAS_012',
            'historical_significance': 'Integration of sub-Himalayan pastoral economy into regional cash markets.'
        },
        {
            'relationship_id': 'REL_010',
            'spatial_scope': 'Village (Micro)',
            'village_or_region': 'Maingal',
            'historical_period': '1961',
            'actor_a': 'Muslim Gujjar Herders',
            'actor_a_type': 'Forest Pastoral Dairymen',
            'actor_b': 'Hindu Brahmins',
            'actor_b_type': 'Nucleated Terraced Cultivators',
            'directionality': 'Multilateral Reciprocal',
            'resource_or_service_exchanged': 'Buffalo manure for terraced fields, loan of draft bullocks, water mill rights, joint path repair',
            'exchange_medium': 'Direct resource reciprocity and neighborly social accommodation',
            'transaction_category': 'Non-Monetary Reciprocal Symbiosis',
            'source_title': 'Census of India 1961: Maingal',
            'page_or_table_ref': 'pp. 12, 33',
            'passage_id': 'PAS_010, PAS_013',
            'historical_significance': 'Peaceful inter-religious coexistence anchored in non-competing ecological niches.'
        },
        {
            'relationship_id': 'REL_011',
            'spatial_scope': 'Regional (Macro)',
            'village_or_region': 'Trans-Dhaula Dhar (Kangra/Chamba)',
            'historical_period': '1881',
            'actor_a': 'Gaddi Agro-Pastoralists',
            'actor_a_type': 'Highland Transhumant Herders',
            'actor_b': 'Dual Territorial States (British & Chamba)',
            'actor_b_type': 'Imperial British & Princely State Authorities',
            'directionality': 'Bilateral Hegemonic',
            'resource_or_service_exchanged': 'Seasonal passage across Dhaula Dhar between Kangra winter wheat and Chamba summer grazing',
            'exchange_medium': 'Pasture grazing taxes (Rs. 15/100 sheep in summer) and British land revenue',
            'transaction_category': 'State Fiscal Dues & Territorial Permits',
            'source_title': 'Report on the Census of the Panjáb 1881',
            'page_or_table_ref': 'para 498',
            'passage_id': 'PAS_015',
            'historical_significance': 'Longue durée baseline proving pastoral mobility spanning distinct political jurisdictions.'
        },
        {
            'relationship_id': 'REL_012',
            'spatial_scope': 'Regional (Macro)',
            'village_or_region': 'Chamba State Regional',
            'historical_period': '1961',
            'actor_a': 'Peasant & Pastoral Families',
            'actor_a_type': 'Rural Households (Brahmaur/Chitrari)',
            'actor_b': 'Rehara Silversmiths',
            'actor_b_type': 'Specialized Itinerant/Resident Metal Craftsmen',
            'directionality': 'Bilateral',
            'resource_or_service_exchanged': 'Casting and chasing of heavy silver ornaments (chiri, ralu, kanbali, dhodku)',
            'exchange_medium': 'Cash fee per tola silver crafted + retention of silver scrap + festive meals',
            'transaction_category': 'Artisanal Piece-Rate & Scrap Retention',
            'source_title': 'Census of India 1961: Brahmaur',
            'page_or_table_ref': 'p. 24, pp. 27-33',
            'passage_id': 'PAS_003',
            'historical_significance': 'Conversion of pastoral wool/animal surplus into portable silver dowry (stridhana).'
        }
    ]

    df_net = pd.DataFrame(net_edges)
    out_file = OUTPUTS_DIR / "exchange_network_edges.csv"
    df_net.to_csv(out_file, index=False)
    print(f"Generated {len(df_net)} records in {out_file}\n")

def generate_analysis_3_crosswalk():
    """Analysis 3: Longitudinal Classification Crosswalk (1881-1961)."""
    print("=" * 80)
    print("ANALYSIS 3: HISTORICAL CLASSIFICATION CROSSWALK (1881-1961)")
    print("=" * 80)

    crosswalk_data = [
        # Gaddi
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Early Colonial (1881)',
            'source_year': 1881,
            'archival_source_title': 'Census of the Panjáb 1881 (Denzil Ibbetson)',
            'original_term_printed': 'Gadi / Gaddi',
            'page_or_table_ref': 'p. 248, para 498',
            'administrative_scale': 'Punjab Province & Chamba State',
            'original_classification_logic': 'Generic geographic-occupational label; includes Brahmins, Khatris, Rajputs; explicitly excludes impure service castes (Badi, Sipi, Hali)',
            'normalized_modern_category': 'Transhumant Agro-Pastoralist',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Early colonial paternal definition excludes attached service castes who share identical dialect, dress, and mountain habitat.'
        },
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Late Colonial Ethnography (1911–1919)',
            'source_year': 1911,
            'archival_source_title': 'Glossary of the Tribes and Castes of Punjab & NWFP, Vol. II (H. A. Rose)',
            'original_term_printed': 'Gaddi',
            'page_or_table_ref': 'Vol. II, pp. 256-258',
            'administrative_scale': 'Punjab Hill States Agency',
            'original_classification_logic': 'Fourfold racialized caste taxonomy; upper Gaddis claimed as immigrant Khatris fleeing Mughal persecution; lower castes ranked as menials',
            'normalized_modern_category': 'Transhumant Agro-Pastoralist',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Constructs a migration myth of Mughal flight to explain caste stratification, obscuring internal social differentiation.'
        },
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Interwar Depression (1931)',
            'source_year': 1931,
            'archival_source_title': 'Census of India 1931, Vol. XVII (Khan Ahmad Hasan Khan)',
            'original_term_printed': 'Gaddi (Tribe/Caste)',
            'page_or_table_ref': 'Vol. XVII, Pt. I, p. 285',
            'administrative_scale': 'Chamba State & Punjab States Agency',
            'original_classification_logic': 'Recorded as distinct Hill Tribe/Caste alongside shift towards principal earners and working dependents in pastoral industry',
            'normalized_modern_category': 'Transhumant Agro-Pastoralist',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Depression-era enumeration captures economic stress; winter census timing (Feb) caught herders in Kangra lowlands.'
        },
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Post-Independence (1961)',
            'source_year': 1961,
            'archival_source_title': 'Census of India 1961: Brahmaur Village Survey',
            'original_term_printed': 'Gaddi (Scheduled Tribe)',
            'page_or_table_ref': 'Monograph No. 5, pp. 18, 43-44',
            'administrative_scale': 'Village Micro-Census (Brahmaur)',
            'original_classification_logic': 'Constitutional Scheduled Tribe category (since 1956); detailed household enumeration of flock-owners (malundis) and wage-herders (pohals)',
            'normalized_modern_category': 'Transhumant Agro-Pastoralist',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'State statutory Scheduled Tribe classification unifies upper and lower castes under single legal umbrella despite persistence of internal hierarchy.'
        },

        # Gujjar
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Early Colonial (1881)',
            'source_year': 1881,
            'archival_source_title': 'Census of the Panjáb 1881 (Denzil Ibbetson)',
            'original_term_printed': 'Gujar / Gujjar',
            'page_or_table_ref': 'para 481, p. 238',
            'administrative_scale': 'Punjab Province & Chamba State',
            'original_classification_logic': 'Pastoralists and cattle graziers; contrasted with Jat cultivators; noted for mountain transhumance',
            'normalized_modern_category': 'Pastoral Buffalo Dairyman',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Broad provincial categorization bundles sedentary plains Gujars with nomadic forest buffalo Gujjars.'
        },
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Late Colonial Ethnography (1911–1919)',
            'source_year': 1911,
            'archival_source_title': 'Glossary of the Tribes and Castes of Punjab & NWFP, Vol. II (H. A. Rose)',
            'original_term_printed': 'Gujar',
            'page_or_table_ref': 'Vol. II, p. 308',
            'administrative_scale': 'Punjab Hill States Agency',
            'original_classification_logic': 'Pejorative colonial characterization: described through hostile proverbs as lazy cultivators and habitual cattle thieves',
            'normalized_modern_category': 'Pastoral Buffalo Dairyman',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Heavy colonial administrative prejudice against mobile cattle-keeping populations reflecting settled agricultural revenue bias.'
        },
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Interwar Depression (1931)',
            'source_year': 1931,
            'archival_source_title': 'Census of India 1931, Vol. XVII (Khan Ahmad Hasan Khan)',
            'original_term_printed': 'Gujjar (Muslim/Hindu)',
            'page_or_table_ref': 'Vol. XVII, Pt. I, p. 290',
            'administrative_scale': 'Chamba State & Agency',
            'original_classification_logic': 'Enumerated by religion (predominantly Muslim in Chamba hills); classified under livestock production and dairying',
            'normalized_modern_category': 'Pastoral Buffalo Dairyman',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Identifies Muslim religious identity but obscures local interactions with Hindu village economies.'
        },
        {
            'category_family': 'Pastoralist Communities',
            'historical_era': 'Post-Independence (1961)',
            'source_year': 1961,
            'archival_source_title': 'Census of India 1961: Maingal Village Survey',
            'original_term_printed': 'Muslim Gujjar (Scheduled Tribe)',
            'page_or_table_ref': 'Monograph No. 27, pp. 12, 14, 33',
            'administrative_scale': 'Village Micro-Census (Maingal)',
            'original_classification_logic': 'Scheduled Tribe (1956); micro-level enumeration of 25 households owning 217 buffaloes, dwelling-byre kothas, and commercial ghee marketing',
            'normalized_modern_category': 'Pastoral Buffalo Dairyman',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Accurate micro-census of settled forest hamlets; ethnographic commentary assumes recent Hindu origin without independent archival proof.'
        },

        # Sipi
        {
            'category_family': 'Artisan and Service Castes',
            'historical_era': 'Early Colonial (1881)',
            'source_year': 1881,
            'archival_source_title': 'Census of the Panjáb 1881 (Denzil Ibbetson)',
            'original_term_printed': 'Sipi',
            'page_or_table_ref': 'para 498, p. 248',
            'administrative_scale': 'Punjab Province & Chamba State',
            'original_classification_logic': 'Ranked as an impure menial service caste of the hills excluded from the proper Gaddi appellation',
            'normalized_modern_category': 'Weaver, Shearer & Ritual Musician',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Dismissed as generic menials without recording their indispensable technological role in mountain wool manufacture.'
        },
        {
            'category_family': 'Artisan and Service Castes',
            'historical_era': 'Late Colonial Ethnography (1911–1919)',
            'source_year': 1914,
            'archival_source_title': 'Glossary of the Tribes and Castes of Punjab & NWFP, Vol. III (H. A. Rose)',
            'original_term_printed': 'Sipi / Sippi',
            'page_or_table_ref': 'Vol. III, p. 407',
            'administrative_scale': 'Punjab Hill States Agency',
            'original_classification_logic': 'Identified specifically as professional wool-shearers and weavers of Gaddi blankets; ranked below upper hill castes',
            'normalized_modern_category': 'Weaver, Shearer & Ritual Musician',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Aknowledges textile skills but treats them as hereditary servile characteristics rather than skilled artisanal craft.'
        },
        {
            'category_family': 'Artisan and Service Castes',
            'historical_era': 'Interwar Depression (1931)',
            'source_year': 1931,
            'archival_source_title': 'Census of India 1931, Vol. XVII (Khan Ahmad Hasan Khan)',
            'original_term_printed': 'Sipi (Depressed Class)',
            'page_or_table_ref': 'Vol. XVII, Pt. I, p. 331',
            'administrative_scale': 'Punjab States Agency',
            'original_classification_logic': 'Enumerated within scheduled depressed classes / exterior castes; occupational breakdown subsumed under general weaving labour',
            'normalized_modern_category': 'Weaver, Shearer & Ritual Musician',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Aggregation into provincial depressed classes obscures unique tripartite role in Himalayan village economy.'
        },
        {
            'category_family': 'Artisan and Service Castes',
            'historical_era': 'Post-Independence (1961)',
            'source_year': 1961,
            'archival_source_title': 'Census of India 1961: Brahmaur Village Survey',
            'original_term_printed': 'Sipi (Scheduled Caste)',
            'page_or_table_ref': 'Monograph No. 5, pp. 18, 24, 38, 44, 62',
            'administrative_scale': 'Village Micro-Census (Brahmaur)',
            'original_classification_logic': 'Scheduled Caste; 15 households (119 pop); tripartite economic monopoly: hired shepherds (pohals), master tweed weavers, and Nawala drummers',
            'normalized_modern_category': 'Weaver, Shearer & Ritual Musician',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Provides richest empirical evidence of contract wages and customary ritual meat perquisites, though intra-household disputes are unrecorded.'
        },

        # Hali / Arya-Hali
        {
            'category_family': 'Agricultural Labour and Tenancy',
            'historical_era': 'Early Colonial (1881)',
            'source_year': 1881,
            'archival_source_title': 'Census of the Panjáb 1881 (Denzil Ibbetson)',
            'original_term_printed': 'Hali',
            'page_or_table_ref': 'para 498, p. 248; Table IX',
            'administrative_scale': 'Punjab Province & Chamba State',
            'original_classification_logic': 'Occupational caste of ploughmen (derived from hal, plough); classified as impure service group',
            'normalized_modern_category': 'Attached Ploughman & Field Labourer',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Conflates functional occupation of ploughing with rigid hereditary caste rank.'
        },
        {
            'category_family': 'Agricultural Labour and Tenancy',
            'historical_era': 'Late Colonial Ethnography (1911–1919)',
            'source_year': 1911,
            'archival_source_title': 'Glossary of the Tribes and Castes of Punjab & NWFP, Vol. II (H. A. Rose)',
            'original_term_printed': 'Hali',
            'page_or_table_ref': 'Vol. II, p. 324',
            'administrative_scale': 'Punjab Hill States Agency',
            'original_classification_logic': 'Field labourers and hereditary attached serfs performing ploughing for landowners under ritual taboos',
            'normalized_modern_category': 'Attached Ploughman & Field Labourer',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Accurately documents high-caste ploughing taboos but portrays attached tenancy as permanent and unchangeable.'
        },
        {
            'category_family': 'Agricultural Labour and Tenancy',
            'historical_era': 'Interwar Depression (1931)',
            'source_year': 1931,
            'archival_source_title': 'Census of India 1931, Vol. XVII (Khan Ahmad Hasan Khan)',
            'original_term_printed': 'Hali / Arya (Depressed Class)',
            'page_or_table_ref': 'Vol. XVII, Pt. I, p. 312',
            'administrative_scale': 'Chamba State & Agency',
            'original_classification_logic': 'Early traces of Arya Samaj socio-religious reform; Halis returning as Aryas to escape stigmatized untouchable status',
            'normalized_modern_category': 'Attached Ploughman & Field Labourer',
            'comparability_level': 'Partial',
            'historiographical_caveat': 'Census officials noted widespread status contestation as lower castes claimed Vedic Arya status to escape menial listings.'
        },
        {
            'category_family': 'Agricultural Labour and Tenancy',
            'historical_era': 'Post-Independence (1961)',
            'source_year': 1961,
            'archival_source_title': 'Census of India 1961: Chitrari Village Survey',
            'original_term_printed': 'Aryas—Halis (Scheduled Caste)',
            'page_or_table_ref': 'Monograph No. 10, pp. 11-12',
            'administrative_scale': 'Village Micro-Census (Chitrari)',
            'original_classification_logic': 'Formally recorded with hyphenated title Aryas—Halis (2 hh / 6 pop); attached ploughmen on Brahmin temple lands utilizing Arya Samaj reform to negotiate status',
            'normalized_modern_category': 'Attached Ploughman & Field Labourer',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Direct proof of ideological mobilization against untouchability, though economic dependence on Brahmin land remained largely unbroken.'
        },

        # Lohar
        {
            'category_family': 'Artisan and Service Castes',
            'historical_era': 'Early Colonial (1881)',
            'source_year': 1881,
            'archival_source_title': 'Census of the Panjáb 1881 (Denzil Ibbetson)',
            'original_term_printed': 'Lohar',
            'page_or_table_ref': 'para 624, p. 310',
            'administrative_scale': 'Punjab Province',
            'original_classification_logic': 'Blacksmith artisan caste; village menials manufacturing iron agricultural implements in exchange for customary village dues',
            'normalized_modern_category': 'Blacksmith Artisan',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'High cross-era comparability: iron tool manufacturing is consistently recognized across all censuses.'
        },
        {
            'category_family': 'Artisan and Service Castes',
            'historical_era': 'Post-Independence (1961)',
            'source_year': 1961,
            'archival_source_title': 'Census of India 1961: Maingal Village Survey',
            'original_term_printed': 'Lohar',
            'page_or_table_ref': 'Monograph No. 27, pp. 12, 33, 38, 40',
            'administrative_scale': 'Village Micro-Census (Maingal)',
            'original_classification_logic': '2 households (8 pop); maintain agricultural iron tools under customary non-monetary jajmani barter (khalian grain sheaves from threshing floor)',
            'normalized_modern_category': 'Blacksmith Artisan',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Exemplifies high institutional continuity in customary artisan remuneration across 80 years.'
        },

        # Dependency Framework
        {
            'category_family': 'Economic Classification Systems',
            'historical_era': 'Early Colonial (1881)',
            'source_year': 1881,
            'archival_source_title': 'Census of the Panjáb 1881 (Denzil Ibbetson)',
            'original_term_printed': 'Occupation by Hereditary Caste',
            'page_or_table_ref': 'Operations Volume, Pt. III',
            'administrative_scale': 'Provincial',
            'original_classification_logic': 'Assumes hereditary caste determines individual occupation; lists traditional caste callings regardless of actual livelihood',
            'normalized_modern_category': 'Hereditary Caste Calling',
            'comparability_level': 'Non-Comparable',
            'historiographical_caveat': 'Severely conflates ritual status with actual productive activity.'
        },
        {
            'category_family': 'Economic Classification Systems',
            'historical_era': 'Interwar Depression (1931)',
            'source_year': 1931,
            'archival_source_title': 'Census of India 1931, Vol. XVII (Khan Ahmad Hasan Khan)',
            'original_term_printed': 'Principal Earners / Working Dependents / Non-Working Dependents',
            'page_or_table_ref': 'Vol. XVII, Pt. I, pp. 210-215',
            'administrative_scale': 'Provincial & State Level',
            'original_classification_logic': 'Replaces hereditary caste with tripartite economic dependency model under Great Depression economic dislocation',
            'normalized_modern_category': 'Economic Earner & Dependency Class',
            'comparability_level': 'Non-Comparable',
            'historiographical_caveat': 'Represents an administrative shift in classification logic, not proof that caste division of labour had dissolved.'
        },
        {
            'category_family': 'Economic Classification Systems',
            'historical_era': 'Post-Independence (1961)',
            'source_year': 1961,
            'archival_source_title': 'Census of India 1961: Village Surveys (Brahmaur, Chitrari, Maingal)',
            'original_term_printed': 'Workers and Non-Workers by Household and Activity',
            'page_or_table_ref': 'Village Monographs (Occupational Tables)',
            'administrative_scale': 'Village Micro-Level',
            'original_classification_logic': 'Direct enumeration of actual primary and subsidiary household productive labour alongside landholding and livestock counts',
            'normalized_modern_category': 'Household Productive Labour',
            'comparability_level': 'Direct',
            'historiographical_caveat': 'Captures actual empirical work, though gendered domestic labour remains partially under-enumerated.'
        }
    ]

    df_cross = pd.DataFrame(crosswalk_data)
    out_file = OUTPUTS_DIR / "classification_crosswalk_1881_1961.csv"
    df_cross.to_csv(out_file, index=False)
    print(f"Generated {len(df_cross)} records in {out_file}\n")

def generate_analysis_4_thematic_coding():
    """Analysis 4: Qualitative Thematic Multi-Label Coding of 20 Passages."""
    print("=" * 80)
    print("ANALYSIS 4: QUALITATIVE THEMATIC MULTI-LABEL CODING (20 PASSAGES)")
    print("=" * 80)

    qual_file = DATA_DIR / "qualitative_passages.csv"
    if not qual_file.exists():
        print("Error: Missing qualitative_passages.csv in data/")
        sys.exit(1)

    qual = pd.read_csv(qual_file)

    coding_dict = {
        'PAS_001': {
            'codes': ['LAB', 'DEP', 'EXC', 'MOB'],
            'primary_actors': 'Malundis (Flock owners) & Pohals (Hired shepherds)',
            'exchange_medium': 'Cash (Rs. 2/mo), meals, wool, 2-4 sheep/100 dividend',
            'coding_rationale': 'Explicit contractual wage shepherding within transhumant pastoralism; dependency of small flock owners on hired labour.',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_002': {
            'codes': ['ECO', 'DEP'],
            'primary_actors': 'Brahmaur Villagers & Water Buffaloes',
            'exchange_medium': 'Lactation yield (drop from 9 to 4 seers)',
            'coding_rationale': 'Definitive ecological constraint: alpine frost induces physiological lactation collapse, enforcing sheep/goat specialization.',
            'essay_application': 'Section 4 (Altitudinal Gradients and Ecological Niches)'
        },
        'PAS_003': {
            'codes': ['LAB', 'EXC', 'RIT'],
            'primary_actors': 'Reharas (Silversmiths) & Peasant Families',
            'exchange_medium': 'Cash per tola, scrap silver retention, wedding feast gifts',
            'coding_rationale': 'Artisanal metal craftsmanship converting pastoral livestock profits into portable silver dowry ornaments.',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_004': {
            'codes': ['LAB', 'DEP', 'EXC'],
            'primary_actors': 'Sipis (Weavers/Tailors) & Gaddi Flock Owners',
            'exchange_medium': 'Raw wool shares, meals, grain perquisites',
            'coding_rationale': 'Lower-caste technical monopoly over shearing (katar), weaving tweed (pattu), and tailoring the traditional Gaddi dress (chola/dora).',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_005': {
            'codes': ['RIT', 'DEP', 'EXC', 'POW'],
            'primary_actors': 'Brahmans, Sipis (Dholak Drummers), Chelas (Mediums)',
            'exchange_medium': 'Ghardi (sacrificial sheep neck), sanctified feast food',
            'coding_rationale': 'Ritual redistribution during Nawala feast crossing purity barriers; Sipi sacred entitlement to sacrificed animal portion.',
            'essay_application': 'Section 5, Section 6 (Ritual Economy & Material Culture)'
        },
        'PAS_006': {
            'codes': ['DEP', 'POW'],
            'primary_actors': 'Landed Brahmins & Shakti Devi Temple Shrine',
            'exchange_medium': 'Royal land endowments (shasan grants) from Raja Meru-Varman',
            'coding_rationale': 'Historical institutional origin of Brahmin landed monopoly (77% pop) in Chitrari basin.',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_007': {
            'codes': ['LAB', 'DEP', 'EXC', 'POW'],
            'primary_actors': 'Brahmin Landowners & Halis (Aryas)',
            'exchange_medium': 'Tied crop-shares, maintenance grain, ploughing labour',
            'coding_rationale': 'High-caste plough taboos enforcing reliance on attached Halis; contestation of untouchability via Arya Samaj mobility.',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_008': {
            'codes': ['ECO', 'MOB', 'EXC', 'REL'],
            'primary_actors': 'Chitrari Hindu Villagers & Visiting Muslim Gujjars',
            'exchange_medium': 'Cash purchase or cereal barter for high-fat milk/butter on high dhars',
            'coding_rationale': 'Inter-community trade during monsoon; local cattle produce negligible milk, forcing dependence on mobile pastoralists.',
            'essay_application': 'Section 4, Section 6 (Markets, Mobility & Religious Relations)'
        },
        'PAS_009': {
            'codes': ['LAB', 'RIT', 'EXC'],
            'primary_actors': 'Bensi Temple Pipers & Village Cultivators',
            'exchange_medium': 'Customary annual grain collections & temple endowment stipends',
            'coding_rationale': 'Institutionalized hereditary service caste attached to village temple cult.',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_010': {
            'codes': ['ECO', 'REL'],
            'primary_actors': 'Muslim Gujjars & Hindu Brahmins',
            'exchange_medium': 'Dispersed kothas in forest hamlets vs nucleated village core',
            'coding_rationale': 'Spatial settlement segregation reflecting distinct production strategies: forest cattle-keeping vs nucleated terraced arable.',
            'essay_application': 'Section 4, Section 6 (Ecological Niches & Religious Co-existence)'
        },
        'PAS_011': {
            'codes': ['LAB', 'DEP', 'EXC'],
            'primary_actors': 'Lohar Blacksmiths & Arable Cultivators',
            'exchange_medium': 'Khalian (customary unhusked grain sheaves from threshing floor)',
            'coding_rationale': 'Definitive proof of non-monetary jajmani tool maintenance operating in Chamba.',
            'essay_application': 'Section 5 (Labour and Hierarchy)'
        },
        'PAS_012': {
            'codes': ['EXC', 'MOB', 'ECO'],
            'primary_actors': 'Muslim Gujjars & Chamba Town Bazaar Merchants',
            'exchange_medium': 'Cash currency and credit advances for clarified butter (ghee)',
            'coding_rationale': 'Commoditization of pastoral surplus linking remote forest hamlets to urban market networks.',
            'essay_application': 'Section 6 (Markets and Mobility)'
        },
        'PAS_013': {
            'codes': ['REL', 'ECO'],
            'primary_actors': 'Muslim Gujjars & Hindu Neighbors (Brahmins/Rajputs)',
            'exchange_medium': 'Shared water points, bullock loans, dung manure exchange',
            'coding_rationale': 'Peaceful multi-religious co-existence anchored in complementary non-competing ecological niches.',
            'essay_application': 'Section 6 (Religious Relations and Ecological Complementarity)'
        },
        'PAS_014': {
            'codes': ['POW', 'LAB'],
            'primary_actors': 'Colonial Census (Ibbetson) & Hill Castes',
            'exchange_medium': 'Administrative categorization',
            'coding_rationale': 'Early colonial racial boundary-making separating Gaddi pastoral core from menial service castes (Sipis, Halis).',
            'essay_application': 'Section 3, Section 7 (Colonial Classification)'
        },
        'PAS_015': {
            'codes': ['ECO', 'MOB', 'POW'],
            'primary_actors': 'Gaddi Pastoralists & Dual Sovereign Authorities (British/Chamba)',
            'exchange_medium': 'Pasture grazing dues (tirni) & British land revenue',
            'coding_rationale': 'Trans-Dhaula Dhar bi-regional landholding navigating overlapping political borders.',
            'essay_application': 'Section 4, Section 7 (Mobility and Environmental History)'
        },
        'PAS_016': {
            'codes': ['ECO', 'MOB', 'GEN'],
            'primary_actors': 'Pahari Proverb / Gaddi Pastoralists',
            'exchange_medium': 'Vernacular folklore',
            'coding_rationale': 'Proverb capturing environmental precariousness and migratory hardship of high-altitude pastoralism.',
            'essay_application': 'Section 6, Section 7 (Material Culture & Oral Evidence)'
        },
        'PAS_017': {
            'codes': ['POW'],
            'primary_actors': 'H. A. Rose & Colonial Ethnographic Taxonomy',
            'exchange_medium': 'Colonial glossary classification',
            'coding_rationale': 'Codification of fourfold Gaddi caste taxonomy and migration myths of Mughal flight.',
            'essay_application': 'Section 7 (Colonial Categories)'
        },
        'PAS_018': {
            'codes': ['LAB', 'POW'],
            'primary_actors': 'H. A. Rose & Sipi Service Caste',
            'exchange_medium': 'Ethnographic ranking',
            'coding_rationale': 'Documentation of Sipi weaving monopoly combined with subordinate caste positioning.',
            'essay_application': 'Section 5, Section 7 (Labour and Colonial Knowledge)'
        },
        'PAS_019': {
            'codes': ['POW', 'REL'],
            'primary_actors': 'H. A. Rose & Colonial Administration',
            'exchange_medium': 'Pejorative proverbs & administrative stereotypes',
            'coding_rationale': 'Colonial criminalization of pastoralists reflecting settled revenue bias against mobile graziers.',
            'essay_application': 'Section 7 (Colonial Categories and Stereotypes)'
        },
        'PAS_020': {
            'codes': ['ECO', 'DEP', 'POW'],
            'primary_actors': 'Khan Ahmad Hasan Khan (1931 Census) & Chamba Population',
            'exchange_medium': 'Statistical dependency enumeration',
            'coding_rationale': 'Transition from caste to economic dependency classes (Earners/Dependents) under Great Depression.',
            'essay_application': 'Section 3, Section 7 (Historical Classification Crosswalk)'
        }
    }

    rows = []
    for _, r in qual.iterrows():
        pid = r['passage_id']
        info = coding_dict.get(pid, {})
        codes = info.get('codes', [])
        rows.append({
            'passage_id': pid,
            'village_or_region': r['village'],
            'source_id': r['source_id'],
            'source_year': r['source_year'],
            'page_section': r['page_section'],
            'assigned_codes': '; '.join(codes),
            'code_count': len(codes),
            'primary_actors': info.get('primary_actors', ''),
            'exchange_medium': info.get('exchange_medium', ''),
            'coding_rationale': info.get('coding_rationale', ''),
            'essay_application': info.get('essay_application', ''),
            'original_excerpt': r['original_excerpt']
        })

    df_coded = pd.DataFrame(rows)
    out_file = OUTPUTS_DIR / "thematic_coding_passages.csv"
    df_coded.to_csv(out_file, index=False)
    print(f"Generated {len(df_coded)} records in {out_file}\n")

    # Display Distribution Matrix
    all_codes = ['LAB', 'DEP', 'EXC', 'ECO', 'MOB', 'REL', 'GEN', 'RIT', 'POW']
    village_theme_counts = {v: {c: 0 for c in all_codes} for v in ['Brahmaur', 'Chitrari', 'Maingal', 'regional_state']}

    for _, r in df_coded.iterrows():
        v = r['village_or_region']
        codes = [c.strip() for c in r['assigned_codes'].split(';') if c.strip()]
        for c in codes:
            if v in village_theme_counts and c in village_theme_counts[v]:
                village_theme_counts[v][c] += 1

    df_dist = pd.DataFrame(village_theme_counts).T
    print("THEME-BY-VILLAGE DISTRIBUTION MATRIX:")
    print(df_dist.to_string())
    print("\nPart 2 Computational Analyses complete.\n")

if __name__ == "__main__":
    generate_analysis_1_comparative_economy()
    generate_analysis_2_network_edges()
    generate_analysis_3_crosswalk()
    generate_analysis_4_thematic_coding()

