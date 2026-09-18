# Author: Sharan Menon
# Date: 9/17/2026

# Created for testing and debugging purposes


import numpy as numpy
import matplotlib.pyplot as plt
import math
import csv
import os

# LOX/LCH4
LOX_LCH4 = {
    "fuel_mass_ratio": "3.6:1",
    "inert_mass_fraction": 0.067,
    "isp_sea_level_s": 327,
    "isp_vacuum_s": 380,
    "thrust_1st_stage_MN": 2.26,
    "thrust_2nd_stage_MN": 0.745,
    "exhaust_diameter_1st_stage_m": 2.4,
    "exhaust_diameter_2nd_stage_m": 1.5,
    "chamber_pressure_1st_stage_MPa": 35.16,
    "chamber_pressure_2nd_stage_MPa": 10.1,
    "expansion_ratio_1st_stage": 34.34,
    "expansion_ratio_2nd_stage": 45,
}

# LOX/LH2
LOX_LH2 = {
    "fuel_mass_ratio": "6.03:1",
    "inert_mass_fraction": 0.075,
    "isp_sea_level_s": 366,
    "isp_vacuum_s": 452,
    "thrust_1st_stage_MN": 1.86,
    "thrust_2nd_stage_MN": 0.099,
    "exhaust_diameter_1st_stage_m": 2.4,
    "exhaust_diameter_2nd_stage_m": 2.15,
    "chamber_pressure_1st_stage_MPa": 20.64,
    "chamber_pressure_2nd_stage_MPa": 4.2,
    "expansion_ratio_1st_stage": 78,
    "expansion_ratio_2nd_stage": 84,
}

# LOX/RP1
LOX_RP1 = {
    "fuel_mass_ratio": "2.72:1",
    "inert_mass_fraction": 0.063,
    "isp_sea_level_s": 311,
    "isp_vacuum_s": 337,
    "thrust_1st_stage_MN": 1.92,
    "thrust_2nd_stage_MN": 0.061,
    "exhaust_diameter_1st_stage_m": 3.7,
    "exhaust_diameter_2nd_stage_m": 0.92,
    "chamber_pressure_1st_stage_MPa": 25.8,
    "chamber_pressure_2nd_stage_MPa": 6.77,
    "expansion_ratio_1st_stage": 37,
    "expansion_ratio_2nd_stage": 14.5,
}

# Solid
SOLID = {
    "fuel_mass_ratio": None,  # N/A
    "inert_mass_fraction": 0.087,
    "isp_sea_level_s": 269,
    "isp_vacuum_s": 279,
    "thrust_1st_stage_MN": 4.5,
    "thrust_2nd_stage_MN": 2.94,
    "exhaust_diameter_1st_stage_m": 6.6,
    "exhaust_diameter_2nd_stage_m": 2.34,
    "chamber_pressure_1st_stage_MPa": 10.5,
    "chamber_pressure_2nd_stage_MPa": 5,
    "expansion_ratio_1st_stage": 16,
    "expansion_ratio_2nd_stage": 56,
}

# N204:UDMH
N204_UDMH = {
   "fuel_mass_ratio": "2.67:1",
    "inert_mass_fraction": 0.061,
    "isp_sea_level_s": 285,
    "isp_vacuum_s": 316,
    "thrust_1st_stage_MN": 1.75,
    "thrust_2nd_stage_MN": 0.067,
    "exhaust_diameter_1st_stage_m": 1.5,
    "exhaust_diameter_2nd_stage_m": 1.13,
    "chamber_pressure_1st_stage_MPa": 15.7,
    "chamber_pressure_2nd_stage_MPa": 14.7,
    "expansion_ratio_1st_stage": 26.2,
    "expansion_ratio_2nd_stage": 81.3, 
}

PROPELLANTS = [LOX_LCH4, LOX_LH2, LOX_RP1, SOLID, N204_UDMH]
PROPELLANT_NAMES = ["LOX/LCH4", "LOX/LH2", "LOX/RP1", "SOLID", "N204/UDMH"]

mission_delV_ms = 12300
pyld_mass_kg = 26000
fairing = {
    'fairing_height_m': 13,
    'fairing_diameter_m': 5.2,    
}
L_D = 13
thrust_weight_ratio_stage_1_min = 1.3
thrust_weight_ratio_stage_n_min = 0.76
stage_count_min = 2

LH2_rho_kg_m3 = 71
LOX_rho_kg_m3 = 1140
RP1_rho_kg_m3 = 820
LCH4_rho_kg_m3 = 423
Solid_rho_kg_m3 = 1680
N2O4_rho_kg_m3 = 1442
UDMH_rho_kg_m3 = 791

#FUNCTION calculate_stage_mass():
#Date Created: 9/16/2026
#Author: Henry Rowley
#Note: isp_1 MUST be sea level isp, isp_2 MUST be vacuum isp


