"""

Author: Shaunn Pavelik (9/21/2026)
Author: Jacob Harmon (9/24/2026)

    python main_section1.py


"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

import TrueConst
import s1_auto_graph as graph
import s1_5_trade_study as study
from s1_make_csv import analyze_propellants_matrix, write_to_csv, write_full_matrix_csv

# (stage 1, stage 2) each teammate plots for S.1.2.a / S.1.3.a.
# Stage 1 must be the teammate's own Table 4 column -- edit the second stage freely.
CHOSEN_PAIRS = {
    "Gregory Kahn":   ("LOX/RP1", "LOX/LCH4"),
    "Henry Rowley":   ("LOX/RP1", "LOX/LH2"),
    "Jacob Harmon":   ("LOX/RP1", "LOX/RP1"),
    "Sharan Menon":   ("LOX/RP1", "SOLID"),
    "Shaunn Pavelik": ("LOX/RP1", "N2O4/UDMH"),
}

def as_designs(matrix):
    """analyze_propellants_matrix() returns one row per pair, while s1_5_trade_study
    reads matrix[first][second][design][key]. Convert between the two shapes here
    rather than duplicating the trade study."""
    out = {}
    for first, rows in matrix.items():
        out[first] = {}
        for row in rows:
            out[first][row[0]] = {
                "mass": {"m0_t": row[1], "dv1_kms": row[2] / 1e3,
                         "dv1_frac": row[3], "cost_B": row[4]},
                "cost": {"m0_t": row[8], "dv1_kms": row[6] / 1e3,
                         "dv1_frac": row[7], "cost_B": row[5]},
            }
    return out


if __name__ == "__main__":

    os.makedirs("figs", exist_ok=True)

    print("\n== design matrix ==")
    results = analyze_propellants_matrix()
    for name in TrueConst.PROPELLANT_NAMES:
        print("wrote", write_to_csv(results, name))

    print("\n== individual trend graphs ==")
    for who, (s1, s2) in CHOSEN_PAIRS.items():
        t = graph.trends(s1, s2)
        tag = f"{s1}__{s2}".replace("/", "_")
        graph.plot_mass(t, f"figs/{tag}_mass_trends.png")
        graph.plot_cost(t, f"figs/{tag}_cost_trends.png")
        plt.close("all")
        print(f"{who}: {tag}")

    print("\n== group S.1.5 graphics ==")
    designs = as_designs(results)
    study.heatmaps(designs, "figs/S1_5_graphic1_heatmaps.png")
    study.ranked_designs(designs, "figs/S1_5_graphic2_ranked_designs.png")
    print("done -- see csvs/ and figs/")

    #Author: Jacob Harmon
    print("\n== design matrix ==")
    results = analyze_propellants_matrix()
    for name in TrueConst.PROPELLANT_NAMES:
        print("wrote", write_to_csv(results, name))
    print("wrote", write_full_matrix_csv(results))
