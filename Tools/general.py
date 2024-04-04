# If you need import libraries it's the site.
import numpy as np

def heat_flow(mass_flow_rate:float, heat_capacity:float, inlet_temperature:float, outlet_temperature:float)->float:
    return mass_flow_rate * heat_capacity * abs(inlet_temperature - outlet_temperature)

def flow_rate(heat_flow:float, heat_capacity:float, inlet_temperature:float, outlet_temperature:float)->float:
    return heat_flow / (heat_capacity * abs(inlet_temperature - outlet_temperature))

def mass_velocity(mass_flow_rate:float, area:float)->float:
    """mass velocity.

    Args:
        mass_flow_rate (float): mass flow rate in lb/h
        area (float): area in ft^2

    Returns:
        float: mass velocity in lb/h*ft2
    """
    return mass_flow_rate / area

def reynolds(diamter:float, mass_vel:float, viscosity:float)->float:
    """reynolds number.

    Args:
        diamter (float): diamter in ft
        mass_vel (float): mass velocity in lb/h*ft^2
        viscosity (float): viscosity in lb/ft*h

    Returns:
        float: Dimensionaless Reynold number.
    """
    if (diamter and mass_vel and viscosity) > 0:
        return diamter * mass_vel / viscosity
    else:
        raise ValueError('Arguments must be positive values.')
    
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

def convective_coeff(Reynold:float, Prandtl:float, thermal_conductivity:float, diameter:float)->float:
    """Calculate the convective heat transfer coefficient."""
    Nusselt = calculate_nusselt(Reynold, Prandtl)
    return Nusselt * thermal_conductivity / diameter

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
        S = (T_cold_out - T_cold_in) / (T_hot_in - T_cold_in)
        numerator = (np.sqrt(R**2 + 1) * np.log((1-S)/(1-R*S)))
        denominator = ((R-1) * np.log((2-S*(R+1-np.sqrt(R**2 + 1)))/(2-S*(R+1+np.sqrt(R**2 + 1)))))
        F = numerator / denominator
        return lmtd_value * F
    else:
        raise ValueError(f'Unsupported exchanger type: {exchanger_type}')