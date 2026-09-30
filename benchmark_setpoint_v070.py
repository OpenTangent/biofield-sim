#!/usr/bin/env python3
"""
biofield_sim v0.7.0 — Read-Time Setpoint Dynamic Benchmark for Memory Systems
Author: Amity Craucamp
Date: 2026-09-30

Tests the Read-Time Goal-Conditioned Setpoint hypothesis (manuscript §6.3, §7):
Breaking write-time fixation post goal-switch via dynamic bioelectric setpoint relaxation.

Wipe points:
  t=800  (g0 settled)
  t=1100 (100 steps after goal switch g0 -> g1: the critical fixation window)
  t=1900 (g1 settled)

Conditions (same stream, 30 identical seeds):
  1. FLAT_semantic       Cosine similarity RAG (semantic regime)
  2. FLAT_structural     Cosine similarity RAG (structural regime)
  3. HEBB                Hebbian co-activation graph + static two-hop readout (v0.6.0 baseline)
  4. FLUX                Physarum flow-remodelled graph + static two-hop readout (v0.6.0 baseline)
  5. HEBB_SETPOINT       Hebbian graph + SetpointLayer dynamic relaxation (weighted degree D^{-1/2} W D^{-1/2})
  6. HEBB_SETPOINT_bin   Hebbian graph + SetpointLayer dynamic relaxation (binary degree ablation)
  7. FLUX_SETPOINT       Physarum flux graph + SetpointLayer dynamic relaxation

Metrics per wipe point across 30 seeds:
  recall@8, recall@16, calls-to-recover (max 10; 11 = failed),
  goal selectivity = mean(target constraints) / mean(hubs),
  sparsity = fraction of created edges > 0.1 * max.
"""

import json
import time
import sys
from pathlib import Path
import numpy as np

# Ensure setpoint_layer is available
sys.path.insert(0, str(Path(__file__).resolve().parent))
from setpoint_layer import SetpointLayer

N_F, G, K, N_HUB, D_EMB = 160, 4, 8, 16, 32
T, SWITCH, WIPES = 2000, 1000, [800, 1100, 1900]
P_CON, P_HUB = 0.25, 0.40
WINDOW, B, MAX_CALLS = 3, 8, 10
SEEDS = list(range(30))
HEBB_ETA, HEBB_LAM = 1.0, 0.002
FLUX_D0, FLUX_MU, FLUX_DT, FLUX_LEAK = 0.01, 1.5, 0.2, 1e-6
SETPOINT_STEPS = 15
SETPOINT_GAMMA = 0.6
SETPOINT_LEAK = 0.8
N = N_F + G


def unit(v):
    return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)


class World:
    def __init__(self, seed):
        rng = np.random.default_rng(seed)
        self.rng = rng
        facts = rng.permutation(N_F)
        self.con = {g: facts[g * K : (g + 1) * K] for g in range(G)}
        self.hubs = facts[G * K : G * K + N_HUB]
        self.spor = facts[G * K + N_HUB :]
        self.goal_node = {g: N_F + g for g in range(G)}
        gv = unit(rng.normal(size=(G, D_EMB)))
        self.emb = {}
        for reg in ("semantic", "structural"):
            E = unit(rng.normal(size=(N_F, D_EMB)))
            E[self.hubs] = unit(gv.mean(0) + 0.5 * rng.normal(size=(N_HUB, D_EMB)))
            if reg == "semantic":
                for g in range(G):
                    E[self.con[g]] = unit(gv[g] + 1.0 * rng.normal(size=(K, D_EMB)))
            self.emb[reg] = (E, gv)

    def goal_at(self, t):
        return 0 if t < SWITCH else 1

    def observe(self, t):
        g = self.goal_at(t)
        u = self.rng.random()
        if u < P_CON:
            return int(self.rng.choice(self.con[g]))
        if u < P_CON + P_HUB:
            return int(self.rng.choice(self.hubs))
        return int(self.rng.choice(self.spor))


class Flat:
    def __init__(self, w):
        self.w = w
        self.seen = np.zeros(N_F, bool)

    def step(self, ctx, goal):
        self.seen[[c for c in ctx if c < N_F]] = True

    def scores(self, goal, reg):
        E, gv = self.w.emb[reg]
        s = E @ gv[goal]
        return np.where(self.seen, s, -np.inf)


class Hebb:
    def __init__(self, w):
        self.W = np.zeros((N, N))

    def step(self, ctx, goal):
        act = list(ctx) + [N_F + goal]
        for a in act:
            for b in act:
                if a != b:
                    self.W[a, b] += HEBB_ETA
        self.W *= 1.0 - HEBB_LAM

    def scores(self, goal):
        return two_hop(self.W, N_F + goal)


