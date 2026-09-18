#Date Created: 9/16/2026
#Author: Henry Rowley
#Wrapper 


import math
from s1_sweep import sweep_delta_v

def min_mass_finder(
        propellant1: dict,
        propellant2: dict,
        delta_v_total:float,
        delta_v1_min: float,
        m_pl: float,
        g0: float,
        dv_step: float
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