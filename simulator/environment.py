import numpy as np


class Environment:
    def __init__(self, config=None):
        self.dt = 0.1
        self.max_speed = 1.0
        self.max_steps = 300

        self.agent_radius = 0.2
        self.goal_tolerance = 0.5

        self.reset()

    def reset(self):
        # Agent state
        self.position = np.array([-4.0, 0.0])
        self.velocity = np.zeros(2)

        # Goal
        self.goal = np.array([4.0, 0.0])

        # Obstacles (support multiple)
        self.obstacles = [
            {"center": np.array([0.0, 0.9]), "radius": 0.8},
            {"center": np.array([0.0, -0.9]), "radius": 0.8},
        ]

        # Episode bookkeeping
        self.steps = 0
        self.done = False
        self.collision = False
        self.reached_goal = False

        return self._get_state()

    def step(self, action):
        """
        Advance simulation by one timestep.

        Args:
            action: np.array of shape (2,) representing acceleration

        Returns:
            state, reward, done, info
        """
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

        # --- Collision check (multi-obstacle) ---
        for obs in self.obstacles:
            dist = np.linalg.norm(self.position - obs["center"])
            if dist <= (self.agent_radius + obs["radius"]):
                self.collision = True
                self.done = True
                break

        # --- Goal check ---
        dist_to_goal = np.linalg.norm(self.position - self.goal)
        if dist_to_goal <= self.goal_tolerance:
            self.reached_goal = True
            self.done = True

        # --- Timeout ---
        if self.steps >= self.max_steps:
            self.done = True

        reward = 0.0  # evaluation-first design

        info = {
            "collision": self.collision,
            "reached_goal": self.reached_goal,
            "steps": self.steps,
            "distance_to_goal": dist_to_goal,
        }

        return self._get_state(), reward, self.done, info

    def _get_state(self):
        """
        Return planner-observable state.
        """
        return {
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "goal": self.goal.copy(),
            "obstacles": self.obstacles,  # NEW: expose full obstacle list
        }
