"""
main_section1.py -- one command that regenerates every Section 1 deliverable.

Author: Shaunn Pavelik (9/21/2026)

    python main_section1.py

1. runs the verification checks (s1_checks.py)
2. solves the full 5x5 matrix, writes results/ CSVs (S.1.2.b, S.1.3.b, S.1.5)
3. draws each teammate's S.1.2.a / S.1.3.a graphs for their chosen pair
4. draws the two group S.1.5 graphics
Everything uses the shared settings in TrueConst (G0, DV_STEP, DV1_MIN).
"""
import runpy

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import TrueConst
import s1_auto_graph as graph
import s1_5_trade_study as study
from s1_make_csv import analyze_propellants_matrix, write_to_csv, write_all_csv

# (stage 1, stage 2) each teammate plots for S.1.2.a / S.1.3.a.
# Stage 1 must be the teammate's own Table 4 column -- edit the second stage freely.
CHOSEN_PAIRS = {
    "Gregory Kahn":   ("LOX/LCH4", "LOX/LH2"),
    "Henry Rowley":   ("LOX/LH2", "LOX/LH2"),
    "Jacob Harmon":   ("LOX/RP1", "LOX/LH2"),
    "Sharan Menon":   ("SOLID", "LOX/LH2"),
    "Shaunn Pavelik": ("N2O4/UDMH", "LOX/LH2"),
}

if __name__ == "__main__":

    print("\n== design matrix ==")
    results = analyze_propellants_matrix()
    for name in TrueConst.PROPELLANT_NAMES:
        print("wrote", write_to_csv(results, name))
    print("wrote", write_all_csv(results))

    print("\n== individual trend graphs ==")
    for who, (s1, s2) in CHOSEN_PAIRS.items():
        t = graph.trends(s1, s2)
        tag = f"{s1}__{s2}".replace("/", "_")
        graph.plot_mass(t, f"figs/{tag}_mass_trends.png")
        graph.plot_cost(t, f"figs/{tag}_cost_trends.png")
        plt.close("all")
        print(f"{who}: {tag}")

    print("\n== group S.1.5 graphics ==")
    study.heatmaps(results, "figs/S1_5_graphic1_heatmaps.png")
    study.ranked_designs(results, "figs/S1_5_graphic2_ranked_designs.png")
    print("done -- see results/ and figs/")
