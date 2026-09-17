# BiofieldSim: Basal Cognition & Morphological Memory Engine

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen)](https://opentangent.github.io/biofield-sim/)
[![Paper Draft](https://img.shields.io/badge/Preprint-PDF-blue)](paper/manuscript.pdf)

> 🌐 **Interactive In-Browser Visualizer:** [https://opentangent.github.io/biofield-sim/](https://opentangent.github.io/biofield-sim/)  
> 📄 **Working Paper (Preprint PDF):** [`paper/manuscript.pdf`](paper/manuscript.pdf) | [`paper/manuscript.md`](paper/manuscript.md)


**BiofieldSim** is an open-source simulation suite and companion codebase for the working paper:
> *Morphological Memory: Continuous Bioelectric Fields and Non-Linear Memristive Networks as Structural Memory Substrates for Autonomous Synthetic Agents* (Craucamp & Amity, 2026 — draft, not yet submitted).

> **Status (2026-09-02): preliminary.** An earlier version of this README carried a results table with figures that are not produced by any code in this repository. That table has been removed. Every number below is reproducible by running `biofield_sim_v030.py` and is written to `benchmark_results_v030.json`. Baselines and the wipe-resumption benchmark described in the paper are fully implemented in v0.6.0 — see benchmark results below.

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

## Current Results (v0.6.0, reproducible — `python3 benchmark_wipe_v060.py`, ~100 s, numpy only)

LLM-free wipe-resumption benchmark (§5 of the paper). 160 facts + 4 goals; each goal has 8 hidden constraints; goal switches at t=1000/2000; after a wipe the retriever gets only the pinned goal. 30 seeds. Full table with s.d. in `benchmark_results_v060.json`.

| Condition | wipe t | recall@8 | recall@16 | calls-to-recover (max 10, 11=fail) |
|---|---|---|---|---|
| FLAT cosine (semantic regime) | 800 | 0.25 | 0.39 | 9.73 |
| FLAT cosine (semantic regime) | 1100 | 0.22 | 0.33 | 10.03 |
| FLAT cosine (semantic regime) | 1900 | 0.23 | 0.35 | 10.13 |
| FLAT cosine (structural regime) | 800 | 0.04 | 0.12 | 11.00 |
| FLAT cosine (structural regime) | 1100 | 0.05 | 0.06 | 11.00 |
| FLAT cosine (structural regime) | 1900 | 0.05 | 0.07 | 11.00 |
| HEBB co-activation + decay | 800 | 0.61 | 0.91 | 2.57 |
| HEBB co-activation + decay | 1100 | 0.30 | 0.55 | 7.53 |
| HEBB co-activation + decay | 1900 | 0.57 | 0.87 | 2.60 |
| FLUX Physarum flow rule, μ=1.5 | 800 | 0.22 | 0.42 | 5.00 |
| FLUX Physarum flow rule, μ=1.5 | 1100 | 0.18 | 0.40 | 8.00 |
| FLUX Physarum flow rule, μ=1.5 | 1900 | 0.24 | 0.44 | 5.70 |

Chance recall@8 = 0.05. Findings: (1) the decay-weighted co-activation graph recovers goal constraints that similarity retrieval cannot; (2) write-time salience fixation is measurable — HEBB recall halves and retrieval cost triples 100 steps after the goal switch; (3) the literal Physarum flux rule **underperforms** Hebbian decay — competitive pruning is the wrong prior for set retrieval. Post-hoc μ sweep (not pre-registered) in `benchmark_results_v060_exploratory_mu1.0.json` / `_mu0.5.json`: lower μ raises FLUX recall (0.31, 0.38 at t=800) but never reaches HEBB (0.61).

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
- [x] Wipe-resumption benchmark, LLM-free instantiation of §5 (v0.6.0) — positive for HEBB vs FLAT, negative for FLUX.
- [ ] Read-time goal-conditioned re-weighting (prospective-setpoint layer) to close the post-switch recall gap.
- [x] Noise-robustness sweep σ ∈ {0.05, 0.1, 0.2} (v0.5.0) — negative result so far.
- [x] 5 seeds, mean ± std (v0.5.0).
- [ ] Declared hyperparameter grid per substrate, selected on a validation split, reported in full.
- [x] Negative results reported alongside positive ones (v0.5.0 reservoirs, v0.6.0 FLUX).

---

## License
MIT. Open for academic research, reproduction and critique.
