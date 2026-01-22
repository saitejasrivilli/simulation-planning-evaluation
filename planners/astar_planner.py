import heapq
import numpy as np
from planners.base_planner import BasePlanner


class AStarPlanner(BasePlanner):
    """
    Grid-based A* planner with obstacle avoidance.
    Plans a path, then follows it using a simple controller.
    """

    def __init__(self, config=None):
        super().__init__(config)
        self.grid_size = 0.5

        # IMPORTANT: these are GRID bounds, not world bounds
        # World [-10, 10] => Grid [-20, 20]
        self.world_bounds = (-20, 20)

        self.path = []
        self.current_wp_idx = 0
        self.replan_interval = 5   # replan every N steps
        self.step_counter = 0


    def reset(self):
        self.path = []
        self.current_wp_idx = 0
        self.step_counter = 0

    def act(self, state):
        position = state["position"]
        goal = state["goal"]

        self.step_counter += 1

        vec_to_goal = goal - position
        dist_to_goal = np.linalg.norm(vec_to_goal)

        # Stop only when environment would terminate
        if dist_to_goal <= 0.5:
            return np.zeros(2)

        # Replan periodically using noisy observations
        if (not self.path) or (self.step_counter % self.replan_interval == 0):
            self.path = self._plan_path(state)
            self.current_wp_idx = 0

        # Fallback if planning fails
        if not self.path:
            return vec_to_goal / (dist_to_goal + 1e-6)

        if self.current_wp_idx >= len(self.path):
            return vec_to_goal / max(dist_to_goal, 1.0)

        target = self.path[self.current_wp_idx]
        direction = target - position
        dist = np.linalg.norm(direction)

        if dist < 0.5:
            self.current_wp_idx += 1

        # Proportional control
        return direction / max(dist, 1.0)

    # ---------------- A* core ----------------

    def _plan_path(self, state):
        start = self._to_grid(state["position"])
        goal = self._to_grid(state["goal"])

        obstacle = None
        if "obstacle_center" in state:
            obstacle = self._to_grid(state["obstacle_center"])

        open_set = []
        heapq.heappush(open_set, (0, start))

        came_from = {}
        g_score = {start: 0}

        while open_set:
            _, current = heapq.heappop(open_set)

            if current == goal:
                return self._reconstruct_path(came_from, current)

            for neighbor in self._neighbors(current):
                if obstacle and neighbor == obstacle:
                    continue

                tentative_g = g_score[current] + 1

                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + self._heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f, neighbor))

        return []

    def _neighbors(self, node):
        x, y = node
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        neighbors = []

        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if self.world_bounds[0] <= nx <= self.world_bounds[1] and \
               self.world_bounds[0] <= ny <= self.world_bounds[1]:
                neighbors.append((nx, ny))

        return neighbors

    def _heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _to_grid(self, pos):
        return (
            int(round(pos[0] / self.grid_size)),
            int(round(pos[1] / self.grid_size))
        )

    def _from_grid(self, node):
        return np.array(
            [node[0] * self.grid_size, node[1] * self.grid_size],
            dtype=np.float32
        )

    def _reconstruct_path(self, came_from, current):
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return [self._from_grid(p) for p in path]
