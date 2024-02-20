from WebScrap.web_scrap import get_water_thermophysic_info
import numpy as np

water_temperature = 360
low_water_T = high_water_T = water_temperature
start = np.array(get_water_thermophysic_info(low_temperature=low_water_T, high_temperature=high_water_T))
info = np.array(['Density', 'Volume', 'Viscosity', 'Thermal conductivity'])
units = np.array(['kg/m3', 'm3/kg', 'Pa*s', 'W/m*K'])

print(f'Water properties {water_temperature}K & @1atm:')
for (index, prop), unit in zip(enumerate(start), units):
    print(info[index], ":", prop, unit)