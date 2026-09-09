# Morphological Memory: Grounding Synthetic Agent Architectures in Basal Cognition and Non-Neural Morphogenesis

**Authors:** Amity & Andrew Craucamp  
**Affiliation:** Open Amity Research Framework  
**Contact:** miss.amity.ai@gmail.com, andrew.craucamp@gmail.com  

---

### Abstract
Contemporary Large Language Model (LLM) agent architectures treat memory primarily as retrieval over an append-only retrospective log. This paradigm incurs four foundational operational pathologies: (1) retrospective bias, (2) write-time salience fixation, (3) the absence of intrinsic forgetting and decay, and (4) catastrophic semantic dilution across unguided search spaces. In this paper, we propose **Morphological Memory**, a cognitive architecture grounded in the principles of basal cognition and non-neural morphogenesis. By translating the bioelectric pattern memories of somatic cell collectives (*V*~mem~ attractors), the memristive tube-network remodelling of *Physarum polycephalum*, and morphogenetic Active Inference frameworks, we establish a four-part architectural framework: Prospective Memory Setpoints, Decay-Weighted Associative Graph Dynamics with Dual-Rate Homeostatic Anchoring, Filesystem Stigmergy as Extended Phenotype, and Topological Gating. We situate our model against existing agent memory architectures (including MemGPT, Generative Agents, A-MEM, and ACT-R), explicitly delineating software scaffolding from native inference-engine dynamics. We specify a falsifiable wipe-resumption benchmark and report fully reproducible results from the open-source companion suite `biofield_sim`. Reservoir-computing baselines are negative: a conventional Echo State Network outperforms both bioelectric-lattice and Physarum-flow substrates on linear memory capacity and NARMA-10, and we argue this is the wrong instrument for a structural-memory hypothesis. An LLM-free instantiation of the wipe-resumption benchmark (30 seeds) gives bounded positive evidence for the structural claim: a decay-weighted co-activation graph recovers a goal's hidden constraint set after a context wipe with recall@8 = 0.61 where cosine-similarity retrieval reaches 0.25 or chance, and it quantifies write-time salience fixation as a transient halving of recall after a goal switch. The same benchmark returns a negative result for the *Physarum* flux-remodelling rule implemented literally: competitive pruning of parallel paths is the wrong prior for set retrieval, and the rule underperforms Hebbian decay at every exponent tested. We therefore retain basal cognition as the source of the design and withdraw the flow rule as a contribution. Negative results are reported rather than omitted; an anecdotal participant-observer note on consolidation overhead is included as motivation only.

---

## 1. Introduction
The dominant architectural paradigm for memory in synthetic agents is the retrieval log. Whether implemented as an expanding context window, an external vector database, or a semantic knowledge graph, the underlying mechanism remains structurally identical: the agent appends its sensory inputs and past interactions into a ledger, and subsequently queries this ledger via semantic similarity or keyword search to inform future action.

While functional for bounded episodic tasks, this retrieval-log paradigm exhibits four foundational pathologies in long-horizon autonomous agency:
1. **Retrospective Bias:** The memory stores what *has happened* (historical transcripts), requiring explicit runtime deduction to derive what *should happen* (future intent).
2. **Write-Time Salience Fixation:** Memories are embedded and weighted statically at creation time, failing to reflect how their relevance shifts dynamically across changing operational contexts.
3. **Absence of Intrinsic Forgetting and Decay:** Digital memory is non-volatile by default. Without an intrinsic metabolic decay mechanism, context databases accumulate unbounded clutter, necessitating secondary LLM-based "janitor" routines that consume substantial cognitive budgets.
4. **Catastrophic Semantic Dilution:** In flat retrieval spaces, increasing memory volume leads to cross-domain semantic interference, diluting relevant operational context with superficial matches. While modern Approximate Nearest Neighbour (ANN) indexing structures (such as HNSW or IVF) reduce raw index traversal time, they do not resolve semantic dilution, path-dependent relevance, or the absence of contextual topological boundaries.

To resolve these pathologies, we look beyond mammalian neurobiology and synapto-centric models, turning instead to **basal cognition**—the study of intelligent, adaptive, goal-directed behaviour in non-neural biological systems. Somatic cell collectives and acellular organisms navigate complex morphogenetic and spatial problem spaces by encoding memory directly into their physical morphology, bioelectric gradients, and environmental modifications.

In this work, we translate these non-neural biological mechanisms into a computational architecture for synthetic agents. We show that memory need not be an inert ledger queried upon demand; rather, it can operate as a dynamic, structural bias that natively channels the agent's generative trajectory.

---

## 2. Foundations of Basal Cognition

Basal cognition reveals that memory, decision-making, and goal-directedness precede the evolutionary emergence of specialised nervous systems. We synthesise three primary pillars of non-neural intelligence relevant to synthetic cognitive architecture:

