from evaluation.evaluator import Evaluator


def test_evaluator_output():
    evaluator = Evaluator()
    info = {
        "collision": False,
        "reached_goal": True,
        "steps": 10
    }
    metrics = evaluator.evaluate_episode(info)
    assert "collision" in metrics
    assert "goal_reached" in metrics
