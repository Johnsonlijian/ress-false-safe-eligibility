# False-safe eligibility auditing for seismic-demand surrogate screening

This repository stages the public reproducibility package for a reliability and system-safety study of machine-learning seismic-demand surrogates under event-level distribution shift.

The package is intentionally narrow. It contains derived, non-sensitive CSV tables, exported figures, and lightweight scripts needed to re-check the reported calibration-gate, robustness, and PGA-shift summaries. It does not contain active submission manuscripts, cover letters, reviewer drafts, internal rounds, private logs, raw third-party ground-motion records, downloaded archives, or OpenSees response databases.

## Contents

- `data/derived/`: derived tables used in the reliability-gate and shift analyses.
- `figures/`: exported manuscript figures in SVG, PDF, and PNG formats.
- `ARTIFACT_QUICKSTART.md`: a short path for checking the package in a few minutes.
- `ARTIFACT_SCOPE.md`: a table mapping claims, files, and reproducibility boundaries.
- `scripts/rebuild_pga_shift_figure.py`: rebuilds the PGA-only source-shift summary and figure from the packaged derived input table.
- `scripts/write_manifest.py`: rebuilds `MANIFEST.csv` with file sizes and SHA-256 hashes.
- `scripts/check_public_package.py`: scans the repository for common private-path, workflow, and raw-data leakage markers.
- `DATASETS_AND_LINKS.csv`: upstream dataset and standards links used by the study.
- `REPRODUCIBLE_RUNBOOK.md`: step-by-step reproduction notes and scope boundaries.

## What can be reproduced from this public package

1. The PGA-only source-shift summaries and comparison statistics.
2. The PGA-shift distribution figure.
3. The already-derived calibration-gate and robustness result tables.
4. The exported figure files used for manuscript review.

The public package does not rerun model training, model inference, OpenSees simulations, or ground-motion acquisition. Those steps depend on raw third-party data and internal response-analysis artifacts that are excluded from public release.

## Quick start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/rebuild_pga_shift_figure.py
python scripts/write_manifest.py
python scripts/check_public_package.py
```

On macOS/Linux, use `source .venv/bin/activate` instead of the Windows activation command.

## Public-data boundary

Raw strong-motion records and third-party archives are not redistributed. Users should obtain upstream data from the official sources listed in `DATASETS_AND_LINKS.csv` and respect each provider's license and access conditions.

For a claim-by-claim boundary map, see `ARTIFACT_SCOPE.md`.

## Repository status

This is a local, GitHub-ready staging package. Repository creation and pushing to GitHub are intentionally left as human-approved actions.
