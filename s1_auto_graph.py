# ENAE 483
# AUTHORS: Gregory Kahn
#
# to run: set stage1/stage2 in the block at the bottom and run it, no arguments

import argparse
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.figure import Figure

import TrueConst
from s1_sweep import sweep_delta_v
from s1_3_cost import stage_cost

DV_TOTAL = TrueConst.mission_delV_ms      # m/s    M1
PAYLOAD = TrueConst.pyld_mass_kg       # kg     M2
G0 = TrueConst.G0               # m/s^2
DV1_MIN = 100         # m/s, sweep starts here
DV_STEP = 1.0       # m/s, 1 is what the team settled on for the final numbers
YLIM_FACTOR = 3.0       # y axis cap, otherwise the edges squash the whole curve

# keys have to match TrueConst.PROPELLANT_NAMES or the lookups in trends() blow up.
# TrueConst still spells the storables one N204_UDMH with a zero, so that's the name used here
PROPS = {
    "LOX/LCH4": TrueConst.LOX_LCH4,
    "LOX/LH2": TrueConst.LOX_LH2,
    "LOX/RP1": TrueConst.LOX_RP1,
    "SOLID": TrueConst.SOLID,
    "N2O4/UDMH": TrueConst.N204_UDMH,
}


def trends(stage1: str, stage2: str, dv_step: float = DV_STEP) -> dict:
    # one row per split, in sweep order
    rows = sweep_delta_v(PROPS[stage1], PROPS[stage2], DV_TOTAL, DV1_MIN,
                         PAYLOAD, G0, dv_step)

    dv1 = np.array([r["delta_v_1"] for r in rows])
    m_in1 = np.array([r["m_in_1"] for r in rows])
    m_in2 = np.array([r["m_in_2"] for r in rows])
    m_gross = np.array([r["m_0"] for r in rows]) / 1e3              # tonnes
    m_stage1 = np.array([r["m_in_1"] + r["m_pr_1"] for r in rows]) / 1e3
    # team convention - stage 2 is its own inert + propellant, payload is not inside it,
    # so stage1 + stage2 + payload comes out as gross. that's what 1.2.a asks for
    m_stage2 = np.array([r["m_in_2"] + r["m_pr_2"] for r in rows]) / 1e3
    cost1 = stage_cost(m_in1) / 1e3                                 # $B 2025
    cost2 = stage_cost(m_in2) / 1e3
    cost = cost1 + cost2

    # splits that don't close come back as zeros from the sweep, and plotting a zero
    # drags the curve down to the axis, so blank them instead
    ok = np.array([not any(r["Error"]) for r in rows])
    if not ok.any():                 # whole sweep failed, nothing worth plotting
        raise ValueError("no feasible split for this pair, try a smaller dv_step")
    for curve in (dv1, m_stage1, m_stage2, m_gross, cost1, cost2, cost):
        curve[~ok] = np.nan

    return {
        "names": (stage1, stage2),
        "ok": ok,
        "dv1": dv1,
        "frac": dv1 / DV_TOTAL,
        "m_stage1": m_stage1,
        "m_stage2": m_stage2,
        "m_gross": m_gross,
        "cost1": cost1,
        "cost2": cost2,
        "cost": cost,
        # nanargmin skips the blanks, plain argmin would hand back the first zero
        "i_mass": int(np.nanargmin(m_gross)),
        "i_cost": int(np.nanargmin(cost)),
    }


def _setup(t: dict) -> tuple[Figure, Axes]:
    # big fonts, this ends up on a projector
    plt.rcParams.update({
        "font.size": 15,
        "axes.titlesize": 19,
        "axes.labelsize": 17,
        "axes.labelweight": "bold",
        "legend.fontsize": 14,
        "figure.figsize": (13, 7.6),
        "figure.dpi": 110,
        "savefig.dpi": 300,
        "savefig.bbox": "tight",
        "lines.linewidth": 3,
    })

    fig, ax = plt.subplots()
    # zoom to the feasible window, there's a long dead patch either side of it
    lo, hi = t["frac"][t["ok"]].min(), t["frac"][t["ok"]].max()
    ax.set_xlim(lo, hi)
    ax.set_xlabel("First stage delta-V fraction,  $\\Delta V_1 / \\Delta V_{total}$")
    ax.grid(alpha=0.35, ls="--")
    return fig, ax


