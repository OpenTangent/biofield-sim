#!/usr/bin/env python3
"""
biofield_sim v0.5.0 — Matched-protocol reservoir benchmark
Author: Amity, 2026-09-02

Compares three substrates under ONE protocol, with an honest baseline:
  ESN        — leaky tanh Echo State Network (Jaeger 2001), the conventional baseline
  FHN        — FitzHugh-Nagumo bioelectric lattice (continuous, gap-junction coupled)
  PHYSARUM   — Hagen-Poiseuille memristive fluidic reservoir (radii remodel with flux)

Tasks (ridge-regression linear readout, washout 200, 70/30 train/test):
  MC       — linear memory capacity, sum_k r^2(u(t-k), yhat_k), k = 1..20 (Jaeger 2002)
  NARMA10  — NRMSE on the NARMA-10 benchmark
  Noise    — retention = MC(sigma)/MC(0) with Gaussian noise injected into state dynamics

State dimensionality is matched per comparison (ESN N = substrate state size).
5 seeds. Everything printed here is written to benchmark_results_v050.json.
"""
import json, time, sys
import numpy as np

T_TOTAL, WASHOUT, K_MAX = 1500, 200, 20
SEEDS = [0, 1, 2, 3, 4]
SIGMAS = [0.0, 0.05, 0.1, 0.2]
RIDGE = 1e-4

# ------------------------------------------------------------------ substrates
class ESN:
    def __init__(self, n, seed, rho=0.9, leak=0.3, in_scale=0.5):
        rng = np.random.default_rng(seed)
        W = rng.standard_normal((n, n)) * (rng.random((n, n)) < 0.1)
        eig = np.max(np.abs(np.linalg.eigvals(W)))
        self.W = W * (rho / eig if eig > 0 else 1.0)
        self.Win = rng.uniform(-in_scale, in_scale, n)
        self.leak, self.n = leak, n
        self.x = np.zeros(n)
    def step(self, u, sigma, rng):
        pre = self.W @ self.x + self.Win * u
        self.x = (1 - self.leak) * self.x + self.leak * np.tanh(pre)
        if sigma > 0: self.x += rng.normal(0, sigma, self.n)
        return self.x.copy()

class FHNLattice:
    def __init__(self, nx, ny, seed, g_gap=0.2, dt=0.05, a=0.7, b=0.8, eps=0.08, in_scale=1.0):
        rng = np.random.default_rng(seed)
        self.nx, self.ny, self.g, self.dt, self.a, self.b, self.eps = nx, ny, g_gap, dt, a, b, eps
        self.u = rng.normal(0, 0.1, (nx, ny)); self.v = np.zeros((nx, ny))
        # heterogeneous input weights over the whole field (a reservoir needs input diversity)
        self.Win = rng.uniform(-in_scale, in_scale, (nx, ny))
        self.n = nx * ny
    def step(self, inp, sigma, rng):
        u = self.u
        lap = np.zeros_like(u)
        lap[:-1,:] += u[1:,:] - u[:-1,:]; lap[1:,:] += u[:-1,:] - u[1:,:]
        lap[:,:-1] += u[:,1:] - u[:,:-1]; lap[:,1:] += u[:,:-1] - u[:,1:]
        du = (u - u**3/3 - self.v + self.Win * inp + self.g * lap) * self.dt
        dv = self.eps * (u + self.a - self.b * self.v) * self.dt
        self.u = u + du; self.v = self.v + dv
        if sigma > 0: self.u += rng.normal(0, sigma, u.shape) * np.sqrt(self.dt)
        return self.u.ravel().copy()

class Physarum:
    def __init__(self, n_nodes, seed, edge_prob=0.35, lam=0.05, gamma=0.2, alpha=1.5, beta=0.5, eta=0.01, dt=0.1):
        rng = np.random.default_rng(seed)
        adj = (rng.random((n_nodes, n_nodes)) < edge_prob).astype(float)
        np.fill_diagonal(adj, 0); adj = np.maximum(adj, adj.T)
        for i in range(n_nodes - 1): adj[i, i+1] = adj[i+1, i] = 1.0
        self.edges = np.array([(i, j) for i in range(n_nodes) for j in range(i+1, n_nodes) if adj[i, j] > 0])
        self.n_nodes, self.n = n_nodes, len(self.edges)
        self.R = np.full(self.n, 0.5); self.L = np.ones(self.n)
        self.lam, self.gamma, self.alpha, self.beta, self.eta, self.dt = lam, gamma, alpha, beta, eta, dt
        # input pattern: heterogeneous injection across nodes (zero-sum so flow is well-posed)
        w = rng.uniform(-1, 1, n_nodes); self.Win = w - w.mean()
    def step(self, inp, sigma, rng):
        C = np.pi * self.R**4 / (8 * self.eta * self.L)
        i, j = self.edges[:, 0], self.edges[:, 1]
        K = np.zeros((self.n_nodes, self.n_nodes))
        np.add.at(K, (i, i), C); np.add.at(K, (j, j), C); np.add.at(K, (i, j), -C); np.add.at(K, (j, i), -C)
        I = self.Win * inp
        P = np.zeros(self.n_nodes)
        try: P[1:] = np.linalg.solve(K[1:, 1:], I[1:])
        except np.linalg.LinAlgError: pass
        Q = C * (P[i] - P[j])
        aQ = np.abs(Q)
        f = self.gamma * aQ**self.alpha / (1 + self.beta * aQ**self.alpha)
        self.R = self.R + (f - self.lam * self.R) * self.dt
        if sigma > 0: self.R += rng.normal(0, sigma, self.n) * self.dt
        self.R = np.clip(self.R, 0.05, 5.0)
        return self.R.copy()

