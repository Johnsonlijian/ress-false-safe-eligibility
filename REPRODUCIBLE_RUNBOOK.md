# Reproducible runbook

## Scope

This package supports public verification of the derived evidence used for false-safe eligibility auditing of seismic-demand surrogate screening. It is designed for checking reported tables and figures, not for rerunning proprietary or third-party-data-dependent experiments.

## Environment

Use Python 3.10 or newer.

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

On macOS/Linux, use `source .venv/bin/activate` instead of the Windows activation command.

## Rebuild the PGA-only shift check

```bash
python scripts/rebuild_pga_shift_figure.py
```

Expected outputs:

- `data/derived/pga_shift_summary.csv`
- `data/derived/pga_shift_comparison.csv`
- `figures/figure_6_pga_shift_existing_derivatives.png`
- `figures/figure_6_pga_shift_existing_derivatives.pdf`
- `figures/figure_6_pga_shift_existing_derivatives.svg`

The script reads only `data/derived/pga_shift_inputs_derived.csv`. It does not access raw accelerograms, private paths, OpenSees outputs, or internal manuscript rounds.

## Rebuild the file manifest

```bash
python scripts/write_manifest.py
```

Expected output:

- `MANIFEST.csv`

The manifest records relative paths, file sizes, and SHA-256 hashes. Paths use forward slashes so the file is stable across operating systems.

## Check package cleanliness

```bash
python scripts/check_public_package.py
```

The scan checks for common private path markers, internal workflow markers, active-submission files, and raw-data archive patterns. It is a guardrail, not a substitute for human inspection before publication.

## Interpreting included tables

- `calibration_gate_summary.csv`: calibration-gate behavior by scenario and risk level.
- `calibration_gate_by_split.csv`: per-split calibration-gate diagnostics.
- `margin_robustness_by_k_tau.csv`: false-safe and coverage behavior across adaptation sizes, thresholds, and margins.
- `event_robustness_summary.csv`: event-conditioned robustness summary.
- `pga_shift_summary.csv`: distribution-level PGA summaries.
- `pga_shift_comparison.csv`: standardized mean difference, KS statistic, and histogram overlap for PGA comparisons.
- `pga_shift_inputs_derived.csv`: derived PGA values used to rebuild the PGA-only shift check.

## Non-reproduced steps

The public package does not rerun:

- model training,
- model inference,
- OpenSees simulations,
- ground-motion downloads,
- raw record preprocessing.

Those steps require data or artifacts that are not redistributed here.

## Fast review path

For a short inspection sequence, use `ARTIFACT_QUICKSTART.md`. For a claim-to-artifact map, use `ARTIFACT_SCOPE.md`.
