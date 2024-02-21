from WebScrap.web_scrap import get_water_thermophysic_info
import numpy as np

def mean_temperature(inlet_temperature: float, outlet_temperature: float) -> float:
    return round((inlet_temperature + outlet_temperature) / 2)

def print_properties(sustance: str, data: tuple , mean_T:int) -> None:
    info = np.array(['Density', 'Viscosity', 'Thermal conductivity'])
    units = np.array(['kg/m3', 'Pa*s', 'W/m*K'])
    print(f'{sustance} properties {mean_T}K & @1atm:')
    for (index, prop), unit in zip(enumerate(data), units):
        print(info[index], ":", prop, unit)