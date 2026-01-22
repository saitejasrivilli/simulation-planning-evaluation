import numpy as np

from simulator.environment import Environment
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from evaluation.evaluator import Evaluator


def run_batch(planner_cls, num_episodes=500, seed=0):
    rng = np.random.default_rng(seed)

    env = Environment()
    planner = planner_cls()
    evaluator = Evaluator()

    all_metrics = []

    for _ in range(num_episodes):
        state = env.reset()
        planner.reset()

        done = False
        info = {}

        while not done:
            action = planner.act(state)
            state, _, done, info = env.step(action)

        metrics = evaluator.evaluate_episode(info)
        all_metrics.append(metrics)

    return all_metrics


def summarize(metrics):
    total = len(metrics)
    collisions = sum(m["collision"] for m in metrics)
    successes = sum(m["goal_reached"] for m in metrics)
    avg_steps = np.mean([m["steps"] for m in metrics])

    return {
        "collision_rate": collisions / total,
        "success_rate": successes / total,
        "avg_steps": avg_steps
    }


if __name__ == "__main__":
    planners = {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner
    }

    results = {}

    for name, planner_cls in planners.items():
        metrics = run_batch(planner_cls)
        results[name] = summarize(metrics)

    print("\nPlanner Comparison Results")
    print("-" * 40)
    for name, res in results.items():
        print(f"{name:12s} | "
              f"Collision: {res['collision_rate']:.2f} | "
              f"Success: {res['success_rate']:.2f} | "
              f"Avg Steps: {res['avg_steps']:.1f}")
