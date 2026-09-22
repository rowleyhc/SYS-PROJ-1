"""
s1_5_trade_study.py -- Section 1.5 group graphics for the full 5x5 design matrix.

Author: Shaunn Pavelik (9/21/2026)

Graphic 1: side-by-side heat maps (Table 4 layout: columns = first stage,
           rows = second stage) of the minimum gross mass and minimum NRE cost.
Graphic 2: all 25 pairs ranked by minimum gross mass, with the program cost of
           the min-mass and min-cost designs beside each bar; coloured by
           second-stage propellant, top designs highlighted.
Also prints a ranked list and a rough first look at Section 2 drivers
(stage-1 engine count for T/W >= 1.3, stage-1 propellant volume).
"""
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm
from matplotlib.patches import Rectangle

import TrueConst as T
from s1_make_csv import analyze_propellants_matrix
# from s1_format import sf

NAMES = T.PROPELLANT_NAMES
INITIALS = {"Gregory Kahn": "GK", "Henry Rowley": "HR", "Jacob Harmon": "JH",
            "Sharan Menon": "SM", "Shaunn Pavelik": "SP"}
SECOND_COLORS = {"LOX/LCH4": "#2a9d8f", "LOX/LH2": "#1f5fa8", "LOX/RP1": "#e76f51",
                 "SOLID": "#6b6b6b", "N2O4/UDMH": "#9b5de5"}
N_TOP = 3


def ranked(results, design="mass", key="m0_t"):
    """All 25 (first, second, value) sorted ascending."""
    rows = [(n1, n2, results[n1][n2][design][key]) for n1 in NAMES for n2 in NAMES]
    return sorted(rows, key=lambda r: r[2])


def _style():
    plt.rcParams.update({"font.size": 15, "axes.titlesize": 19, "axes.titleweight": "bold",
                         "axes.labelsize": 17, "savefig.dpi": 250, "savefig.bbox": "tight",
                         "font.family": "serif",
        # Palatino family to match the ENAE 483 lecture slides (falls back to any serif)
        "font.serif": ["Palatino Linotype", "Palatino", "TeX Gyre Pagella", "Book Antiqua", "DejaVu Serif"],
        "mathtext.fontset": "stix"})


