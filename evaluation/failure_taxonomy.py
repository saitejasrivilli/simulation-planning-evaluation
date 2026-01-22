def classify_failure(metric, max_steps):
    """
    Classify episode outcome into interpretable failure modes
    based on evaluation-level metrics.
    """

    if metric["collision"]:
        if metric["steps"] < 0.3 * max_steps:
            return "CollisionEarly"
        else:
            return "CollisionLate"

    if not metric["goal_reached"]:
        # Near-goal oscillation vs no progress
        if metric.get("distance_to_goal", float("inf")) < 1.0:
            return "OscillationNearGoal"
        return "TimeoutNoProgress"

    return "Success"
