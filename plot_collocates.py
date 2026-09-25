#!/usr/bin/env python3
"""Visualise the collocates of 王小波 with qhchina.analytics.collocations.plot_collocates."""

import pandas as pd
from qhchina import load_fonts
from qhchina.analytics.collocations import plot_collocates

CSV_FILE = "collocates_王小波.csv"
OUTPUT_PNG = "collocates_王小波.png"


def main() -> None:
    df = pd.read_csv(CSV_FILE)

    load_fonts()  # load default CJK font before rendering

    plot_collocates(
        df,
        x_col="ratio_local",
        y_col="p_value",
        x_scale="log",
        y_scale="log",
        color_by="obs_local",
        show_labels=True,
        label_top_n=30,
        title="「王小波」的显著搭配词（window 法，左右各 5 词）",
        xlabel="局部频率比率 (obs/exp, log)",
        ylabel="p 值 (log)",
        filename=OUTPUT_PNG,
        figsize=(11, 8),
    )
    print(f"Saved plot to {OUTPUT_PNG}")


if __name__ == "__main__":
    main()