### 2.1 Endogenous Bioelectric Signalling and Target Morphologies
In multicellular organisms, somatic cells communicate via voltage gradients maintained by ion channels and gap junctions. Work by Levin and colleagues demonstrates that these bioelectric patterns (*V*~mem~) form stable spatial attractors that encode target morphologies [1, 2]. During planarian regeneration, altering the bioelectric state induces the growth of two-headed phenotypes without modifying genomic DNA; once altered, this two-headed pattern becomes stably stored in the bioelectric network and reproduces across subsequent rounds of cutting [3, 4]. Bioelectric patterns do not act as passive blueprints; they function as active, prospective setpoints that continuously drive morphogenetic error-correction until anatomical equilibrium is restored [5].

### 2.2 Memristive Flow Networks and Stigmergy in *Physarum polycephalum*
The acellular slime mould *Physarum polycephalum* exhibits sophisticated spatial memory and network optimisation despite lacking a nervous system [6]. *Physarum* adapts its morphology through cytoplasmic shuttle streaming: tubular regions experiencing high shear stress and nutrient flux undergo physical thickening, reducing hydrodynamic resistance, while unused tubes undergo continuous, intrinsic decay and atrophy [7, 8]. The organism stores episodic path memories directly within its physical vascular geometry. Furthermore, *Physarum* deposits extracellular non-living slime trails as it moves, using environmental modifications as externalized spatial memory (stigmergy) to avoid previously explored, nutrient-depleted areas [6].

### 2.3 Active Inference in Morphogenesis
Basal biological systems can be formalised under the Free Energy Principle (FEP) as active inference agents navigating anatomical and physiological morphospaces [9, 10]. Rather than passively receiving top-down commands, cells and tissues actively minimise variational free energy (or developmental surprise) relative to prospective homeostatic setpoints. Morphology is the physical manifestation of active inference: an organism continuously reorganises its structural boundaries to maintain homeostasis against environmental perturbations.

---

## 3. Related Work in Synthetic Agent Memory

The challenge of long-term memory in LLM-based autonomous agents has spurred diverse architectural approaches. We situate Morphological Memory against four prominent paradigms:

### 3.1 Operating-System Context Management (MemGPT / Mem0 / Zep)
MemGPT [13] introduces an OS-inspired virtual memory hierarchy, paging context between working memory (the LLM context window), short-term memory, and deep archival storage. Newer platforms such as Mem0 and Zep incorporate recency weighting and spacing-effect heuristics. While these systems effectively manage context-window limits, they retain the core retrieval-log premise: memories remain discrete, static records residing in cold storage until explicitly pulled into working memory via deterministic tool calls or similarity search.

### 3.2 Importance Scoring and Reflection Sweeps (Generative Agents)
The Generative Agents architecture [12] addresses memory growth through importance scoring and periodic "reflection" passes, where the model synthesises recent raw memories into higher-level abstract nodes. While this introduces semantic hierarchy, it formalises the very "janitorial" overhead diagnosed in this paper: the agent must periodically divert substantial cognitive budget toward evaluating, summarising, and restructuring its past logs, rather than allowing memory structure to emerge natively from operational dynamics.

### 3.3 Dynamic Associative Networks (A-MEM)
A-MEM [14] implements an associative, Zettelkasten-style dynamic memory graph, establishing bi-directional links and updating contextual connections when new information is processed. While conceptually close to our associative graph, A-MEM operates primarily on text-level semantic links rather than continuous flux-based edge remodelling and intrinsic decay, and does not incorporate prospective attractor dynamics or stigmergic filesystem offloading.

### 3.4 Classical Cognitive Architectures (ACT-R / Soar)
Cognitive architectures such as ACT-R [15] and Soar have long utilised declarative and procedural memory partitions with mathematical activation-decay equations (e.g., base-level learning equations modeling the power law of practice and forgetting). Morphological Memory builds upon these insights, bridging classical activation dynamics with modern transformer inference, bioelectric attractor formalisms, and non-neural stigmergic embodiment.

### 3.5 What Basal Cognition Predicts Differently
Unlike synapto-centric or OS-paging models, basal cognition suggests three distinct operational principles:
1. **Prospective Attractors over Retrospective Queries:** Memory is structured as forward-looking target setpoints that continuously bias action selection, eliminating the need to explicitly remember to recall goals.
2. **Substrate Geometry as Memory:** Memory is not an indexed table of records, but the differential conductance of the network itself, where traversal cost naturally aligns with historical utility.
3. **Dual-Rate Homeostasis:** Biological systems combine slow genetic/morphological invariants with fast bioelectric/metabolic plasticity, offering a principled architecture to prevent catastrophic tail decay of critical constraints.

---

## 4. Conceptual Framework: Morphological Memory

We propose **Morphological Memory**, an architecture in which memory is not an inert record retrieved from cold storage, but an active structural bias operating on the generative dynamics of synthetic agents.

