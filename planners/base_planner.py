from abc import ABC, abstractmethod


class BasePlanner(ABC):
    """
    Abstract base class for all planners.
    Ensures a common interface for evaluation.
    """

    def __init__(self, config=None):
        self.config = config

    @abstractmethod
    def reset(self):
        """
        Reset planner internal state between episodes.
        """
        pass

    @abstractmethod
    def act(self, state):
        """
        Given current state, return an action.

        Args:
            state (dict): environment state

        Returns:
            action (np.ndarray): shape (2,)
        """
        pass