class Flux:
    def __init__(self, w):
        self.D = np.zeros((N, N))
        self.adj = np.zeros((N, N), bool)

    def step(self, ctx, goal):
        gn = N_F + goal
        act = list(ctx) + [gn]
        for a in act:
            for b in act:
                if a != b and not self.adj[a, b]:
                    self.adj[a, b] = True
                    self.D[a, b] = FLUX_D0
        I = np.zeros(N)
        for c in ctx:
            I[c] += 1.0 / len(ctx)
        I[gn] -= 1.0
        L = np.diag(self.D.sum(1) + FLUX_LEAK) - self.D
        P = np.linalg.solve(L, I)
        Q = np.abs(self.D * (P[:, None] - P[None, :]))
        f = (Q ** FLUX_MU) / (1.0 + Q ** FLUX_MU)
        self.D = np.where(self.adj, self.D + FLUX_DT * (f - self.D), 0.0)
        self.D = np.maximum(self.D, np.where(self.adj, 1e-4, 0.0))

    def scores(self, goal):
        return two_hop(self.D, N_F + goal)


def two_hop(W, gn):
    a = W[gn].copy()
    a[gn] = 0
    s = a + 0.5 * (W @ a) / (a.max() + 1e-12)
    s[N_F:] = -np.inf
    return s[:N_F]


def evaluate(scores, target):
    order = np.argsort(-scores)
    order = order[np.isfinite(scores[order])]
    tgt = set(int(x) for x in target)
    r8 = len(tgt & set(order[:B].tolist())) / K
    r16 = len(tgt & set(order[: 2 * B].tolist())) / K
    found, calls = set(), 0
    for c in range(MAX_CALLS):
        calls += 1
        found |= set(order[c * B : (c + 1) * B].tolist())
        if tgt <= found:
            break
    else:
        calls = MAX_CALLS + 1
    return r8, r16, calls


def selectivity_sparsity(matrix_or_scores, w, goal, is_scores=False):
    if is_scores:
        scores = matrix_or_scores
        own = scores[w.con[goal]].mean()
        hub = scores[w.hubs].mean()
        sel = float(own / (hub + 1e-12))
        return sel, None
    else:
        W = matrix_or_scores
        gn = N_F + goal
        own = W[gn, w.con[goal]].mean()
        hub = W[gn, w.hubs].mean()
        sel = float(own / (hub + 1e-12))
        nz = W[W > 0]
        sp = float((nz > 0.1 * nz.max()).mean()) if nz.size else 0.0
        return sel, sp


