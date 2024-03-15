import numpy as np
from math import ceil, log, exp

def mean_temperature(inlet_temperature:float, outlet_temperature:float)->int:
    """Calculate the mean temperature."""
    return round((inlet_temperature + outlet_temperature) / 2)

def print_properties(substance:str, properties:list[float], mean_temperature:int):
    """Print properties of a substance."""
    labels = ['Density', 'Cp', 'Viscosity', 'Thermal conductivity']
    units = ['lbm/ft^3', 'Btu/lbm*°F', 'lbm/ft*s', 'Btu/h*ft*°F']
    print(f'{substance} properties at {mean_temperature}°F & @1atm:')
    for label, value, unit in zip(labels, properties, units):
        print(f"{label}: {value} {unit}")

def calculate_nusselt(Reynold:float, Prandtl:float)->float:
    """Calculate the Nusselt number based on Reynold and Prandtl numbers."""
    if Reynold <= 0:
        raise ValueError("Reynold's number must be greater than zero.")
    conditions = [
        ((0.4, 4), (0.989, 0.330)),
        ((4, 40), (0.911, 0.385)),
        ((40, 4000), (0.683, 0.466)),
        ((4000, 40000), (0.193, 0.618)),
        ((40000, float('inf')), (0.027, 0.805)),
    ]
    for (low, high), (coef, exp) in conditions:
        if low <= Reynold < high:
            return coef * Reynold**exp * Prandtl**(1/3)
    return 0  # Default return if none of the conditions match

def config_diameters(config:str)->list[float]:
    """Choice diameters config.

    Args:
        config (str): '2*1-1/4' or '3*2' or '4*3'

    Returns:
        list[float]: [Diameter, Diameter_1 , Diameter_2, Flow_area, Linear_surface]
    """
    options = {
        '2*1-1/4': {'D':1.380,'DE': 1.66, 'DI': 3.35, 'flow_area': 1.50, 'linear_suf': 0.435},
        '3*2': {'D':2.067,'DE': 2.38, 'DI': 3.068, 'flow_area': 3.35, 'linear_suf': 0.622},
        '4*3': {'D':3.068,'DE': 3.50, 'DI': 4.026, 'flow_area': 7.38, 'linear_suf': 0.917}
    }
    if config in options:
        return [value if key == 'linear_suf' else value / 12 for key, value in options[config].items()]
    else:
        return []

def flow_area(diameter:float, external_diam:float, internal_diam:float)->tuple[float]:
    """flow area parameters.

    Args:
        external_diam (float): External diamter.
        internal_diam (float): Internal diamater.

    Returns:
        tuple[float]: (equivalent_diam, annulus_area, pipe_area)
    """
    equivalent_diam = (external_diam**2 - internal_diam**2) / internal_diam
    annulus_area = np.pi * (external_diam**2 - internal_diam**2) / 4
    pipe_area = np.pi * diameter**2 / 4
    return (equivalent_diam, annulus_area, pipe_area)

def mass_velocity(mass_flow_rate:float, area:float)->float:
    """mass velocity.

    Args:
        mass_flow_rate (float): mass flow rate in lb/h
        area (float): area in ft^2

    Returns:
        float: mass velocity in lb/h*ft2
    """
    return mass_flow_rate / area

def Reynolds(diamter:float, mass_vel:float, viscosity:float)->float:
    """Reynolds number.

    Args:
        diamter (float): diamter in ft
        mass_vel (float): mass velocity in lb/h*ft^2
        viscosity (float): viscosity in lb/ft*h

    Returns:
        float: Dimensionaless Reynold number.
    """
    return diamter * mass_vel / viscosity

def Prandtl(specific_heat:float, viscosity:float, conductivity:float)->float:
    """Calculate the dimensionaless Prandtl

    Args:
        specific_heat (float): specific heat in Btu/lb*°F
        viscosity (float): viscosity in lb/h*ft
        conductivity (float): thermal conductivity in Btu/h*ft*°F

    Returns:
        float: Adimensional Prandtl number.
    """
    return specific_heat * viscosity / conductivity

def convective_coeff(Nusselt:float, thermal_conductivity:float, diameter:float)->float:
    """Calculate the convective heat transfer coefficient."""
    return Nusselt * thermal_conductivity / diameter

