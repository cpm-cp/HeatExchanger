from specs_cooling_tower import (
    Water, Air, Technical,
    blow_down_losses, tower_dimensions
)
import numpy as np

water = Water()
air = Air()
technical = Technical()
air_flow_rate = 100 # lb/h

cta = water.outlet_temperature - technical.wet_bulb_temperature
ctr = water.inlet_temperature - water.outlet_temperature
mass_water_in_cooling = water.volume_circulation * water.mass_density
heat_loss_water = mass_water_in_cooling * water.heat_capacity_isobaric * (
    water.inlet_temperature - water.outlet_temperature
)
volume_required_air = (heat_loss_water * air.inlet_specific_volume) / (
    (air.outlet_enthalpy - air.intlet_enthalpy) - 
    (air.outlet_specific_humidity - air.inlet_specific_humidity) * 
    water.heat_capacity_isobaric * air.inlet_temperature
)
mass_air_required = volume_required_air / air.inlet_specific_volume
make_up_water = ((volume_required_air * (air.outlet_specific_humidity - air.inlet_specific_humidity)) / 
                 air.outlet_specific_volume) * (1 + technical.allowable_evaporating_losses)
make_up_water /= 60 # h to min
effectiveness_cooling_tower = ctr / (cta + ctr)

# Losses in cooling tower:
drift_losses = 0.2 * mass_water_in_cooling / 100
windage_losses = 0.005 * mass_water_in_cooling
evaporating_losses = (0.01 * mass_water_in_cooling * (water.intlet_temperature_fahrenheit() - water.outlet_temperature_fahrenheit())) / 10
blow_down_loss = blow_down_losses(windage_losses, evaporating_losses, drift_losses)

# Structural design:
cooling_tower_charact = cta * np.mean([0.0909, 0.08696, 0.08333, 0.08, 0.0667, 0.06897])
Z, B, fill_volume = tower_dimensions(cooling_tower_charact, 3.55, air_flow_rate)

# Results by calculous:
print(f"cta: {cta} °C")
print(f"ctr: {ctr} °C")
print(f"mass_water_in_cooling: {mass_water_in_cooling:.4f} kg/h")
print(f"heat_loss_water: {heat_loss_water:.4f} kJ/h")
print(f"volume_required_air: {volume_required_air:.4f} m^3/h")
print(f"mass_air_required: {mass_air_required:.4f} kg/h")
print(f"make_up_water: {make_up_water:.4f} kg/min")
print(f"effectiveness_cooling_tower: {effectiveness_cooling_tower * 100}%")
print(f"drift_losses: {drift_losses:.4f} kg/h")
print(f"windage_losses: {windage_losses:.4f} kg/h")
print(f"evaporating_losses: {evaporating_losses:.4f} kg/h")
print(f"blow_down_loss: {blow_down_loss:.4f} kg/h")
print(f"cooling_tower_charact: {cooling_tower_charact:.4f} kg_air/kg_water")
print(f"Z: {Z} m")
print(f"B: {B:.4f} m^2")
print(f"fill_volume: {fill_volume:.4f} m^3")