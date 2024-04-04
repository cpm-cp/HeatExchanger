# Libraries
from icecream import ic
from Tools.general import *
from Tools.auxiliar import *
from Tools.tools import *

# Data:
# - Acetone
inlet_acetone_T:float = 163.868 # °F
outlet_acetone_T:float = 140.198 # °F
cp_acetone:float = 0.3438 # Btu/lb*°F
conductivity_acetone:float = 0.087 # Btu/lb*h*°F
density_acetone:float = 0.13 # lb/ft^3
viscosity_acetone:float = 0.0178 # lb/ft*h

# - Water
inlet_water_T:float = 81.968 # °F
oulet_water_T:float = 119.112 # °F
cp_water:float = 1.0097 # Btu/lb*°F
conductivity_water:float = 0.3616 # Btu/lb*h*°F
density_water:float = 62.38 # lb/ft3
viscosity_water:float = 1.7119 # lb/ft*h
mass_water_rate:float = 422.4975 # lb/h

# - Exchanger config
type_exchanger:str = 'pipe and shell'
flow_config:str = 'counter-current'
config:str = '1'
config_in_numb:float = Fraction(config) / 12 # ft
pipe_arrangement:str = 'square'
bwg:int = 13


# - Calculus
heat_flow_rate = heat_flow(mass_water_rate, cp_water, inlet_water_T, oulet_water_T)
mass_acetone_rate = flow_rate(heat_flow_rate, cp_acetone, inlet_acetone_T, outlet_acetone_T)
delta_T_log = lmtd(type_exchanger, flow_config, inlet_acetone_T, outlet_acetone_T, inlet_water_T, oulet_water_T)
thickness, pipe_diameter, eq_diameter, shell_area_, pipe_area, pitch, linear_surf = flow_area(config, type_exchanger, bwg, pipe_arrangement)
eq_diameter/= 12
pipe_diameter/= 12
shell_mass_velocity, pipe_mass_velocity = mass_velocity(mass_water_rate, shell_area_), mass_velocity(mass_acetone_rate, pipe_area)
pipe_flow_velocity = pipe_mass_velocity / 3600 * density_acetone
shell_reynold, pipe_reynold = reynolds(eq_diameter, shell_mass_velocity, viscosity_water), reynolds(pipe_diameter, pipe_mass_velocity, viscosity_acetone)
shell_prandtl, pipe_prandtl = Prandtl(cp_water, viscosity_water, conductivity_water), Prandtl(cp_acetone, viscosity_acetone, conductivity_acetone)
shell_conv_coeff, pipe_conv_coeff = convective_coeff(shell_reynold, shell_prandtl, conductivity_water, eq_diameter), convective_coeff(pipe_reynold, pipe_prandtl, conductivity_acetone, pipe_diameter)
corrected_pipe_conv_coeff = corrected_inside_coeff(pipe_conv_coeff, [config_in_numb, pipe_diameter])
u_C = clean_total_coeff(corrected_pipe_conv_coeff, shell_conv_coeff)

ic(u_C)
ic(delta_T_log)
ic(linear_surf)
ic(heat_flow_rate)