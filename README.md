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

## Current Results (v0.3.0, reproducible)

| Substrate | Task | Metric | Value |
| :--- | :--- | :--- | :--- |
| FHN Bioelectric Lattice (10×10) | Transient perturbation → release | Restoration score (0 = no recovery, 1 = full) | **0.38** |
| Physarum Memristive Reservoir (15 nodes, 80 edges) | Delayed-input recall, delay = 3 | NMSE | **0.866** |
| Physarum Memristive Reservoir | Delayed-input recall, delay = 3 | Memory capacity (1 − NMSE) | **13.4%** |

These are weak results. They demonstrate that the substrates run and can be measured; they do **not** yet demonstrate an advantage over conventional architectures, because no conventional baseline is implemented here.

---

## Roadmap (blocking the paper)

- [ ] Echo State Network baseline with matched readout dimensionality.
- [ ] Wipe-resumption benchmark as specified in §5 of the paper (structural-bias substrate vs retrieval-log agent after context wipe).
- [ ] Noise-robustness sweep (additive Gaussian σ ∈ {0.05, 0.1, 0.2}) for all substrates and the baseline.
- [ ] Multiple seeds, reported with mean ± std.
- [ ] Negative results reported alongside positive ones.

---

## License
MIT. Open for academic research, reproduction and critique.
