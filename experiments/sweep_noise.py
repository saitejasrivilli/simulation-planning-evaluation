from experiments.run_batch import run_batch, summarize
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner
from simulator.environment import Environment

# Observation noise levels (meters)
noise_levels = [0.0, 0.2, 0.5, 1.0, 1.5, 2.0]

planners = {
    "RuleBased": RuleBasedPlanner,
    "AStar": AStarPlanner
}

for noise in noise_levels:
    print(f"\nObservation noise std = {noise}")

    for name, planner_cls in planners.items():
        # Create environment with observation noise
        env = Environment()
        env.obs_noise_std = noise

        metrics = run_batch(
            planner_cls,
            num_episodes=300,
            seed=42
        )

        summary = summarize(metrics)

        print(
            f"{name:10s} | "
            f"Collision: {summary['collision_rate']:.2f} | "
            f"Success: {summary['success_rate']:.2f}"
        )
