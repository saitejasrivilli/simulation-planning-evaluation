def build_single_obstacle(center, radius):
    return {
        "center": center,
        "radius": radius
    }


def build_corridor(left_center, right_center, radius):
    return [
        {"center": left_center, "radius": radius},
        {"center": right_center, "radius": radius}
    ]
