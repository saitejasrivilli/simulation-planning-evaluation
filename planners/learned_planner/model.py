import torch
import torch.nn as nn


class MLPPolicy(nn.Module):
    """
    Simple feedforward policy network for behavior cloning.

    Input:  state vector (8,)
    Output: action vector (2,)
    """

    def __init__(self, state_dim=8, action_dim=2, hidden_dim=128):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(state_dim, hidden_dim),
            nn.ReLU(),

            nn.Linear(hidden_dim, hidden_dim),
            nn.ReLU(),

            nn.Linear(hidden_dim, action_dim),
            nn.Tanh()  # actions are clipped to [-1, 1]
        )

    def forward(self, state):
        """
        Args:
            state: Tensor of shape (B, state_dim)

        Returns:
            action: Tensor of shape (B, action_dim)
        """
        return self.net(state)