def heatmaps(results, path):
    """Graphic 1 -- matrix heat maps with values printed in every cell."""
    _style()
    fig, axes = plt.subplots(1, 2, figsize=(20, 8.6))
    panels = [("mass", "m0_t", "Minimum-mass designs: gross LV mass (t)", "YlOrRd"),
              ("cost", "cost_B", "Minimum-cost designs: program NRE cost ($B2025)", "PuBu")]
    for ax, (design, key, title, cmap) in zip(axes, panels):
        # grid[row = second stage, col = first stage]
        grid = np.array([[results[n1][n2][design][key] for n1 in NAMES] for n2 in NAMES])
        im = ax.imshow(grid, cmap=cmap, norm=LogNorm(grid.min(), grid.max()))
        for r in range(5):
            for c in range(5):
                v = grid[r, c]
                dark = np.log(v / grid.min()) > 0.6 * np.log(grid.max() / grid.min())
                ax.text(c, r, round(v, 2), ha="center", va="center", fontsize=15,
                        fontweight="bold", color="white" if dark else "black")
        top = ranked(results, design, key)[:N_TOP]
        # for rank, (n1, n2, _) in enumerate(top, 1): # we chose to remove this ranking thing
        #     c, r = NAMES.index(n1), NAMES.index(n2)
        #     ax.add_patch(Rectangle((c - .5, r - .5), 1, 1, fill=False, ec="#00a651", lw=4.5))
        #     ax.text(c + .42, r - .40, f"#{rank}", ha="right", va="top", fontsize=12,
        #             fontweight="bold", color="#00a651")
        ax.set_xticks(range(5), [f"{n}\n({INITIALS[T.COLUMN_OWNER[n]]})" for n in NAMES])
        ax.set_yticks(range(5), NAMES)
        ax.set_xlabel("First-stage propellant (analyst)")
        ax.set_ylabel("Second-stage propellant")
        ax.set_title(title, pad=12)
        cb = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
        cb.ax.tick_params(labelsize=12)
    fig.suptitle("Vehicle-level trade study: all 25 propellant combinations (green = top 3)",
                 fontsize=21, fontweight="bold", y=1.0)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def ranked_designs(results, path):
    """Graphic 2 -- all 25 pairs ranked by minimum gross mass; left panel = gross
    mass of the min-mass design, right panel = program cost of both designs.
    Bars are coloured by second-stage propellant; top designs highlighted."""
    _style()
    order = ranked(results)                       # best (lightest) first
    labels = [f"{n1}  /  {n2}" for n1, n2, _ in order]
    y = np.arange(len(order))[::-1]               # best at the top
    fig, (axm, axc) = plt.subplots(1, 2, figsize=(18, 11.5), sharey=True,
                                   gridspec_kw={"width_ratios": [1.35, 1], "wspace": 0.05})
    for yy, (n1, n2, m0) in zip(y, order):
        col = SECOND_COLORS[n2]
        axm.barh(yy, m0, color=col, edgecolor="black", lw=.6)
        axm.text(m0 * 1.06, yy, round(m0, 2), va="center", fontsize=12)
        cm = results[n1][n2]["mass"]["cost_B"]
        cc = results[n1][n2]["cost"]["cost_B"]
        axc.plot([cc, cm], [yy, yy], color=col, lw=2)
        axc.plot(cm, yy, "o", ms=10, color=col, mec="black")
        axc.plot(cc, yy, "D", ms=9, mfc="white", mec=col, mew=2.2)
        axc.text(max(cc, cm) * 1.07, yy, round(cc, 2), va="center", fontsize=12)
    for yy in y[:N_TOP]:
        for ax in (axm, axc):
            ax.axhspan(yy - .5, yy + .5, color="#00a651", alpha=.13, zorder=0)
    axm.set_yticks(y, labels, fontsize=13)
    for k in range(N_TOP):
        axm.get_yticklabels()[k].set_fontweight("bold")
        axm.get_yticklabels()[k].set_color("#007a3d")
    axm.set_xscale("log")
    axm.set_xlim(1e3, 5e5)
    axm.set_xlabel("Min-mass design gross LV mass (t)  [log]")
    axm.set_ylabel("Stage 1  /  Stage 2 propellant")
    axc.set_xscale("log")
    axc.set_xlim(8, 200)
    axc.set_xlabel("Program NRE cost ($B2025)  [log]")
    for ax in (axm, axc):
        ax.grid(axis="x", which="both", alpha=.3, ls="--")
        ax.set_ylim(-.6, len(order) - .4)
    handles = [plt.Line2D([], [], marker="s", ls="", ms=13, color=c, label=f"Stage 2: {n}")
               for n, c in SECOND_COLORS.items()]
    handles += [plt.Line2D([], [], marker="o", ls="", ms=10, color="#888", mec="black",
                           label="Cost of min-mass design"),
                plt.Line2D([], [], marker="D", ls="", ms=9, mfc="white", mec="#555", mew=2.2,
                           label="Min-cost design (value shown)"),
                plt.Rectangle((0, 0), 1, 1, color="#00a651", alpha=.25, label="Top 3 designs")]
    axc.legend(handles=handles, loc="upper right", fontsize=12, framealpha=.95)
    fig.suptitle("All 25 designs ranked by minimum gross mass -- every top design uses a LOX/LH2 upper stage",
                 fontsize=19, fontweight="bold", y=.94)
    fig.savefig(path)
    plt.close(fig)


def section2_preview(results, n=5):
    """Rough look at what Section 2 will stress for the leading designs."""
    rho = {"LOX/LCH4": (3.6, T.LOX_rho_kg_m3, T.LCH4_rho_kg_m3),
           "LOX/LH2": (6.03, T.LOX_rho_kg_m3, T.LH2_rho_kg_m3),
           "LOX/RP1": (2.72, T.LOX_rho_kg_m3, T.RP1_rho_kg_m3),
           "N2O4/UDMH": (2.67, T.N2O4_rho_kg_m3, T.UDMH_rho_kg_m3)}
    out = []
    for n1, n2, m0 in ranked(results)[:n]:
        raw = results[n1][n2]["mass"]["raw"]
        thrust_req = T.thrust_weight_ratio_stage_1_min * raw["m_0"] * T.G0 / 1e6     # MN
        engines = int(np.ceil(thrust_req / T.PROPS[n1]["thrust_1st_stage_MN"]))
        if n1 == "Solid":
            vol = raw["m_pr_1"] / T.SOLID_rho_kg_m3
        else:
            of, rox, rfu = rho[n1]
            vol = raw["m_pr_1"] * (of / (of + 1)) / rox + raw["m_pr_1"] / (of + 1) / rfu
        out.append((n1, n2, m0, engines, vol))
    return out


if __name__ == "__main__":
    os.makedirs("figs", exist_ok=True)
    res = analyze_propellants_matrix()
    heatmaps(res, "figs/S1_5_graphic1_heatmaps.png")
    ranked_designs(res, "figs/S1_5_graphic2_ranked_designs.png")
    print("Top min-mass:", [(a, b, round(v)) for a, b, v in ranked(res)[:5]])
    print("Top min-cost:", [(a, b, round(v, 2)) for a, b, v in ranked(res, "cost", "cost_B")[:5]])
    for row in section2_preview(res):
        print("S2 preview %-9s/%-9s m0=%6.0f t  stage-1 engines=%2d  stage-1 prop vol=%6.0f m^3" % row)
