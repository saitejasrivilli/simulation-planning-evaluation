from experiments.run_batch import run_batch
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from analysis.failure_analysis import failure_breakdown


if __name__ == "__main__":
    planners = {
        "RuleBased": RuleBasedPlanner,
        "AStar": AStarPlanner,
    }

    for name, planner_cls in planners.items():
        metrics = run_batch(planner_cls, num_episodes=500, seed=42)
        breakdown = failure_breakdown(metrics, max_steps=300)

        print(f"\n{name} Failure Breakdown")
        for k, v in breakdown.items():
            print(f"{k:25s}: {v}")