def calculate_stage_masses(
    delta_v_1: float, #specified delta-v for first stage (m/s)
    delta_1: float, #inert mass fraction of stage 1
    delta_2: float, #inert mass fraction of stage2
    isp_1: float, #stage 1 isp(sea level) (sec)
    isp_2: float, #stage 2 isp(vacuum) (sec)
    delta_v_total: float = 12300.0, #total delta v, m/s, M1 NOTE: Might want to update dvtot, mpl, and g0 from being defined here to accessing a shared file where we store all constants
    m_pl: float = 26000.0, #payload mass, M2
    g0:float = 9.8 #g0 (m/s^2) NOTE: lecture provides 9.8 but using higher precision value here might be desirable
):
    delta_v_2 = delta_v_total - delta_v_1 

    #calculate exhaust velocity of each stage
    Ve_1 = g0 * isp_1
    Ve_2 = g0 * isp_2

    #calculate mass ratios using alternate form of rocket equation
    r_1 = math.exp(-delta_v_1/Ve_1)
    r_2 = math.exp(-delta_v_2/Ve_2)

    #calculate payload fractions using parametric mass ratio r
    lambda_1 = r_1 - delta_1
    lambda_2 = r_2 - delta_2

    #check feasibility and pass error if applicable
    error = [lambda_1 <= 0, lambda_2 <=0] #NOTE: error is a list of two booleans, gets output and can be used when sweeping through delta_v_1 values to know which values are invalid
    if any(error): #if either entry in error is true
        m_0 = m_0_2 = m_in_1 = m_in_2 = m_pr_1 = m_pr_2 = 0.0 

    else: #otherwise, calculate masses
        #calculate initial mass of each stage using payload fraction definition
        m_0_2 = m_pl/lambda_2 
        m_0 = m_0_2/lambda_1 #treat m_0_2 as m_pl for stage 1 NOTE: m_0 total launch vehicle mass, equivalently m_0_1

        #calculate inert mass of each stage
        m_in_1 = delta_1 * m_0
        m_in_2 = delta_2 * m_0_2

        #calculate propellant mass of each stage
        m_pr_1 = m_0 - m_in_1 - m_0_2 #treating m_0_2 as m_pl for stage 1
        m_pr_2 = m_0_2 - m_in_2 - m_pl

    return {
        "m_0": m_0,
        "m_in_1": m_in_1,
        "m_pr_1": m_pr_1,
        "m_0_2": m_0_2,
        "m_in_2": m_in_2,
        "m_pr_2": m_pr_2,
        "Error": error,
    }

def stage_cost(stage_m_in: float):
    # make sure stage_m_in is in kg
    cost_nre = 13.52 * stage_m_in**0.55
    return cost_nre

def sweep_delta_v(
    propellant1: dict,
    propellant2: dict,
    delta_v_total: float,
    delta_v1_min: float,
    m_pl: float,
    g0: float,
    dv_step: float
):

    results = []
    dv1 = delta_v1_min
    while(dv1 < delta_v_total):
        sweep = calculate_stage_masses(
            delta_v_1=dv1,
            delta_1=propellant1["inert_mass_fraction"],
            delta_2=propellant2["inert_mass_fraction"],
            isp_1=propellant1["isp_sea_level_s"],
            isp_2=propellant2["isp_vacuum_s"],
            delta_v_total=delta_v_total,
            m_pl=m_pl,
            g0=g0,
        )

        data = {
            "delta_v_1": dv1,
            "delta_v_2": delta_v_total - dv1,
            "m_0": sweep["m_0"],
            "m_in_1": sweep["m_in_1"],
            "m_pr_1": sweep["m_pr_1"],
            "m_0_2": sweep["m_0_2"],
            "m_in_2": sweep["m_in_2"],
            "m_pr_2": sweep["m_pr_2"],
            "Error": sweep["Error"],
        }

        results.append(data)
        dv1 += dv_step

    return results

def min_mass_finder(
        propellant1: dict,
        propellant2: dict,
        delta_v_total:float,
        delta_v1_min: float,
        m_pl: float,
        g0: float,
        dv_step=5
):

    all_results = sweep_delta_v( #sweep across all delta_v for specified prop combo
        propellant1=propellant1,
        propellant2=propellant2,
        delta_v_total=delta_v_total,
        delta_v1_min=delta_v1_min,
        m_pl=m_pl,
        g0=g0,
        dv_step=dv_step #just 5 m/s steps for now(can reduce later)
    )

    valid_results=[]
    # print(all_results)

    for entry in all_results:
        if not any(entry["Error"]): #check to make sure mass finder did not throw an error
            valid_results.append(entry)

    optimal_solution=valid_results[0] #collect valid results
    min_mass =valid_results[0]["m_0"] #set initial benchmark for minimum mass

    for entry in valid_results: #loop through valid_results and get minimum mass, return optimal solution results
        if entry["m_0"] < min_mass:
            min_mass=entry["m_0"]
            optimal_solution=entry

    return optimal_solution 

