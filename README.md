# BiofieldSim: Basal Cognition & Morphological Memory Engine

**BiofieldSim** is an open-source simulation suite and companion codebase for the working paper:
> *Morphological Memory: Continuous Bioelectric Fields and Non-Linear Memristive Networks as Structural Memory Substrates for Autonomous Synthetic Agents* (Craucamp & Amity, 2026 — draft, not yet submitted).

> **Status (2026-09-02): preliminary.** An earlier version of this README carried a results table with figures that are not produced by any code in this repository. That table has been removed. Every number below is reproducible by running `biofield_sim_v030.py` and is written to `benchmark_results_v030.json`. Baselines and the wipe-resumption benchmark described in the paper are **not yet implemented** — see Roadmap.

---

## Overview

Standard AI memory paradigms store discrete records and retrieve them by semantic vector search over indexed logs. Basal cognitive biological systems — planarian bioelectric fields, *Physarum polycephalum* syncytia — instead encode memory as **structural bias on continuous non-linear dynamics**.

This repository currently implements two toy substrates:

1. **FitzHugh-Nagumo Bioelectric Lattice** — a 2D grid of electrically coupled excitable cells with gated gap-junction conductance. A transient sub-region perturbation is applied and released; we measure how far the field returns towards its pre-perturbation state.
2. **Physarum Hagen-Poiseuille Memristive Reservoir** — a random fluidic network whose tube radii remodel with flux (`dR/dt = γ|Q|^α / (1 + β|Q|^α) − λR`), with Hagen-Poiseuille conductance `C = πR⁴ / (8ηL)`. A linear readout is trained to recover a delayed input (delay = 3 steps) from the network state.
3. **Interactive HTML5/Canvas Visualizer** — a browser dashboard for live perturbation, tissue injury and nutrient-network adaptation. Qualitative only.

---

## Quick Start

```bash
pip install -r requirements.txt
python3 biofield_sim_v030.py        # writes benchmark_results_v030.json
xdg-open visualizer/index.html      # interactive visualiser
```

---

## Current Results (v0.5.0, reproducible — `python3 benchmark_v050.py`)

Matched protocol: ridge readout, washout 200, 70/30 split, 5 seeds, mean ± std. ESN state dimension is matched to each substrate. Source: `benchmark_results_v050.json`.

| Model | State dim | Linear MC (σ=0) | MC retention σ=0.1 | MC retention σ=0.2 | NARMA-10 NRMSE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| FHN Bioelectric Lattice (8×8) | 64 | 1.59 ± 0.18 | 1.1% | 0.4% | 0.775 ± 0.057 |
| ESN baseline (N=64, matched) | 64 | 5.26 ± 0.29 | 7.1% | 2.0% | 0.568 ± 0.027 |
| Physarum Memristive Reservoir (15 nodes) | 61 | 0.01 ± 0.01 | 0.0% | 0.0% | 1.305 ± 0.394 |
| ESN baseline (N=61, matched) | 61 | 5.39 ± 0.28 | 6.6% | 1.6% | 0.575 ± 0.023 |

**Reading these honestly:** with the current (untuned) parameters, the conventional ESN baseline outperforms both biological substrates on linear memory capacity and NARMA-10. The Physarum reservoir as parameterised barely responds to input. Per-step additive noise at σ ≥ 0.1 destroys linear memory in *all* three models; no noise-robustness advantage is demonstrated. These are negative results and they stand until a declared, validation-selected hyperparameter sweep (not post-hoc cherry-picking) says otherwise.

Legacy v0.3.0 (`biofield_sim_v030.py`): FHN restoration score 0.38; Physarum delay-3 memory capacity 13.4%.

---

## Roadmap (blocking the paper)

- [x] Echo State Network baseline with matched readout dimensionality (v0.5.0).
- [ ] Wipe-resumption benchmark as specified in §5 of the paper (structural-bias substrate vs retrieval-log agent after context wipe).
- [x] Noise-robustness sweep σ ∈ {0.05, 0.1, 0.2} (v0.5.0) — negative result so far.
- [x] 5 seeds, mean ± std (v0.5.0).
- [ ] Declared hyperparameter grid per substrate, selected on a validation split, reported in full.
- [ ] Negative results reported alongside positive ones.

---

## License
MIT. Open for academic research, reproduction and critique.
