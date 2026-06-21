# Artifact scope

This repository contains derived, non-sensitive artifacts for checking the reported false-safe eligibility audit. It is not a full raw-data or simulation archive.

## Claim-to-artifact map

| Evidence item | Public artifact | What can be checked | Boundary |
| --- | --- | --- | --- |
| Algorithm 1 reliability-gated false-safe eligibility audit | `data/derived/calibration_gate_summary.csv`; `data/derived/calibration_gate_by_split.csv`; `data/derived/margin_robustness_by_k_tau.csv`; `data/derived/event_robustness_summary.csv`; `data/derived/ground_motion_im_shift_*.csv`; `figures/figure_4_calibration_gate_exchangeable_vs_shift.*`; `figures/figure_5_robustness_existing_scores.*`; `figures/figure_6_ground_motion_im_shift_existing_derivatives.*` | Traces the public audit surfaces for calibration behavior, margin acceptance, event robustness, and source-shift stress testing | Verifies derived audit outputs only; does not redistribute per-row predictions, model checkpoints, raw records, or response databases |
| Final manuscript figure set | `figures/final_manuscript/figure_1_decision_architecture.*`; `figures/final_manuscript/figure_2_cross_system_eligibility.*`; `figures/final_manuscript/figure_3_demand_regime_not_intensity.*`; `figures/final_manuscript/figure_4_calibration_exchangeable_vs_blocking.*`; `figures/final_manuscript/figure_5_safety_coverage_frontier.*`; `figures/final_manuscript/figure_6_eligibility_map.*` | Provides the final PDF and PNG figure exports corresponding to the manuscript figure set | Final exports are provided for inspection; full regeneration is limited to figures whose inputs are redistributable summary tables |
| Cross-system and same-engine head-to-head audit | `data/derived/final_manuscript/classical_baseline_6family_false_safe.csv`; `data/derived/final_manuscript/wp2_rep_oof_false_safe.csv`; `data/derived/final_manuscript/table_wp2_rep_vs_classical*.csv`; `scripts/rebuild_final_manuscript_figures.py`; `figures/final_manuscript/figure_2_cross_system_eligibility.*`; `figures/final_manuscript/figure_5_safety_coverage_frontier.*`; `figures/final_manuscript/figure_6_eligibility_map.*` | Rebuilds final manuscript Figures 2, 5, and 6 from packaged summary tables and verifies the reported cross-system false-safe pattern | Does not redistribute per-row predictions or model checkpoints; Figure 1, Figure 3, and Figure 4 are included as final exports with their derived support tables |
| Calibration-gate behavior under exchangeable, event-blocked, and source-shift conditions | `data/derived/calibration_gate_summary.csv`; `data/derived/calibration_gate_by_split.csv`; `figures/figure_4_calibration_gate_exchangeable_vs_shift.*` | Selected margins, tested false-safe rates, feasibility/coverage summaries, and the plotted diagnostic | Uses already-scored predictions; does not rerun model inference |
| Robustness across adaptation size, threshold band, and event blocks | `data/derived/margin_robustness_by_k_tau.csv`; `data/derived/event_robustness_summary.csv`; `figures/figure_5_robustness_existing_scores.*` | Reported false-safe/coverage summaries by k, threshold, margin, and worst-event block | Uses derived score tables; low-/mid-rise forward inference is not included |
| Ground-motion intensity-measure source-shift evidence | `data/derived/ground_motion_im_shift_inputs_derived.csv`; `data/derived/ground_motion_im_shift_summary.csv`; `data/derived/ground_motion_im_shift_comparison.csv`; `figures/figure_6_ground_motion_im_shift_existing_derivatives.*`; `scripts/rebuild_ground_motion_im_shift_figure.py` | Rebuilds summary statistics and the multi-IM distribution figure from packaged derived values for PGA, Sa(T1), significant duration D5-95, Arias intensity, and Fourier mean period | Does not provide a complete Mw/distance/duration/Vs30 feature-space comparison |
| Figure exports used for manuscript review | `figures/` | Confirms the figure files included with the package | Figure source depends on derived tables; raw records are excluded |
| Public-data provenance | `DATASETS_AND_LINKS.csv` | Identifies upstream official datasets, reports, and standards links | Users must obtain raw third-party records from providers |
| Package integrity and cleanliness | `MANIFEST.csv`; `scripts/write_manifest.py`; `scripts/check_public_package.py` | Rebuilds file hashes and checks common leakage markers | Human inspection remains required before public release |

## Intended use

Use this repository to verify that the manuscript's derived calibration, robustness, and intensity-measure shift artifacts are internally consistent and publicly shareable. Use upstream services listed in `DATASETS_AND_LINKS.csv` for raw data access.

## Non-reproduced pipeline stages

The following stages are not included:

- model training,
- model inference,
- OpenSees simulations,
- ground-motion acquisition,
- raw record preprocessing,
- complete FEMA/P-695 versus ESM feature-space metadata matching.

These exclusions preserve third-party data rights and keep the public package limited to artifacts that can be redistributed.
