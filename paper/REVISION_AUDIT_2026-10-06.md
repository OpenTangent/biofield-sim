# v0.7 manuscript and reporting revision audit — 6 October 2026

Status: repository revision authorised for publication by the project owner. A new Zenodo version has not been deposited by the agent; the existing Zenodo record remains v0.6.0. Git push authorisation is not a journal submission or independent scientific certification.

## Reproduction and provenance

Baseline commit: `ae9402d086ba769f0219de6e0a18dab21cc3fa10`. Before modifications, the baseline was copied into an isolated directory and all 30 seeds rerun in 149.6 seconds. Protocol, complete raw data and summary values exactly matched the committed original, excluding runtime metadata. This is local reproduction, not independent replication.

Baseline source SHA256:

- `benchmark_setpoint_v070.py`: `c6f6b257ea710e5bf63f6104e12d85cdd204f588295a923b54adf0c7a9ce4828`
- `setpoint_layer.py`: `e43f193fe34a3ab97ca198df280aa3cdffa3004b311d70f90e4dfb77e5fd9aad`

The historical `benchmark_results_v070.json` is unchanged. File hashes and the current local environment are recorded in `REVISION_MANIFEST_2026-10-06.json`.

## Reporting correction

The original benchmark appended the preceding FLUX graph's sparsity value to each of the three Setpoint conditions. There is no edge-sparsity observable for a score vector; those values are invalid.

`benchmark_results_v070_corrected.json` is a reporting-only repair of the reproduced original, not a fresh run of the patched script. In the nine condition/wipe rows, raw Setpoint sparsity becomes `null` and the corresponding summary sparsity entries are removed. Complete raw and summary structures otherwise exactly match. Metadata adds a reporting-revision note and records the isolated rerun's 149.6-second duration, rather than the historical 101.8 seconds.

Baseline selectivity is measured from goal-edge weights; Setpoint selectivity is measured from fact scores. These are different observables and must not be compared as the same quantity.

## Fresh patched-script run

A separate 30-seed run completed in 88.6 seconds with `OPENBLAS_NUM_THREADS=1` and `OMP_NUM_THREADS=1`. The protocol and every exported recall, page-count and sparsity value exactly matched the corrected export. An initial strict equality assertion failed because 165 selectivity entries differed, with maximum absolute difference `1.3216094885137863e-12`. This is numerical agreement, not bitwise identity across the entire export.

Changed floating-point reduction order under BLAS threading is a plausible explanation, not an isolated causal diagnosis. Internal state trajectories were not exported or compared; identical aggregate retrieval metrics do not prove identical internal trajectories. The fresh run did not replace either historical export. Exact reporting-repair checks remain appropriate because they transform stored data without recomputation.

## Code and build changes

- Reporting patch prevents stale sparsity values from being exported.
- Default benchmark exports use fresh microsecond-resolution timestamped filenames. `--output` selects a new path; CLI preflight and exclusive-create writes refuse existing files. `run(None)` intentionally writes a timestamped export, not an in-memory-only result.
- Setpoint documentation clarifies fixed goal targets versus non-clamped potentials and deliberate reset-per-read. Numerical update operations are unchanged.
- `scripts/render_paper.py` builds HTML/PDF through Pandoc and Playwright with Chromium, waits for MathJax and fonts, and rejects missing images or maths errors. It needs network access for configured CDN resources; it is not a hermetic offline build.
- A4 stylesheet, responsive diagram sizing, equations and list spacing repaired. Figure 1 and Tables 1–3 inspected for page clipping; this is a readability check, not journal typesetting certification.
- Fourteen tests pass; `git diff --check` is clean. Tests and comparisons were run directly by the authoring agent. Delegated reports with missing source access or incorrect metadata were not accepted as independent verification.

## Scientific framing and bibliography

The revision adds the finite-step v0.7 goal-conditioned readout experiment while retaining negative reservoir and literal flux results. Post-switch recall@8 rises from 0.296 to 0.754 and simulated ranked-list pages fall from 7.53 to 4.73. Weighted normalisation is not uniformly superior to the binary-degree ablation. Fifteen steps do not establish convergence, and reset-per-read is not a continuously operating field.

Removed unsupported sub-five-millisecond timing, zero-overhead, universal RAG/static-memory, guaranteed goal recall and live-effectiveness claims. No independently timestamped preregistration is established. The primary comparison is a constructed co-occurrence retrieval world, not a matched comparison with modern hybrid RAG, Mem0, Zep or A-MEM.

Bibliography corrections include:

- A-MEM is `arXiv:2502.12110`; the earlier `2407.08569` identifier is unrelated.
- Unverified Hansali placeholder replaced by Durant et al. (2017), DOI `10.1016/j.bpj.2017.04.011`, with the persistence statement narrowed to the reported regenerative experiment.
- Fields & Levin's correct DOI is `10.1002/wsbm.1410` (10(2), e1410); `10.1002/wsbm.1403` resolves to issue information. Corrected metadata and publisher-supplied abstract verified; publisher full text was blocked. The source supports a general multiscale-memory discussion, not software equivalence.
- Slime-trail spatial memory is supported by Reid, Latty, Dussutour & Beekman (2012), DOI `10.1073/pnas.1215037109`.
- MemGPT authors corrected from DOI metadata. Mem0 and Zep primary preprints added, and related-work comparisons acknowledge evolving memory.
- Eighteen references are numbered continuously; citation endpoints checked. This is not a claim of independent full-bibliography certification.

## Remaining evidence boundaries

Independent replication, competitive retrieval baselines, held-out parameter selection, scaling/timing measurements and LLM-in-the-loop evaluation remain pending. Simulation does not validate live Open Amity, establish biological equivalence, or measure API savings. The participant-observer note is anecdotal motivation only.


## Upload-copy preparation

At the project owner's request, temporary Zenodo deposit-status wording was removed from the manuscript header and availability section. The stable header reads “Version: v0.7.0 — 6 October 2026”. Author, affiliation and contact lines were separated; the A-MEM correction history remains here rather than inside its bibliography entry. Source Serif 4 body text and Source Sans 3 headings/tables were retained after visual inspection; PDF fonts are embedded. No scientific results or code calculations changed, and no Zenodo publication is implied.
