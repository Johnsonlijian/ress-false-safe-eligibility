# Artifact quickstart

This package is designed for a short, bounded artifact check. It verifies derived tables and figures used in the false-safe eligibility audit without redistributing raw third-party records or rerunning simulation/model pipelines.

## Five-minute check

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/rebuild_pga_shift_figure.py
python scripts/write_manifest.py
python scripts/check_public_package.py
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

## What should change

The PGA-only shift script may refresh these files:

- `data/derived/pga_shift_summary.csv`
- `data/derived/pga_shift_comparison.csv`
- `figures/figure_6_pga_shift_existing_derivatives.png`
- `figures/figure_6_pga_shift_existing_derivatives.pdf`
- `figures/figure_6_pga_shift_existing_derivatives.svg`

`scripts/write_manifest.py` then refreshes `MANIFEST.csv`.

## What to inspect first

1. `ARTIFACT_SCOPE.md` for the claim-to-artifact map.
2. `data/derived/calibration_gate_summary.csv` for calibration-gate outcomes.
3. `data/derived/margin_robustness_by_k_tau.csv` for threshold and adaptation-size robustness.
4. `data/derived/pga_shift_comparison.csv` for the PGA-only source-shift comparison.
5. `figures/figure_4_calibration_gate_exchangeable_vs_shift.*`, `figure_5_robustness_existing_scores.*`, and `figure_6_pga_shift_existing_derivatives.*` for the main diagnostic figures.

## What this package does not claim

- It does not rerun model training or model inference.
- It does not rerun OpenSees simulations.
- It does not redistribute raw ESM or FEMA/P-695 strong-motion records.
- It does not provide a full Mw/distance/duration/Vs30 source-shift table.

Those exclusions are intentional publication-boundary choices, not hidden positive results.
