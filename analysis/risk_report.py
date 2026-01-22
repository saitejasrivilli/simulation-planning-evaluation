from experiments.run_batch import run_batch
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from analysis.failure_analysis import risk_summary


def print_report(name, summary):
    print(f"\n{name} Risk Report")
    print("-" * 30)
    for k, v in summary.items():
        if isinstance(v, float):
            print(f"{k:30s}: {v:.3f}")
        else:
            print(f"{k:30s}: {v}")


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

        summary = risk_summary(metrics)
        print_report(name, summary)