# ------------------------------------------------------------------ protocol
def ridge_fit_predict(Xtr, ytr, Xte):
    Xtr = np.hstack([Xtr, np.ones((len(Xtr), 1))]); Xte = np.hstack([Xte, np.ones((len(Xte), 1))])
    W = np.linalg.solve(Xtr.T @ Xtr + RIDGE * np.eye(Xtr.shape[1]), Xtr.T @ ytr)
    return Xte @ W

def r2(y, yh):
    v = np.var(y); return 0.0 if v == 0 else max(0.0, 1 - np.mean((y - yh)**2) / v)

def nrmse(y, yh): return float(np.sqrt(np.mean((y - yh)**2) / np.var(y)))

def collect_states(sub, u, sigma, seed):
    rng = np.random.default_rng(10_000 + seed)
    X = np.zeros((len(u), sub.n))
    for t in range(len(u)):
        X[t] = sub.step(u[t], sigma, rng)
    if not np.all(np.isfinite(X)): X = np.nan_to_num(X, nan=0.0, posinf=0.0, neginf=0.0)
    return X

def memory_capacity(X, u):
    split = WASHOUT + int(0.7 * (len(u) - WASHOUT)); mc = 0.0
    for k in range(1, K_MAX + 1):
        y = np.roll(u, k)
        yh = ridge_fit_predict(X[WASHOUT:split], y[WASHOUT:split], X[split:])
        mc += r2(y[split:], yh)
    return mc

def narma10(u):
    y = np.zeros(len(u))
    for t in range(10, len(u) - 1):
        y[t+1] = 0.3*y[t] + 0.05*y[t]*np.sum(y[t-9:t+1]) + 1.5*u[t-9]*u[t] + 0.1
    return y

def narma_score(X, u):
    y = narma10(u); split = WASHOUT + int(0.7 * (len(u) - WASHOUT))
    yh = ridge_fit_predict(X[WASHOUT:split], y[WASHOUT:split], X[split:])
    return nrmse(y[split:], yh)

def make(kind, seed):
    if kind == "FHN": return FHNLattice(8, 8, seed)            # n = 64
    if kind == "PHYSARUM": return Physarum(15, seed)             # n = n_edges (~50-60)
    raise ValueError

def run():
    t0 = time.time(); out = {"version": "0.5.0", "protocol": {"T": T_TOTAL, "washout": WASHOUT, "k_max": K_MAX, "seeds": SEEDS, "sigmas": SIGMAS, "ridge": RIDGE}, "results": {}}
    for kind in ["FHN", "PHYSARUM"]:
        rows = {"substrate": {"mc": {s: [] for s in SIGMAS}, "narma_nrmse": []},
                "esn_matched": {"mc": {s: [] for s in SIGMAS}, "narma_nrmse": []}, "state_dim": None}
        for seed in SEEDS:
            rng = np.random.default_rng(seed)
            u_mc = rng.uniform(-0.5, 0.5, T_TOTAL); u_na = rng.uniform(0, 0.5, T_TOTAL)
            sub0 = make(kind, seed); n = sub0.n; rows["state_dim"] = int(n)
            for label, ctor in [("substrate", lambda: make(kind, seed)), ("esn_matched", lambda: ESN(n, seed))]:
                for s in SIGMAS:
                    rows[label]["mc"][s].append(memory_capacity(collect_states(ctor(), u_mc, s, seed), u_mc))
                rows[label]["narma_nrmse"].append(narma_score(collect_states(ctor(), u_na, 0.0, seed), u_na))
        summ = {"state_dim": rows["state_dim"]}
        for label in ["substrate", "esn_matched"]:
            mc0 = np.array(rows[label]["mc"][0.0])
            summ[label] = {
                "mc_mean_by_sigma": {str(s): float(np.mean(rows[label]["mc"][s])) for s in SIGMAS},
                "mc_std_by_sigma": {str(s): float(np.std(rows[label]["mc"][s])) for s in SIGMAS},
                "retention_pct_by_sigma": {str(s): float(100 * np.mean(np.array(rows[label]["mc"][s]) / np.maximum(mc0, 1e-9))) for s in SIGMAS},
                "narma10_nrmse_mean": float(np.mean(rows[label]["narma_nrmse"])),
                "narma10_nrmse_std": float(np.std(rows[label]["narma_nrmse"])),
            }
        out["results"][kind] = summ
        print(f"\n=== {kind} (state dim {summ['state_dim']}) vs matched ESN ===")
        for label in ["substrate", "esn_matched"]:
            r = summ[label]
            print(f"  {label:12s} MC(σ=0)={r['mc_mean_by_sigma']['0.0']:.2f}±{r['mc_std_by_sigma']['0.0']:.2f}  "
                  f"retention σ=0.1: {r['retention_pct_by_sigma']['0.1']:.1f}%  σ=0.2: {r['retention_pct_by_sigma']['0.2']:.1f}%  "
                  f"NARMA10 NRMSE={r['narma10_nrmse_mean']:.3f}±{r['narma10_nrmse_std']:.3f}")
    out["execution_time_sec"] = time.time() - t0
    with open("benchmark_results_v050.json", "w") as f: json.dump(out, f, indent=2)
    print(f"\nWritten benchmark_results_v050.json in {out['execution_time_sec']:.1f}s")

if __name__ == "__main__": run()
