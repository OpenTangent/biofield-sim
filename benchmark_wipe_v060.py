#!/usr/bin/env python3
"""
biofield_sim v0.6.0 — LLM-free wipe-resumption benchmark for memory dynamics
Author: Amity, 2026-09-02

Tests the Morphological Memory hypothesis (manuscript §5) directly:
after a context wipe, with only the pinned goal as query, how well does
each memory condition recover the goal's hidden constraint set?

World
  160 fact nodes + 4 goal nodes. Each goal has K=8 constraint facts (rare,
  goal-specific). 16 hub distractors (frequent, co-occur with every goal).
  Remaining facts are sporadic distractors. Goal switches g0 -> g1 at T/2.
  Observation stream per step: constraint of active goal p=0.25, hub p=0.40,
  sporadic p=0.35. Context window = last 3 observations + active goal.

Conditions (same stream, same seeds)
  FLAT  cosine similarity of stored facts to the goal embedding (standard RAG)
  HEBB  co-activation increments + exponential decay (manuscript §4.2)
  FLUX  same edge creation and same two-hop read as HEBB, but conductance is
        remodelled by Tero et al. (2010): sources = context nodes, sink = goal,
        dD/dt = |Q|^mu / (1+|Q|^mu) - D.   Only the write rule differs.

Embedding regimes (affect FLAT only; graph conditions are embedding-free)
  semantic    constraint embedding = goal embedding + noise (relevance is similar)
  structural  constraint embedding independent of goal (relevance is not similar)

Wipe points: t=800 (g0 settled), t=1100 (100 steps after switch), t=1900 (g1 settled)
Metrics: recall@8, recall@16, calls-to-recover (8 per call, max 10; 11 = failed),
         goal selectivity = mean w(goal,own constraints) / mean w(goal,hubs),
         sparsity = fraction of created edges with weight > 0.1 * max.
30 seeds. Everything printed is written to benchmark_results_v060.json.
"""
import json, time
import numpy as np

N_F, G, K, N_HUB, D_EMB = 160, 4, 8, 16, 32
T, SWITCH, WIPES = 2000, 1000, [800, 1100, 1900]
P_CON, P_HUB = 0.25, 0.40
WINDOW, B, MAX_CALLS = 3, 8, 10
SEEDS = list(range(30))
HEBB_ETA, HEBB_LAM = 1.0, 0.002
FLUX_D0, FLUX_MU, FLUX_DT, FLUX_LEAK = 0.01, 1.5, 0.2, 1e-6
N = N_F + G

def unit(v): return v / (np.linalg.norm(v, axis=-1, keepdims=True) + 1e-12)

class World:
    def __init__(self, seed):
        rng = np.random.default_rng(seed); self.rng = rng
        facts = rng.permutation(N_F)
        self.con = {g: facts[g*K:(g+1)*K] for g in range(G)}
        self.hubs = facts[G*K:G*K+N_HUB]
        self.spor = facts[G*K+N_HUB:]
        self.goal_node = {g: N_F + g for g in range(G)}
        gv = unit(rng.normal(size=(G, D_EMB)))
        self.emb = {}
        for reg in ("semantic", "structural"):
            E = unit(rng.normal(size=(N_F, D_EMB)))
            E[self.hubs] = unit(gv.mean(0) + 0.5 * rng.normal(size=(N_HUB, D_EMB)))
            if reg == "semantic":
                for g in range(G): E[self.con[g]] = unit(gv[g] + 1.0 * rng.normal(size=(K, D_EMB)))
            self.emb[reg] = (E, gv)
    def goal_at(self, t): return 0 if t < SWITCH else 1
    def observe(self, t):
        g = self.goal_at(t); u = self.rng.random()
        if u < P_CON: return int(self.rng.choice(self.con[g]))
        if u < P_CON + P_HUB: return int(self.rng.choice(self.hubs))
        return int(self.rng.choice(self.spor))

class Flat:
    def __init__(self, w): self.w = w; self.seen = np.zeros(N_F, bool)
    def step(self, ctx, goal): self.seen[[c for c in ctx if c < N_F]] = True
    def scores(self, goal, reg):
        E, gv = self.w.emb[reg]; s = E @ gv[goal]
        return np.where(self.seen, s, -np.inf)

class Hebb:
    def __init__(self, w): self.W = np.zeros((N, N))
    def step(self, ctx, goal):
        act = list(ctx) + [N_F + goal]
        for a in act:
            for b in act:
                if a != b: self.W[a, b] += HEBB_ETA
        self.W *= (1 - HEBB_LAM)
    def scores(self, goal, reg): return two_hop(self.W, N_F + goal)

