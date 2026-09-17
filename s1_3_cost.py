#Date Created: 9/17/2026
#Author: Henry Rowley


import math


def stage_cost(stage_m_in: float):
    cost_nre = 13.52 * stage_m_in**0.55
    return cost_nre