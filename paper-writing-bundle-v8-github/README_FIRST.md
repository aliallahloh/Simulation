# Paper Writing Bundle (V8) — GitHub-Safe Edition

This folder is the GitHub-safe paper-writing bundle for the validated V8 branch.

It is designed to be used as the evidence package for drafting the paper. It contains the prompt, dataset card, methods/results summaries, exact configs, compact benchmark metadata, and the key full-run metrics needed to write the manuscript honestly and professionally.

## What is included here

- `PAPER_WRITING_PROMPT.txt`
- `DATASET_CARD.md`
- `METHODS_SUMMARY.md`
- `RESULTS_SUMMARY.md`
- `PAPER_POSITIONING_AND_LIMITATIONS.md`
- `configs/full.yaml`, `configs/quick.yaml`, `configs/smoke.yaml`
- `dataset_core/overlays/battery/battery_assets.csv`
- `evidence/metrics/*.csv` (compact full-run result tables)
- `evidence/artifacts/summary_report.md`

## Why this is GitHub-safe

The original local bundle included very large raw benchmark and time-series artifacts. Those files are not necessary for drafting the paper and are awkward to publish reliably through this GitHub connector path.

This GitHub bundle therefore focuses on the files that actually support paper writing:
- the validated result summaries
- the exact experimental configurations
- the compact evidence tables
- the writing prompt and guardrails

## Ground-truth framing

Use this package to write a paper about:

**a trustworthy federated hybrid digital twin for resilient renewable energy management in grid-interactive virtual power plants**

Do **not** overclaim:
- no deep MARL implementation
- no unconstrained RL baseline
- no universal peak-demand dominance
- no universally beneficial uncertainty module
- no battery-degradation optimization beyond throughput proxy evidence

## Strongest evidence in the full run

- the hybrid twin strongly improves **load** calibration over the physics-only twin
- personalized hybrid/federated forecasting strongly outperforms global-only variants
- trust-aware control materially reduces **operating cost** under stressed scenarios
- peak-import improvements are present but generally modest
- battery throughput rises materially under trust-aware stress handling, so discuss that tradeoff explicitly

## Source-of-truth files

Start with:
- `RESULTS_SUMMARY.md`
- `METHODS_SUMMARY.md`
- `evidence/metrics/forecast_main_results.csv`
- `evidence/metrics/twin_results.csv`
- `evidence/metrics/scenario_key_results.csv`
- `evidence/metrics/ablation_key_results.csv`
- `evidence/artifacts/summary_report.md`

Then read:
- `PAPER_POSITIONING_AND_LIMITATIONS.md`
- `configs/full.yaml`

Manifest status: `ok`
