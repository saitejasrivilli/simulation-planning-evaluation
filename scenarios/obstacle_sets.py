import numpy as np

def corridor(gap_width=0.6):
    """
    Two circular obstacles forming a corridor.
    gap_width controls the free space between them.
    """
    radius = 0.8
    offset = radius + gap_width / 2.0

    obstacles = [
        {"center": np.array([0.0,  offset]), "radius": radius},
        {"center": np.array([0.0, -offset]), "radius": radius},
    ]
    return obstacles


def single_obstacle():
    return [
        {"center": np.array([0.0, 0.0]), "radius": 0.8}
    ]


def narrow_corridor():
    return [
        {"center": np.array([0.0, 1.0]), "radius": 0.65},
        {"center": np.array([0.0, -1.0]), "radius": 0.65},
    ]
