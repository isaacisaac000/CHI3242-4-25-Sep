#!/usr/bin/env python3
"""
Find statistically significant collocates of 王小波 in the novel.

1. Split the novel into sentences.
2. Tokenize each sentence into words with jieba.
3. Use qhchina.find_collocates (method='window', horizon=5, p < 0.05).
4. Save results as a CSV file.
"""

import re

import jieba
import pandas as pd
from qhchina import find_collocates
from qhchina.helpers.texts import load_stopwords

NOVEL_FILE = "78_黄金时代.txt"
OUTPUT_CSV = "collocates_王小波.csv"
TARGET_WORD = "王小波"
P_VALUE = 0.05
HORIZON = 5


def split_sentences(text: str) -> list[str]:
    """Split the novel into sentences on Chinese sentence-ending punctuation."""
    import re
    sentences = re.split(r"([。！？!?……]+)", text)
    # Re-join each sentence with its ending punctuation
    result = []
    for i in range(0, len(sentences) - 1, 2):
        result.append(sentences[i] + sentences[i + 1])
    if sentences[-1].strip():
        result.append(sentences[-1])
    return [s.strip() for s in result if s.strip()]


def tokenize(sentences: list[str]) -> list[list[str]]:
    """Tokenize each sentence into words with jieba, keeping only words of 2+ characters."""
    return [
        [w for w in jieba.cut(s) if len(w) > 1 and not re.fullmatch(r"\W", w)]
        for s in sentences
    ]


def main() -> None:
    with open(NOVEL_FILE, encoding="utf-8") as f:
        text = f.read()

    sentences = split_sentences(text)
    print(f"Sentences: {len(sentences)}")

    tokenized = tokenize(sentences)

    stopwords = load_stopwords("zh_sim")
    result = find_collocates(
        sentences=tokenized,
        target_words=TARGET_WORD,
        method="window",
        horizon=HORIZON,
        filters={"stopwords": list(stopwords)},
    )

    if isinstance(result, pd.DataFrame):
        result.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"Saved {len(result)} collocates to {OUTPUT_CSV}")
        print(result.head(20).to_string())
    else:
        df = pd.DataFrame(result)
        df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")
        print(f"Saved {len(df)} collocates to {OUTPUT_CSV}")


if __name__ == "__main__":
    main()