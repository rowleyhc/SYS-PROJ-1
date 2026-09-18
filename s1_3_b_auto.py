#Date Created: 9/17/2026
#Author: Henry Rowley
#Wrapper for sweep to calculate NRE

import math
from s1_sweep import sweep_delta_v
from s1_3_cost import stage_cost

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
        dv_step=dv_step
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