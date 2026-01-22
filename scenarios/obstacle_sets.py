import numpy as np

def single_obstacle():
    return [
        {"center": np.array([0.0, 0.0]), "radius": 1.0}
    ]


def corridor():
    return [
        {"center": np.array([0.0, 1.2]), "radius": 1.0},
        {"center": np.array([0.0, -1.2]), "radius": 1.0}
    ]
import numpy as np

def narrow_corridor():
    return [
        {"center": np.array([0.0, 1.0]), "radius": 0.65},
        {"center": np.array([0.0, -1.0]), "radius": 0.65},
    ]
