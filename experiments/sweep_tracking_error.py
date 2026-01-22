# experiments/sweep_tracking_error.py

import numpy as np

from simulator.environment import Environment
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from evaluation.evaluator import Evaluator


def run_sweep(planner_cls, noise_levels, episodes=300):
    evaluator = Evaluator()
    results = []

    for noise in noise_levels:
        env = Environment(
            scenario_name="corridor",
            scenario_kwargs={"gap_width": 0.6},  # feasible geometry
            control_noise=noise,
            control_delay=0
        )

        planner = planner_cls()
        metrics = []

        for _ in range(episodes):
            state = env.reset()
            planner.reset()
            done = False
            info = {}

            while not done:
                action = planner.act(state)
                state, _, done, info = env.step(action)

            metrics.append(evaluator.evaluate_episode(info))

        collision_rate = np.mean([m["collision"] for m in metrics])
        success_rate = np.mean([m["goal_reached"] for m in metrics])

        results.append({
            "noise": noise,
            "collision_rate": collision_rate,
            "success_rate": success_rate
        })

    return results


if __name__ == "__main__":
    noise_levels = np.linspace(0.0, 0.6, 7)

    planners = {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner,
    }

    for name, planner_cls in planners.items():
        results = run_sweep(planner_cls, noise_levels)

        print(f"\n{name} Tracking Error Sweep")
        for r in results:
            print(
                f"noise={r['noise']:.2f} | "
                f"collision_rate={r['collision_rate']:.2f} | "
                f"success_rate={r['success_rate']:.2f}"
            )
