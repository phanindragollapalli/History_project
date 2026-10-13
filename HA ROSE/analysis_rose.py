#!/usr/bin/env python3
"""
Computational Analysis: H. A. Rose's Ethnographic Glossary (1911-1919)

Tasks:
1. Search H. A. Rose volumes (13438.txt, 13664.txt, VOL1.md) for Gaddi, Gujar, Sipi, Hali, Lohar, Rehara.
2. Extract Keyword-in-Context (KWIC) ethnographic descriptions.
3. Compute colonial discourse metrics (pejorative/racial/criminal terms associated with pastoral groups).
4. Save structured outputs to 'output_rose_keyword_summary.csv', 'output_rose_concordance.csv', and 'output_rose_bias_analysis.csv'.
"""

import os
import re
from pathlib import Path
import pandas as pd

HERE = Path(__file__).resolve().parent

TARGET_COMMUNITIES = {
    'gaddi': r'\b(gaddi|gaddis|gadi|gadis)\b',
    'gujjar': r'\b(gujjar|gujjars|gujar|gujars)\b',
    'sipi': r'\b(sipi|sipis)\b',
    'hali': r'\b(hali|halis)\b',
    'lohar': r'\b(lohar|lohars)\b',
    'rehara': r'\b(rehara|reharas|rihara|riharas)\b',
    'chamba': r'\bchamba\b',
    'barmaur': r'\b(barmaur|brahmaur|barmor)\b'
}

COLONIAL_BIAS_TERMS = {
    'menial': r'\bmenial\b',
    'dependant': r'\b(dependant|dependent)\b',
    'thief_thieving': r'\b(thief|thieves|thieving|theft|cattle-lifter|cattle-thief)\b',
    'lazy_indolent': r'\b(lazy|indolent|wretched)\b',
    'impure': r'\b(impure|outcaste|degraded)\b',
    'caste_pride': r'\b(sacred thread|janeu|twice-born)\b'
}

