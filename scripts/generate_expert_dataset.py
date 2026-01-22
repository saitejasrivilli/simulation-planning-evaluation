import os
import pickle
import numpy as np
from tqdm import tqdm

from simulator.environment import Environment
from planners.astar_planner import AStarPlanner


OUTPUT_DIR = "data/processed"
OUTPUT_FILE = "expert_astar.pkl"

NUM_EPISODES = 1000
MAX_STEPS = 300


def flatten_state(state):
    """
    Convert structured state dict into a flat numeric vector.
    Robust to missing fields.
    """
    obstacle = state.get("obstacle_center", np.zeros(2, dtype=np.float32))

    return np.concatenate([
        state["position"],
        state["velocity"],
        state["goal"],
        obstacle
    ]).astype(np.float32)



def collect_expert_data():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    env = Environment()
    planner = AStarPlanner()

    states = []
    actions = []

    for _ in tqdm(range(NUM_EPISODES), desc="Collecting expert rollouts"):
        state = env.reset()
        planner.reset()

        for _ in range(MAX_STEPS):
            action = planner.act(state)

            states.append(flatten_state(state))
            actions.append(action.copy())

            state, _, done, _ = env.step(action)
            if done:
                break

    dataset = {
        "states": np.array(states, dtype=np.float32),
        "actions": np.array(actions, dtype=np.float32),
    }

    output_path = os.path.join(OUTPUT_DIR, OUTPUT_FILE)
    with open(output_path, "wb") as f:
        pickle.dump(dataset, f)

    print(f"Saved expert dataset to {output_path}")
    print(f"Total samples: {len(states)}")


if __name__ == "__main__":
    collect_expert_data()
