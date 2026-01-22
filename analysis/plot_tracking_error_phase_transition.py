import numpy as np
import matplotlib.pyplot as plt

from experiments.sweep_tracking_error import run_sweep
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner


def plot_phase_transition():
    noise_levels = np.linspace(0.0, 0.6, 7)

    planners = {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner,
    }

    plt.figure()

    for name, planner_cls in planners.items():
        results = run_sweep(planner_cls, noise_levels)

        noises = [r["noise"] for r in results]
        collision_rates = [r["collision_rate"] for r in results]

        plt.plot(noises, collision_rates, marker="o", label=name)

    plt.xlabel("Tracking Noise Std")
    plt.ylabel("Collision Rate")
    plt.title("Planning–Control Mismatch Phase Transition")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()

    plt.savefig("figures/tracking_error_phase_transition.png")
    plt.close()

    print("Saved tracking error phase transition plot")


if __name__ == "__main__":
    plot_phase_transition()
