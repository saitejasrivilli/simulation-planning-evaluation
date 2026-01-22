import numpy as np
from simulator.environment import Environment
from planners.rule_based_planner import RuleBasedPlanner
from planners.astar_planner import AStarPlanner


def test_rule_based_planner_runs():
    env = Environment()
    planner = RuleBasedPlanner()
    state = env.reset()
    action = planner.act(state)
    assert action.shape == (2,)


def test_astar_planner_runs():
    env = Environment()
    planner = AStarPlanner()
    state = env.reset()
    action = planner.act(state)
    assert action.shape == (2,)