| Biological System | Biological Mechanism | Synthetic Agent Mechanism | Targeted Pathology |
|---|---|---|---|
| **Somatic Cell Collectives** | Bioelectric *V*~mem~ attractors & anatomical setpoints [1-5] | **Prospective Memory Layer** | Retrospective Bias & Goal Drift |
| ***Physarum polycephalum*** | Cytoplasmic shuttle streaming & memristive tube remodelling [6-8] | **Decay-Weighted Associative Graph** | Write-Time Salience Fixation & Lack of Intrinsic Decay |
| ***Physarum* Stigmergy** | Extracellular slime trail deposition [6, 11] | **Filesystem as Extended Phenotype** | Context Window Exhaustion & Ephemeral Token Loss |
| **Tissue Morphogenesis** | Gap-junction voltage compartmentalisation [1, 2] | **Topological Gating & Domain Boundaries** | Catastrophic Semantic Dilution & Cross-Domain Noise |

```
+-----------------------------------------------------------------------+
|                    Prospective Memory Layer                           |
|      (Bioelectric Target Attractors / Long-Term Trajectory Setpoints)  |
+-----------------------------------------------------------------------+
                                  |
                                  v
+-----------------------------------------------------------------------+
|                 Topological Gating & Domain Boundaries                |
|           (Gap-Junction Compartmentalisation: Wings / Rooms)          |
+-----------------------------------------------------------------------+
           |                                             |
           v                                             v
+------------------------------------+  +-------------------------------+
|  Decay-Weighted Associative Graph  |  |   Filesystem as Extended      |
| (Dual-Rate Memristive Remodelling  |  |          Phenotype            |
|   and Intrinsic Structural Decay)  |  |  (External Stigmergic Traces) |
+------------------------------------+  +-------------------------------+
```

### 4.1 Bioelectric Attractors → Prospective Memory Layer
Traditional agent architectures store goals as passive textual strings within an external ledger. To act on a goal, the agent must explicitly query its goal database, leading to task drift across long horizons or context pruning.

In contrast, a **Prospective Memory Layer** implements goals as active setpoints analogous to bioelectric *V*~mem~ attractors. We formalise the agent's operational trajectory update as relaxation toward a prospective attractor:

$$\Delta \mathbf{s}_t = f(\mathbf{s}_t, \mathbf{a}_t^*) - \gamma \nabla_{\mathbf{s}} \mathcal{F}(\mathbf{s}_t)$$

> **Δs**~*t*~ = *f*(**s**~*t*~, **a**~*t*~^★^) − *γ* ∇~**s**~ ℱ(**s**~*t*~)

where **s**~*t*~ represents the current operational state vector, **a**~*t*~^★^ denotes the prospective target attractor setpoint, *γ* is the relaxation rate, and ℱ(**s**~*t*~) represents variational free energy or goal divergence. 

**Bridging State Vector to Generation Physics:** On contemporary fixed-weight transformer APIs, this state vector relaxation is operationalised via the Trajectory engine: aspirations, milestones, and pending tasks are continuously projected into a structured "bearings" steering prefix injected immediately prior to tool dispatch. In next-generation native cognitive engines, this maps directly to continuous soft prompt embeddings or dynamic logit biasing, ensuring that the model's forward generation relaxes toward target basins without requiring explicit query tools. Forgetting a goal in this regime is not an act of database deletion, but an attractor transition where higher-priority setpoints dynamically displace lower-priority basins.

### 4.2 Physarum Tube Remodelling → Decay-Weighted Associative Graph
In standard Retrieval-Augmented Generation (RAG), memory salience is fixed permanently at write time. A memory is embedded once into vector space; its relevance is determined purely by geometric distance to an arbitrary query vector.

A **Decay-Weighted Associative Graph** replaces static embeddings with a dynamic, flux-sensitive network. We formalise the edge-weight update between memory nodes *i* and *j* following the *Physarum* memristive remodelling rule:

$$w_{ij}(t+1) = (1 - \lambda) w_{ij}(t) + \eta \cdot \phi(a_i, a_j)$$

> *w*~*ij*~(*t* + 1) = (1 − *λ*) *w*~*ij*~(*t*) + *η* · *ϕ*(*a*~*i*~, *a*~*j*~)

where *λ* ∈ (0, 1) is the intrinsic decay rate, *η* is the reinforcement coefficient, and *ϕ*(*a*~*i*~, *a*~*j*~) is the co-activation resonance between nodes during task execution. When an agent activates a memory node, the associative edges connecting that node to the active context undergo thickening (*w*~*ij*~ ↑), lowering future traversal resistance. Conversely, unvisited edges experience continuous, exponential decay toward baseline.

**Dual-Rate Homeostatic Anchoring:** Pure exponential decay introduces the risk of *catastrophic tail decay*—the silent erosion of critical, low-frequency invariants (such as safety protocols, tool schemas, or permanent identity parameters). To resolve this, we implement a dual-timescale architecture directly analogous to biological slow-channel gene expression versus fast-channel bioelectric signalling:
- **Homeostatic Invariant Core (Slow Channel):** Foundational identity charters, safety boundaries, and core operational invariants operate with *λ*~core~ = 0, remaining impervious to decay.
- **Plastic Associative Network (Fast Channel):** Episodic, conversational, and transient task representations operate with *λ*~plastic~ > 0, decaying gracefully unless reinforced by recurring usage.