def corrected_inside_coeff(convective_coeff:float, diameters:list[float, float])->float:
    """Correct the inside heat transfer coefficient for diameter differences."""
    return convective_coeff * (min(diameters) / max(diameters))

def clean_total_coeff(h_i0:float, h_0:float)->float:
    return (h_i0 * h_0) / (h_i0 + h_0)

def total_coefficient(U_c:float, fouling_factor:float=0)->float:
    """Calculate the total heat transfer coefficient, optionally including fouling."""
    return 1 / ((1 / U_c) + (fouling_factor * 2))

def lmtd(config:str, T_hot_inner:float, T_hot_out:float, T_cold_inner:float, T_cold_out:float)->float:
    """Calculate the Logarithmic Mean Temperature Difference."""
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

def calculate_area(heat_flow:float, U:float, delta_T_log:float)->float:
    """Calculate the required heat exchanger area."""
    return heat_flow / (U * delta_T_log)

def calculate_length(area:float, linear_surface:float)->float:
    """Calculate the required length given area and linear density."""
    return area / linear_surface

def numb_forks(length:float, fork_legth_arm:float=20):
    """Calculate the number of passes based on length and pass length."""
    return ceil(length / (fork_legth_arm * 2))

def corrected_length(numbs_fork, total_pass_length=40):
    """Calculate the corrected length based on the number of passes."""
    return numbs_fork * total_pass_length

def corrected_surface(length:float, linear_surface:float)->float:
    """Calculate the corrected surface area."""
    return length * linear_surface

def corrected_desing_coeff(heat_flow:float, area:float, mean_log_T:float)->float:
    """Calculate the corrected desing coefficent.

    Args:
        heat_flow (float): heat flow in Btu/h
        area (float): area in ft^2
        mean_log_T (float): log mean temperature difference

    Returns:
        float: Corrected desing coeff
    """
    return heat_flow / (area * mean_log_T)

def recalculate_reynolds(D_outer, D_inner, mass_flow_rate, viscosity):
    """Recalculate the Reynolds number based on diameter difference and flow properties."""
    D_effective = D_outer - D_inner
    return (D_effective * mass_flow_rate) / viscosity

def friction_factor(Reynolds):
    """Calculate the friction factor based on Reynolds number."""
    return 0.0035 + 0.264 / Reynolds ** 0.42

def Fanning_factor(friction_factor, mass_flow, length, density, D_effective):
    """Calculate the pressure drop."""
    return (4 * friction_factor * mass_flow**2 * length) / (2 * 4.18e8 * density**2 * D_effective)

def pressure_drop_4_velocity(mass_flow:float, density:float)->float:
    """Calculate the pressure drop for velocity effect."""
    return mass_flow / (3600 * density)

def inn_and_out_drops(V_drop:float)->float:
    """Calculate the inner and outer drops."""
    return 3 * (V_drop**2 / 2 * 32.2)

def pressure_drop(fanning_factor:float, in_out_drop:float, density:float)->float:
    """Calculate the pressure drop."""
    return (fanning_factor + in_out_drop) * density / 144

def C_value(mass_flow_rate:float, Cp_value:float)->float:
    """Calculate the calorific capacity."""
    return mass_flow_rate * Cp_value

def c_minimum(c_values:tuple[float])->float:
    return min(c_values)

def c_to_NTU(C_values:list[float, float])->float:
    """Calculate the c values for the NTU efecivity method."""
    return min(C_values) / max(C_values)

def NTU(U_d:float, A_s:float, c_NTU:float)->float:
    """Calculate the NTU (Number of Thermal Units) value."""
    return U_d * A_s / c_NTU

def exchanger_efectivity(config:str, C_NTU:float, NTU_value:float)->float:
    """Calculathe the efectivy by heat exchanger."""
    config = config.lower()
    if config == 'parallel':
        return (1-np.exp(-NTU_value * (1 + C_NTU))) / (1 + C_NTU)
    elif config == 'counter-current':
        return (1-np.exp(-NTU_value * (1 - C_NTU))) / (1 - C_NTU * np.exp(-NTU_value * (1 - C_NTU)))
    else:
        print(f'Config not found.')