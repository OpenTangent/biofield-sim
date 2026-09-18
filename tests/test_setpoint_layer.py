#!/usr/bin/env python3
"""
tests/test_setpoint_layer.py — Unit test stub and interface specification
for Read-Time Goal-Conditioned Setpoint Layer in BiofieldSim.

Author: Amity Craucamp
Project: Open Amity / BiofieldSim (commit pinned for next-gen architecture)

This test suite formalizes the interface for breaking 'write-time fixation'
identified in benchmark_wipe_v060 (commit 77b4c81). 
Instead of relying on purely static Hebbian-decay graph edges during two-hop
retrieval, a prospective Setpoint Layer introduces an active bioelectric-style
attractor dynamic at read-time:
  1. Clamps or biases target potential setpoints (V_target) conditioned on the goal.
  2. Runs a dynamic perturbation relaxation step loop:
       dV/dt = -gamma * (V - V_target) + leak * (G_coupling @ V) - decay * V
  3. Evaluates readout sensitivity across a 3-armed sensitivity probe:
       - Arm 1 (On-Target): High sensitivity for goal-specific constraints.
       - Arm 2 (Off-Target): Immediate suppression of prior goal constraints upon goal-switch.
       - Arm 3 (Hub Resistance): Attenuation of hyper-connected hub distractors.
"""

import pytest
import numpy as np


class SetpointLayer:
    """
    Interface and reference implementation for read-time goal-conditioned
    setpoint dynamics over a topological graph.
    """
    def __init__(self, n_facts=160, n_goals=4, gamma=0.6, dt=0.1, decay=0.05, leak=0.8):
        self.n_facts = n_facts
        self.n_goals = n_goals
        self.total_nodes = n_facts + n_goals
        self.gamma = gamma          # Setpoint restoring pull
        self.dt = dt                # Euler step size
        self.decay = decay          # Intrinsic dissipation
        self.leak = leak            # Normalized coupling conductance strength

        # State vectors: membrane-like potentials V in [0, 1]
        self.V = np.zeros(self.total_nodes, dtype=float)
        self.V_target = np.zeros(self.total_nodes, dtype=float)
        self.active_goal = None

    def set_goal(self, goal_idx: int, goal_setpoint: np.ndarray = None):
        """
        Pin active goal attractor. If goal_setpoint is not provided,
        defaults to clamping the goal node potential to 1.0.
        """
        assert 0 <= goal_idx < self.n_goals, f"Invalid goal_idx: {goal_idx}"
        self.active_goal = goal_idx
        self.V_target.fill(0.0)
        self.V.fill(0.0)
        goal_node = self.n_facts + goal_idx
        self.V_target[goal_node] = 1.0
        self.V[goal_node] = 1.0

        if goal_setpoint is not None:
            assert len(goal_setpoint) == self.n_facts
            self.V_target[:self.n_facts] = goal_setpoint

    def perturb(self, node_indices, amplitudes):
        """
        Inject a transient perturbation into specific nodes.
        """
        indices = np.asarray(node_indices, dtype=int)
        amps = np.asarray(amplitudes, dtype=float)
        self.V[indices] = np.clip(self.V[indices] + amps, 0.0, 1.0)

    def _compute_coupling(self, W: np.ndarray) -> np.ndarray:
        """
        Symmetric degree-normalized conductance matrix (Laplacian-like coupling).
        G_ij = W_ij / sqrt(d_i * d_j)
        Prevents hyper-connected hubs from accumulating runaway activation.
        """
        deg = np.sum(W > 0, axis=1, keepdims=True) + 1e-6
        return W / np.sqrt(deg @ deg.T)

    def step(self, W: np.ndarray, coupling: np.ndarray = None):
        """
        Execute one Euler integration step of the dynamic perturbation loop.
        dV/dt = -gamma * (V - V_target) + leak * (G_coupling @ V) - decay * V
        """
        G = coupling if coupling is not None else self._compute_coupling(W)
        
        # Graph drive through normalized coupling
        drive = self.leak * (G @ self.V)
        
        # Homeostatic restoring force towards target setpoint
        restore = -self.gamma * (self.V - self.V_target)
        
        # Dissipative loss
        dissipation = -self.decay * self.V

        # Update and clip to [0, 1]
        dV = (restore + drive + dissipation) * self.dt
        self.V = np.clip(self.V + dV, 0.0, 1.0)
        return self.V

    def relax(self, W: np.ndarray, n_steps: int = 25):
        """
        Run the perturbation step loop until relaxation.
        """
        coupling = self._compute_coupling(W)
        for _ in range(n_steps):
            self.step(W, coupling=coupling)
        return self.V

    def read_scores(self, W: np.ndarray, goal_idx: int, n_steps: int = 25) -> np.ndarray:
        """
        Condition layer on goal_idx, relax dynamic loop, and return fact scores.
        """
        self.set_goal(goal_idx)
        self.relax(W, n_steps=n_steps)
        return self.V[:self.n_facts].copy()