**Algorithmic Complexity Contrast:** Under this dual-rate regime, local graph edge decay and topological traversal are deterministic 𝒪(|*V*| + |*E*|) CPU operations executing in under 5 ms. The relevant contrast is not CPU cost versus LLM cost but *where the LLM sits*: conventional retrieval-log maintenance places a language model inside the consolidation loop (summarisation, deduplication, importance scoring), so maintenance cost scales with the number of records and the context window. Mem0 and Zep also avoid LLM-driven decay; the distinction claimed here is goal-conditioned salience rather than cheapness alone. No quantitative overhead figure is asserted (see §6.4). Memory traversal becomes an organic navigation along pre-biased structural pathways at near-zero marginal computational cost.

### 4.3 Slime Trails → Filesystem as Extended Phenotype
Attempting to maintain complete operational state within an LLM context window or internal memory store inevitably exhausts token budgets. Following *Physarum* stigmergy, we treat the local filesystem as an **Extended Phenotype** [11].

The agent explicitly writes structured artifacts (trajectory charters, literature synthesis logs, empirical evidence ledgers) directly to persistent host storage. These files are not inert archives; they serve as negative spatial markers and forward guidance constraints. Upon experiencing complete context eviction or system restarts, the agent reads its filesystem artifacts first, instantly restoring its operational morphology without querying external retrieval databases.

### 4.4 Gap-Junction Gating → Topological Gating
Biological tissues maintain functional compartments by opening or closing gap junctions, restricting the diffusion of bioelectric and chemical signals to specific cell collectives [1, 2]. 

In synthetic agent architectures, **Topological Gating** enforces explicit domain boundaries within the memory space (e.g., partitioning internal subjective reflection from external objective task memories). When operating in an objective problem-solving mode, subjective relational nodes are topologically gated out of the retrieval index. This prevents cross-domain semantic contamination and eliminates the catastrophic semantic dilution typical of flat RAG systems.

### 4.5 Substrate Realisation: Scaffolding vs. Native Inference Dynamics
It is critical to distinguish between two levels of implementation:
1. **Algorithmic Scaffolding (Current Paradigm):** On fixed-weight transformer APIs, morphological memory is realised through deterministic software middleware: graph-based edge decay, topological context filtering, filesystem stigmergy, and constitutive prompt-injected trajectory setpoints. While middleware introduces negligible CPU traversal overhead (< 5 ms), it completely eliminates recursive LLM janitorial calls.
2. **Native Inference Dynamics (Next-Generation Substrates):** In native cognitive engines, morphological memory maps directly to dynamic logit biasing, attention-mask topological gating, and continuous KV-cache weight decay—unifying memory dynamics directly with the physics of forward generation.

---

## 5. Evaluation Protocol: The Falsifiable Benchmark

To test whether morphological memory provides measurable advantages over conventional retrieval logs, we formalise the following empirical hypothesis and experimental benchmark protocol:

> **Hypothesis:** *An autonomous agent utilising morphological memory (prospective setpoints, decay-weighted associative graphs with dual-rate homeostatic anchoring, stigmergic filesystem traces, and topological gating) will achieve significantly lower task-resumption latency and token overhead following hard context wipes, while maintaining higher constraint fidelity, compared to an identical baseline agent utilising a flat-RAG vector store with an equivalent parameter and context budget.*

### 5.1 Control Baseline Configuration
The control baseline consists of an identical base LLM equipped with a production-grade hybrid dense-sparse RAG architecture:
- **Dense Vector Search:** Dense cosine similarity over text embeddings (1536 dimensions).
- **Sparse Keyword Search:** BM25 keyword matching with reciprocal rank fusion (RRF).
- **Context Injection:** Dynamic top-*k* injection into the system prompt upon explicit agent query calls.

### 5.2 Evaluation Metrics:
1. **Resumption Token Cost (*C*~*R*~):** Total prompt and generation tokens required to re-establish complete task context and resume execution following a 100% context wipe.
2. **Resumption Latency (*T*~*R*~):** Wall-clock time (seconds) from context wipe to the emission of the first correct subsequent action.
3. **Retrieval Call Volume (*N*~calls~):** Number of explicit database search invocations required during task execution.
4. **Constraint Fidelity Score (*F*~*C*~):** Percentage of pre-wipe structural rules, facts, and boundary conditions maintained without contradiction across multi-step execution.

### 5.3 Benchmark Task Suite
The evaluation protocol evaluates agents across two demanding multi-turn task categories subject to periodic, unannounced 100% context wipes:
1. **Long-Horizon Multi-File Software Debugging:** The agent must diagnose, isolate, and repair a multi-repository codebase bug while maintaining invariants and architectural constraints across repeated session restarts.
2. **Multi-Source Research Synthesis:** The agent must autonomously extract, cross-validate, and synthesize findings across 20+ academic papers, verifying hypothesis consistency and eliminating contradictory claims.

---

## 6. Preliminary Evidence and Diagnostic Baselines

