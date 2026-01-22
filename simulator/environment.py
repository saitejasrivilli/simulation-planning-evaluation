import numpy as np
from collections import deque
from scenarios.scenario_generator import generate


class Environment:
    def __init__(
        self,
        scenario_name="single",
        scenario_kwargs=None,
        control_noise=0.0,
        control_delay=0
    ):
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

        # --- NEW: execution realism ---
        self.control_noise = control_noise
        self.control_delay = control_delay
        self.action_buffer = deque(maxlen=control_delay + 1)

        self.reset()

    def reset(self):
        # Agent state
        self.position = np.array([-4.0, 0.0])
        self.velocity = np.zeros(2)

        # Goal
        self.goal = np.array([4.0, 0.0])

        # Obstacles
        self.obstacles = generate(self.scenario_name, **self.scenario_kwargs)

        # Episode bookkeeping
        self.steps = 0
        self.done = False
        self.collision = False
        self.reached_goal = False
        self.collision_dist = None

        # Reset action buffer
        self.action_buffer.clear()

        return self._get_state()

    def step(self, planned_action):
        if self.done:
            raise RuntimeError("Episode already finished. Call reset().")

        planned_action = np.clip(planned_action, -1.0, 1.0)

        # --- NEW: execution mismatch ---
        executed_action = self._apply_control_noise_and_delay(planned_action)

        # Update velocity using executed action
        self.velocity += executed_action * self.dt
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
            # Optional but useful
            "control_noise": self.control_noise,
            "control_delay": self.control_delay,
        }

        return self._get_state(), 0.0, self.done, info

    def _apply_control_noise_and_delay(self, action):
        """
        Models execution error: noise + delay.
        Planner is unaware of this.
        """
        noisy_action = action + np.random.normal(
            0.0, self.control_noise, size=action.shape
        )

        self.action_buffer.append(noisy_action)

        if self.control_delay > 0 and len(self.action_buffer) > self.control_delay:
            return self.action_buffer[0]

        return noisy_action

    def _get_state(self):
        return {
            "position": self.position.copy(),
            "velocity": self.velocity.copy(),
            "goal": self.goal.copy(),
            "obstacles": self.obstacles,
        }
