import numpy as np
import matplotlib.pyplot as plt

from experiments.run_batch import run_batch
from planners.rule_based_planner import RuleBasedPlanner

if __name__ == "__main__":
    metrics = run_batch(RuleBasedPlanner, num_episodes=500, seed=0)

    collision_dists = [
        m["collision_distance"]
        for m in metrics
        if m["collision"] and m["collision_distance"] is not None
    ]

    if len(collision_dists) == 0:
        raise RuntimeError("No collision distances found. Check evaluator propagation.")

    collision_dists = np.array(collision_dists)

    plt.hist(collision_dists, bins=30)
    plt.xlabel("Collision distance")
    plt.ylabel("Count")
    plt.title(
        f"Collision Distance Distribution\n"
        f"(mean={collision_dists.mean():.3f}, std={collision_dists.std():.3f})"
    )
    plt.tight_layout()
    plt.savefig("analysis/collision_distance_hist.png")
    print(
        f"Saved collision distance histogram "
        f"(mean={collision_dists.mean():.3f}, std={collision_dists.std():.3f})"
    )