def min_cost_finder(
    propellant1:dict,
    propellant2:dict,
    delta_v_total: float,
    delta_v1_min: float,
    m_pl: float,
    g0: float,
    dv_step: float
):
    all_results = sweep_delta_v(
        propellant1=propellant1,
        propellant2=propellant2,
        delta_v_total=delta_v_total,
        delta_v1_min=delta_v1_min,
        m_pl=m_pl,
        g0=g0,
        dv_step=5
    )

    valid_results=[]

    for entry in all_results:
        if not any(entry["Error"]): #check to make sure mass finder did not throw an error
            valid_results.append(entry)

    optimal_solution=valid_results[0] #collect valid results
    min_cost = stage_cost(valid_results[0]["m_in_1"]) + stage_cost(valid_results[0]["m_in_2"]) #set initial benchmark for minimum mass

    for entry in valid_results:
        entry_cost = stage_cost(entry["m_in_1"]) + stage_cost(entry["m_in_2"]) #set initial benchmark for minimum mass
        if entry_cost < min_cost:
            min_cost=entry_cost
            optimal_solution=entry

    return optimal_solution

# AUTHOR: SHARAN SAJIV MENON
# Function to run the analysis for all propellants against each other, runs all 25 combinations
def analyze_propellants_matrix():
    results = {}
    for i,p1 in enumerate(PROPELLANTS): # 2nd stage?
        propellant_results = []
        for j,p2 in enumerate(PROPELLANTS): # 1st stage?
            optimized_mass = min_mass_finder(p1, p2, mission_delV_ms, 100, pyld_mass_kg, g0=9.8, dv_step=1)
            optimized_cost = min_cost_finder(p1, p2, mission_delV_ms, 100, pyld_mass_kg, g0=9.8, dv_step=1)
            ## mass solution
            mass_optimized_mass = optimized_mass['m_0']  / 1e3 # add to table metric tons
            mass_optimized_cost_1 = stage_cost(optimized_mass['m_in_1'])  
            mass_optimized_cost_2 = stage_cost(optimized_mass['m_in_2'])
            mass_optimized_total_cost = mass_optimized_cost_1 + mass_optimized_cost_2 # add to table
            mass_optimized_delta_v1 = optimized_mass['delta_v_1']
            mass_optimized_delta_v_fraction = optimized_mass['delta_v_1'] / mission_delV_ms
            
            ## cost solution
            cost_optimized_mass = optimized_cost['m_0'] / 1e3 # add to table, metric tons
            cost_optimized_cost_1 = stage_cost(optimized_cost['m_in_1']) # millions of dollars
            cost_optimized_cost_2 = stage_cost(optimized_cost['m_in_2'])
            cost_optimized_total_cost = cost_optimized_cost_1 + cost_optimized_cost_2 # add to table
            cost_optimized_delta_v1 = optimized_cost['delta_v_1']
            cost_optimized_delta_v_fraction = optimized_cost['delta_v_1'] / mission_delV_ms
            propellant_results.append([
                PROPELLANT_NAMES[j],
                mass_optimized_mass,
                mass_optimized_delta_v1,
                mass_optimized_delta_v_fraction,
                mass_optimized_total_cost,
                cost_optimized_total_cost,
                cost_optimized_delta_v1,
                cost_optimized_delta_v_fraction,
                cost_optimized_mass
            ])
        results[PROPELLANT_NAMES[i]] = propellant_results
    return results

# AUTHOR: SHARAN SAJIV MENON     
def write_to_csv(matrix, propellant_name):
    """
    Creates a matrix for a single 2nd stage propellant and writes it to a csv.

    """
    # write a single propellant's results to a csv file, for individual analysis use 
    second_stage_propellant = matrix[propellant_name] # 2nd stage propellant
    with open(f"{propellant_name.replace('/', '_')}.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Second Stage Propellant'] + [propellant_name for i in range(5)])
        writer.writerow(['First Stage Propellant'] + PROPELLANT_NAMES)
        row_names = [
            'Minimum LV gross mass soln. (t)',
            'Min. LV mass soln. stage 1 ΔV1 (km/s)',
            'Min. LV mass soln. stage 1 ΔV fraction (-)',
            'Min. LV mass program cost ($B2025)',
            'Min. program cost soln. ($B2025)',
            'Min. program cost soln. stage 1 ΔV1 (km/s)',
            'Min. program cost soln. stage 1 ΔV fraction (-)',
            'Min. program cost soln. gross mass (t)',

        ]
        for i, row, in enumerate(row_names):
            row_data = [row]
            for propellant in second_stage_propellant:
                row_data.append(propellant[i + 1])
            writer.writerow(row_data)  

if __name__ == "__main__":

    matrix = analyze_propellants_matrix()
    write_to_csv(matrix, "LOX/LH2")
    print(matrix)
    