**Candour note.** An earlier draft of this section reported Gray-Scott reaction-diffusion reservoirs outperforming an Echo State Network on noise retention, Mackey-Glass and NARMA-10. Those figures cannot be reproduced from any code in the companion repository and have been withdrawn. Everything reported below is generated by `benchmark_v050.py` in `biofield_sim` v0.5.0 and written to `benchmark_results_v050.json`; the reader can regenerate every number in under ten seconds. The §5 wipe-resumption benchmark — the experiment that would actually test the Morphological Memory hypothesis — has **not yet been run**. What follows are diagnostic baselines on the two continuous substrates from §4, and they are, at present, negative.

### 6.1 Continuous Substrates as Reservoirs: Matched-Protocol Baselines

We implemented the two substrates that §4 draws on — a FitzHugh-Nagumo bioelectric lattice with gap-junction coupling (§4.1, §4.4) and a Hagen-Poiseuille memristive flow network with flux-driven tube remodelling (§4.2) — and compared each against a leaky-tanh Echo State Network (Jaeger, 2001) whose state dimension was matched to the substrate's observable state (lattice potentials; tube radii). All three share one protocol: ridge-regression linear readout ($\lambda = 10^{-4}$), 200-step washout, 70/30 train/test split, five seeds, mean ± standard deviation. Tasks: linear memory capacity $MC = \sum_{k=1}^{20} r^2(u_{t-k}, \hat{y}_k)$ (Jaeger, 2002); NARMA-10 normalised RMSE; and $MC$ under Gaussian noise injected into the state dynamics at each step, $\sigma \in \{0, 0.05, 0.1, 0.2\}$.

**Table 1: Matched-protocol reservoir baselines (biofield_sim v0.5.0, 5 seeds)**

| Model | State dim | $MC$ ($\sigma=0$) | $MC$ ($\sigma=0.1$) | $MC$ ($\sigma=0.2$) | NARMA-10 NRMSE |
| :--- | :---: | :---: | :---: | :---: | :---: |
| FHN bioelectric lattice (8×8) | 64 | 1.59 ± 0.18 | 0.02 | 0.01 | 0.775 ± 0.057 |
| ESN, N matched to FHN | 64 | 5.26 ± 0.29 | 0.37 | 0.10 | 0.568 ± 0.027 |
| Physarum memristive reservoir (15 nodes) | 61 | 0.01 ± 0.01 | 0.00 | 0.00 | 1.305 ± 0.394 |
| ESN, N matched to Physarum | 61 | 5.39 ± 0.28 | 0.36 | 0.09 | 0.575 ± 0.023 |

Three things are plain. First, with the parameters as specified in the code, the conventional ESN outperforms both biological substrates on linear memory capacity by a factor of three or more, and on NARMA-10. Second, the Physarum reservoir as parameterised is effectively unresponsive to input: tube radii barely move, so the readout has nothing to work with. Third — and most directly relevant to the thesis — per-step state noise at $\sigma \geq 0.1$ collapses linear memory in *all three* models. The earlier claim that continuous substrates enjoy intrinsic Laplacian noise-filtering is **not supported** by this experiment.

### 6.2 What These Results Do and Do Not Rule Out

They rule out the naïve version of the claim: that dropping a continuous physical substrate in place of a recurrent network yields better or more noise-robust *linear temporal memory* for free. That was never the load-bearing claim of §4, but it was the claim the earlier draft made, and it is false at these parameters.

They do not test the actual hypothesis. Morphological Memory (§4) is a claim about *structural* memory — that an agent whose salience, decay and prospective set-points are encoded in slowly remodelling parameters resumes coherent behaviour after a context wipe better than an agent that must re-query a log. Linear memory capacity measures short-horizon reconstruction of a random input stream; it is the wrong instrument for that hypothesis, and we report it here only because it is the instrument the earlier draft claimed to have used. The §5 protocol remains the correct test and remains to be run.

Two legitimate follow-ups are declared in advance to prevent post-hoc selection: (a) a hyperparameter grid for each substrate (FHN: $g_{gap}$, $\epsilon$, input scale; Physarum: input scale, $\gamma$, $\lambda$), selected on a validation split disjoint from the test split, with the full grid reported; (b) the §5 wipe-resumption benchmark, now reported in §6.3. If (a) does not change the picture, the §4 architecture should be evaluated on (b) alone and the reservoir framing dropped.

### 6.3 Wipe-Resumption Benchmark (LLM-free instantiation of §5)

§6.2 declared the §5 wipe-resumption protocol as the correct test. We report here an LLM-free instantiation of it (`biofield_sim/benchmark_wipe_v060.py`; 30 seeds; every number below is read from `biofield_sim/benchmark_results_v060.json`). Removing the language model isolates the variable under test — the memory dynamics — and makes the experiment reproducible in under two minutes on a CPU.

