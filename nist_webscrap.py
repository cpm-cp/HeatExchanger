from WebScrap.web_scrap import get_water_thermophysic_info
from Tools.tools import mean_temperature, print_properties
import numpy as np

# Water values
sustance_1:str = 'water'
low_water_T:float = 81.986 # °F
high_water_T:float = 109.112 # °F
water_T_props = mean_temperature(inlet_temperature=low_water_T,outlet_temperature=high_water_T)
water_density, water_Cp, water_viscosity, water_conductivity = get_water_thermophysic_info(mean_Temperature=water_T_props)
water_data = (water_density, water_Cp, water_viscosity, water_conductivity)
print_properties('water', water_data, water_T_props)

# Acetoen values
acetone_density:float = 743.83 # kg/m3
acetone_conductivity:float = 0.13955 # W/m*K
acetone_viscosity:float = 0.37786 # cP;  1 cP = 0.001 Pa*s
acetone_viscosity *= 0.001 # Pa*s
low_acetone_T:float = 176.504 # °F
high_acetone_T:float = 199.868 # °F
acetone_T_props = mean_temperature(inlet_temperature=high_acetone_T, outlet_temperature=low_acetone_T)