def goal_reached(info):
    """
    Returns 1 if goal was reached, else 0.
    """
    return int(info.get("reached_goal", False))


def steps_to_termination(info):
    """
    Number of steps taken in the episode.
    """
    return info.get("steps", 0)
