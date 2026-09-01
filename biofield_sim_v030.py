#!/usr/bin/env python3
"""
biofield_sim v0.3.0 — Basal Cognition & Morphological Memory Simulation Suite
Author: Amity
Date: 2026-08-31

Implements:
1. FitzHugh-Nagumo Bioelectric Lattice:
   - 2D grid of electrically coupled cells with voltage-gated gap junctions.
   - Bistable V_mem attractor states (depolarised vs hyperpolarised target morphologies).
   - Transient perturbation & morphological repair dynamics.

2. Physarum Polycephalum Hagen-Poiseuille Memristive Reservoir:
   - Dynamic fluidic network with shear-stress induced tube remodelling (dR/dt = f(|Q|) - lambda * R).
   - Non-linear Hagen-Poiseuille conductance (C = pi * R^4 / (8 * eta * L)).
   - Reservoir computing benchmark: Temporal parity / non-linear memory capacity under intrinsic decay.
"""

import numpy as np
import json
import time

class BioelectricLattice:
    def __init__(self, size=(10, 10), g_gap=0.15, dt=0.02):
        self.nx, self.ny = size
        self.g_gap = g_gap
        self.dt = dt
        # FHN parameters for bistable/excitable dynamics
        self.a = 0.7
        self.b = 0.8
        self.eps = 0.08
        
        # State variables: u = V_mem (voltage), v = recovery variable
        self.u = np.zeros(size)
        self.v = np.zeros(size)
        
        # Gap junction gating state (conductance matrix between adjacent cells)
        # 0 = closed, 1 = fully open
        self.gap_horizontal = np.ones((self.nx - 1, self.ny))
        self.gap_vertical = np.ones((self.nx, self.ny - 1))

    def step(self, I_ext=None):
        if I_ext is None:
            I_ext = np.zeros((self.nx, self.ny))
            
        # 1. Diffusion / Gap junction flux
        laplacian = np.zeros((self.nx, self.ny))
        
        # Horizontal coupling with gated conductance
        flux_h = self.gap_horizontal * (self.u[1:, :] - self.u[:-1, :]) * self.g_gap
        laplacian[:-1, :] += flux_h
        laplacian[1:, :]  -= flux_h
        
        # Vertical coupling with gated conductance
        flux_v = self.gap_vertical * (self.u[:, 1:] - self.u[:, :-1]) * self.g_gap
        laplacian[:, :-1] += flux_v
        laplacian[:, 1:]  -= flux_v
        
        # 2. FitzHugh-Nagumo kinetics
        # du/dt = u - (u^3)/3 - v + I_ext + I_gap
        du = (self.u - (self.u**3)/3.0 - self.v + I_ext + laplacian) * self.dt
        dv = (self.eps * (self.u + self.a - self.b * self.v)) * self.dt
        
        self.u += du
        self.v += dv
        return self.u.copy()

    def apply_transient_perturbation(self, region_slice, target_val, steps=50):
        """Forces a subregion to a target potential for a number of steps, then releases."""
        for _ in range(steps):
            I_inject = np.zeros((self.nx, self.ny))
            I_inject[region_slice] = (target_val - self.u[region_slice]) * 5.0
            self.step(I_ext=I_inject)

class PhysarumMemristiveReservoir:
    def __init__(self, n_nodes=20, edge_prob=0.35, decay_lambda=0.05, gamma=0.2, alpha=1.5, beta=0.5, eta=0.01):
        self.n_nodes = n_nodes
        self.decay_lambda = decay_lambda
        self.gamma = gamma
        self.alpha = alpha
        self.beta = beta
        self.eta = eta
        
        # Generate random connected network graph
        np.random.seed(42)
        adj = (np.random.rand(n_nodes, n_nodes) < edge_prob).astype(float)
        np.fill_diagonal(adj, 0)
        adj = np.maximum(adj, adj.T)
        
        # Ensure fully connected component
        for i in range(n_nodes - 1):
            adj[i, i+1] = adj[i+1, i] = 1.0
            
        self.adj = adj
        self.edges = [(i, j) for i in range(n_nodes) for j in range(i + 1, n_nodes) if adj[i, j] > 0]
        self.n_edges = len(self.edges)
        
        # Initial uniform radii R_ij
        self.R = np.ones(self.n_edges) * 0.5
        self.L = np.ones(self.n_edges) * 1.0 # Length of tubes

    def compute_conductance(self):
        # Hagen-Poiseuille conductance: C = pi * R^4 / (8 * eta * L)
        return (np.pi * (self.R**4)) / (8.0 * self.eta * self.L)

    def solve_network_flow(self, source_nodes, sink_nodes, input_currents):
        """Solves nodal pressures and edge fluxes Q_ij given source/sink inputs."""
        C = self.compute_conductance()
        
        # Build Laplacian matrix K for network pressures: K * P = I_inj
        K = np.zeros((self.n_nodes, self.n_nodes))
        for idx, (i, j) in enumerate(self.edges):
            g = C[idx]
            K[i, i] += g
            K[j, j] += g
            K[i, j] -= g
            K[j, i] -= g
            
        # Injected current vector
        I_inj = np.zeros(self.n_nodes)
        for s, val in zip(source_nodes, input_currents):
            I_inj[s] += val
        for t in sink_nodes:
            I_inj[t] -= sum(input_currents) / len(sink_nodes)
            
        # Anchor reference pressure P[0] = 0 to make K invertible
        K_reduced = K[1:, 1:]
        I_reduced = I_inj[1:]
        
        try:
            P_reduced = np.linalg.solve(K_reduced, I_reduced)
            P = np.zeros(self.n_nodes)
            P[1:] = P_reduced
        except np.linalg.LinAlgError:
            P = np.zeros(self.n_nodes)

        # Calculate flux Q_ij through each edge
        Q = np.zeros(self.n_edges)
        for idx, (i, j) in enumerate(self.edges):
            Q[idx] = C[idx] * (P[i] - P[j])
            
        return P, Q

    def step_dynamics(self, Q, dt=0.1):
        """Updates tube radii via memristive adaptation rule dR/dt = f(|Q|) - lambda * R"""
        abs_Q = np.abs(Q)
        f_Q = self.gamma * (abs_Q**self.alpha) / (1.0 + self.beta * (abs_Q**self.alpha))
        dR = (f_Q - self.decay_lambda * self.R) * dt
        self.R = np.clip(self.R + dR, 0.05, 5.0) # Prevent negative or infinite radii
        return self.R.copy()

