# author: sharan sajiv menon
import numpy as np
from S2_1 import run_systems_analysis
import utils.TrueConst as TrueConst
import csv
import os

## think this is the cost function, if we have something updated
# please replace this
def stage_cost(stage_m_in: float):
    cost_nre = 13.52 * stage_m_in**0.55
    return cost_nre

DELTA_V_1 = 6000.0  # m/s

### author: sharan sajiv menon
def create_table_of_masses(results: dict):
    # masses of subsystems for each stage
    stage1 = results["stage_1"]
    stage2 = results["stage_2"]
    stage1_masses = list(filter(lambda x: "mass" in x, list(stage1.keys())))
    stage2_masses = list(filter(lambda x: "mass" in x, list(stage2.keys())))
    print(stage1_masses)
    print(stage2_masses)
    ## calculate costs
    stage1_total_mass = stage1['stage_mass']
    stage2_total_mass = stage2['stage_mass']
    
    # input should be in mt
    total_cost = stage_cost(stage1_total_mass / 1e3) + stage_cost(stage2_total_mass /1e3)
    ## csv will have 3 columns
    # stage, component_name (total if total mass), mass
    # total masses at the bottom
    path = "csvs/S2_2_table_of_masses.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stage", "Component Name", "Mass (kg)"])
        for mass_name in stage1_masses:
            writer.writerow(["Stage 1", mass_name.replace("_", " ").title(), stage1[mass_name]])
        for mass_name in stage2_masses:
            writer.writerow(["Stage 2", mass_name.replace("_", " ").title(), stage2[mass_name]])
        writer.writerow(
            ["LV", "Total Mass", stage1["stage_mass"] + stage2["stage_mass"]]
        )
        writer.writerow(["LV", "Total Cost ($B2025)", total_cost/1e3])
    return path

if __name__ == "__main__":
    # pick your propellant combo
    stage1 = "SOLID"
    stage2 = "LOX/LCH4"
    analysis_data = run_systems_analysis(stage1, stage2, DELTA_V_1)
    create_table_of_masses(analysis_data)