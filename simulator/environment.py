import numpy as np
from scenarios.scenario_generator import generate


class Environment:
    def __init__(self, scenario_name="single", scenario_kwargs=None):
        # Simulation parameters
        self.dt = 0.1
        self.max_speed = 1.0
        self.max_steps = 300

        # Geometry
        self.agent_radius = 0.2
        self.goal_tolerance = 0.5

        # Scenario config
        self.scenario_name = scenario_name
        self.scenario_kwargs = scenario_kwargs or {}

        self.reset()

    def reset(self):
        # Agent state
        self.position = np.array([-4.0, 0.0])
        self.velocity = np.zeros(2)

        # Goal
        self.goal = np.array([4.0, 0.0])

        # Obstacles (from scenario generator)
        self.obstacles = generate(self.scenario_name, **self.scenario_kwargs)

        # Episode bookkeeping
        self.steps = 0
        self.done = False
        self.collision = False
        self.reached_goal = False
        self.collision_dist = None

        return self._get_state()

    def step(self, action):
        if self.done:
            raise RuntimeError("Episode already finished. Call reset().")

        action = np.clip(action, -1.0, 1.0)

        # Update velocity
        self.velocity += action * self.dt
        speed = np.linalg.norm(self.velocity)
        if speed > self.max_speed:
            self.velocity = self.velocity / speed * self.max_speed

        # Update position
        self.position += self.velocity * self.dt
        self.steps += 1

        # --- Collision check ---
        for obs in self.obstacles:
            dist = np.linalg.norm(self.position - obs["center"])
            if dist <= (self.agent_radius + obs["radius"]):
                self.collision = True
                self.done = True
                self.collision_dist = dist
                break

        # --- Goal check ---
        dist_to_goal = np.linalg.norm(self.position - self.goal)
        if dist_to_goal <= self.goal_tolerance:
            self.reached_goal = True
            self.done = True

        # --- Timeout ---
        if self.steps >= self.max_steps:
            self.done = True

        info = {
            "collision": self.collision,
            "reached_goal": self.reached_goal,
            "steps": self.steps,
            "distance_to_goal": dist_to_goal,
            "collision_distance": self.collision_dist,
        }

        return self._get_state(), 0.0, self.done, info

    def _get_state(self):
        return {
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "goal": self.goal.copy(),
            "obstacles": self.obstacles,
        }
