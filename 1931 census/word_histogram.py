#!/usr/bin/env python3
"""
Word-frequency histograms for every document in this folder, plus the words that
are common to ALL documents in the folder.

A "document" is any <name>.txt that has a matching <name>.pdf (so key.txt, notes
and other stray .txt files are ignored).

Outputs (in word_histogram_output/):
  words_per_document.csv   every word, its count in each document, total, #docs
  common_words.csv         words present (>= MIN_DOC_COUNT times) in EVERY document,
                           with per-document counts and the combined total
  hist_<doc>.png           bar chart of the TOP most frequent words in each document
  hist_common_combined.png top common words, bars stacked by document
  summary.txt              what was counted

Usage:  .venv/bin/python word_histogram.py [--top 30] [--min-doc-count 3]
"""
import argparse
import re
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")                      # draw to files, no window needed
import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).resolve().parent
OUT = HERE / "word_histogram_output"

STOPWORDS = set("""
a about above after again against all also am an and any are as at be because been
before being below between both but by can could did do does doing down during each
few for from further had has have having he her here hers him his how i if in into is
it its itself just me more most my no nor not now of off on once only or other our out
over own same she should so some such than that the their them then there these they
this those through to too under until up very was we were what when where which while
who whom why will with would you your yours one two three four five six seven eight
nine ten per may shall upon thus however etc nil see table total
said many much per cent among within without whose whether since still yet will
us even like made make well first second third part each very new old
""".split())


def tokens(text):
    out = []
    for w in re.findall(r"[a-z]+", text.lower()):
        if 3 <= len(w) <= 20 and w not in STOPWORDS and not re.search(r"(.)\1\1", w):
            out.append(w)
    return out


def find_documents():
    docs = []
    for txt in sorted(HERE.glob("*.txt")):
        if (HERE / f"{txt.stem}.pdf").exists():
            docs.append(txt)
    return docs


def bar_chart(counter, title, dest, top):
    items = counter.most_common(top)[::-1]          # biggest at the top
    fig, ax = plt.subplots(figsize=(8, 0.28 * len(items) + 1.5))
    ax.barh([w for w, _ in items], [c for _, c in items], color="#4a7ebb")
    ax.set_title(title)
    ax.set_xlabel("occurrences")
    fig.tight_layout()
    fig.savefig(dest, dpi=150)
    plt.close(fig)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--top", type=int, default=30, help="words shown per histogram")
    ap.add_argument("--min-doc-count", type=int, default=3,
                    help="a word is 'in' a document if it occurs at least this often")
    args = ap.parse_args()

    docs = find_documents()
    if not docs:
        raise SystemExit("No <name>.txt with a matching <name>.pdf found in this folder.")
    OUT.mkdir(exist_ok=True)

    counts = {}
    for txt in docs:
        counts[txt.stem] = Counter(tokens(txt.read_text(errors="ignore")))
        print(f"{txt.stem}: {sum(counts[txt.stem].values()):,} words, "
              f"{len(counts[txt.stem]):,} distinct")

    df = pd.DataFrame(counts).fillna(0).astype(int)
    names = list(counts)
    df["total"] = df[names].sum(axis=1)
    df["n_docs_present"] = (df[names] >= args.min_doc_count).sum(axis=1)
    df = df.sort_values("total", ascending=False)
    df.index.name = "word"
    df.to_csv(OUT / "words_per_document.csv", encoding="utf-8-sig")

    common = df[df["n_docs_present"] == len(names)].copy()
    common.to_csv(OUT / "common_words.csv", encoding="utf-8-sig")

    for name, c in counts.items():
        bar_chart(c, f"{name}: top {args.top} words", OUT / f"hist_{name}.png", args.top)

    if len(common):
        top = common.head(args.top)[::-1]
        fig, ax = plt.subplots(figsize=(9, 0.3 * len(top) + 1.8))
        left = pd.Series(0, index=top.index)
        for name in names:
            ax.barh(top.index, top[name], left=left, label=name)
            left += top[name]
        ax.set_title(f"Top {len(top)} words common to all {len(names)} documents")
        ax.set_xlabel("occurrences (stacked by document)")
        ax.legend(fontsize=7)
        fig.tight_layout()
        fig.savefig(OUT / "hist_common_combined.png", dpi=150)
        plt.close(fig)

    summary = [f"Documents: {', '.join(names)}",
               f"Distinct words overall: {len(df):,}",
               f"Words common to all documents (>= {args.min_doc_count} each): {len(common):,}",
               "", "Top 20 common words (combined count):"]
    summary += [f"  {w}: {int(r['total'])}" for w, r in common.head(20).iterrows()]
    (OUT / "summary.txt").write_text("\n".join(summary), encoding="utf-8")
    print("\n" + "\n".join(summary))
    print(f"\nOutputs in {OUT}")


if __name__ == "__main__":
    main()
