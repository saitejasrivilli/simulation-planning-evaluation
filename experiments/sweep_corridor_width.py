# experiments/sweep_corridor_width.py
import numpy as np
from simulator.environment import Environment
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from evaluation.evaluator import Evaluator

def run_sweep(planner_cls, gap_widths, episodes=200, return_metrics=False):
    evaluator = Evaluator()
    results = []

    for gap in gap_widths:
        env = Environment(
            scenario_name="corridor",
            scenario_kwargs={"gap_width": gap}
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
        if return_metrics:
            results.append(metrics)
        else:
            results.append((gap, collision_rate))

    return results


if __name__ == "__main__":
    gap_widths = np.linspace(1.2, 0.1, 12)

    for name, planner in {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner,
    }.items():
        results = run_sweep(planner, gap_widths)

        print(f"\n{name} Corridor Sweep")
        for gap, rate in results:
            print(f"gap={gap:.2f} | collision_rate={rate:.2f}")
