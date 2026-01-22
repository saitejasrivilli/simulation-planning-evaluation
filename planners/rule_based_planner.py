import numpy as np
from planners.base_planner import BasePlanner


class RuleBasedPlanner(BasePlanner):
    """
    Simple planner that drives straight toward the goal.
    """

    def __init__(self, config=None):
        super().__init__(config)

    def reset(self):
        pass

    def act(self, state):
        position = state["position"]
        goal = state["goal"]

        direction = goal - position
        norm = np.linalg.norm(direction)

        if norm > 1e-5:
            direction = direction / norm
        else:
            direction = np.zeros_like(direction)

        # Simple proportional controller
        action = 1.0 * direction
        return action
