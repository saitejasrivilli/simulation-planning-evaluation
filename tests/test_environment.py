import numpy as np
from simulator.environment import Environment


def test_environment_reset():
    env = Environment()
    state = env.reset()
    assert "position" in state
    assert "goal" in state


def test_environment_step_runs():
    env = Environment()
    state = env.reset()
    action = np.zeros(2)
    state, reward, done, info = env.step(action)
    assert isinstance(done, bool)
    assert "collision" in info