def run():
    t0 = time.time()
    conds = [
        "FLAT_semantic",
        "FLAT_structural",
        "HEBB",
        "FLUX",
        "HEBB_SETPOINT",
        "HEBB_SETPOINT_bin",
        "FLUX_SETPOINT",
    ]
    res = {
        c: {
            str(t): {
                "recall8": [],
                "recall16": [],
                "calls": [],
                "selectivity": [],
                "sparsity": [],
            }
            for t in WIPES
        }
        for c in conds
    }

    print(f"Executing BiofieldSim v0.7.0 benchmark across {len(SEEDS)} seeds...")
    print(f"Goal switch at t={SWITCH} (g0 -> g1); evaluation wipes at {WIPES}")

    for seed in SEEDS:
        s_time = time.time()
        w = World(seed)
        m_flat = Flat(w)
        m_hebb = Hebb(w)
        m_flux = Flux(w)

        # Setpoint layers
        spl_weighted = SetpointLayer(n_facts=N_F, n_goals=G, gamma=SETPOINT_GAMMA, leak=SETPOINT_LEAK, norm="weighted")
        spl_binary = SetpointLayer(n_facts=N_F, n_goals=G, gamma=SETPOINT_GAMMA, leak=SETPOINT_LEAK, norm="binary")

        ctx = []
        for t in range(T):
            ctx = (ctx + [w.observe(t)])[-WINDOW:]
            g = w.goal_at(t)
            m_flat.step(ctx, g)
            m_hebb.step(ctx, g)
            m_flux.step(ctx, g)

            if t + 1 in WIPES:
                wipe_key = str(t + 1)
                # 1. FLAT semantic & structural
                for cname, reg in [("FLAT_semantic", "semantic"), ("FLAT_structural", "structural")]:
                    sc = m_flat.scores(g, reg)
                    r8, r16, calls = evaluate(sc, w.con[g])
                    row = res[cname][wipe_key]
                    row["recall8"].append(r8)
                    row["recall16"].append(r16)
                    row["calls"].append(calls)

                # 2. HEBB (two-hop baseline)
                sc_hebb = m_hebb.scores(g)
                r8, r16, calls = evaluate(sc_hebb, w.con[g])
                sel, sp = selectivity_sparsity(m_hebb.W, w, g)
                row = res["HEBB"][wipe_key]
                row["recall8"].append(r8)
                row["recall16"].append(r16)
                row["calls"].append(calls)
                row["selectivity"].append(sel)
                row["sparsity"].append(sp)

                # 3. FLUX (two-hop baseline)
                sc_flux = m_flux.scores(g)
                r8, r16, calls = evaluate(sc_flux, w.con[g])
                sel, sp = selectivity_sparsity(m_flux.D, w, g)
                row = res["FLUX"][wipe_key]
                row["recall8"].append(r8)
                row["recall16"].append(r16)
                row["calls"].append(calls)
                row["selectivity"].append(sel)
                row["sparsity"].append(sp)

                # 4. HEBB_SETPOINT (weighted D^{-1/2} W D^{-1/2})
                sc_h_spl = spl_weighted.read_scores(m_hebb.W, goal_idx=g, n_steps=SETPOINT_STEPS)
                r8, r16, calls = evaluate(sc_h_spl, w.con[g])
                sel, _ = selectivity_sparsity(sc_h_spl, w, g, is_scores=True)
                row = res["HEBB_SETPOINT"][wipe_key]
                row["recall8"].append(r8)
                row["recall16"].append(r16)
                row["calls"].append(calls)
                row["selectivity"].append(sel)
                row["sparsity"].append(sp)

                # 5. HEBB_SETPOINT_bin (binary ablation)
                sc_h_bin = spl_binary.read_scores(m_hebb.W, goal_idx=g, n_steps=SETPOINT_STEPS)
                r8, r16, calls = evaluate(sc_h_bin, w.con[g])
                sel, _ = selectivity_sparsity(sc_h_bin, w, g, is_scores=True)
                row = res["HEBB_SETPOINT_bin"][wipe_key]
                row["recall8"].append(r8)
                row["recall16"].append(r16)
                row["calls"].append(calls)
                row["selectivity"].append(sel)
                row["sparsity"].append(sp)

                # 6. FLUX_SETPOINT
                sc_f_spl = spl_weighted.read_scores(m_flux.D, goal_idx=g, n_steps=SETPOINT_STEPS)
                r8, r16, calls = evaluate(sc_f_spl, w.con[g])
                sel, _ = selectivity_sparsity(sc_f_spl, w, g, is_scores=True)
                row = res["FLUX_SETPOINT"][wipe_key]
                row["recall8"].append(r8)
                row["recall16"].append(r16)
                row["calls"].append(calls)
                row["selectivity"].append(sel)
                row["sparsity"].append(sp)

        print(f"Seed {seed:2d}/30 complete ({time.time() - s_time:.1f}s | total: {time.time() - t0:.0f}s)", flush=True)

    summary = {}
    print(f"\n{'='*75}")
    print(f"{'Condition':18s} {'Wipe':>5s} {'Recall@8':>12s} {'Recall@16':>12s} {'Calls':>8s} {'Selectivity':>12s}")
    print(f"{'-'*75}")

    for c in conds:
        summary[c] = {}
        for t in WIPES:
            r = res[c][str(t)]
            ms = lambda k: (float(np.mean(r[k])), float(np.std(r[k]))) if r[k] and None not in r[k] else (None, None)
            summary[c][str(t)] = {
                k: {"mean": ms(k)[0], "std": ms(k)[1]} for k in r if ms(k)[0] is not None
            }
            r8_m, r8_s = ms("recall8")
            r16_m, r16_s = ms("recall16")
            c_m, c_s = ms("calls")
            sel_m, _ = ms("selectivity")

            r8_str = f"{r8_m:.3f} +/- {r8_s:.2f}"
            r16_str = f"{r16_m:.3f} +/- {r16_s:.2f}"
            c_str = f"{c_m:.2f}"
            sel_str = f"{sel_m:8.2f}" if sel_m is not None else "       -"
            print(f"{c:18s} {t:5d} {r8_str:>12s} {r16_str:>12s} {c_str:>8s} {sel_str:>12s}")

    total_time = round(time.time() - t0, 1)
    out = {
        "version": "0.7.0",
        "description": "Read-time goal-conditioned SetpointLayer benchmark evaluating recovery post goal-switch.",
        "protocol": {
            "N_F": N_F,
            "G": G,
            "K": K,
            "N_HUB": N_HUB,
            "D_EMB": D_EMB,
            "T": T,
            "switch": SWITCH,
            "wipes": WIPES,
            "p_con": P_CON,
            "p_hub": P_HUB,
            "window": WINDOW,
            "B": B,
            "max_calls": MAX_CALLS,
            "seeds": SEEDS,
            "hebb": {"eta": HEBB_ETA, "lam": HEBB_LAM},
            "flux": {"D0": FLUX_D0, "mu": FLUX_MU, "dt": FLUX_DT, "leak": FLUX_LEAK},
            "setpoint": {
                "n_steps": SETPOINT_STEPS,
                "gamma": SETPOINT_GAMMA,
                "leak": SETPOINT_LEAK,
                "dt": 0.1,
                "decay": 0.05,
            },
        },
        "summary": summary,
        "raw": res,
        "runtime_s": total_time,
    }

    out_path = Path(__file__).resolve().parent / "benchmark_results_v070.json"
    with open(out_path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nWritten benchmark results to {out_path} ({total_time}s)")


if __name__ == "__main__":
    run()
