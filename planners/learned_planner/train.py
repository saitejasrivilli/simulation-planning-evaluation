import os
import pickle
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

from planners.learned_planner.model import MLPPolicy


DATA_PATH = "data/processed/expert_astar.pkl"
CHECKPOINT_DIR = "data/processed/checkpoints"
CHECKPOINT_PATH = os.path.join(CHECKPOINT_DIR, "mlp_policy.pt")

BATCH_SIZE = 256
EPOCHS = 20
LEARNING_RATE = 1e-3
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


class ImitationDataset(Dataset):
    def __init__(self, states, actions):
        self.states = torch.from_numpy(states)
        self.actions = torch.from_numpy(actions)

    def __len__(self):
        return len(self.states)

    def __getitem__(self, idx):
        return self.states[idx], self.actions[idx]


def load_dataset():
    with open(DATA_PATH, "rb") as f:
        data = pickle.load(f)

    return data["states"], data["actions"]


def train():
    os.makedirs(CHECKPOINT_DIR, exist_ok=True)

    states, actions = load_dataset()

    dataset = ImitationDataset(states, actions)
    dataloader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        drop_last=True
    )

    model = MLPPolicy().to(DEVICE)
    optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
    criterion = nn.MSELoss()

    model.train()

    for epoch in range(EPOCHS):
        total_loss = 0.0

        for batch_states, batch_actions in dataloader:
            batch_states = batch_states.to(DEVICE)
            batch_actions = batch_actions.to(DEVICE)

            pred_actions = model(batch_states)
            loss = criterion(pred_actions, batch_actions)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_loss = total_loss / len(dataloader)
        print(f"Epoch {epoch + 1}/{EPOCHS} | Loss: {avg_loss:.6f}")

    torch.save(model.state_dict(), CHECKPOINT_PATH)
    print(f"Saved trained policy to {CHECKPOINT_PATH}")


if __name__ == "__main__":
    train()
