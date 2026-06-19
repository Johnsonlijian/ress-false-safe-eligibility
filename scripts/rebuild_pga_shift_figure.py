from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"


def ks_statistic(x: np.ndarray, y: np.ndarray) -> float:
    x = np.sort(np.asarray(x, dtype=float))
    y = np.sort(np.asarray(y, dtype=float))
    vals = np.sort(np.unique(np.concatenate([x, y])))
    fx = np.searchsorted(x, vals, side="right") / max(len(x), 1)
    fy = np.searchsorted(y, vals, side="right") / max(len(y), 1)
    return float(np.max(np.abs(fx - fy)))


def overlap_coefficient(x: np.ndarray, y: np.ndarray, bins: int = 40) -> float:
    x = np.asarray(x, dtype=float)
    y = np.asarray(y, dtype=float)
    lo = float(min(np.min(x), np.min(y)))
    hi = float(max(np.max(x), np.max(y)))
    if hi <= lo:
        return 1.0
    edges = np.linspace(lo, hi, bins + 1)
    hx, _ = np.histogram(x, bins=edges, density=True)
    hy, _ = np.histogram(y, bins=edges, density=True)
    return float(np.sum(np.minimum(hx, hy) * np.diff(edges)))


def summary(name: str, values: np.ndarray, provenance: str, comparable_scale: str) -> dict[str, object]:
    values = np.asarray(values, dtype=float)
    return {
        "distribution": name,
        "n": int(values.size),
        "mean_pga_g": float(np.mean(values)),
        "sd_pga_g": float(np.std(values, ddof=1)) if values.size > 1 else 0.0,
        "median_pga_g": float(np.median(values)),
        "q25_pga_g": float(np.quantile(values, 0.25)),
        "q75_pga_g": float(np.quantile(values, 0.75)),
        "min_pga_g": float(np.min(values)),
        "max_pga_g": float(np.max(values)),
        "provenance": provenance,
        "comparable_scale": comparable_scale,
    }


def comparison(source_name: str, source: np.ndarray, target_name: str, target: np.ndarray, note: str) -> dict[str, object]:
    source = np.asarray(source, dtype=float)
    target = np.asarray(target, dtype=float)
    pooled_var = ((source.size - 1) * np.var(source, ddof=1) + (target.size - 1) * np.var(target, ddof=1))
    pooled = np.sqrt(pooled_var / max(source.size + target.size - 2, 1))
    smd = float((np.mean(target) - np.mean(source)) / pooled) if pooled > 0 else 0.0
    return {
        "source_distribution": source_name,
        "target_distribution": target_name,
        "source_n": int(source.size),
        "target_n": int(target.size),
        "source_mean_pga_g": float(np.mean(source)),
        "target_mean_pga_g": float(np.mean(target)),
        "standardized_mean_difference_target_minus_source": smd,
        "ks_statistic": ks_statistic(source, target),
        "overlap_coefficient_histogram": overlap_coefficient(source, target),
        "note": note,
    }


def values(df: pd.DataFrame, name: str) -> np.ndarray:
    return df.loc[df["distribution"].eq(name), "pga_g"].to_numpy(float)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    input_path = DATA / "pga_shift_inputs_derived.csv"
    df = pd.read_csv(input_path)
    required = {"distribution", "pga_g", "comparable_scale"}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{input_path} is missing required columns: {sorted(missing)}")

    source_all = values(df, "local_P695_scaled_analysis_all_sets")
    source_farfield = values(df, "local_P695_scaled_analysis_farfield_only")
    esm_scaled = values(df, "ESM_scaled_holdout_analysis")
    esm_raw = values(df, "ESM_raw_record_package")

    summaries = [
        summary(
            "local_P695_scaled_analysis_all_sets",
            source_all,
            "packaged derived response-analysis PGA values from the local P-695 source analyses",
            "scaled analysis input PGA",
        ),
        summary(
            "local_P695_scaled_analysis_farfield_only",
            source_farfield,
            "packaged derived response-analysis PGA values from the local P-695 farfield sensitivity subset",
            "scaled analysis input PGA",
        ),
        summary(
            "ESM_scaled_holdout_analysis",
            esm_scaled,
            "packaged derived response-analysis PGA values from the scaled ESM holdout analyses",
            "scaled analysis input PGA",
        ),
        summary(
            "ESM_raw_record_package",
            esm_raw,
            "packaged derived PGA metadata for the selected ESM record package before response-analysis scaling",
            "raw record PGA",
        ),
    ]
    pd.DataFrame(summaries).to_csv(DATA / "pga_shift_summary.csv", index=False)

    comparisons = [
        comparison(
            "local_P695_scaled_analysis_all_sets",
            source_all,
            "ESM_scaled_holdout_analysis",
            esm_scaled,
            "Most comparable available response-analysis PGA comparison; both sides are scaled analysis inputs.",
        ),
        comparison(
            "local_P695_scaled_analysis_farfield_only",
            source_farfield,
            "ESM_scaled_holdout_analysis",
            esm_scaled,
            "Farfield-only sensitivity using packaged derived source-analysis values.",
        ),
        comparison(
            "local_P695_scaled_analysis_all_sets",
            source_all,
            "ESM_raw_record_package",
            esm_raw,
            "Less comparable diagnostic: scaled source analyses versus raw selected-record PGA metadata.",
        ),
    ]
    pd.DataFrame(comparisons).to_csv(DATA / "pga_shift_comparison.csv", index=False)

    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 9,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )
    fig, ax = plt.subplots(figsize=(7.0, 3.8))
    high = max(np.max(source_all), np.max(source_farfield), np.max(esm_scaled), np.max(esm_raw))
    bins = np.linspace(0, high * 1.02, 34)
    ax.hist(source_all, bins=bins, density=True, histtype="step", linewidth=2.0, color="#4b5563", label="P-695 source analyses")
    ax.hist(source_farfield, bins=bins, density=True, histtype="step", linewidth=1.6, linestyle="--", color="#111827", label="P-695 farfield sensitivity")
    ax.hist(esm_scaled, bins=bins, density=True, alpha=0.30, color="#c2410c", label="ESM scaled holdout analyses")
    ax.hist(esm_raw, bins=bins, density=True, histtype="step", linewidth=1.6, color="#2563eb", label="ESM raw records")
    ax.set_xlabel("PGA (g)")
    ax.set_ylabel("Density")
    ax.set_title("PGA shift check from packaged derived sources")
    ax.legend(frameon=False, fontsize=8)
    fig.tight_layout()
    for ext in ("png", "pdf", "svg"):
        fig.savefig(FIGURES / f"figure_6_pga_shift_existing_derivatives.{ext}", dpi=300)
    plt.close(fig)


if __name__ == "__main__":
    main()
