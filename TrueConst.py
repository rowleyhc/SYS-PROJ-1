# Author: Jacob Harmon
# Date: 9/16/2026

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

mission_delV_ms = 12.3
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
