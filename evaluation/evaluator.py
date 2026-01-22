from evaluation.metrics.safety import collision_occurred
from evaluation.metrics.task_success import goal_reached, steps_to_termination


class Evaluator:
    """
    Computes evaluation metrics for a single episode.
    """

    def evaluate_episode(self, info):
        metrics = {
            "collision": collision_occurred(info),
            "goal_reached": goal_reached(info),
            "steps": steps_to_termination(info)
        }
        return metrics
