import numpy as np
import torch

from planners.base_planner import BasePlanner
from planners.learned_planner.model import MLPPolicy


CHECKPOINT_PATH = "data/processed/checkpoints/mlp_policy.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def flatten_state(state):
    """
    Convert structured environment state to flat vector.
    Must match dataset generation exactly.
    """
    obstacle = state.get("obstacle_center", np.zeros(2, dtype=np.float32))

    return np.concatenate([
        state["position"],
        state["velocity"],
        state["goal"],
        obstacle
    ]).astype(np.float32)


class LearnedPlanner(BasePlanner):
    """
    Learned planner using behavior cloning from A* demonstrations.
    """

    def __init__(self, config=None):
        super().__init__(config)

        self.model = MLPPolicy()
        self.model.load_state_dict(
            torch.load(CHECKPOINT_PATH, map_location=DEVICE)
        )
        self.model.to(DEVICE)
        self.model.eval()

    def reset(self):
        """
        No internal state to reset for feedforward policy.
        """
        pass

    @torch.no_grad()
    def act(self, state):
        state_vec = flatten_state(state)
        state_tensor = torch.from_numpy(state_vec).unsqueeze(0).to(DEVICE)

        # Learned direction
        action = self.model(state_tensor).cpu().numpy()[0]

        # --- Goal-aware proportional control ---
        pos = state["position"]
        goal = state["goal"]
        direction = goal - pos
        dist = np.linalg.norm(direction)

        # Stop if close enough
        if dist < 0.6:
            return np.zeros(2)

        direction = direction / (dist + 1e-6)

        # Blend learned action with goal direction
        action = 0.5 * action + 0.5 * direction

        # Scale up to overcome velocity integration
        action = 1.5 * action

        return np.clip(action, -1.0, 1.0)
