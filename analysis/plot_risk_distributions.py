import numpy as np
import matplotlib.pyplot as plt

from experiments.run_batch import run_batch
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner


def plot_distributions(name, metrics):
    steps = np.array([m["steps"] for m in metrics])
    successes = np.array([m["goal_reached"] for m in metrics])

    # ---------- Histogram ----------
    plt.figure()
    plt.hist(steps, bins=30, alpha=0.7)
    plt.xlabel("Steps")
    plt.ylabel("Count")
    plt.title(f"{name}: Steps Distribution")
    plt.tight_layout()
    plt.savefig(f"analysis/{name}_steps_hist.png")
    plt.close()

    # ---------- CDF (Tail Risk) ----------
    plt.figure()
    sorted_steps = np.sort(steps)
    cdf = np.arange(1, len(sorted_steps) + 1) / len(sorted_steps)
    plt.plot(sorted_steps, cdf)
    plt.xlabel("Steps")
    plt.ylabel("CDF")
    plt.title(f"{name}: Steps CDF (Tail Behavior)")
    plt.tight_layout()
    plt.savefig(f"analysis/{name}_steps_cdf.png")
    plt.close()

    # ---------- Failure-conditioned ----------
    if (~successes).any():
        plt.figure()
        plt.hist(steps[~successes], bins=20, alpha=0.7)
        plt.xlabel("Steps (Failure Only)")
        plt.ylabel("Count")
        plt.title(f"{name}: Steps Given Failure")
        plt.tight_layout()
        plt.savefig(f"analysis/{name}_failure_steps.png")
        plt.close()


if __name__ == "__main__":
    planners = {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner
    }

    for name, planner_cls in planners.items():
        metrics = run_batch(
            planner_cls,
            num_episodes=500,
            seed=42
        )
        plot_distributions(name, metrics)

    print("Saved risk distribution plots to analysis/")
