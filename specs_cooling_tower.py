from dataclasses import dataclass
from math import ceil

@dataclass
class Water():
    __volume_circulation: int = 320 # m3/h
    __inlet_temperature: int = 30 # °C
    __outlet_temperature: int = 25 # °C
    __inlet_enthalpy: float = 104.9 # kJ/kg
    __outlet_enthalpy: float = 125.8 # kJ/kg
    __mass_density: int = 1000
    __heat_capacity_isobaric: float = 4.186

    @property
    def volume_circulation(self):
        return self.__volume_circulation
    
    @property
    def inlet_temperature(self):
        return self.__inlet_temperature
    
    @property
    def outlet_temperature(self):
        return self.__outlet_temperature
    
    @property
    def inlet_enthalpy(self):
        return self.__inlet_enthalpy
    
    @property
    def outlet_enthalpy(self):
        return self.__outlet_enthalpy
    
    @property
    def mass_density(self):
        return self.__mass_density
    
    @property
    def heat_capacity_isobaric(self):
        return self.__heat_capacity_isobaric
    
    def intlet_temperature_fahrenheit(self):
        return (self.__inlet_temperature * (9 / 5)) + 32
    
    def outlet_temperature_fahrenheit(self):
        return (self.__outlet_temperature * (9 / 5)) + 32

@dataclass
class Air():
    __inlet_temperature: int = 25 # °C
    __outlet_temperature: int = 28 # °C
    __intlet_enthalpy: float = 65 # kJ/kg
    __outlet_enthalpy: float = 75 # kJ/kg 
    __inlet_specific_humidity: float = 0.016
    __outlet_specific_humidity: float = 0.019
    __inlet_specific_volume: float = 0.8605
    __outlet_specific_volume: float = 0.88

    @property
    def inlet_temperature(self):
        return self.__inlet_temperature

    @property
    def outlet_temperature(self):
        return self.__outlet_temperature

    @property
    def intlet_enthalpy(self):
        return self.__intlet_enthalpy

    @property
    def outlet_enthalpy(self):
        return self.__outlet_enthalpy

    @property
    def inlet_specific_humidity(self):
        return self.__inlet_specific_humidity

    @property
    def outlet_specific_humidity(self):
        return self.__outlet_specific_humidity

    @property
    def inlet_specific_volume(self):
        return self.__inlet_specific_volume

    @property
    def outlet_specific_volume(self):
        return self.__outlet_specific_volume

@dataclass
class Technical():
    __relative_humidity: float = 0.8
    __allowable_evaporating_losses: float = 0.0144
    __wet_bulb_temperature: int = 22

    @property
    def relative_humidity(self):
        return self.__relative_humidity
    
    @property
    def allowable_evaporating_losses(self):
        return self.__allowable_evaporating_losses
    
    @property
    def wet_bulb_temperature(self):
        return self.__wet_bulb_temperature

def blow_down_losses(WL:float, EL:float, DL:float)->float:
    M = sum([WL, EL, DL])
    COC = M / (M - EL)
    return EL / (COC - 1)

def tower_dimensions(cooling_tower_chart:float, L:float, Ka:float)->float:
    Ka = Ka * 0.47 / 100
    Z = ceil((cooling_tower_chart * L) / Ka)
    B = 88.89 / L
    fill_volume = B * Z

    return Z, B, fill_volume