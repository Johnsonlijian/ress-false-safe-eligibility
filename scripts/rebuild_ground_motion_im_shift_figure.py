from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived"
FIGURES = ROOT / "figures"

METRICS = [
    ("pga_g", "PGA (g)"),
    ("sa_t1_g", "Sa(T1), 5% damped (g)"),
    ("significant_duration_d5_95_s", "D5-95 (s)"),
    ("arias_intensity_m_s", "Arias intensity (m/s)"),
    ("fourier_mean_period_s", "Fourier mean period (s)"),
]

SOURCE_ALL = "local_P695_scaled_analysis_all_sets"
SOURCE_FARFIELD = "local_P695_scaled_analysis_farfield_only"
TARGET = "ESM_scaled_holdout_analysis"


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


def values(df: pd.DataFrame, distribution: str, metric: str) -> np.ndarray:
    return df.loc[df["distribution"].eq(distribution), metric].dropna().to_numpy(float)


def summarize_distribution(df: pd.DataFrame, distribution: str, metric: str) -> dict[str, object]:
    vals = values(df, distribution, metric)
    return {
        "distribution": distribution,
        "metric": metric,
        "n": int(vals.size),
        "mean": float(np.mean(vals)),
        "sd": float(np.std(vals, ddof=1)) if vals.size > 1 else 0.0,
        "median": float(np.median(vals)),
        "q25": float(np.quantile(vals, 0.25)),
        "q75": float(np.quantile(vals, 0.75)),
        "min": float(np.min(vals)),
        "max": float(np.max(vals)),
    }


def compare_distributions(df: pd.DataFrame, source: str, target: str, metric: str) -> dict[str, object]:
    x = values(df, source, metric)
    y = values(df, target, metric)
    pooled_var = ((x.size - 1) * np.var(x, ddof=1) + (y.size - 1) * np.var(y, ddof=1))
    pooled = np.sqrt(pooled_var / max(x.size + y.size - 2, 1))
    smd = float((np.mean(y) - np.mean(x)) / pooled) if pooled > 0 else 0.0
    return {
        "source_distribution": source,
        "target_distribution": target,
        "metric": metric,
        "source_n": int(x.size),
        "target_n": int(y.size),
        "source_mean": float(np.mean(x)),
        "target_mean": float(np.mean(y)),
        "source_median": float(np.median(x)),
        "target_median": float(np.median(y)),
        "standardized_mean_difference_target_minus_source": smd,
        "ks_statistic": ks_statistic(x, y),
        "overlap_coefficient_histogram": overlap_coefficient(x, y),
    }


def plot_panel(df: pd.DataFrame) -> None:
    import matplotlib.pyplot as plt

    plt.rcParams.update(
        {
            "font.family": "DejaVu Sans",
            "font.size": 8.5,
            "axes.spines.top": False,
            "axes.spines.right": False,
        }
    )

    fig, axes = plt.subplots(2, 3, figsize=(9.2, 5.6))
    axes = axes.ravel()
    for ax, (metric, label) in zip(axes, METRICS):
        source = values(df, SOURCE_ALL, metric)
        farfield = values(df, SOURCE_FARFIELD, metric)
        target = values(df, TARGET, metric)
        high = max(np.max(source), np.max(farfield), np.max(target))
        low = min(np.min(source), np.min(farfield), np.min(target))
        bins = np.linspace(low, high * 1.02 if high > 0 else 1.0, 34)
        ax.hist(source, bins=bins, density=True, histtype="step", linewidth=1.8, color="#4b5563", label="P-695 source")
        ax.hist(farfield, bins=bins, density=True, histtype="step", linewidth=1.5, linestyle="--", color="#111827", label="P-695 farfield")
        ax.hist(target, bins=bins, density=True, alpha=0.30, color="#c2410c", label="ESM holdout")
        ax.set_xlabel(label)
        ax.set_ylabel("Density")
    axes[-1].axis("off")
    axes[-1].text(
        0.02,
        0.70,
        "Packaged derived analyses only\nNo raw records, model inference,\nor simulations.",
        va="top",
    )
    axes[0].legend(frameon=False, fontsize=8)
    fig.suptitle("Ground-motion intensity-measure shift from packaged derived analyses", fontsize=12, fontweight="bold")
    fig.tight_layout(rect=[0, 0, 1, 0.95])
    for ext in ("png", "pdf", "svg"):
        output_path = FIGURES / f"figure_6_ground_motion_im_shift_existing_derivatives.{ext}"
        fig.savefig(output_path, dpi=300)
        if ext == "svg":
            lines = output_path.read_text(encoding="utf-8").splitlines()
            output_path.write_text("\n".join(line.rstrip() for line in lines) + "\n", encoding="utf-8")
    plt.close(fig)


def main() -> None:
    DATA.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    input_path = DATA / "ground_motion_im_shift_inputs_derived.csv"
    df = pd.read_csv(input_path)
    required = {"distribution", *(metric for metric, _ in METRICS)}
    missing = required.difference(df.columns)
    if missing:
        raise ValueError(f"{input_path} is missing required columns: {sorted(missing)}")

    summaries = [
        summarize_distribution(df, distribution, metric)
        for distribution in (SOURCE_ALL, SOURCE_FARFIELD, TARGET)
        for metric, _ in METRICS
    ]
    pd.DataFrame(summaries).to_csv(DATA / "ground_motion_im_shift_summary.csv", index=False)

    comparisons = [
        compare_distributions(df, source, TARGET, metric)
        for source in (SOURCE_ALL, SOURCE_FARFIELD)
        for metric, _ in METRICS
    ]
    pd.DataFrame(comparisons).to_csv(DATA / "ground_motion_im_shift_comparison.csv", index=False)
    plot_panel(df)


if __name__ == "__main__":
    main()