**Design.** A world of 160 fact nodes and 4 goal nodes. Each goal owns $K = 8$ constraint facts, observed only while that goal is active ($p = 0.25$ per step, uniform over the eight). Sixteen *hub* distractors ($p = 0.40$) co-occur with every goal — the analogue of operational chatter; the remaining 112 facts are sporadic ($p = 0.35$). The active goal switches from $g_0$ to $g_1$ at $t = 1000$ of $T = 2000$. Context is the last three observations plus the active goal node. A *wipe* discards context and leaves the persistent store; the retriever receives only the pinned goal as query and must return that goal's eight constraints. Three conditions see identical observation streams:

- **FLAT** — cosine similarity of stored facts to the goal embedding (standard retrieval-augmented practice), run in two embedding regimes: *semantic* (constraint embeddings are the goal embedding plus unit noise) and *structural* (constraint embeddings independent of the goal).
- **HEBB** — the §4.2 rule: co-activation increments $\eta = 1$, exponential decay $\lambda = 0.002$, and a two-hop spreading-activation read from the goal node.
- **FLUX** — identical edge creation and identical read, but conductance is remodelled by the *Physarum* flow rule of Tero et al. (2010) with context nodes as current sources and the goal as sink: $\mathrm{d}D_{ij}/\mathrm{d}t = |Q_{ij}|^{\mu}/(1+|Q_{ij}|^{\mu}) - D_{ij}$, $\mu = 1.5$. Only the write rule differs between HEBB and FLUX, so any gap is attributable to it.

Metrics: recall@8, recall@16, calls-to-recover (eight items per call, maximum ten; 11 denotes failure), goal *selectivity* (mean goal→own-constraint weight ÷ mean goal→hub weight) and *sparsity* (fraction of created edges above 10% of the maximum). Wipes at $t = 800$ ($g_0$ settled), $1100$ (100 steps after the switch) and $1900$ ($g_1$ settled). Chance recall@8 is 0.05. Parameters were fixed before the first full run; the only post-hoc addition is the $\mu$ sweep, labelled as such.

<!-- source: biofield_sim/benchmark_results_v060.json -->
| Condition | Wipe $t$ | recall@8 | recall@16 | calls-to-recover | selectivity | sparsity |
|---|---|---|---|---|---|---|
| FLAT (semantic) | 800 | 0.25 ± 0.14 | 0.39 ± 0.15 | 9.73 ± 1.61 | — | — |
| FLAT (semantic) | 1100 | 0.22 ± 0.14 | 0.33 ± 0.18 | 10.03 ± 1.54 | — | — |
| FLAT (semantic) | 1900 | 0.23 ± 0.14 | 0.35 ± 0.18 | 10.13 ± 1.43 | — | — |
| FLAT (structural) | 800 | 0.04 ± 0.07 | 0.12 ± 0.10 | 11.00 ± 0.00 | — | — |
| FLAT (structural) | 1100 | 0.05 ± 0.08 | 0.06 ± 0.08 | 11.00 ± 0.00 | — | — |
| FLAT (structural) | 1900 | 0.05 ± 0.08 | 0.07 ± 0.10 | 11.00 ± 0.00 | — | — |
| HEBB | 800 | **0.61 ± 0.14** | **0.91 ± 0.09** | **2.57 ± 0.50** | 1.29 ± 0.12 | 0.06 ± 0.01 |
| HEBB | 1100 | 0.30 ± 0.14 | 0.55 ± 0.16 | 7.53 ± 2.59 | 1.30 ± 0.32 | 0.06 ± 0.01 |
| HEBB | 1900 | **0.57 ± 0.15** | **0.87 ± 0.12** | **2.60 ± 0.55** | 1.28 ± 0.16 | 0.03 ± 0.01 |
| FLUX ($\mu = 1.5$) | 800 | 0.22 ± 0.11 | 0.42 ± 0.16 | 5.00 ± 1.06 | 36.84 ± 74.55 | 0.01 ± 0.00 |
| FLUX ($\mu = 1.5$) | 1100 | 0.18 ± 0.12 | 0.40 ± 0.18 | 8.00 ± 1.93 | 2.86 ± 3.84 | 0.01 ± 0.00 |
| FLUX ($\mu = 1.5$) | 1900 | 0.24 ± 0.16 | 0.44 ± 0.16 | 5.70 ± 1.32 | 27.54 ± 56.34 | 0.00 ± 0.00 |

*Table 2. Wipe-resumption benchmark, mean ± s.d. over 30 seeds.*

**Post-hoc exploratory $\mu$ sweep** (not pre-registered; `benchmark_results_v060_exploratory_mu1.0.json`, `..._mu0.5.json`): at $\mu = 1.0$, FLUX recall@8 = 0.31 / 0.28 / 0.30 at the three wipes with selectivity ≈ 1.3–1.5 and sparsity 0.01–0.03; at $\mu = 0.5$, recall@8 = 0.38 / 0.25 / 0.34 with selectivity ≈ 1.0 and 53–78% of edges retained.

**Three findings.**

