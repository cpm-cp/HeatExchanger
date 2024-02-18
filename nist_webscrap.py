from WebScrap.web_scrap import get_water_thermophysic_info
import numpy as np

start = np.array(get_water_thermophysic_info(low_temperature=360, high_temperature=360))
info = np.array(['Density', 'Volume', 'Viscosity', 'Thermal conductivity'])
units = np.array(['kg/m3', 'm3/kg', 'Pa*s', 'W/m*K'])

print('Water properties @360K & @1atm:')
for (index, prop), unit in zip(enumerate(start), units):
    print(info[index], ": ", prop, unit)