def _mark(ax: Axes, x: float, y: float, label: str, colour: str) -> None:
    # star on the optimum, named only. the value used to be printed here too but
    # :,.0f turned $10.56B into "11", and the slide callout and the T.6 table carry it
    ax.plot(x, y, "*", ms=22, color=colour, mec="black", zorder=6, label=label)
    ax.annotate(label, (x, y), xytext=(10, 14),
                textcoords="offset points", fontweight="bold", color=colour,
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=colour),
                arrowprops=dict(arrowstyle="->", color=colour, lw=2), zorder=7)


def _save(fig: Figure, path: str | None) -> None:
    # only print when we're actually writing a file
    if path:
        fig.savefig(path)
        print(f"saved {path}")


def plot_mass(t: dict, path: str | None = None) -> Figure:
    fig, ax = _setup(t)
    cap = YLIM_FACTOR * t["m_gross"][t["i_mass"]]

    # as dv1 goes up one of the stages stops closing and the mass heads off the top of
    # the chart. cut it at the cap so the interesting part stays readable
    for curve, colour, label in ((t["m_stage1"], "tab:blue", "Stage 1 mass"),
                                 (t["m_stage2"], "tab:orange", "Stage 2 mass"),
                                 (t["m_gross"], "black", "Gross LV mass (incl. payload)")):
        ax.plot(t["frac"], np.where(curve <= cap, curve, np.nan), color=colour, label=label)

    _mark(ax, t["frac"][t["i_mass"]], t["m_gross"][t["i_mass"]], "Minimum gross mass", "red")
    # dashed guide at the *other* optimum, used on the 1.4 slide
    ax.axvline(t["frac"][t["i_cost"]], color="purple", ls="--", lw=2,
               label="Min-cost $\\Delta V_1$ split")

    ax.set_ylim(0, cap)
    ax.set_ylabel("Mass  (t)")
    ax.set_title(f"Mass trends - Stage 1: {t['names'][0]}, Stage 2: {t['names'][1]}")
    ax.legend(loc="upper center", ncol=2)
    _save(fig, path)
    return fig


def plot_cost(t: dict, path: str | None = None) -> Figure:
    fig, ax = _setup(t)
    cap = YLIM_FACTOR * t["cost"][t["i_cost"]]
    # cost curve is a lot flatter round the minimum than the mass one, which is why the
    # two splits are ~1 km/s apart but only 3% apart in cost

    for curve, colour, label in ((t["cost1"], "tab:green", "Stage 1 NRE cost"),
                                 (t["cost2"], "tab:red", "Stage 2 NRE cost"),
                                 (t["cost"], "black", "Total NRE cost")):
        ax.plot(t["frac"], np.where(curve <= cap, curve, np.nan), color=colour, label=label)

    _mark(ax, t["frac"][t["i_cost"]], t["cost"][t["i_cost"]], "Minimum program cost", "blue")
    ax.axvline(t["frac"][t["i_mass"]], color="purple", ls="--", lw=2,
               label="Min-mass $\\Delta V_1$ split")

    ax.set_ylim(0, cap)
    ax.set_ylabel("Program cost  ($B 2025)")
    ax.set_title(f"Cost trends - Stage 1: {t['names'][0]}, Stage 2: {t['names'][1]}")
    ax.legend(loc="upper center", ncol=2)
    _save(fig, path)
    return fig


def report(t: dict) -> None:
    # the two optima in the terminal, quicker than opening the pngs
    for label, i in (("min mass", t["i_mass"]), ("min cost", t["i_cost"])):
        print(f"{label}: dV1 = {t['dv1'][i] / 1e3:.2f} km/s ({t['frac'][i]:.3f} of total), "
              f"LV mass = {t['m_gross'][i]:.1f} t, program cost = ${t['cost'][i]:.2f}B")



if __name__ == "__main__":
    stage1 = "SOLID" # change to your propellants here
    stage2 = "LOX/LH2"
    out = "figs/"
    show = False # if you want to see the figures

    t = trends(stage1, stage2, DV_STEP)

    os.makedirs(out, exist_ok=True)
    # both stages in the filename so the 25 pairs don't overwrite each other
    tag = f"{stage1}__{stage2}".replace("/", "_")
    plot_mass(t, os.path.join(out, tag + "_mass_trends.png"))
    plot_cost(t, os.path.join(out, tag + "_cost_trends.png"))
    report(t)

    if show:
        plt.show()
    else:
        plt.close("all")
