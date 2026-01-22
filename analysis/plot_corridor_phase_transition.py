import numpy as np
import matplotlib.pyplot as plt
from experiments.sweep_corridor_width import run_sweep
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner


def plot_phase_transition():
    gap_widths = np.linspace(1.2, 0.1, 12)

    plt.figure(figsize=(8, 5))

    for name, planner_cls in {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner,
    }.items():
        results = run_sweep(planner_cls, gap_widths)
        gaps, collision_rates = zip(*results)

        # Sort by gap width for plotting
        gaps = np.array(gaps)
        collision_rates = np.array(collision_rates)
        order = np.argsort(gaps)

        plt.plot(
            gaps[order],
            collision_rates[order],
            marker="o",
            label=name,
        )

    # --- Failure boundary (the key insight) ---
    plt.axvline(
        x=0.35,
        color="red",
        linestyle="--",
        alpha=0.7,
        label="Feasibility boundary",
    )

    plt.xlabel("Corridor Gap Width")
    plt.ylabel("Collision Rate")
    plt.title("Phase Transition: Geometry vs Planning")

    plt.ylim(-0.05, 1.05)
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig("figures/corridor_phase_transition.png")
    plt.show()


if __name__ == "__main__":
    plot_phase_transition()
