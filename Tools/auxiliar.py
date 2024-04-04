# If you need import libraries it's the site.

def mean_temperature(inlet_temperature:float, outlet_temperature:float)->int:
    """Calculate the mean temperature."""
    return round((inlet_temperature + outlet_temperature) / 2)

def print_properties(substance:str, properties:list[float], mean_temperature:int):
    """Print properties of a substance."""
    labels = ['Density', 'Cp', 'Viscosity', 'Thermal conductivity']
    units = ['lbm/ft^3', 'Btu/lbm*°F', 'lbm/ft*s', 'Btu/h*ft*°F']
    print(f'{substance} properties at {mean_temperature}°F & @1atm:')
    for label, value, unit in zip(labels, properties, units):
        print(f"{label}: {value} {unit}")

def c_prime_shell_and_pipe(pitch:float, int_diameter:float, thickness:float)->float:
    """Calculate the c prime value for a shell and pipe exchanger.

    Args:
        pitch (float): Pitch value.
        int_diameter (float): Internal diameter in inches.
        thickness (float): Thickness value in inches.

    Returns:
        float: C' value.
    """
    return pitch - (int_diameter + 2*thickness)

def shell_area(int_diam_shell:float, c_prime:float, baffles_distance:float, pitch:float)->float:
    return int_diam_shell * c_prime * baffles_distance / pitch * 144