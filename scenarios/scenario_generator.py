from scenarios.obstacle_sets import single_obstacle, corridor

def generate(name="single", **kwargs):
    if name == "single":
        return single_obstacle()
    if name == "corridor":
        return corridor(**kwargs)
    raise ValueError(f"Unknown scenario: {name}")