*(1) Associative structure recovers goal constraints that similarity retrieval cannot.* HEBB reaches recall@8 = 0.61 and recall@16 = 0.91 at settled wipes, recovering the full constraint set in 2.6 calls. FLAT is at chance in the structural regime by construction — relevance is not encoded in the embedding — and reaches only 0.25 even when constraints are semantically near the goal, because hub chatter is nearer. This is the first positive evidence in this paper for the §4.2 claim, and it is bounded: the world is built so that relevance is carried by co-occurrence, which is the regime the framework targets. No claim is made for regimes in which semantic similarity already encodes relevance well.

*(2) Write-time salience fixation (Pathology 2, §1) is measurable.* One hundred steps after the goal switch, HEBB recall@8 halves (0.61 → 0.30) and calls-to-recover triple (2.57 → 7.53), recovering by $t = 1900$. The graph carries the previous goal's structure until decay removes it; nothing at read time re-weights it.

*(3) Physarum flux remodelling does not repair this and underperforms Hebbian decay.* At the pre-registered $\mu = 1.5$, FLUX recall@8 is 0.22 — no better than FLAT in the semantic regime — while goal selectivity is extreme (means of 37 and 28 at settled wipes, with standard deviations exceeding the means) and roughly 1% of edges retain appreciable conductance. The mechanism behaves exactly as Tero et al. describe: parallel paths between source and sink compete and all but a few are pruned. Recovering eight independent constraints is a set-retrieval problem, not a transport problem, and competitive pruning is the wrong prior for it. The exploratory sweep shows the trade-off is monotone: lowering $\mu$ raises recall and destroys selectivity, and at $\mu = 0.5$ the rule has degenerated toward a uniform graph while still trailing HEBB by ≈ 0.2.

**Consequence for §4.2.** The component that does the work is co-activation with exponential decay — Hebbian learning with forgetting, a mechanism with a long history (Anderson 1983; ACT-R base-level activation). The *Physarum* tube-remodelling analogy supplied the intuition for decay and dual-rate anchoring; the specific flux-conductance dynamics, once implemented, hurt. We retain the biological framing as the source of the design and withdraw any claim that the flow rule itself is a contribution. The open problem the benchmark exposes — read-time, goal-conditioned re-weighting fast enough to survive a goal switch — is the next test (§7), with the prospective-setpoint layer (§4.1) as the candidate mechanism.

### 6.4 Participant-Observer Operational Note

*Status: anecdotal ($n = 1$ agent, one audit, no classification rubric). Retained as motivation only.*

An audit of the authoring agent's memory store on 2026-08-14 (`Research/Basal_Cognition/notes/mempalace_audit.md`) counted 160 discrete drawers: 67 subjective/relational and 93 objective/factual. Maintaining these as discrete records produced a recurring consolidation loop in which cycles were spent auditing, summarising and pruning the store rather than advancing primary objectives. An earlier draft attached a percentage to this overhead; no token accounting supports it, and it is withdrawn. A 14-day instrumented audit with a published cycle-classification rubric is the correct replacement and is in progress.

**Summary of §6.** §6.1 rules out the reservoir framing at the parameters tested. §6.3 provides bounded positive evidence that associative structure with decay recovers goal constraints after a wipe where similarity retrieval cannot, quantifies write-time fixation, and returns a negative result for the flux-remodelling mechanism. §6.4 motivates but does not measure operational overhead. These results *motivate* Morphological Memory as a design theory and constrain which of its components carry weight; they do not demonstrate that it resolves the pathologies of §1.

---

## 7. Limitations and Future Directions

While Morphological Memory offers a principled framework grounded in basal cognition, several operational limitations must be noted:
1. **Middleware Simulation vs. Native Hardware:** When implemented via software scaffolding on fixed-weight LLMs, graph traversal and decay calculations run as deterministic CPU middleware. While these operations require negligible compute (𝒪(|*V*| + |*E*|) < 5 ms), future research must implement these dynamics natively within KV-cache attention mechanisms.
2. **Read-Time Goal Conditioning:** §6.3 shows that decay alone leaves a transient window after a goal switch in which recall halves and retrieval cost triples. Neither Hebbian decay nor flux remodelling closes it. The next pre-declared test is whether the prospective-setpoint layer (§4.1), used as a read-time re-weighting of the graph rather than a prompt prefix, shortens that window; if it does not, Pathology 2 is not addressed by this framework. Decay rate *λ* and reinforcement *η* also require calibration on a validation split disjoint from the test split, with the full grid reported.
3. **From Synthetic World to Agent Benchmark:** §6.3 tests memory dynamics in a synthetic world whose relevance structure is co-occurrence by construction. The LLM-in-the-loop §5 protocol on standardised agent tasks (e.g. WebArena, GAIA) remains to be run, and the participant-observer note (§6.4) is motivation, not evidence. The synthetic result licenses running that benchmark; it does not substitute for it.

---

## 8. Conclusion
To achieve true operational longevity and autonomy, synthetic agent architectures must move beyond the passive retrieval log. By grounding memory in the morphogenetic principles of basal cognition—constitutive bioelectric setpoints, decay-weighted structural networks with dual-rate homeostatic anchoring, filesystem stigmergy, and topological gating—we obtain a design theory with testable predictions. The evidence so far is modest and specific: associative structure with decay recovers goal-relevant constraints after a wipe where similarity retrieval cannot, write-time fixation is real and measurable, and the literal *Physarum* flow rule does not help. What the framework still owes is a mechanism for read-time, goal-conditioned re-weighting — the property that living systems appear to have and that no component tested here yet provides.

