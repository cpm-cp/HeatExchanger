import numpy as np
from fractions import Fraction
from tables import double_pipe_data, pipe_shell_data

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

def flow_area(config:str, exchanger_type:str, bwg: int|None = None, pipe_arrangement: str = None)->list[float]:
    """Choice diameters config for heat exchanger as double pipe and pipe and shell.

    Args:
        config (str): double-pipe: '2*1-1/4', '3*2' or '4*3'.
        pipe-shell: '1/2', '3/4' or '1'.
        exchanger_type (str): exchanger type: 'double pipe' or 'pipe and shell'.
        bwg (int | None): bwg value.
        pipe_arrangement (str): Pipe arrangement for pipe-shell: 'square' or 'triangle'.

    Returns:
        list[float]: Parameteres for the selected exchanger and selected config.
    """
    if exchanger_type == 'double pipe':
        if config in ['2*1-1/4', '3*2', '4*3']:
            options = double_pipe_data
            diameter, int_diameter, ext_diameter, flow_area, lin_surface =  [value if key == 'linear_suf' else value / 12 for key, value in options[config].items()]
            equivalent_diam = (ext_diameter**2 - int_diameter**2) / int_diameter
            annulus_area = np.pi * (ext_diameter**2 - int_diameter**2) / 4
            pipe_area = np.pi * diameter**2 / 4
            return (equivalent_diam, annulus_area, pipe_area)
        
    elif exchanger_type == 'pipe and shell':
        if config in ['1/2', '3/4', '1']:
            options = pipe_shell_data
            specific_dict =  filter(lambda aux: aux['BWG'] == bwg, options[config])
            thickness, int_diameter, flow_area, lin_surf = [list(d.values())[1:] for d in specific_dict][0]
            ext_diameter = float(Fraction(config))

    else:
        return []

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

def lmtd(exchanger_type: str, config: str, T_hot_in: float, T_hot_out: float, T_cold_in: float, T_cold_out: float) -> float:
    """Calculate the Logarithmic Mean Temperature Difference (LMTD) and apply correction factor if needed.
    
    Parameters:
    - exchanger_type: The type of heat exchanger ('double pipe' or 'pipe and shell').
    - config: The configuration of flow ('parallel' or 'counter-current').
    - T_hot_in: Temperature of the hot fluid entering the heat exchanger.
    - T_hot_out: Temperature of the hot fluid exiting the heat exchanger.
    - T_cold_in: Temperature of the cold fluid entering the heat exchanger.
    - T_cold_out: Temperature of the cold fluid exiting the heat exchanger.
    
    Returns:
    - The LMTD value, corrected if applicable for the heat exchanger type.
    
    Raises:
    - ValueError: If an unsupported configuration or exchanger type is provided.
    """
    config = config.lower()
    exchanger_type = exchanger_type.lower()

    # Calculate temperature differences based on flow configuration
    delta_t1, delta_t2 = (T_hot_out - T_cold_out, T_hot_in - T_cold_in) if config == 'parallel' else \
    (T_hot_out - T_cold_in, T_hot_in - T_cold_out) if config == 'counter-current' else \
    (None, None)

    if delta_t1 is None or delta_t2 is None:
        raise ValueError(f'Unsupported configuration: {config}')
    
    lmtd_value = (delta_t2 - delta_t1) / np.log(delta_t2 / delta_t1)

    if exchanger_type == 'double pipe':
        return lmtd_value
    elif exchanger_type == 'pipe and shell':
        R = (T_hot_in - T_hot_out) / (T_cold_out - T_cold_in)
        S = (T_cold_out - T_cold_in) / (T_hot_in - T_hot_out)
        numerator = (np.sqrt(R**2 + 1) * np.log((1-S)/(1-R*S)))
        denominator = ((R-1) * np.log((2-S*(R+1-np.sqrt(R**2 + 1)))/(2-S*(R+1+np.sqrt(R**2 + 1)))))
        F = numerator / denominator
        return lmtd_value * F
    else:
        raise ValueError(f'Unsupported exchanger type: {exchanger_type}')

def calculate_area(heat_flow:float, U:float, delta_T_log:float)->float:
    """Calculate the required heat exchanger area."""
    return heat_flow / (U * delta_T_log)

def calculate_length(area:float, linear_surface:float)->float:
    """Calculate the required length given area and linear density."""
    return area / linear_surface

def numb_forks(length:float, fork_legth_arm:float=20):
    """Calculate the number of passes based on length and pass length."""
    return np.ceil(length / (fork_legth_arm * 2))

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