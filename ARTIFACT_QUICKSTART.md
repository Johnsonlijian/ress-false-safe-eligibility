# Artifact quickstart

This package is designed for a short, bounded artifact check. It verifies derived tables and figures used in the false-safe eligibility audit without redistributing raw third-party records or rerunning simulation/model pipelines.

## Five-minute check

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/rebuild_final_manuscript_figures.py
python scripts/rebuild_ground_motion_im_shift_figure.py
python scripts/write_manifest.py
python scripts/check_public_package.py
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

## What should change

The final-manuscript rebuild script may refresh these files:

- `figures/final_manuscript/figure_2_cross_system_eligibility.png`
- `figures/final_manuscript/figure_2_cross_system_eligibility.pdf`
- `figures/final_manuscript/figure_5_safety_coverage_frontier.png`
- `figures/final_manuscript/figure_5_safety_coverage_frontier.pdf`
- `figures/final_manuscript/figure_6_eligibility_map.png`
- `figures/final_manuscript/figure_6_eligibility_map.pdf`

The ground-motion intensity-measure shift script may refresh these files:

- `data/derived/ground_motion_im_shift_summary.csv`
- `data/derived/ground_motion_im_shift_comparison.csv`
- `figures/figure_6_ground_motion_im_shift_existing_derivatives.png`
- `figures/figure_6_ground_motion_im_shift_existing_derivatives.pdf`
- `figures/figure_6_ground_motion_im_shift_existing_derivatives.svg`

`scripts/write_manifest.py` then refreshes `MANIFEST.csv`.

## Before public release

The quickstart above checks the artifact package. It does not clear the package for public release. Before creating or pushing the public repository, follow `RELEASE_GATE.md` and run:

```bash
python scripts/check_release_ready.py
```

## What to inspect first

1. `ARTIFACT_SCOPE.md` for the claim-to-artifact map.
2. `REPRODUCIBLE_RUNBOOK.md` for the Algorithm 1 audit-trace table.
3. `data/derived/calibration_gate_summary.csv` for calibration-gate outcomes.
4. `data/derived/margin_robustness_by_k_tau.csv` for threshold and adaptation-size robustness.
5. `data/derived/event_robustness_summary.csv` for event-conditioned robustness.
6. `data/derived/ground_motion_im_shift_comparison.csv` for the intensity-measure source-shift comparison.
7. `figures/final_manuscript/figure_*.pdf` and `figures/final_manuscript/figure_*.png` for the final manuscript figure exports.
8. `figures/figure_4_calibration_gate_exchangeable_vs_shift.*`, `figure_5_robustness_existing_scores.*`, and `figure_6_ground_motion_im_shift_existing_derivatives.*` for the earlier staged diagnostic figures.

## What this package does not claim

- It does not rerun model training or model inference.
- It does not rerun OpenSees simulations.
- It does not redistribute raw ESM or FEMA/P-695 strong-motion records.
- It does not provide a full Mw/distance/duration/Vs30 source-shift table.

Those exclusions are intentional publication-boundary choices, not hidden positive results.
