
# Author: Jacob Harmon
# Date: 9/16/2026

import math

from s1_1 import calculate_stage_masses # imports definitions to calculate mass


def sweep_delta_v(               # takes in each given prop parameter
    propellant1: dict,
    propellant2: dict,
    delta_v_total: float,        # required total delV
    delta_v1_min: float,         # where we set the minimum delV that the first stage can have
    m_pl: float,                 # payload mass
    g0: float,    
    dv_step: float               # designated delV step
):

    results = []                                            # make the results array
    dv1 = delta_v1_min                                      # sets the first stage dV and adds 1 each loop until total dV
    while(dv1 < delta_v_total):
        sweep = calculate_stage_masses(                     # calls to get the masses for each dV step
            dV_1=dv1,
            delta_1=propellant1["inert_mass_fraction"],
            delta_2=propellant2["inert_mass_fraction"],
            isp_1=propellant1["isp_sea_level_s"],
            isp_2=propellant2["isp_vacuum_s"],
            dV_tot=delta_v_total,
            m_pl=m_pl,
            g_0=g0,
        )

        data = {                                            # compiles the data array for that dV composed of the masses
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

    return results                                          # returns the results
 



    
