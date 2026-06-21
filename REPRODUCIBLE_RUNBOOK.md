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

## Trace Algorithm 1 from public artifacts

The public package does not rerun private per-row scoring. It supports a bounded check of the manuscript's Algorithm 1 audit sequence from derived, redistributable artifacts:

| Algorithm 1 surface | Public artifact to inspect | Check enabled by this package |
| --- | --- | --- |
| Calibration-gate comparator | `data/derived/calibration_gate_summary.csv`; `data/derived/calibration_gate_by_split.csv`; `figures/figure_4_calibration_gate_exchangeable_vs_shift.*` | Confirms the reported calibration-gate scenarios, risk levels, feasibility/coverage summaries, and exchangeable-versus-shift diagnostic |
| Margin gate and acceptance boundary | `data/derived/margin_robustness_by_k_tau.csv`; `figures/figure_5_robustness_existing_scores.*` | Confirms false-safe and coverage summaries across adaptation size, threshold band, and margin |
| Event-conditioned robustness | `data/derived/event_robustness_summary.csv`; `figures/figure_5_robustness_existing_scores.*` | Confirms the reported event-conditioned robustness summary used to localize residual exposure |
| Source-shift stress test | `data/derived/ground_motion_im_shift_inputs_derived.csv`; `data/derived/ground_motion_im_shift_summary.csv`; `data/derived/ground_motion_im_shift_comparison.csv`; `figures/figure_6_ground_motion_im_shift_existing_derivatives.*` | Rebuilds the multi-intensity-measure shift summaries and plotted diagnostic from packaged derived values |

## Rebuild the ground-motion intensity-measure shift check

```bash
python scripts/rebuild_ground_motion_im_shift_figure.py
```

Expected outputs:

- `data/derived/ground_motion_im_shift_summary.csv`
- `data/derived/ground_motion_im_shift_comparison.csv`
- `figures/figure_6_ground_motion_im_shift_existing_derivatives.png`
- `figures/figure_6_ground_motion_im_shift_existing_derivatives.pdf`
- `figures/figure_6_ground_motion_im_shift_existing_derivatives.svg`

The script reads only `data/derived/ground_motion_im_shift_inputs_derived.csv`. It does not access raw accelerograms, private paths, OpenSees outputs, or internal manuscript rounds.

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

## Check release readiness

```bash
python scripts/check_release_ready.py
```

The release-ready check is stricter than the package-cleanliness check. In the local staging state, it should fail until `CITATION.cff` is updated with final author-approved citation metadata. See `RELEASE_GATE.md`.

## Interpreting included tables

- `calibration_gate_summary.csv`: calibration-gate behavior by scenario and risk level.
- `calibration_gate_by_split.csv`: per-split calibration-gate diagnostics.
- `margin_robustness_by_k_tau.csv`: false-safe and coverage behavior across adaptation sizes, thresholds, and margins.
- `event_robustness_summary.csv`: event-conditioned robustness summary.
- `ground_motion_im_shift_summary.csv`: distribution-level summaries for PGA, Sa(T1), significant duration D5-95, Arias intensity, and Fourier mean period.
- `ground_motion_im_shift_comparison.csv`: standardized mean difference, KS statistic, and histogram overlap for intensity-measure comparisons.
- `ground_motion_im_shift_inputs_derived.csv`: derived intensity-measure values used to rebuild the shift check.

## Non-reproduced steps

The public package does not rerun:

- model training,
- model inference,
- OpenSees simulations,
- ground-motion downloads,
- raw record preprocessing.

Those steps require data or artifacts that are not redistributed here.

## Fast review path

For a short inspection sequence, use `ARTIFACT_QUICKSTART.md`. For a claim-to-artifact map, use `ARTIFACT_SCOPE.md`. For public release blockers, use `RELEASE_GATE.md`.
