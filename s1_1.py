import math

#FUNCTION calculate_stage_mass():
#Date Created: 9/16/2026
#Author: Henry Rowley
#Note: isp_1 MUST be sea level isp, isp_2 MUST be vacuum isp


def calculate_stage_masses(
    dV_1: float, #specified delta-v for first stage (m/s)
    delta_1: float, #inert mass fraction of stage 1
    delta_2: float, #inert mass fraction of stage2
    isp_1: float, #stage 1 isp(sea level) (sec)
    isp_2: float, #stage 2 isp(vacuum) (sec)
    dV_tot: float = 12300.0, #total delta v, m/s, M1 NOTE: Might want to update dvtot, mpl, and g_0 from being defined here to accessing a shared file where we store all constants
    m_pl: float = 26000.0, #payload mass, M2
    g_0:float = 9.8 #g_0 (m/s^2) NOTE: lecture provides 9.8 but using higher precision value here might be desirable
):
    dV_2 = dV_tot - dV_1 

    #calculate exhaust velocity of each stage
    Ve_1 = g_0 * isp_1
    Ve_2 = g_0 * isp_2

    #calculate mass ratios using alternate form of rocket equation
    r_1 = math.exp(-dV_1/Ve_1)
    r_2 = math.exp(-dV_2/Ve_2)

    #calculate payload fractions using parametric mass ratio r
    lambda_1 = r_1 - delta_1
    lambda_2 = r_2 - delta_2

    #check feasibility and pass error if applicable
    error = [lambda_1 <= 0, lambda_2 <=0] #NOTE: error is a list of two booleans, gets output and can be used when sweeping through dV_1 values to know which values are invalid
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