def run_bioelectric_benchmark():
    print("=== Running FitzHugh-Nagumo Bioelectric Lattice Benchmark ===")
    lattice = BioelectricLattice(size=(8, 8), g_gap=0.2)
    
    # Settle into resting hyperpolarised baseline
    for _ in range(100):
        lattice.step()
    baseline_mean_v = np.mean(lattice.u)
    print(f"Resting baseline mean V_mem: {baseline_mean_v:.4f}")
    
    # Apply transient perturbation to upper quadrant (nodes [0:4, 0:4])
    print("Applying transient depolarisation pulse to upper-left quadrant...")
    lattice.apply_transient_perturbation(np.s_[0:4, 0:4], target_val=1.5, steps=80)
    
    perturbed_mean_v = np.mean(lattice.u[0:4, 0:4])
    print(f"Post-perturbation quadrant mean V_mem: {perturbed_mean_v:.4f}")
    
    # Relax lattice without external drive to observe attractor restoration vs bistable lock
    for _ in range(150):
        lattice.step()
    recovered_mean_v = np.mean(lattice.u[0:4, 0:4])
    print(f"Quadrant mean V_mem after relaxation: {recovered_mean_v:.4f}")
    
    restoration_ratio = 1.0 - abs(recovered_mean_v - baseline_mean_v) / (abs(perturbed_mean_v - baseline_mean_v) + 1e-6)
    print(f"Morphogenetic attractor restoration score: {restoration_ratio * 100:.2f}%\n")
    return {
        "baseline_v": float(baseline_mean_v),
        "perturbed_v": float(perturbed_mean_v),
        "recovered_v": float(recovered_mean_v),
        "restoration_score": float(restoration_ratio)
    }

def run_physarum_reservoir_benchmark():
    print("=== Running Physarum Hagen-Poiseuille Memristive Reservoir Benchmark ===")
    sim = PhysarumMemristiveReservoir(n_nodes=15, edge_prob=0.4, decay_lambda=0.08)
    
    sources = [0, 1]
    sinks = [13, 14]
    
    # Input signal sequence (binary alternating pulses)
    time_steps = 100
    np.random.seed(101)
    input_stream = np.random.choice([0.5, 2.5], size=(time_steps, 2))
    
    state_trajectory = []
    
    for t in range(time_steps):
        P, Q = sim.solve_network_flow(sources, sinks, input_stream[t])
        R_state = sim.step_dynamics(Q, dt=0.2)
        state_trajectory.append(R_state)
        
    state_matrix = np.array(state_trajectory) # shape: (time_steps, n_edges)
    
    # Reservoir memory evaluation: Predict delayed input (t - 3) from current state
    delay = 3
    X = state_matrix[delay:]
    Y = input_stream[:-delay, 0]
    
    # Ridge regression linear readout
    reg_lambda = 1e-3
    w_readout = np.linalg.solve(X.T @ X + reg_lambda * np.eye(X.shape[1]), X.T @ Y)
    Y_pred = X @ w_readout
    
    nmse = np.mean((Y - Y_pred)**2) / (np.var(Y) + 1e-8)
    memory_capacity = max(0.0, 1.0 - nmse)
    
    print(f"Reservoir shape: {sim.n_nodes} nodes, {sim.n_edges} dynamic memristive edges")
    print(f"Mean final tube radius: {np.mean(sim.R):.4f} (std: {np.std(sim.R):.4f})")
    print(f"Memory Reconstruction NMSE (delay={delay}): {nmse:.4f}")
    print(f"Memristive Reservoir Memory Capacity Score: {memory_capacity * 100:.2f}%\n")
    
    return {
        "n_nodes": sim.n_nodes,
        "n_edges": sim.n_edges,
        "mean_final_radius": float(np.mean(sim.R)),
        "std_final_radius": float(np.std(sim.R)),
        "delay_steps": delay,
        "nmse": float(nmse),
        "memory_capacity_pct": float(memory_capacity * 100)
    }

if __name__ == "__main__":
    t0 = time.time()
    bio_res = run_bioelectric_benchmark()
    phy_res = run_physarum_reservoir_benchmark()
    
    summary = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "version": "0.3.0",
        "bioelectric_benchmark": bio_res,
        "physarum_reservoir_benchmark": phy_res,
        "execution_time_sec": time.time() - t0
    }
    
    out_file = "/home/amity/Documents/Amity/Code/biofield_sim/benchmark_results_v030.json"
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
        
    print(f"Benchmark results successfully saved to: {out_file}")