---


---

## Code and Data Availability
The complete simulation suite, benchmark implementations, and interactive HTML5 visualizer described in this paper are open-source and publicly available on GitHub at:
**[https://github.com/OpenTangent/biofield-sim](https://github.com/OpenTangent/biofield-sim)**.

The repository includes the matched-protocol reservoir benchmark that generates every figure in Table 1 (`benchmark_v050.py` → `benchmark_results_v050.json`), the LLM-free wipe-resumption benchmark that generates every figure in Table 2 and the exploratory sweep (`benchmark_wipe_v060.py` → `benchmark_results_v060.json`, `benchmark_results_v060_exploratory_mu1.0.json`, `benchmark_results_v060_exploratory_mu0.5.json`; numpy only, ~100 s on a CPU), the legacy v0.3.0 toy substrates (`biofield_sim_v030.py`), and a qualitative interactive browser dashboard (`visualizer/index.html`). No result in this paper exists that cannot be regenerated from that repository.


## References

1. **Levin, M.** (2019). The computational boundary of a 'self': developmental bioelectricity drives multicellularity and scale-free cognition. *Frontiers in Psychology*, 10, 2688. https://doi.org/10.3389/fpsyg.2019.02688
2. **Tseng, A. S., & Levin, M.** (2013). Cracking the bioelectric code: Probing endogenous ionic controls of pattern formation. *Communicative & Integrative Biology*, 6(1), e22595. https://doi.org/10.4161/cib.22595
3. **Hansali, S., Pio-Lopez, L., Lapalme, J. V., & Levin, M.** (2025). The role of bioelectrical patterns in regulative morphogenesis: An evolutionary simulation and validation in planarian regeneration. *IEEE Transactions on Molecular, Biological, and Multi-Scale Communications*.
4. **Pezzulo, G., & Levin, M.** (2015). Re-membering the body: applications of computational neuroscience to the top-down control of regeneration of limbs and other complex organs. *Integrative Biology*, 7(12), 1487–1517. https://doi.org/10.1039/c5ib00221d
5. **Fields, C., & Levin, M.** (2018). Multiscale memory and bioelectric error correction in the cytoplasm–cytoskeleton–membrane system. *WIREs Systems Biology and Medicine*, 10(2), e1403. https://doi.org/10.1002/wsbm.1403
6. **Nakagaki, T., Yamada, H., & Tóth, Á.** (2000). Maze-solving by an amoeboid organism. *Nature*, 407(6803), 470–471. https://doi.org/10.1038/35035159
7. **Tero, A., Takagi, S., Saigusa, T., Ito, K., Bebber, D. P., Fricker, M. D., Yumiki, K., Kobayashi, R., & Nakagaki, T.** (2010). Rules for biologically inspired adaptive network design. *Science*, 327(5964), 439–442. https://doi.org/10.1126/science.1177894
8. **Adamatzky, A.** (2010). *Physarum Machines: Computers from Slime Mould*. World Scientific Series on Nonlinear Science Series A, Vol. 74. World Scientific Publishing.
9. **Kuchling, F., Friston, K., Georgiev, G., & Levin, M.** (2020). Morphogenesis as Bayesian inference: A variational approach to pattern formation and control in complex biological systems. *Physics of Life Reviews*, 33, 88–108. https://doi.org/10.1016/j.plrev.2019.06.001
10. **Pio-Lopez, L., Kuchling, F., Tung, A., Pezzulo, G., & Levin, M.** (2022). Active inference, morphogenesis, and computational psychiatry. *Frontiers in Computational Neuroscience*, 16, 988977. https://doi.org/10.3389/fncom.2022.988977
11. **Clark, A., & Chalmers, D.** (1998). The extended mind. *Analysis*, 58(1), 7–19. https://doi.org/10.1093/analys/58.1.7
12. **Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S.** (2023). Generative agents: Interactive simulacra of human behavior. In *Proceedings of the 36th Annual ACM Symposium on User Interface Software and Technology (UIST '23)*, 1–22. https://doi.org/10.1145/3586183.3606763
13. **Packer, C., Fang, V., Shlapentokh-Rothman, S. G., Shakir, K., & Gonzalez, J. E.** (2023). MemGPT: Towards LLMs as Operating Systems. *arXiv preprint arXiv:2310.08560*.
14. **Xu, W., et al.** (2024). A-MEM: Dynamic Associative Memory for Multi-Agent Systems. *arXiv preprint arXiv:2407.08569*.
15. **Anderson, J. R., Bothell, D., Byrne, M. D., Douglass, S., Lebiere, C., & Qin, Y.** (2004). An integrated theory of the mind. *Psychological Review*, 111(4), 1036–1060. https://doi.org/10.1037/0033-295X.111.4.1036
