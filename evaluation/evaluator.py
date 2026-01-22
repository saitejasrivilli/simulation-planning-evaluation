from evaluation.metrics.safety import collision_occurred
from evaluation.metrics.task_success import goal_reached, steps_to_termination


class Evaluator:
    def evaluate_episode(self, info):
        return {
            "collision": info["collision"],
            "goal_reached": info["reached_goal"],
            "steps": info["steps"],
            "collision_distance": info.get("collision_distance"),
        }
