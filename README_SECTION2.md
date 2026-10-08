# Section 2 update (Shaunn, 10/8)

This folder is the whole repo (GitHub commit 6b2c438 + the Section 2 changes), so it runs on its own.

1. Right-click the zip > **Extract All** (don't run files from inside the zip - Windows only
   pulls out the one file you clicked, so the imports fail).
2. One time: `python -m pip install numpy matplotlib` (use the same python VS Code runs).
3. VS Code > File > Open Folder > `SYS-PROJ-1`, open `main_section2.py`, press Run.
   It works from any terminal folder; outputs always land next to the script.

Takes about 2 minutes. It writes `csvs/` and `figs/` for every pair in `CHOSEN_PAIRS`
(right now everyone's Section 1 pair: own column over LOX/LH2), plus the all-25 table and
two group graphics. Change your pair at the top of `main_section2.py` if you switch.

## What you get

| Output | For |
|---|---|
| `csvs/S2_2_table_of_masses_<pair>_dv1_<dv1>.csv` | S.2.2 table, every value with units, 4 s.f. (min-mass and min-cost split) |
| `figs/S2_2_<pair>_<mass/cost>_breakdown.png` | subsystem masses, both stages |
| `figs/S2_2_<pair>_<mass/cost>_vl_vs_sl.png` | system level vs Section 1 vehicle level, mass and cost |
| `figs/S2_2_<pair>_<mass/cost>_sketch.png` | dimensioned side view (CAD starting point) |
| `figs/S2_2_<pair>_dv1_sweep.png` | does the Section 1 split still hold at system level? |
| `figs/S2_group_team_designs.png` | group graphic: our five designs, VL vs SL |
| `figs/S2_group_matrix_mass.png` | group graphic: all 25 pairs |
| `csvs/S2_all25_system_level.csv` | all 25 pairs x both splits: mass, cost, D, L, L/D, engines |

## Files

| File | What changed |
|---|---|
| `S2_1.py` | Fixed the crash, put the real Lecture 8 MERs in, delta-V closure, stage layout and fairings, diameter pick |
| `S2_2.py` | Cost now on inert mass in kg (same as Section 1); units on every row; one CSV per design |
| `S2_auto_graph.py` | New: breakdown, vehicle vs system level, delta-V sweep, vehicle sketch, team + all-25 graphics. Greg: merge with yours or replace |
| `main_section2.py` | New: runs everything |

## Bugs fixed in what was on GitHub (commit 6b2c438)

1. **Crash:** `mer_insulation_mass(geometry["total_tank_area"], info["needs_insulation"])` - the function now takes `(geometry, info)` and liquids had no `total_tank_area` key, so every liquid stage threw `KeyError`.
2. **Placeholder MERs:** engines, thrust structure, solid casing, gimbals, avionics, wiring and every fairing were "TEMPORARY EQUATION"s. All now use Lecture 8 (slide refs in the code).
3. **Delta-V not met:** the loop kept the Section 1 propellant fixed, so once the inert mass changed the vehicle no longer delivered 12.3 km/s (Shaunn's design came out 308 m/s short). Each pass now re-solves propellant from the rocket equation. `close_delta_v=False` still gives the old behavior.
4. **S2_2 cost:** used total stage mass (propellant included) in tonnes. The cost relation is on inert mass in kg -> $M, same as `s1_3_cost.stage_cost`.
5. **Tank geometry:** Greg's domed area kept; length was still a flat cylinder, and tanks smaller than one sphere gave a negative cylinder length. Now consistent, and small tanks become spheres.
6. **Payload fairing** was a 13 m cone at 5.2 m diameter - the payload envelope (5.2 m x 13 m) would not fit. Now a cylinder over the envelope plus a nose cone.
7. **Diameter** was 5.2 m, which is the payload envelope itself. Now 5.6 m minimum (0.2 m clearance), then the lightest diameter that meets L/D <= 13.

## MER check

Lecture 8 (public F24 deck, 483F24L08): tanks slide 7, insulation slide 9, fairings/avionics/wiring
slide 22, areas slide 23, engines/thrust structure/casing slide 27, gimbals slide 28. Check the
slide numbers against our F26 deck before they go on a slide.

Reproduces every number in the Lecture 8 SSTO example: engines 2236 kg, gimbals 81 kg, avionics
744 kg, wiring 886 kg, payload fairing 645 kg, thrust structure 497 kg. The engine MER needs
`sqrt(Ae/At)` and the wiring MER needs `L^0.25` to hit those (the PDF text drops both).

Insulation (Greg's question): the MER is kg per m^2 of tank area (2.88 LH2, 1.123 LOX/LCH4), so
it works for any tank shape. The lecture's spheres were only its first-pass geometry.

## Team decisions still open

- Require engines to fit inside the stage diameter? (`ENFORCE_ENGINE_FIT`, off by default - on, designs go to 8-24 m diameters, and LOX/RP1 and solid first stages find no diameter that fits)
- Payload fairing carried for the whole stage 2 burn (conservative) vs dropped early
- Avionics/wiring M0 = mass at that stage's ignition (stage + everything above), L = stage length
- Section 1 delta-V split as the S.2.1 input (handout) vs the system-level optimum (the sweep graph)
- Nose cone height = 1.0 x diameter, 0.5 m inter-tank gap, 0.5 m payload adapter gap, 0.2 m radial clearance
- Gimbals on solid stages (included - solids still need TVC)
