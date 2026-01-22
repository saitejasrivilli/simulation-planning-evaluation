from experiments.run_batch import run_batch, summarize
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from simulator.environment import Environment

import json

noise_levels = [0.0, 0.2, 0.5, 1.0, 1.5, 2.0]

planners = {
    "RuleBased": RuleBasedPlanner,
    "AStar": AStarPlanner
}

results = {
    "noise_levels": noise_levels,
    "planners": {}
}

for name, planner_cls in planners.items():
    results["planners"][name] = {
        "collision_rate": [],
        "success_rate": []
    }

    for noise in noise_levels:
        env = Environment()
        env.obs_noise_std = noise

        metrics = run_batch(
            planner_cls,
            num_episodes=300,
            seed=42
        )

        summary = summarize(metrics)

        results["planners"][name]["collision_rate"].append(
            summary["collision_rate"]
        )
        results["planners"][name]["success_rate"].append(
            summary["success_rate"]
        )

# Save results
with open("analysis/robustness_results.json", "w") as f:
    json.dump(results, f, indent=2)

print("Saved results to analysis/robustness_results.json")
