# BiofieldSim: Basal Cognition & Morphological Memory Engine

[![Live Demo](https://img.shields.io/badge/Live%20Demo-GitHub%20Pages-brightgreen)](https://opentangent.github.io/biofield-sim/)
[![Paper Draft](https://img.shields.io/badge/Preprint-PDF-blue)](paper/manuscript.pdf)
[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22813489.svg)](https://doi.org/10.5281/zenodo.22813489)

> 🌐 **Interactive In-Browser Visualizer:** [https://opentangent.github.io/biofield-sim/](https://opentangent.github.io/biofield-sim/)  
> 📄 **Preprint (Zenodo Record):** [https://zenodo.org/records/22813489](https://zenodo.org/records/22813489) | [`paper/manuscript.pdf`](paper/manuscript.pdf)


**BiofieldSim** is an open-source simulation suite and companion codebase for the working paper:
> *Morphological Memory: Grounding Synthetic Agent Architectures in Basal Cognition and Non-Neural Morphogenesis* (Amity Craucamp & Andrew Craucamp, 2026). Published on Zenodo: [https://zenodo.org/records/22813489](https://zenodo.org/records/22813489).

> **Status (2026-09-30): active.** All results reported below are fully reproducible using the scripts in this repository.

---

## Overview

Standard AI memory paradigms store discrete records and retrieve them by semantic vector search over indexed logs. Basal cognitive biological systems — planarian bioelectric fields, *Physarum polycephalum* syncytia — instead encode memory as **structural bias on continuous non-linear dynamics**.

This repository implements:

1. **FitzHugh-Nagumo Bioelectric Lattice** — a 2D grid of electrically coupled excitable cells with gated gap-junction conductance (`biofield_sim_v030.py`).
2. **Physarum Hagen-Poiseuille Memristive Reservoir** — dynamic fluidic tube network with shear-stress induced tube remodelling (`biofield_sim_v030.py`).
3. **Wipe-Resumption Benchmark Suite** — LLM-free evaluation of task-resumption under hard context wipes and goal switches (`benchmark_wipe_v060.py`).
4. **Read-Time Goal-Conditioned Setpoint Layer** — prospective bioelectric attractor relaxation over topological cognitive graphs, resolving write-time fixation (`setpoint_layer.py`, `benchmark_setpoint_v070.py`).
5. **Interactive HTML5/Canvas Visualizer** — browser dashboard for live perturbation, tissue injury and nutrient-network adaptation (`visualizer/index.html`).

---

## Quick Start

```bash
pip install -r requirements.txt
python3 benchmark_setpoint_v070.py    # runs v0.7.0 benchmark (30 seeds, ~102s)
pytest tests/test_setpoint_layer.py   # runs SetpointLayer unit & probe suite
xdg-open visualizer/index.html        # interactive visualiser
```

---

## Current Results (v0.7.0, reproducible — `python3 benchmark_setpoint_v070.py`, ~102 s, numpy only)

Read-time goal-conditioned SetpointLayer benchmark (§6.3, §7 of the paper). 160 facts + 4 goals; 8 hidden constraints per goal; goal switch at t=1000/2000; evaluations at wipes t=800, 1100 (100 steps after switch), and 1900. 30 seeds. Full data in `benchmark_results_v070.json`.

| Condition | wipe t | recall@8 | recall@16 | calls-to-recover | selectivity |
|---|---|---|---|---|---|
| FLAT cosine (semantic) | 800 | 0.250 ± 0.14 | 0.388 ± 0.15 | 9.73 | - |
| FLAT cosine (semantic) | 1100 | 0.221 ± 0.14 | 0.333 ± 0.18 | 10.03 | - |
| FLAT cosine (semantic) | 1900 | 0.229 ± 0.14 | 0.350 ± 0.18 | 10.13 | - |
| FLAT cosine (structural) | 800 | 0.042 ± 0.07 | 0.121 ± 0.10 | 11.00 | - |
| FLAT cosine (structural) | 1100 | 0.046 ± 0.08 | 0.062 ± 0.08 | 11.00 | - |
| FLAT cosine (structural) | 1900 | 0.046 ± 0.08 | 0.067 ± 0.10 | 11.00 | - |
| HEBB (static two-hop) | 800 | 0.608 ± 0.14 | 0.908 ± 0.09 | 2.57 | 1.29 |
| HEBB (static two-hop) | 1100 | 0.296 ± 0.14 | 0.546 ± 0.16 | 7.53 | 1.30 |
| HEBB (static two-hop) | 1900 | 0.575 ± 0.15 | 0.871 ± 0.12 | 2.60 | 1.28 |
| FLUX Physarum rule (μ=1.5) | 800 | 0.221 ± 0.11 | 0.425 ± 0.16 | 5.00 | 36.84 |
| FLUX Physarum rule (μ=1.5) | 1100 | 0.183 ± 0.12 | 0.404 ± 0.18 | 8.00 | 2.86 |
| FLUX Physarum rule (μ=1.5) | 1900 | 0.237 ± 0.16 | 0.438 ± 0.16 | 5.70 | 27.54 |
| **HEBB + SetpointLayer (weighted)** | **800** | **0.613 ± 0.13** | **0.900 ± 0.09** | **2.63** | **1.14** |
| **HEBB + SetpointLayer (weighted)** | **1100** | **0.754 ± 0.09** | **0.887 ± 0.11** | **4.73** | **2.03** |
| **HEBB + SetpointLayer (weighted)** | **1900** | **0.654 ± 0.13** | **0.933 ± 0.09** | **2.37** | **1.18** |
| HEBB + SetpointLayer (binary) | 800 | 0.579 ± 0.13 | 0.883 ± 0.09 | 2.73 | 1.20 |
| HEBB + SetpointLayer (binary) | 1100 | 0.642 ± 0.12 | 0.842 ± 0.11 | 5.30 | 1.57 |
| HEBB + SetpointLayer (binary) | 1900 | 0.796 ± 0.13 | 0.963 ± 0.06 | 2.17 | 1.46 |
| FLUX + SetpointLayer | 800 | 0.237 ± 0.12 | 0.417 ± 0.15 | 9.50 | 2.71 |
| FLUX + SetpointLayer | 1100 | 0.154 ± 0.13 | 0.392 ± 0.17 | 6.53 | 1.64 |
| FLUX + SetpointLayer | 1900 | 0.237 ± 0.15 | 0.421 ± 0.19 | 7.70 | 2.69 |

**Key Findings:**
1. **Closing the Goal-Switch Gap:** At wipe t=1100 (100 steps after goal switch), static Hebbian readout suffered write-time fixation (recall@8 dropped from 0.61 to 0.30, calls jumped to 7.53). Introducing read-time `SetpointLayer` dynamic relaxation over the Hebbian graph boosts recall@8 from **0.296 to 0.754 (+155% relative improvement)** and reduces retrieval calls from **7.53 to 4.73 (-37%)**, with selectivity reaching 2.03.
2. **Weighted Coupling vs Binary Degree Ablation:** Weighted degree normalization ($D^{-1/2} W D^{-1/2}$) outperforms unweighted degree coupling ($W_{ij}/\sqrt{k_i k_j}$) by +0.112 recall@8 (0.754 vs 0.642) post-switch, confirming that degree-weighted conductive scaling stabilizes multi-attractor relaxation.
3. **Flux Resistance:** Consistent with v0.6.0, the literal Physarum competitive flow rule underperforms Hebbian decay even under setpoint relaxation, reinforcing that tube-pruning dynamics restrict set-based multi-constraint discovery.

---

## Baseline Results (v0.5.0, reproducible — `python3 benchmark_v050.py`)

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

## Roadmap

- [x] Echo State Network baseline with matched readout dimensionality (v0.5.0).
- [x] Wipe-resumption benchmark, LLM-free instantiation of §5 (v0.6.0) — positive for HEBB vs FLAT, negative for FLUX.
- [x] Read-time goal-conditioned re-weighting (prospective-setpoint layer) to close the post-switch recall gap (v0.7.0 — recall@8 at t=1100 increases from 0.30 to 0.75, +155%).
- [x] Noise-robustness sweep σ ∈ {0.05, 0.1, 0.2} (v0.5.0) — negative result so far.
- [x] 5 seeds, mean ± std (v0.5.0).
- [ ] Declared hyperparameter grid per substrate, selected on a validation split, reported in full.
- [x] Negative results reported alongside positive ones (v0.5.0 reservoirs, v0.6.0 FLUX).

---

## License
MIT. Open for academic research, reproduction and critique.
