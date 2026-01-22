import numpy as np

from collections import Counter
from evaluation.failure_taxonomy import classify_failure
from collections import Counter

def failure_breakdown(metrics, max_steps):
    modes = []
    for m in metrics:
        mode = classify_failure(m, max_steps)
        modes.append(mode)
    return Counter(modes)

def failure_breakdown(metrics, max_steps):
    """
    Aggregate failure modes across episodes.
    """
    modes = []

    for m in metrics:
        mode = classify_failure(m, max_steps)
        modes.append(mode)

    return Counter(modes)


def risk_summary(metrics):
    """
    Compute distributional and tail-risk statistics.

    Args:
        metrics: list of dicts with keys:
            - collision (bool)
            - goal_reached (bool)
            - steps (int)

    Returns:
        dict of risk-aware statistics
    """
    steps = np.array([m["steps"] for m in metrics])
    collisions = np.array([m["collision"] for m in metrics])
    successes = np.array([m["goal_reached"] for m in metrics])

    summary = {
        # Basic rates
        "collision_rate": collisions.mean(),
        "success_rate": successes.mean(),

        # Distributional statistics
        "mean_steps": steps.mean(),
        "median_steps": np.median(steps),
        "p90_steps": np.percentile(steps, 90),
        "p95_steps": np.percentile(steps, 95),
        "max_steps": steps.max(),

        # Conditional risk
        "mean_steps_given_failure": (
            steps[~successes].mean() if (~successes).any() else 0.0
        ),
        "collision_given_failure": (
            collisions[~successes].mean() if (~successes).any() else 0.0
        ),
    }

    return summary
