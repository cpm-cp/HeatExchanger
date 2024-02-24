from WebScrap.web_scrap import get_water_thermophysic_info
import numpy as np
from math import ceil

def mean_temperature(inlet_temperature: float, outlet_temperature: float) -> float:
    # 
    return round((inlet_temperature + outlet_temperature) / 2)

def print_properties(sustance: str, data: tuple , mean_T:int) -> None:
    info = np.array(['Density', 'Cp', 'Viscosity', 'Thermal conductivity'])
    units = np.array(['lbm/ft^3', 'Btu/lbm*°F', 'lbm/ft*s', 'Btu/h*ft*°F'])
    print(f'{sustance} properties {mean_T}°F & @1atm:')
    for (index, prop), unit in zip(enumerate(data), units):
        print(info[index], ":", prop, unit)

def Nusselt_calc(Reynold:float, Prandtl:float) -> float:
    if Reynold > 0:
        if 0.4 <= Reynold < 4:
            nusselt_ = 0.989 * Reynold**0.330 * Prandtl**1/3
        elif 4 <= Reynold < 40:
            nusselt_ = 0.911 * Reynold**0.385 * Prandtl**1/3
        elif 40 <= Reynold < 4000:
            nusselt_ = 0.683 * Reynold**0.466 * Prandtl**1/3
        elif 4000 <= Reynold < 40000:
            nusselt_ = 0.193 * Reynold**0.618 * Prandtl**1/3
        else:
            nusselt_ = 0.027 * Reynold**0.805 * Prandtl**1/3
        return nusselt_
    else:
        print("Reynold's number must be greater than zero.")

def convective_coeff(Nusselt:float, thermal_conductivity:float, diameter:float) -> float:
    return (Nusselt * thermal_conductivity) / diameter

def corrected_inside_coeff(convective_coeff_:float, diameter:float, diameter_1:float) -> float:
    if diameter > diameter_1:
        return convective_coeff_ * (diameter / diameter_1)
    else:
        print('diameter_1 greater than diameter.')

def total_clean_coeff(h_i0:float, h_0:float) -> float:
    return (h_i0 * h_0) / (h_i0 + h_0)

def total_design_coeff(U_C:float, fouling_value:float = 0.001) -> float:
    return (1 / ((1 / U_C) + (fouling_value * 2)))

def LMTD(config:str ,T_hot_inner:int, T_hot_out:int, T_cold_inner:int, T_cold_out:int) -> float:
    config = config.lower()
    if config == 'parallel':
        Delta_T2 = (T_hot_inner - T_cold_inner)
        Delta_T1 = (T_hot_out - T_cold_out)
    elif config == 'counter-current':
        Delta_T2 = (T_hot_inner - T_cold_out)
        Delta_T1 = (T_hot_out - T_cold_inner)
    else:
        print('Out of bounds config.')
    return (Delta_T2 - Delta_T1) / np.log(Delta_T2 / Delta_T1)
    

def required_area(heat_flow:float, U_D:float, mean_log_T:float) -> float:
    return heat_flow / (U_D * mean_log_T)

def required_legth(A_r:float, lineal_surface:float) -> float:
    return A_r / lineal_surface

def number_of_forks(L_r:float, fork_legth_arm:float = 20) -> int:
    return ceil(L_r / (fork_legth_arm * 2))

def corrected_legth(numb_fork:int, total_legth_fork:float = 40) -> float:
    return numb_fork * total_legth_fork

def corrected_surface(L_c:float, lineal_surface:float) -> float:
    return L_c * lineal_surface

def corrected_design_coeff(heat_flow:float, A_c:float, mean_log_T:float)->float:
    return heat_flow / (A_c * mean_log_T)

def corrected_encrustment_factor(U_c:float, U_dc:float)->float:
    return (U_c - U_dc) / (U_c * U_dc)   

def recalc_Reynold(D_2:float, D_1:float, mass_flow_rate:float, viscosity:float)->float:
    D_ec = D_2 - D_1
    return (D_ec * mass_flow_rate) / viscosity

def f_a(Reynold_number:float)->float:
   return (0.0035 + (0.264/Reynold_number**0.42))

def Fanning_factor(f_a:float, mass_flow:float, L_c:float, density:float, D_ec:float)->float:
    return (
        (4 * f_a * mass_flow**2 * L_c)/(2 * 4.18e8 * density**2 * D_ec)
    )

def drop_pressure_4_velocity(mass_flow:float, density:float)->float:
    return mass_flow / (3600 * density)

def inner_and_out_drops(V_drop:float)->float:
    return 3 * (V_drop**2 / 2 * 32.2)

def pressure_drop(Delta_Fa:float, F_l:float, density:float)->float:
    return (Delta_Fa + F_l) * density / 144

def Q_max(mass_flow_A:float, mass_flow_B:float, Cp_A:float, Cp_B:float, T_hot_inner:float, T_cold_out:float):
    C_a = mass_flow_A * Cp_A
    C_b = mass_flow_B * Cp_B

    if C_a > C_b:
        return C_b * (T_hot_inner - T_cold_out)
    else:
        return C_a * (T_hot_inner - T_cold_out)
    
def NTU(U_d:float, A_s:float, C_min:float)->float:
    return U_d * A_s / C_min

def C_to_NTU(C_values:list[float])->float:
    if C_values[0] < C_values[1]:
        return C_values[0] / C_values[1]
    else:
        return C_values[1] / C_values[0]

def exchanger_efectivity(config:str, C_NTU:float, NTU_value:float)->float:
    config = config.lower()
    if config == 'parallel':
        return (1-np.exp(-NTU_value * (1 + C_NTU))) / (1 + C_NTU)
    elif config == 'counter-current':
        return (1-np.exp(-NTU_value * (1 - C_NTU))) / (1 - C_NTU * np.exp(-NTU_value * (1 - C_NTU)))
    else:
        print(f'Config not found.')