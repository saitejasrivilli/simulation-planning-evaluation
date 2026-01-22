import numpy as np
import matplotlib.pyplot as plt

from experiments.sweep_corridor_width import run_sweep
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner


def plot_collision_distance_vs_gap():
    gap_widths = np.linspace(1.2, 0.1, 12)

    plt.figure()

    for name, planner_cls in {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner,
    }.items():

        mean_dists = []

        for gap in gap_widths:
            results = run_sweep(
                planner_cls,
                [gap],
                episodes=200,
                return_metrics=True,   # important
            )[0]

            collision_dists = [
                m["collision_distance"]
                for m in results
                if m["collision"] and m["collision_distance"] is not None
            ]

            if len(collision_dists) == 0:
                mean_dists.append(np.nan)
            else:
                mean_dists.append(np.mean(collision_dists))

        plt.plot(gap_widths, mean_dists, marker="o", label=name)

    plt.xlabel("Corridor Gap Width")
    plt.ylabel("Mean Collision Distance")
    plt.title("Collision Proximity vs Corridor Width")
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.savefig("figures/collision_distance_vs_gap.png")
    plt.show()


if __name__ == "__main__":
    plot_collision_distance_vs_gap()
