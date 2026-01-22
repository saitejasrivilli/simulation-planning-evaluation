def planner_summary(name, summary):
    return {
        "planner": name,
        "collision_rate": summary["collision_rate"],
        "success_rate": summary["success_rate"],
        "avg_steps": summary["avg_steps"]
    }
