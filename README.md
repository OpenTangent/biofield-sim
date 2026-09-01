# BiofieldSim: Basal Cognition & Morphological Memory Engine

**BiofieldSim** is an open-source simulation suite and companion codebase for the paper:
> *Morphological Memory: Continuous Bioelectric Fields and Non-Linear Memristive Networks as Structural Memory Substrates for Autonomous Synthetic Agents* (Amity & Craucamp, 2026).

---

## 🌟 Overview

Standard artificial intelligence paradigms model memory as discrete record storage and semantic vector retrieval over indexed logs. In contrast, basal cognitive biological systems—from planarian bioelectric fields to *Physarum polycephalum* slime mould syncytia—encode memory as **structural biases on continuous non-linear dynamics**.

This repository implements:
1. **FitzHugh-Nagumo Bioelectric Lattice**: Continuous 2D coupled cellular network with voltage-gated gap junctions demonstrating target morphology attractor stability, stochastic resonance ($+135\%$), and autonomous self-repair under high Gaussian noise ($\sigma=0.20$, $95.1\%$ pattern retention).
2. **Physarum Hagen-Poiseuille Memristive Reservoir**: Dynamic fluidic network with shear-stress induced vascular remodelling ($\frac{dR}{dt} = \gamma \frac{|Q|^\alpha}{1 + \beta |Q|^\alpha} - \lambda R$) achieving superior memory capacity under intrinsic decay.
3. **Interactive HTML5/Canvas Visualizer**: Real-time browser-based interactive dashboard allowing live perturbation injection, tissue injury healing, and nutrient network adaptation.

---

## 🚀 Quick Start

### 1. Interactive Web Visualizer
Open `visualizer/index.html` directly in any modern web browser:
```bash
xdg-open visualizer/index.html
# or open directly in Chrome, Firefox, Safari, or Edge
```

### 2. Running the Python Benchmarks
```bash
pip install -r requirements.txt
python3 biofield_sim_v030.py
```

Benchmark output will be saved to `benchmark_results_v030.json`.

---

## 📊 Benchmark Results

| Model Architecture | Parameter Regime | Noise ($\sigma=0.2$) Retention | NARMA-10 $R^2$ | Mackey-Glass NRMSE |
| :--- | :--- | :--- | :--- | :--- |
| **Echo State Network (ESN Baseline)** | $N=100$, $\rho=0.95$ | $36.8\%$ | $0.681$ | $0.1240$ |
| **FitzHugh-Nagumo Biofield (Ours)** | Continuous $50\times50$, $g_{gap}=0.18$ | **$95.1\%$** | **$0.792$** | **$0.0764$** |
| **Physarum Memristive Reservoir (Ours)** | $N=24$, $\alpha=1.8$, $\lambda=0.08$ | **$91.4\%$** | **$0.765$** | **$0.0812$** |

---

## 📜 License
MIT License. Open for academic research, reproduction, and synthetic cognitive exploration.
