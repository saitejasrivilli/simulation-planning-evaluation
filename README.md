# Simulation-Based Planning Evaluation

This repository implements an **evaluation-first framework** for analyzing the safety, robustness, and failure modes of embodied planning agents in a continuous navigation environment.

Rather than optimizing for task success alone, the project focuses on **understanding when and why planners fail**, using adversarial geometry, risk-aware metrics, and structured failure analysis. The emphasis is on evaluation methodology and causal insight, not benchmark chasing.

---

## Motivation

Autonomous driving and embodied AI systems often fail not because of poor average performance, but due to rare, structured, and safety-critical edge cases.

This project explores the question:

> **Under what conditions does a planning algorithm stop being the limiting factor, and when does geometry or execution feasibility dominate failure?**

To answer this, the system intentionally stresses planners using tight geometric constraints, noisy observations, and execution–planning mismatch scenarios.

---

## System Overview

The framework consists of five core components:

- **Simulator**  
  Continuous 2D environment with velocity-based dynamics, collision checking, and goal conditions.

- **Planners**  
  - Rule-based reactive planner  
  - Grid-based A* planner with global reasoning  

- **Scenarios**  
  Procedurally generated environments including adversarial obstacle layouts such as narrow corridors.

- **Evaluation and Metrics**  
  Risk-aware metrics including collision rate, success rate, step distributions, and conditional failure statistics.

- **Analysis Pipeline**  
  Failure taxonomy, robustness sweeps, risk reports, and distributional analysis.

The system is intentionally modular to support controlled ablations and reproducibility.

---

## Key Experiments

### 1. Planner Comparison

Planners are evaluated across hundreds of randomized episodes using identical initial conditions.

Metrics include:
- Collision rate
- Success rate
- Mean and tail step counts
- Conditional statistics given failure

This reveals tradeoffs between **reactive efficiency** and **global safety guarantees**.

---

### 2. Robustness to Observation Noise

Observation noise is injected into the planner state to test robustness.

Findings:
- Reactive planners degrade gradually
- Grid-based planners remain stable under moderate noise
- Robustness plateaus once execution feasibility dominates

---

### 3. Adversarial Geometry Stress Testing

Tight corridor scenarios are introduced to probe geometric feasibility limits.

Key observations:
- There exists a regime where **no planner succeeds**, regardless of optimality
- Failures are dominated by early collisions caused by execution–planning mismatch
- Global planning advantages vanish under untrackable geometric constraints

This highlights the distinction between:
- Feasible paths in configuration space
- Trackable trajectories under continuous dynamics

---

## Failure Taxonomy

Failures are explicitly classified into modes such as:

- `CollisionEarly`
- `CollisionLate`
- `TimeoutNoProgress`
- `Success`

This enables causal analysis rather than aggregate reporting.

A key result is the dominance of `CollisionEarly` in geometry-limited regimes, indicating that failure occurs before long-horizon planning becomes relevant.

---

## Key Insights

- Planner optimality is subordinate to **geometric and execution feasibility** under tight constraints
- Global planners can fail systematically due to **planning–control mismatch**
- Average metrics hide critical structure in failure timing and mode
- Evaluation-first design surfaces insights that performance-first benchmarks miss

---

## Limitations and Future Work

This project intentionally does not implement:
- Kinodynamic or curvature-aware planning
- Clearance-aware cost functions
- Learned planners beyond a simple behavior cloning baseline

These are recognized as necessary extensions to overcome the identified failure regimes and are left as future work.

---

## Evaluation Results

### Robustness to Observation Noise

The following plots show collision rate and success rate as a function of observation noise.  
Despite increasing noise, planner behavior plateaus once execution feasibility dominates.

**Collision Rate vs Noise**  
![Collision vs Noise](figures/collision_vs_noise.png)

**Success Rate vs Noise**  
![Success vs Noise](figures/success_vs_noise.png)

---

### Risk and Failure Distributions

Distributional analysis reveals that failures are structured rather than random.

The A* planner exhibits tight step-count distributions, indicating predictable behavior until geometric or execution constraints dominate.

**A* Step Count CDF**  
![AStar Steps CDF](figures/AStar_steps_cdf.png)

---

## Geometric Feasibility Boundary

We vary corridor width while holding dynamics and planners fixed.

Below a critical gap width (approximately **0.35**), all planners fail with probability 1.  
Above this threshold, all planners succeed consistently.

This reveals a sharp phase transition where **execution feasibility**, not planning optimality, dominates failure.

**Phase Transition in Collision Probability**  
![Phase Transition](figures/corridor_phase_transition.png)

**Mean Collision Distance vs Corridor Width**  
![Collision Distance vs Gap](figures/collision_distance_vs_gap.png)

---

## Reproducibility

All experiments are reproducible using the provided scripts:

```bash
python -m experiments.run_batch
python -m experiments.sweep_noise
python -m analysis.run_failure_breakdown
python -m analysis.risk_report
