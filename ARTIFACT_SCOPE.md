# Artifact scope

This repository contains derived, non-sensitive artifacts for checking the reported false-safe eligibility audit. It is not a full raw-data or simulation archive.

## Claim-to-artifact map

| Evidence item | Public artifact | What can be checked | Boundary |
| --- | --- | --- | --- |
| Calibration-gate behavior under exchangeable, event-blocked, and source-shift conditions | `data/derived/calibration_gate_summary.csv`; `data/derived/calibration_gate_by_split.csv`; `figures/figure_4_calibration_gate_exchangeable_vs_shift.*` | Selected margins, tested false-safe rates, feasibility/coverage summaries, and the plotted diagnostic | Uses already-scored predictions; does not rerun model inference |
| Robustness across adaptation size, threshold band, and event blocks | `data/derived/margin_robustness_by_k_tau.csv`; `data/derived/event_robustness_summary.csv`; `figures/figure_5_robustness_existing_scores.*` | Reported false-safe/coverage summaries by k, threshold, margin, and worst-event block | Uses derived score tables; low-/mid-rise forward inference is not included |
| PGA-only source-shift evidence | `data/derived/pga_shift_inputs_derived.csv`; `data/derived/pga_shift_summary.csv`; `data/derived/pga_shift_comparison.csv`; `figures/figure_6_pga_shift_existing_derivatives.*`; `scripts/rebuild_pga_shift_figure.py` | Rebuilds summary statistics and the PGA distribution figure from packaged derived values | Does not provide a complete Mw/distance/duration/Vs30 feature-space comparison |
| Figure exports used for manuscript review | `figures/` | Confirms the figure files included with the package | Figure source depends on derived tables; raw records are excluded |
| Public-data provenance | `DATASETS_AND_LINKS.csv` | Identifies upstream official datasets, reports, and standards links | Users must obtain raw third-party records from providers |
| Package integrity and cleanliness | `MANIFEST.csv`; `scripts/write_manifest.py`; `scripts/check_public_package.py` | Rebuilds file hashes and checks common leakage markers | Human inspection remains required before public release |

## Intended use

Use this repository to verify that the manuscript's derived calibration, robustness, and PGA-only shift artifacts are internally consistent and publicly shareable. Use upstream services listed in `DATASETS_AND_LINKS.csv` for raw data access.

## Non-reproduced pipeline stages

The following stages are not included:

- model training,
- model inference,
- OpenSees simulations,
- ground-motion acquisition,
- raw record preprocessing,
- complete FEMA/P-695 versus ESM feature-space metadata matching.

These exclusions preserve third-party data rights and keep the public package limited to artifacts that can be redistributed.
