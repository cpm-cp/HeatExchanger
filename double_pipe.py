from WebScrap.web_scrap import get_water_thermophysic_info
from Tools.tools import *
import numpy as np

# Water values
sustance_1:str = 'water'
low_water_T:float = 81.986 # °F
high_water_T:float = 109.112 # °F
water_mass_flow:float = 169.999 # lb/h
water_T_props = mean_temperature(inlet_temperature=low_water_T,outlet_temperature=high_water_T)
water_density, water_Cp, water_viscosity, water_conductivity = get_water_thermophysic_info(mean_Temperature=water_T_props)
water_data = (water_density, water_Cp, water_viscosity, water_conductivity)
# print_properties('water', water_data, water_T_props)

# Acetoen values
acetone_density:float = 45.499 # lb/ft^3
acetone_conductivity:float = 8.0516e-2 # Btu/ft*h*°F
acetone_viscosity:float = 0.9148 # lb/ft*h
acetone_Cp:float = 0.55488 # Btu/lb*°F
low_acetone_T:float = 176.504 # °F
high_acetone_T:float = 199.868 # °F

# Pipe config:
config_diam = "3*2"
config_flow = "counter-current"

exchanger_type = 'double pipe'

heat_flow = water_mass_flow * water_Cp * (high_water_T - low_water_T) # Ideal heat transfer
acetone_mass_flow = heat_flow / (acetone_Cp  * (high_acetone_T - low_acetone_T))

log_mean_T = lmtd(config_flow, high_acetone_T, low_acetone_T, high_water_T, low_water_T)
diameter ,D_1, D_2, Flow_area, lin_surface = flow_area(config_diam, exchanger_type)

equivalent_diam, annulus_area, pipe_area = flow_area(diameter, D_2, D_1)

annulus_mass_velocity, pipe_mass_velocity = mass_velocity(water_mass_flow, annulus_area), mass_velocity(acetone_mass_flow, pipe_area)
annulus_Reynold, pipe_Reynold = Reynolds(equivalent_diam, annulus_mass_velocity, water_viscosity), Reynolds(diameter, pipe_mass_velocity, acetone_viscosity)
annulus_Prandtl, pipe_Prandtl = Prandtl(water_Cp, water_viscosity, water_conductivity), Prandtl(acetone_Cp, acetone_viscosity, acetone_conductivity)
annulus_Nusselt, pipe_Nusselt = calculate_nusselt(annulus_Reynold, annulus_Prandtl), calculate_nusselt(pipe_Reynold, pipe_Prandtl)
annulus_convective_coeff, pipe_convective_coeff = convective_coeff(annulus_Nusselt, water_conductivity, equivalent_diam), convective_coeff(pipe_Nusselt, acetone_conductivity, diameter)
corrected_pipe_conv_coeff = corrected_inside_coeff(pipe_convective_coeff, (diameter, D_1))
U_c = clean_total_coeff(corrected_pipe_conv_coeff, annulus_convective_coeff)
U_d = total_coefficient(U_c, 0.001)
required_area = calculate_area(heat_flow, U_d, log_mean_T)
required_length = calculate_length(required_area, lin_surface)
forks_number = numb_forks(required_length)
new_length = corrected_length(forks_number)
new_surface = corrected_surface(new_length, lin_surface)
U_dc = corrected_desing_coeff(heat_flow, new_surface, log_mean_T)
corrected_foulling_factor = (U_c - U_dc) / (U_c * U_dc)
corrected_annulus_Reynold = recalculate_reynolds(D_2, D_1, water_mass_flow, water_viscosity)
annulus_friction_factor = friction_factor(corrected_annulus_Reynold)
annulus_Fanning_factor = Fanning_factor(annulus_friction_factor, water_mass_flow, new_length, water_density, (D_2 - D_1))
drop_press_4_velocity = pressure_drop_4_velocity(water_mass_flow, water_density)
inn_and_out_losses = inn_and_out_drops(drop_press_4_velocity)
annulus_pressure_drop = pressure_drop(annulus_Fanning_factor, inn_and_out_losses, water_density)
pipe_friction_factor = friction_factor(pipe_Reynold)
pipe_Fanning_factor = Fanning_factor(pipe_friction_factor, acetone_mass_flow, new_length, acetone_density, diameter)
pipe_pressure_drop = (pipe_Fanning_factor) * acetone_density / 144
c_cold, c_hot = C_value(water_mass_flow, water_Cp), C_value(acetone_mass_flow, acetone_Cp)
c_ntu = c_to_NTU((c_cold, c_hot))
c_min = c_minimum((c_cold, c_hot))
numb_thermal_units = NTU(U_d, new_surface, c_min)
Q_max = c_min * (high_acetone_T - low_water_T)
effectivity = exchanger_efectivity(config_flow, c_ntu, numb_thermal_units)

print(f'The corrected length is: {new_length:.3f} ft')
print(f'The corrected area is: {new_surface:.3f} ft^2.')
print(f'The corrected desing coeff is: {U_dc:.3f} Btu/h*°F*ft^2.')
print(f'The corrected foulling factor is: {corrected_foulling_factor:.3f}')
print(f'The annulus drop pressure is: {annulus_pressure_drop:.6f} lb/in^2.')
print(f'The pipe drop pressure is: {pipe_pressure_drop:.6f} lb/in^2.')
print(f'The max heat transfer is: {Q_max:.3f} Btu/h')
print(f'The exchanger efectivity is: {(effectivity * 100):.5f}%')