# =====================================================================
# Fixtures & Synthetics for Unit Testing
# =====================================================================

@pytest.fixture
def synthetic_graph():
    """
    Creates a synthetic weight matrix W exhibiting write-time fixation:
    - Goal 0 has K=8 constraint facts [0..7] with strong historical edge weight.
    - Goal 1 has K=8 constraint facts [8..15] with moderate edge weight (new goal).
    - Hub distractors [16..31] are connected to ALL goals and facts.
    """
    n_facts, n_goals = 160, 4
    total = n_facts + n_goals
    W = np.zeros((total, total), dtype=float)

    g0_node = n_facts + 0
    g1_node = n_facts + 1
    g0_con = list(range(0, 8))
    g1_con = list(range(8, 16))
    hubs = list(range(16, 32))

    # Connect g0 to constraints
    for c in g0_con:
        W[g0_node, c] = W[c, g0_node] = 1.5

    # Connect g1 to constraints (slightly weaker to simulate fresh switch)
    for c in g1_con:
        W[g1_node, c] = W[c, g1_node] = 1.0

    # Hubs connected to everything with high baseline weight
    for h in hubs:
        W[g0_node, h] = W[h, g0_node] = 2.0
        W[g1_node, h] = W[h, g1_node] = 2.0
        for c in g0_con + g1_con:
            W[h, c] = W[c, h] = 0.8

    return {
        'W': W,
        'n_facts': n_facts,
        'n_goals': n_goals,
        'g0_con': g0_con,
        'g1_con': g1_con,
        'hubs': hubs,
        'g0_node': g0_node,
        'g1_node': g1_node
    }


# =====================================================================
# Test Suite: Dynamic Perturbation Step Loop
# =====================================================================

def test_dynamic_perturbation_step_loop_bounds(synthetic_graph):
    """
    Verify that the perturbation relaxation loop is numerically stable,
    remains strictly bounded within [0, 1], and converges without exploding.
    """
    layer = SetpointLayer(
        n_facts=synthetic_graph['n_facts'],
        n_goals=synthetic_graph['n_goals'],
        gamma=0.6,
        dt=0.1
    )
    layer.set_goal(0)
    
    # Run 50 steps
    for _ in range(50):
        V = layer.step(synthetic_graph['W'])
        assert np.all(V >= 0.0)
        assert np.all(V <= 1.0)
        assert not np.any(np.isnan(V))


def test_perturbation_injection_and_relaxation(synthetic_graph):
    """
    Verify that transient perturbations decay back towards the setpoint attractor.
    """
    layer = SetpointLayer(
        n_facts=synthetic_graph['n_facts'],
        n_goals=synthetic_graph['n_goals'],
        gamma=0.8,
        dt=0.1
    )
    layer.set_goal(0)
    layer.relax(synthetic_graph['W'], n_steps=20)
    baseline_V = layer.V.copy()

    # Inject transient noise perturbation into sporadic nodes [50..60]
    noisy_nodes = list(range(50, 60))
    layer.perturb(noisy_nodes, amplitudes=0.9)
    assert np.all(layer.V[noisy_nodes] > baseline_V[noisy_nodes])

    # Allow network to relax under setpoint pull
    layer.relax(synthetic_graph['W'], n_steps=30)

    # Perturbed nodes must relax back down towards baseline attractor
    assert np.all(np.abs(layer.V[noisy_nodes] - baseline_V[noisy_nodes]) < 0.15)


