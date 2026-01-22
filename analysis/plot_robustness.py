import json
import matplotlib.pyplot as plt

with open("analysis/robustness_results.json", "r") as f:
    data = json.load(f)

noise = data["noise_levels"]

# ---------- Collision Rate Plot ----------
plt.figure()
for planner, stats in data["planners"].items():
    plt.plot(
        noise,
        stats["collision_rate"],
        marker="o",
        label=planner
    )

plt.xlabel("Observation Noise Std (meters)")
plt.ylabel("Collision Rate")
plt.title("Collision Rate vs Observation Noise")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("analysis/collision_vs_noise.png")
plt.close()

# ---------- Success Rate Plot ----------
plt.figure()
for planner, stats in data["planners"].items():
    plt.plot(
        noise,
        stats["success_rate"],
        marker="o",
        label=planner
    )

plt.xlabel("Observation Noise Std (meters)")
plt.ylabel("Success Rate")
plt.title("Success Rate vs Observation Noise")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("analysis/success_vs_noise.png")
plt.close()

print("Saved plots:")
print(" - analysis/collision_vs_noise.png")
print(" - analysis/success_vs_noise.png")
