# author: sharan sajiv menon
import numpy as np
from S2_1 import run_systems_analysis
import utils.TrueConst as TrueConst
from utils.sf import sf
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
    ## calculate costs
    stage1_total_mass = stage1['dry_mass_with_margin']
    stage2_total_mass = stage2['dry_mass_with_margin']
    
    # input should be in mt
    stage1_cost = stage_cost(stage1_total_mass / 1e3) # convert to mt 
    stage2_cost = stage_cost(stage2_total_mass / 1e3)
    total_cost = stage1_cost + stage2_cost
    ## csv will have 3 columns
    # stage, component_name (total if total mass), mass
    # total masses at the bottom
    path = "csvs/S2_2_table_of_masses.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Stage", "Component Name", "Value", "Unit"])
        for mass_name in stage1_masses:
            writer.writerow(["Stage 1", mass_name.replace("_", " ").title(), sf(stage1[mass_name]), "kg"])
        writer.writerow(["Stage 1", "TotaL Cost", stage1_cost, "$B (FY2025)"])
        for mass_name in stage2_masses:
            writer.writerow(["Stage 2", mass_name.replace("_", " ").title(), sf(stage2[mass_name]), "kg"])
        writer.writerow(["Stage 2", "Total Cost", stage2_cost, "$B (FY2025)"])
        ## launch vehicle stats
        writer.writerow(["LV", "Payload", sf(26000), "kg"])
        writer.writerow(["LV", "Total Mass (system level)", sf(results["systems_gross_mass"]), "kg"])
        writer.writerow(["LV", "Total Mass (vehicle level)", sf(results["ideal_gross_mass"]), "kg"])
        writer.writerow(["LV", "Total Cost ($B2025)", sf(total_cost), "$B (FY2025)"])
    return path

if __name__ == "__main__":
    # pick your propellant combo
    stage1 = "SOLID"
    stage2 = "LOX/LCH4"
    analysis_data = run_systems_analysis(stage1, stage2, DELTA_V_1)
    create_table_of_masses(analysis_data)