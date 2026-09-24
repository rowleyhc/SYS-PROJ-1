import TrueConst
from s1_2_b_auto import min_mass_finder
from s1_3_b_auto import min_cost_finder
from s1_3_cost import stage_cost
import csv
import numpy as np
import os
import math
ROW_NAMES = [
        'Minimum LV gross mass soln. (t)',
        'Min. LV mass soln. stage 1 ΔV1 (m/s)',
        'Min. LV mass soln. stage 1 ΔV fraction (-)',
        'Min. LV mass program cost ($B2025)',
        'Min. program cost soln. ($B2025)',
        'Min. program cost soln. stage 1 ΔV1 (m/s)',
        'Min. program cost soln. stage 1 ΔV fraction (-)',
        'Min. program cost soln. gross mass (t)',
    ]


## quick significant figures function
SIG_FIGS = 4
def sf(x, n=SIG_FIGS):
    """Round x to n significant figures and return it as a string with
    thousands separators, e.g. sf(1852.5) -> '1,850', sf(0.30488) -> '0.305'."""
    if x == 0 or not math.isfinite(x):
        return str(x)
    digits = n - int(math.floor(math.log10(abs(x)))) - 1
    r = round(x, digits)
    return f"{r:,.{max(digits, 0)}f}"

# AUTHOR: SHARAN SAJIV MENON
# Function to run the analysis for all propellants against each other, runs all 25 combinations
def analyze_propellants_matrix():
    results = {}
    for i,p1 in enumerate(TrueConst.PROPELLANTS): # 1st stage
        propellant_results = []
        for j,p2 in enumerate(TrueConst.PROPELLANTS): # 2nd stage
            optimized_mass = min_mass_finder(p1, p2, TrueConst.mission_delV_ms, 100, TrueConst.pyld_mass_kg, g0=9.8, dv_step=1)
            optimized_cost = min_cost_finder(p1, p2, TrueConst.mission_delV_ms, 100, TrueConst.pyld_mass_kg, g0=9.8, dv_step=1)
            ## mass solution
            mass_optimized_mass = optimized_mass['m_0']  / 1e3 # add to table metric tons
            mass_optimized_total_cost = (stage_cost(optimized_mass['m_in_1']) + stage_cost(optimized_mass['m_in_2'])) / 1e3  # $B2025, add to table
            mass_optimized_delta_v1 = optimized_mass['delta_v_1']
            mass_optimized_delta_v_fraction = optimized_mass['delta_v_1'] / TrueConst.mission_delV_ms
            
            ## cost solution
            cost_optimized_mass = optimized_cost['m_0'] / 1e3 # add to table, metric tons
            cost_optimized_total_cost = (stage_cost(optimized_cost['m_in_1']) + stage_cost(optimized_cost['m_in_2'])) / 1e3  # $B2025, add to table
            cost_optimized_delta_v1 = optimized_cost['delta_v_1']
            cost_optimized_delta_v_fraction = optimized_cost['delta_v_1'] / TrueConst.mission_delV_ms
            propellant_results.append([
                TrueConst.PROPELLANT_NAMES[j],
                mass_optimized_mass,
                mass_optimized_delta_v1,
                mass_optimized_delta_v_fraction,
                mass_optimized_total_cost,
                cost_optimized_total_cost,
                cost_optimized_delta_v1,
                cost_optimized_delta_v_fraction,
                cost_optimized_mass
            ])
        results[TrueConst.PROPELLANT_NAMES[i]] = propellant_results
    return results

# AUTHOR: SHARAN SAJIV MENON     
def write_to_csv(matrix, propellant_name):
    """
    Creates a matrix for a single 2nd stage propellant and writes it to a csv.

    """
    # write a single propellant's results to a csv file, for individual analysis use
    os.makedirs("csvs", exist_ok=True)
    second_stage_propellant = matrix[propellant_name] # 2nd stage propellant
    path = f"csvs/{propellant_name.replace('/', '_')}.csv"
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['First Stage Propellant'] + [propellant_name for i in range(5)])
        writer.writerow(['Second Stage Propellant'] + TrueConst.PROPELLANT_NAMES)
        for i, row, in enumerate(ROW_NAMES):
            row_data = [row]
            for propellant in second_stage_propellant:
                row_data.append(sf(propellant[i + 1], 2))
            writer.writerow(row_data)  
    return path


# AUTHOR: JACOB HARMON
def write_full_matrix_csv(matrix, path="csvs/all_combinations.csv"):
    """
    Writes every (first stage, second stage) combination from the matrix
    into a single flat csv, one row per pair.
    """
    os.makedirs("csvs", exist_ok=True)
    with open(path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(['First Stage Propellant', 'Second Stage Propellant'] + ROW_NAMES)
        for second_stage, rows in matrix.items():
            for row in rows:
                first_stage = row[0]
                writer.writerow([first_stage, second_stage] + [sf(v) for v in row[1:]])
    return path

if __name__ == "__main__":
    if not os.path.exists('csvs'):
        os.mkdir('csvs')
    matrix = analyze_propellants_matrix()
    for name in TrueConst.PROPELLANT_NAMES:
        write_to_csv(matrix, name)
    print(matrix)
