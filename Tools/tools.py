import numpy as np
from fractions import Fraction
from Tools.tables import double_pipe_data, pipe_shell_data, pipe_and_shell_pitch_data
from Tools.auxiliar import c_prime_shell_and_pipe



def flow_area(config:str, exchanger_type:str, bwg:int|None = None, pipe_arrangement:str = None)->list[float]:
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
            pitch = find_pitch(pipe_arrangement, ext_diameter)
            B:int = 5 # in
            c_prime = c_prime_shell_and_pipe(pitch, int_diameter, thickness)

            eq_diameter = 4 * (pitch**2 - np.pi * (Fraction(config)**2 / 4)) / np.pi * Fraction(config) if pipe_arrangement == 'square' else \
            4 * (1/2*pitch*0.86*pitch - 1/2 * np.pi * (Fraction(config)**2 / 4)) / 1/2 * np.pi * Fraction(config) if pipe_arrangement == 'triangle' else None
            shell_area = 21.25 * c_prime * B / (pitch * 144)
            pipe_area = (flow_area * 158) / (144 * 4)

            return (thickness, int_diameter, eq_diameter, shell_area, pipe_area, pitch, lin_surf)
    else:
        return []



def corrected_inside_coeff(convective_coeff:float, diameters:list[float, float])->float:
    """Correct the inside heat transfer coefficient for diameter differences."""
    return convective_coeff * (min(diameters) / max(diameters))

def clean_total_coeff(h_i0:float, h_0:float)->float:
    return (h_i0 * h_0) / (h_i0 + h_0)

def total_coefficient(U_c:float, fouling_factor:float=0)->float:
    """Calculate the total heat transfer coefficient, optionally including fouling."""
    return 1 / ((1 / U_c) + (fouling_factor * 2))


    
def find_pitch(array_type:str, diameter:float, unit:str="in", data:dict=pipe_and_shell_pitch_data)->float:
    """Search the pitch value for a specific array ttpe and pipe diameter.

    Args:
        array_type (str): "Square Array" or "Triangular Array".
        diameter (float): Pipe diameter in fractional or decimal.
        unit (str, optional): "in" or "mm". Defaults to "in".
        data (dict, optional): Storage data. Defaults to pipe_and_shell_pitch_data.

    Returns:
        float: Pitch value.
    """
    try:
        diameter_index = data[array_type]["Tube Diameter"][unit].index(diameter)
    except ValueError:
        return None

    pitch = data[array_type]["Pitch"][unit][diameter_index]

    return pitch


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
    """Recalculate the reynolds number based on diameter difference and flow properties."""
    D_effective = D_outer - D_inner
    return (D_effective * mass_flow_rate) / viscosity

def friction_factor(reynolds):
    """Calculate the friction factor based on reynolds number."""
    return 0.0035 + 0.264 / reynolds ** 0.42

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

def exchanger_efectivity(config:str, C_NTU:float, NTU_value:float)->float:
    """Calculathe the efectivy by heat exchanger."""
    config = config.lower()
    if config == 'parallel':
        return (1-np.exp(-NTU_value * (1 + C_NTU))) / (1 + C_NTU)
    elif config == 'counter-current':
        return (1-np.exp(-NTU_value * (1 - C_NTU))) / (1 - C_NTU * np.exp(-NTU_value * (1 - C_NTU)))
    else:
        print(f'Config not found.')