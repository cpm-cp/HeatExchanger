double_pipe_data = {
            '2*1-1/4': {'D':1.380,'DE': 1.66, 'DI': 3.35, 'flow_area': 1.50, 'linear_suf': 0.435},
            '3*2': {'D':2.067,'DE': 2.38, 'DI': 3.068, 'flow_area': 3.35, 'linear_suf': 0.622},
            '4*3': {'D':3.068,'DE': 3.50, 'DI': 4.026, 'flow_area': 7.38, 'linear_suf': 0.917}
        }

pipe_shell_data = {
            '1/2': [
                {'BWG': 12, 'delta': 0.109, 'DI': 0.282, 'flow_area': 0.0625, 'lin_surf': 0.1309},
                {'BWG': 14, 'delta': 0.083, 'DI': 0.334, 'flow_area': 0.0876, 'lin_surf': 0.1309},
                {'BWG': 16, 'delta': 0.065, 'DI': 0.370, 'flow_area': 0.1076, 'lin_surf': 0.1309},
                {'BWG': 20, 'delta': 0.035, 'DI': 0.430, 'flow_area': 0.145, 'lin_surf': 0.1309}
            ],
            '3/4': [
                {'BWG': 10, 'delta': 0.134, 'DI': 0.482, 'flow_area': 0.182, 'lin_surf': 0.1963},
                {'BWG': 11, 'delta': 0.120, 'DI': 0.510, 'flow_area': 0.204, 'lin_surf': 0.1963},
                {'BWG': 12, 'delta': 0.109, 'DI': 0.532, 'flow_area': 0.223, 'lin_surf': 0.1963},
                {'BWG': 13, 'delta': 0.095, 'DI': 0.560, 'flow_area': 0.247, 'lin_surf': 0.1963},
                {'BWG': 14, 'delta': 0.083, 'DI': 0.584, 'flow_area': 0.268, 'lin_surf': 0.1963},
                {'BWG': 15, 'delta': 0.072, 'DI': 0.606, 'flow_area': 0.289, 'lin_surf': 0.1963},
                {'BWG': 16, 'delta': 0.065, 'DI': 0.620, 'flow_area': 0.302, 'lin_surf': 0.1963},
                {'BWG': 17, 'delta': 0.058, 'DI': 0.634, 'flow_area': 0.314, 'lin_surf': 0.1963},
                {'BWG': 18, 'delta': 0.049, 'DI': 0.652, 'flow_area': 0.334, 'lin_surf': 0.1963}
            ],
            '1': [
                {'BWG': 8, 'delta': 0.165, 'DI':0.670, 'flow_area':0.355, 'lin_surf': 0.2618},
                {'BWG': 9, 'delta': 0.148, 'DI':0.704, 'flow_area':0.389, 'lin_surf': 0.2618},
                {'BWG': 10, 'delta': 0.134, 'DI': 0.732, 'flow_area': 0.421, 'lin_surf': 0.2618},
                {'BWG': 11, 'delta': 0.120, 'DI': 0.760, 'flow_area': 0.455, 'lin_surf': 0.2618},
                {'BWG': 12, 'delta': 0.105, 'DI': 0.762, 'flow_area': 0.478, 'lin_surf': 0.2618},
                {'BWG': 13, 'delta': 0.095, 'DI': 0.810, 'flow_area': 0.515, 'lin_surf': 0.2618},
                {'BWG': 14, 'delta': 0.083, 'DI': 0.834, 'flow_area': 0.546, 'lin_surf': 0.2618},
                {'BWG': 15, 'delta': 0.072, 'DI': 0.856, 'flow_area': 0.576, 'lin_surf': 0.2618},
                {'BWG': 16, 'delta': 0.065, 'DI': 0.870, 'flow_area': 0.594, 'lin_surf': 0.2618}
            ]
        }

pipe_and_shell_pitch_data = {
    "square": {
        "Tube Diameter": {
            "in": [3/4, 1, 1 + 1/4, 1 + 1/2],
            "mm": [19, 25, 32, 39]
        },
        "Pitch": {
            "in": [1, 1 + 1/4, 1 + 9/16, 1 + 7/8],
            "mm": [25, 32, 40, 48]
        }
    },
    "triangle": {
        "Tube Diameter": {
            "in": [3/4, 1, 1 + 1/4, 1 + 1/2],
            "mm": [19, 25, 32, 39]
        },
        "Pitch": {
            "in": [1, 1 + 1/4, 1 + 9/16, 1 + 7/8],
            "mm": [25, 32, 40, 48]
        }
    }
}