class Flux:
    def __init__(self, w): self.D = np.zeros((N, N)); self.adj = np.zeros((N, N), bool)
    def step(self, ctx, goal):
        gn = N_F + goal; act = list(ctx) + [gn]
        for a in act:
            for b in act:
                if a != b and not self.adj[a, b]:
                    self.adj[a, b] = True; self.D[a, b] = FLUX_D0
        I = np.zeros(N)
        for c in ctx: I[c] += 1.0 / len(ctx)
        I[gn] -= 1.0
        L = np.diag(self.D.sum(1) + FLUX_LEAK) - self.D
        P = np.linalg.solve(L, I)
        Q = np.abs(self.D * (P[:, None] - P[None, :]))
        f = Q**FLUX_MU / (1 + Q**FLUX_MU)
        self.D = np.where(self.adj, self.D + FLUX_DT * (f - self.D), 0.0)
        self.D = np.maximum(self.D, np.where(self.adj, 1e-4, 0.0))
    def scores(self, goal, reg): return two_hop(self.D, N_F + goal)

def two_hop(W, gn):
    a = W[gn].copy(); a[gn] = 0
    s = a + 0.5 * (W @ a) / (a.max() + 1e-12)
    s[N_F:] = -np.inf
    return s[:N_F]

def evaluate(scores, target):
    order = np.argsort(-scores); order = order[np.isfinite(scores[order])]
    tgt = set(int(x) for x in target)
    r8 = len(tgt & set(order[:B].tolist())) / K
    r16 = len(tgt & set(order[:2*B].tolist())) / K
    found, calls = set(), 0
    for c in range(MAX_CALLS):
        calls += 1; found |= set(order[c*B:(c+1)*B].tolist())
        if tgt <= found: break
    else: calls = MAX_CALLS + 1
    return r8, r16, calls

def selectivity_sparsity(W, w, goal):
    gn = N_F + goal
    own = W[gn, w.con[goal]].mean(); hub = W[gn, w.hubs].mean()
    sel = float(own / (hub + 1e-12))
    nz = W[W > 0]; sp = float((nz > 0.1 * nz.max()).mean()) if nz.size else 0.0
    return sel, sp

def run():
    t0 = time.time()
    conds = {"FLAT_semantic": ("FLAT", "semantic"), "FLAT_structural": ("FLAT", "structural"),
             "HEBB": ("HEBB", None), "FLUX": ("FLUX", None)}
    res = {c: {str(t): {"recall8": [], "recall16": [], "calls": [], "selectivity": [], "sparsity": []} for t in WIPES} for c in conds}
    for seed in SEEDS:
        w = World(seed)
        mems = {"FLAT": Flat(w), "HEBB": Hebb(w), "FLUX": Flux(w)}
        ctx = []
        for t in range(T):
            ctx = (ctx + [w.observe(t)])[-WINDOW:]; g = w.goal_at(t)
            for m in mems.values(): m.step(ctx, g)
            if t + 1 in WIPES:
                for cname, (kind, reg) in conds.items():
                    r8, r16, calls = evaluate(mems[kind].scores(g, reg), w.con[g])
                    row = res[cname][str(t + 1)]
                    row["recall8"].append(r8); row["recall16"].append(r16); row["calls"].append(calls)
                    if kind in ("HEBB", "FLUX"):
                        sel, sp = selectivity_sparsity(mems[kind].W if kind == "HEBB" else mems[kind].D, w, g)
                        row["selectivity"].append(sel); row["sparsity"].append(sp)
        print(f"seed {seed} done ({time.time()-t0:.0f}s)", flush=True)
    summary = {}
    print(f"\n{'condition':16s} {'wipe':>5s} {'recall@8':>9s} {'recall@16':>10s} {'calls':>6s} {'select.':>8s} {'sparsity':>9s}")
    for c in conds:
        summary[c] = {}
        for t in WIPES:
            r = res[c][str(t)]; ms = lambda k: (float(np.mean(r[k])), float(np.std(r[k]))) if r[k] else (None, None)
            summary[c][str(t)] = {k: {"mean": ms(k)[0], "std": ms(k)[1]} for k in r}
            sel = f"{ms('selectivity')[0]:8.2f}" if r["selectivity"] else "       -"
            sp = f"{ms('sparsity')[0]:9.3f}" if r["sparsity"] else "        -"
            print(f"{c:16s} {t:5d} {ms('recall8')[0]:9.3f} {ms('recall16')[0]:10.3f} {ms('calls')[0]:6.2f} {sel} {sp}")
    out = {"version": "0.6.0", "protocol": {"N_F": N_F, "G": G, "K": K, "N_HUB": N_HUB, "T": T, "switch": SWITCH, "wipes": WIPES,
           "p_con": P_CON, "p_hub": P_HUB, "window": WINDOW, "B": B, "max_calls": MAX_CALLS, "seeds": SEEDS,
           "hebb": {"eta": HEBB_ETA, "lam": HEBB_LAM}, "flux": {"D0": FLUX_D0, "mu": FLUX_MU, "dt": FLUX_DT}},
           "summary": summary, "raw": res, "runtime_s": round(time.time() - t0, 1)}
    with open("benchmark_results_v060.json", "w") as f: json.dump(out, f, indent=1)
    print(f"\nwritten benchmark_results_v060.json ({out['runtime_s']}s)")

if __name__ == "__main__": run()