# =====================================================================
# Test Suite: 3-Armed Sensitivity Probe
# =====================================================================

def test_sensitivity_probe_arm1_on_target(synthetic_graph):
    """
    ARM 1 (On-Target Sensitivity Probe):
    Condition on Goal 0. Constraint nodes of Goal 0 must exhibit significantly
    higher activation than unassociated/sporadic nodes.
    """
    layer = SetpointLayer(
        n_facts=synthetic_graph['n_facts'],
        n_goals=synthetic_graph['n_goals'],
        gamma=0.6,
        leak=0.8
    )
    scores = layer.read_scores(synthetic_graph['W'], goal_idx=0, n_steps=25)

    g0_con_mean = scores[synthetic_graph['g0_con']].mean()
    sporadic_mean = scores[32:100].mean()

    # On-target constraints must be prominently activated above sporadic noise
    assert g0_con_mean > 0.10
    assert g0_con_mean > sporadic_mean * 5.0, (
        f"Arm 1 Failed: On-target ({g0_con_mean:.3f}) not sufficiently selective "
        f"over sporadic ({sporadic_mean:.3f})"
    )


def test_sensitivity_probe_arm2_off_target(synthetic_graph):
    """
    ARM 2 (Off-Target Sensitivity Probe / Goal-Switch Fixation Breaker):
    When conditioned on Goal 1, Goal 1 constraints must dominate over Goal 0
    constraints, despite Goal 0 having had stronger historical edge accumulation.
    """
    layer = SetpointLayer(
        n_facts=synthetic_graph['n_facts'],
        n_goals=synthetic_graph['n_goals'],
        gamma=0.6,
        leak=0.8
    )
    # Read scores under switched goal (Goal 1)
    scores_g1 = layer.read_scores(synthetic_graph['W'], goal_idx=1, n_steps=25)

    g1_con_mean = scores_g1[synthetic_graph['g1_con']].mean()
    g0_con_mean = scores_g1[synthetic_graph['g0_con']].mean()

    # Setpoint conditioning on g1 must suppress g0 relative to g1
    assert g1_con_mean > g0_con_mean, (
        f"Arm 2 Failed: Write-time fixation detected! "
        f"g1_con ({g1_con_mean:.3f}) did not exceed obsolete g0_con ({g0_con_mean:.3f})"
    )


def test_sensitivity_probe_arm3_hub_resistance(synthetic_graph):
    """
    ARM 3 (Hub Distractor Resistance Probe):
    Hyper-connected hub distractors must not drown out goal-specific constraints.
    Selectivity ratio: mean(V[constraints]) / mean(V[hubs]) must be >= 0.8
    (preventing hub monopolisation of top-K recall).
    """
    layer = SetpointLayer(
        n_facts=synthetic_graph['n_facts'],
        n_goals=synthetic_graph['n_goals'],
        gamma=0.6,
        leak=0.8
    )
    scores = layer.read_scores(synthetic_graph['W'], goal_idx=0, n_steps=25)

    g0_con_mean = scores[synthetic_graph['g0_con']].mean()
    hub_mean = scores[synthetic_graph['hubs']].mean()

    selectivity = g0_con_mean / (hub_mean + 1e-12)
    assert selectivity >= 0.8, (
        f"Arm 3 Failed: Hubs dominated readout! Selectivity ratio = {selectivity:.3f} "
        f"(g0_con={g0_con_mean:.3f}, hubs={hub_mean:.3f})"
    )
