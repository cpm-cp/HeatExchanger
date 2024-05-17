import numpy as np

def real_heat(global_coeff:float, exchanger_area:float, lmtd:float)->float:
    return global_coeff * exchanger_area * lmtd

def exchanger_area(numb_pipes:int, length_pipe:float, ext_diameter:float)->float:
    lin_surface = np.pi * ext_diameter
    return numb_pipes * lin_surface * length_pipe