def analyze_rose_corpus():
    print("Analyzing H. A. Rose Ethnographic Glossary (1911–1919)...")
    # Identify available text and markdown source files for Rose glossary volumes
    txt_files = [f for f in HERE.glob("*.txt") if not f.name.startswith("key")]
    md_files = list(HERE.glob("*.md"))
    all_files = sorted(txt_files + [f for f in md_files if f.name != "README.md"])

    summary_records = []
    concordance_records = []
    bias_records = []

    for fpath in all_files:
        doc_name = fpath.name
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
        
        full_text = " ".join(lines)
        total_words = len(re.findall(r'\b[A-Za-z]+\b', full_text))
        print(f"Loaded {doc_name}: {len(lines):,} lines, {total_words:,} words")

        doc_counts = {'document': doc_name, 'total_words': total_words}
        for term_label, pattern in TARGET_COMMUNITIES.items():
            matches = list(re.finditer(pattern, full_text, flags=re.IGNORECASE))
            doc_counts[term_label] = len(matches)
        summary_records.append(doc_counts)

        # KWIC concordance extraction
        for i, line in enumerate(lines):
            # Check community matches
            for term_label, pattern in TARGET_COMMUNITIES.items():
                if re.search(pattern, line, flags=re.IGNORECASE):
                    start_idx = max(0, i - 2)
                    end_idx = min(len(lines), i + 3)
                    context_snippet = " ".join([l.strip() for l in lines[start_idx:end_idx] if l.strip()])
                    context_snippet = re.sub(r'\s+', ' ', context_snippet)[:300]
                    
                    concordance_records.append({
                        'document': doc_name,
                        'line_number': i + 1,
                        'community': term_label,
                        'matched_text': line.strip()[:100],
                        'kwic_context': context_snippet
                    })

            # Check bias terms co-occurring with pastoral communities
            for bias_label, bias_pattern in COLONIAL_BIAS_TERMS.items():
                if re.search(bias_pattern, line, flags=re.IGNORECASE):
                    start_idx = max(0, i - 2)
                    end_idx = min(len(lines), i + 3)
                    context_snippet = " ".join([l.strip() for l in lines[start_idx:end_idx] if l.strip()])
                    context_snippet = re.sub(r'\s+', ' ', context_snippet)[:300]
                    
                    # Detect if Gaddi or Gujar is in the context
                    co_gaddi = bool(re.search(TARGET_COMMUNITIES['gaddi'], context_snippet, re.IGNORECASE))
                    co_gujar = bool(re.search(TARGET_COMMUNITIES['gujjar'], context_snippet, re.IGNORECASE))
                    
                    if co_gaddi or co_gujar:
                        bias_records.append({
                            'document': doc_name,
                            'line_number': i + 1,
                            'bias_category': bias_label,
                            'associated_group': 'Gaddi' if co_gaddi else 'Gujjar',
                            'context': context_snippet
                        })

    df_summary = pd.DataFrame(summary_records)
    summary_out = HERE / "output_rose_keyword_summary.csv"
    df_summary.to_csv(summary_out, index=False, encoding='utf-8-sig')
    print(f"Saved keyword summary to {summary_out}")

    df_concordance = pd.DataFrame(concordance_records)
    df_concordance = df_concordance.drop_duplicates(subset=['document', 'line_number', 'community'])
    concordance_out = HERE / "output_rose_concordance.csv"
    df_concordance.to_csv(concordance_out, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df_concordance):,} ethnographic concordance records to {concordance_out}")

    df_bias = pd.DataFrame(bias_records)
    bias_out = HERE / "output_rose_bias_analysis.csv"
    df_bias.to_csv(bias_out, index=False, encoding='utf-8-sig')
    print(f"Saved {len(df_bias):,} colonial bias analysis records to {bias_out}")

    # Extract timeline-specific ethnographic terms audit
    rose_terms = [
        {
            "term_id": "ETH_01",
            "caste_term": "Gaddi",
            "volume_page_ref": "Vol II, pp. 256-270",
            "colonial_ethnographic_definition": "Four-tier racial taxonomy: (1) Brahmans, (2) Khatris/Rajputs wearing sacred thread, (3) Thakurs/Rathis, (4) Menials (Sipi, Hali, Lohar, Rehara)",
            "colonial_bias_or_stereotype": "Posits that true Gaddis are high-caste Hindu refugees fleeing Mughal persecution, treating lower service castes as unacknowledged menials.",
            "micro_survey_1961_reality": "Refuted by 1961 micro-data: Gaddi operates as a multi-caste regional federation bound by ritual co-participation (Nawala) and reciprocal labour.",
            "bias_severity": "High",
            "historical_significance": "Essentialises fluid mountain transhumance into rigid racial origin myths."
        },
        {
            "term_id": "ETH_02",
            "caste_term": "Gujar",
            "volume_page_ref": "Vol II, pp. 306-318",
            "colonial_ethnographic_definition": "Quotes pejorative plains proverbs: 'When all other castes are dead make friends with a Gujar... lazy to a degree, and a wretched cultivator... fondness for cattle extends to other people's'",
            "colonial_bias_or_stereotype": "Codes nomadic buffalo pasturing as indolence, economic failure, and chronic cattle theft.",
            "micro_survey_1961_reality": "Disproven by 1961 Maingal survey: Gujjars are industrious commercial dairymen constructing complex kothas, protecting maize crops via machans, and supplying urban ghee.",
            "bias_severity": "Extreme",
            "historical_significance": "Reflects colonial sedentarist hostility toward mobile pastoralists."
        },
        {
            "term_id": "ETH_03",
            "caste_term": "Sipi",
            "volume_page_ref": "Vol III, p. 407",
            "colonial_ethnographic_definition": "Defines Sipi as 'the weaver of the Gaddi tribes; found in the Barmaur wizarat... virtually the same as the Hali. A low hill-caste who are professional sheep-shearers'",
            "colonial_bias_or_stereotype": "Reduces Sipi to a generic degraded menial, conflating them indiscriminately with Halis.",
            "micro_survey_1961_reality": "Corrected by 1961 Brahmaur survey: Sipis hold a unique tripartite monopoly (wage shepherds, wool weavers/tailors, and sacred Nawala drummers).",
            "bias_severity": "Moderate",
            "historical_significance": "Conflates distinct occupational specializations under generic menial labels."
        },
        {
            "term_id": "ETH_04",
            "caste_term": "Hali",
            "volume_page_ref": "Vol II, p. 324",
            "colonial_ethnographic_definition": "Defines Hali as hereditary low-caste ploughmen bound to landholders, derived from 'hal' (plough).",
            "colonial_bias_or_stereotype": "Treats plough servitude as immutable caste destiny without political agency.",
            "micro_survey_1961_reality": "Qualified by 1961 Chitrari survey: Documents conscious social mobilization under the Arya Samaj, adopting the reformist title Aryas-Halis.",
            "bias_severity": "Moderate",
            "historical_significance": "Ignores socio-religious agency and modern anti-caste mobilization."
        },
        {
            "term_id": "ETH_05",
            "caste_term": "Rehara",
            "volume_page_ref": "Vol III, p. 306",
            "colonial_ethnographic_definition": "Classified as menial metalworkers and scavengers in hill states.",
            "colonial_bias_or_stereotype": "Obscures their artistic and economic function as silversmiths.",
            "micro_survey_1961_reality": "Corrected by 1961 Brahmaur survey: Reharas are skilled silversmiths converting pastoral livestock profits into portable stridhana jewelry (chiri, ralu).",
            "bias_severity": "Moderate",
            "historical_significance": "Degrades sophisticated metallurgical craftsmanship into menial scavenging."
        }
    ]
    df_terms = pd.DataFrame(rose_terms)
    terms_out = HERE / "output_rose_terms.csv"
    df_terms.to_csv(terms_out, index=False, encoding='utf-8-sig')
    print(f"Saved Rose ethnographic terms audit to {terms_out}")

    # Extract timeline-specific qualitative passages
    rose_passages = [
        {
            "passage_id": "PAS_017",
            "source_id": "SRC_ROSE_GLOSS_V2",
            "source_year": 1911,
            "village": "regional_state",
            "geographic_level": "Punjab Region",
            "page_section": "p. 256, Gaddi Classification",
            "original_excerpt": "The Gaddis are divided into four classes: (i) Brahmans, (ii) Khatris and Rajputs who regularly wear the sacred thread, (iii) Thakurs and Rathis who usually do not wear it, and (iv) a menial or dependant class, comprising Kolis, Riharas, Lohars, Badhis, Sipi and Halis, to whom the title of Gaddi is incorrectly applied by outsiders as inhabitants of the Gaderan, though the true Gaddis do not acknowledge them as Gaddis at all.",
            "neutral_summary": "Four-tier hierarchical taxonomy of Gaddi society distinguishing thread-wearing upper strata from menial dependent artisan castes.",
            "theme_code": "hierarchy",
            "actor_1": "Upper Gaddis (Brahmans, Khatris, Rajputs)",
            "actor_2": "Dependent Castes (Kolis, Riharas, Lohars, Badhis, Sipis, Halis)",
            "relationship_type": "service",
            "evidence_level": "explicit",
            "term_notes": "Gaderan denotes the homeland of Gaddis; Janeu marks ritual status.",
            "verified": "checked",
            "coder_notes": "Foundational text for analyzing social stratification and occupational dependence."
        },
        {
            "passage_id": "PAS_018",
            "source_id": "SRC_ROSE_GLOSS_V3",
            "source_year": 1919,
            "village": "regional_state",
            "geographic_level": "Punjab Region",
            "page_section": "p. 407, Sipi Definition",
            "original_excerpt": "Sipi,—The weaver of the Gaddi tribes; found in the Barmaur wizarat of the Chamba State, and virtually the same as the Hali. A low hill-caste who are professional sheep-shearers.",
            "neutral_summary": "Identifies Sipi as professional wool-shearers and weavers specific to Brahmaur wizarat, equating their status with Halis.",
            "theme_code": "occupation",
            "actor_1": "Sipi",
            "actor_2": "Gaddi flock owners",
            "relationship_type": "service",
            "evidence_level": "explicit",
            "term_notes": "Equates Sipi with Hali; pinpoints Brahmaur wizarat as habitat.",
            "verified": "checked",
            "coder_notes": "Direct historical definition of occupational role in wool production."
        },
        {
            "passage_id": "PAS_019",
            "source_id": "SRC_ROSE_GLOSS_V2",
            "source_year": 1911,
            "village": "regional_state",
            "geographic_level": "Punjab Region",
            "page_section": "p. 308, Gujar Stereotypes",
            "original_excerpt": "When all other castes are dead make friends with a Gujar... But he is far inferior in both personal character and repute to the Jat. He is lazy to a degree, and a wretched cultivator... while his fondness for cattle extends to those of other people.",
            "neutral_summary": "Colonial ethnographic depiction recording pejorative stereotypes of Gujjars as poor cultivators prone to cattle lifting.",
            "theme_code": "hierarchy",
            "actor_1": "Colonial Ethnographer",
            "actor_2": "Gujjar Pastoralists",
            "relationship_type": "unclear",
            "evidence_level": "explicit",
            "term_notes": "Demonstrates British colonial bias against nomadic pastoralism versus settled agriculture.",
            "verified": "checked",
            "coder_notes": "Essential for deconstructing colonial bias in Rose."
        }
    ]
    df_pas = pd.DataFrame(rose_passages)
    pas_out = HERE / "output_rose_passages.csv"
    df_pas.to_csv(pas_out, index=False, encoding='utf-8-sig')
    print(f"Saved Rose timeline passages to {pas_out}")

if __name__ == '__main__':
    analyze_rose_corpus()
