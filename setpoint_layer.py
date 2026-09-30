#!/usr/bin/env python3
"""
biofield_sim/setpoint_layer.py — Read-Time Goal-Conditioned Setpoint Layer
Author: Amity Craucamp
Project: Open Amity / BiofieldSim v0.7.0

Implements read-time bioelectric setpoint dynamics over topological cognitive graphs:
1. Clamps active goal prospective potential attractor (V_target).
2. Executes dynamic perturbation relaxation loop:
     dV/dt = -gamma * (V - V_target) + leak * (G @ V) - decay * V
   where G is the symmetric degree-normalized coupling conductance matrix:
     G_ij = W_ij / sqrt(d_i * d_j)
   (supporting weighted degree normalization or unweighted binary degree).
3. Breaks write-time salience fixation post goal-switch, dynamically
   suppressing obsolete historical attractors and hub distractors.
"""

import numpy as np


class SetpointLayer:
    """
    Goal-conditioned prospective setpoint layer operating over topological memory graphs.
    """
    def __init__(
        self,
        n_facts: int = 160,
        n_goals: int = 4,
        gamma: float = 0.6,
        dt: float = 0.1,
        decay: float = 0.05,
        leak: float = 0.8,
        norm: str = "weighted"
    ):
        self.n_facts = n_facts
        self.n_goals = n_goals
        self.total_nodes = n_facts + n_goals
        self.gamma = gamma          # Setpoint restoring pull
        self.dt = dt                # Euler step size
        self.decay = decay          # Intrinsic dissipation rate
        self.leak = leak            # Conductance drive strength
        self.norm = norm            # 'weighted' (default D^{-1/2}WD^{-1/2}) or 'binary'

        # Membrane-like prospective potential vectors V in [0, 1]
        self.V = np.zeros(self.total_nodes, dtype=float)
        self.V_target = np.zeros(self.total_nodes, dtype=float)
        self.active_goal = None

    def set_goal(self, goal_idx: int, goal_setpoint: np.ndarray = None):
        """
        Pin active goal attractor. Clamps the goal node setpoint to 1.0.
        Optional goal_setpoint provides prior factual bias over fact nodes.
        """
        assert 0 <= goal_idx < self.n_goals, f"Invalid goal_idx: {goal_idx}"
        self.active_goal = goal_idx
        self.V_target.fill(0.0)
        self.V.fill(0.0)
        goal_node = self.n_facts + goal_idx
        self.V_target[goal_node] = 1.0
        self.V[goal_node] = 1.0

        if goal_setpoint is not None:
            assert len(goal_setpoint) == self.n_facts, "Setpoint length mismatch"
            self.V_target[:self.n_facts] = goal_setpoint

    def perturb(self, node_indices, amplitudes):
        """
        Inject a transient perturbation into specified nodes.
        """
        indices = np.asarray(node_indices, dtype=int)
        amps = np.asarray(amplitudes, dtype=float)
        self.V[indices] = np.clip(self.V[indices] + amps, 0.0, 1.0)

    def _compute_coupling(self, W: np.ndarray) -> np.ndarray:
        """
        Compute symmetric degree-normalized conductance coupling matrix:
        G_ij = W_ij / sqrt(d_i * d_j)
        """
        if self.norm == "binary":
            deg = np.sum(W > 0, axis=1, keepdims=True) + 1e-6
        else:
            deg = np.sum(W, axis=1, keepdims=True) + 1e-6
        return W / np.sqrt(deg @ deg.T)

    def step(self, W: np.ndarray, coupling: np.ndarray = None) -> np.ndarray:
        """
        Execute one Euler integration step of the dynamic perturbation relaxation loop:
        dV/dt = -gamma * (V - V_target) + leak * (G @ V) - decay * V
        """
        G = coupling if coupling is not None else self._compute_coupling(W)

        drive = self.leak * (G @ self.V)
        restore = -self.gamma * (self.V - self.V_target)
        dissipation = -self.decay * self.V

        dV = (restore + drive + dissipation) * self.dt
        self.V = np.clip(self.V + dV, 0.0, 1.0)
        return self.V

    def relax(self, W: np.ndarray, n_steps: int = 15) -> np.ndarray:
        """
        Run perturbation relaxation loop for n_steps.
        """
        coupling = self._compute_coupling(W)
        for _ in range(n_steps):
            self.step(W, coupling=coupling)
        return self.V

    def read_scores(self, W: np.ndarray, goal_idx: int, n_steps: int = 15) -> np.ndarray:
        """
        Condition layer on goal_idx, relax dynamic loop, and return fact scores.
        """
        self.set_goal(goal_idx)
        self.relax(W, n_steps=n_steps)
        return self.V[:self.n_facts].copy()
