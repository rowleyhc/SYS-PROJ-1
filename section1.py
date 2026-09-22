#


# Author: Jacob Harmon
# Date: 9/16/2026


import math
import numpy as np

# List of true constants for propelant mixures
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
Solid = {
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
g0 = 9.8

LH2_rho_kg_m3 = 71
LOX_rho_kg_m3 = 1140
RP1_rho_kg_m3 = 820
LCH4_rho_kg_m3 = 423
Solid_rho_kg_m3 = 1680
N2O4_rho_kg_m3 = 1442
UDMH_rho_kg_m3 = 791


def calculate_stage_masses(
    delta_v_1: float, #specified delta-v for first stage (m/s)
    delta_1: float, #inert mass fraction of stage 1
    delta_2: float, #inert mass fraction of stage2
    isp_1: float, #stage 1 isp(sea level) (sec)
    isp_2: float, #stage 2 isp(vacuum) (sec)
    # check TrueConstants.py
    delta_v_total: float, #total delta v, m/s, M1 NOTE: Might want to update dvtot, mpl, and g0 from being defined here to accessing a shared file where we store all constants
    m_pl: float, #payload mass, M2
    g0: float  #g0 (m/s^2) NOTE: lecture provides 9.8 but using higher precision value here might be desirable
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
):

    all_results = sweep_delta_v( #sweep across all delta_v for specified prop combo
        propellant1=propellant1,
        propellant2=propellant2,
        delta_v_total=delta_v_total,
        delta_v1_min=delta_v1_min,
        m_pl=m_pl,
        g0=g0,
        dv_step=5 #just 5 m/s steps for now(can reduce later)
    )

    valid_results=[]

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


def stage_cost(stage_m_in: float):
    cost_nre = 13.52 * stage_m_in**0.55
    return cost_nre


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




# TESTING

# ============================================================
# MAIN PROGRAM
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Select propellant combination
    # --------------------------------------------------------
    propellant1 = LOX_LH2       # First stage
    propellant2 = LOX_LH2       # Second stage

    # --------------------------------------------------------
    # Mission inputs
    # --------------------------------------------------------
    delta_v_total = mission_delV_ms
    m_pl = pyld_mass_kg
    g0_value = g0

    # Minimum allowable first-stage delta-v
    delta_v1_min = 1000  # m/s

    # --------------------------------------------------------
    # Find minimum-mass solution
    # --------------------------------------------------------
    optimal = sweep_delta_v(
        propellant1=propellant1,
        propellant2=propellant2,
        delta_v_total=delta_v_total,
        delta_v1_min=delta_v1_min,
        m_pl=m_pl,
        g0=g0_value,
        dv_step=5
    )

    optimal_mass = min_mass_finder(
        propellant1=propellant1,
        propellant2=propellant2,
        delta_v_total=delta_v_total,
        delta_v1_min=delta_v1_min,
        m_pl=m_pl,
        g0=g0_value,
    )

    optimal_cost = min_cost_finder(
        propellant1=propellant1,
        propellant2=propellant2,
        delta_v_total=delta_v_total,
        delta_v1_min=delta_v1_min,
        m_pl=m_pl,
        g0=g0_value,
        dv_step=5
    )

    print("optimal mass")
    print(optimal_mass)

    print("optimal cost")
    print(optimal_cost)
    # --------------------------------------------------------
    # Print results
    # --------------------------------------------------------
    print("\n========================================")
    print("      TWO-STAGE ROCKET MASS ANALYSIS")
    print("========================================")

    # Save the array to a text file
    np.savetxt("optimal_results.txt", optimal, fmt="%s", header="Optimal Rocket Mass Results")
    print("Results saved to optimal_results.txt")
