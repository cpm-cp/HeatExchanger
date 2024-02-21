from WebScrap.web_scrap import get_water_thermophysic_info
from Tools.tools import mean_temperature, print_properties
import numpy as np

# Water values
sustance_1:str = 'water'
low_water_T:float = 300.91 # K
high_water_T:float = 315.99 # K
water_T_props = mean_temperature(inlet_temperature=low_water_T,outlet_temperature=high_water_T)
water_rho, water_K, water_mu = get_water_thermophysic_info(mean_Temperature=water_T_props)
water_data = np.array([water_rho, water_K, water_mu])

# Acetoen values
acetone_density:float = 743.83 # kg/m3
acetone_conductivity:float = 0.13955 # W/m*K
acetone_viscosity:float = 0.37786 # cP;  1 cP = 0.001 Pa*s
acetone_viscosity *= 0.001 # Pa*s
low_acetone_T:float = 353.43 # K
high_acetone_T:float = 366.41 # K
acetone_T_props = mean_temperature(inlet_temperature=high_acetone_T, outlet_temperature=low_acetone_T)




