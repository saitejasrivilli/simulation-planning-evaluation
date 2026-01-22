import numpy as np
from simulator.environment import Environment
from planners.rule_based_planner import RuleBasedPlanner

env = Environment()
planner = RuleBasedPlanner()

state = env.reset()
planner.reset()

done = False

while not done:
    action = planner.act(state)
    state, reward, done, info = env.step(action)

print("Episode finished")
print("Collision:", info["collision"])
print("Reached goal:", info["reached_goal"])
print("Steps:", info["steps"])
from evaluation.evaluator import Evaluator

evaluator = Evaluator()
metrics = evaluator.evaluate_episode(info)

print("Episode finished")
print(metrics)
