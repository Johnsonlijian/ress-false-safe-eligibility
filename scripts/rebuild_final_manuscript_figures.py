from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "derived" / "final_manuscript"
FIGURES = ROOT / "figures" / "final_manuscript"

BLUE = "#2c6fbb"
ORANGE = "#e08214"
GREEN = "#2a9d4a"
RED = "#c0392b"
GREY = "#888888"


def clopper_pearson(x: int, n: int, alpha: float = 0.05) -> tuple[float, float]:
    lo = 0.0 if x == 0 else float(stats.beta.ppf(alpha / 2, x, n - x + 1))
    hi = 1.0 if x == n else float(stats.beta.ppf(1 - alpha / 2, x + 1, n - x))
    return lo, hi


def save(fig: plt.Figure, stem: str) -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(FIGURES / f"{stem}.{ext}", bbox_inches="tight", dpi=200)
    plt.close(fig)


def rebuild_figure_2() -> None:
    rep = pd.read_csv(DATA / "wp2_rep_oof_false_safe.csv")
    clf = pd.read_csv(DATA / "classical_baseline_6family_false_safe.csv")
    families = ["rc_wall", "rcf_tall", "steel_frame", "steel_braced"]
    labels = ["RC wall", "RC tall", "Steel moment", "Steel braced"]

    fig, (ax_a, ax_b) = plt.subplots(1, 2, figsize=(11.5, 5.3))

    rep_v: list[float] = []
    rep_e: list[list[float]] = [[], []]
    clf_v: list[float] = []
    clf_e: list[list[float]] = [[], []]
    for family in families:
        r = rep[(rep.family == family) & (rep.margin == 0)].iloc[0]
        rep_v.append(float(r.fs))
        rep_e[0].append(float(r.fs - r.ci_lo))
        rep_e[1].append(float(r.ci_hi - r.fs))

        c = clf[(clf.family == family) & (clf.margin == 0)].iloc[0]
        value = float(c.n_false_safe / c.n_unsafe)
        lo, hi = clopper_pearson(int(c.n_false_safe), int(c.n_unsafe))
        clf_v.append(value)
        clf_e[0].append(value - lo)
        clf_e[1].append(hi - value)

    x = np.arange(len(families))
    width = 0.38
    ax_a.bar(x - width / 2, rep_v, width, yerr=rep_e, capsize=3, color=BLUE, label="REP (pretrained encoder)")
    ax_a.bar(x + width / 2, clf_v, width, yerr=clf_e, capsize=3, color=ORANGE, label="classical IM baseline")
    ax_a.axhline(0.01, ls="--", color=GREY, lw=1)
    ax_a.set_xticks(x)
    ax_a.set_xticklabels(labels, fontsize=9)
    ax_a.set_ylabel("Raw false-safe among unsafe (95% CI)")
    rho, _ = stats.spearmanr(rep_v, clf_v)
    ax_a.set_title(
        "Head-to-head: eligibility is surrogate-specific\n"
        + r"(per-system ranks anti-correlated, Spearman $\rho$="
        + f"{rho:.2f})",
        fontsize=10,
    )
    ax_a.text(-0.12, 1.08, "(a)", transform=ax_a.transAxes, fontsize=12, fontweight="bold", va="top", ha="left")
    ax_a.legend(fontsize=8.5, loc="upper right")
    ax_a.set_ylim(0, 0.78)
    ax_a.annotate(
        "REP fails where the\nclassical baseline succeeds\n(rc_wall: CIs disjoint)",
        (0, 0.45),
        (0.35, 0.66),
        fontsize=8,
        color=RED,
        arrowprops=dict(arrowstyle="->", color=RED),
    )

    margins = [0.0, 0.5, 0.75]
    rep_steel = rep[rep.family == "steel_frame"].set_index("margin")
    clf_steel = clf[clf.family == "steel_frame"].set_index("margin")
    rep_values = [float(rep_steel.loc[m, "fs"]) for m in margins]
    rep_errors = [
        [float(rep_steel.loc[m, "fs"] - rep_steel.loc[m, "ci_lo"]) for m in margins],
        [float(rep_steel.loc[m, "ci_hi"] - rep_steel.loc[m, "fs"]) for m in margins],
    ]
    clf_values: list[float] = []
    clf_errors: list[list[float]] = [[], []]
    for margin in margins:
        x_false = int(clf_steel.loc[margin, "n_false_safe"])
        n_unsafe = int(clf_steel.loc[margin, "n_unsafe"])
        value = x_false / n_unsafe
        lo, hi = clopper_pearson(x_false, n_unsafe)
        clf_values.append(value)
        clf_errors[0].append(value - lo)
        clf_errors[1].append(hi - value)

    ax_b.errorbar(margins, rep_values, yerr=rep_errors, fmt="-o", color=BLUE, lw=2, ms=8, capsize=3, label="REP")
    ax_b.errorbar(margins, clf_values, yerr=clf_errors, fmt="-s", color=ORANGE, lw=2, ms=8, capsize=3, label="classical")
    ax_b.axhline(0.01, ls="--", color=GREY, lw=1)
    ax_b.text(0.45, 0.016, "false-safe target 0.01", fontsize=8, color=GREY)
    ax_b.set_xlabel("margin m")
    ax_b.set_ylabel("Steel moment frame false-safe (95% CI)")
    ax_b.set_title("Steel moment frame:\ndo-not-screen under BOTH surrogates", fontsize=10)
    ax_b.text(-0.12, 1.08, "(b)", transform=ax_b.transAxes, fontsize=12, fontweight="bold", va="top", ha="left")
    ax_b.legend(fontsize=9)
    ax_b.set_xticks(margins)
    ax_b.set_ylim(-0.02, 0.48)
    fig.tight_layout()
    save(fig, "figure_2_cross_system_eligibility")


def rebuild_figure_5_and_6() -> None:
    df = pd.read_csv(DATA / "classical_baseline_6family_false_safe.csv")
    order = ["rc_wall", "rcf_low", "rcf_mid", "rcf_tall", "steel_braced", "steel_frame"]
    labels = ["RC wall", "RC frame (low)", "RC frame (mid)", "RC frame (tall)", "Steel braced", "Steel moment"]
    margins = [0.0, 0.25, 0.5, 0.75]
    colors = [GREEN, "#5aa0d0", BLUE, "#8e6fb0", ORANGE, RED]
    markers = ["o", "s", "^", "D", "v", "P"]

    fig, ax = plt.subplots(figsize=(7.4, 5.4))
    for family, label, color, marker in zip(order, labels, colors, markers):
        subset = df[df.family == family].sort_values("margin")
        ax.plot(subset.coverage, subset.fs_among_unsafe, "-", marker=marker, color=color, lw=1.8, ms=7, label=label)
    ax.axhline(0.01, ls="--", color=GREY, lw=1.2)
    ax.text(0.02, 0.013, "false-safe target 0.01", fontsize=8, color="#555")
    ax.set_xlabel("Accepted-safe coverage")
    ax.set_ylabel("False-safe rate among unsafe cases")
    ax.set_title("Safety-coverage frontier across six structural systems (classical baseline)", fontsize=10)
    ax.set_xlim(0, 0.72)
    ax.set_ylim(-0.01, 0.34)
    ax.grid(True, alpha=0.25)
    ax.legend(fontsize=8, loc="upper left", ncol=2)
    ax.annotate(
        "margin increases\n(toward lower-left)",
        (0.13, 0.02),
        (0.30, 0.06),
        fontsize=8,
        color="#555",
        arrowprops=dict(arrowstyle="->", color="#999"),
    )
    fig.tight_layout()
    save(fig, "figure_5_safety_coverage_frontier")

    matrix = np.array(
        [[df[(df.family == family) & (np.isclose(df.margin, margin))].fs_among_unsafe.iloc[0] for margin in margins] for family in order]
    )
    fig, ax = plt.subplots(figsize=(6.8, 4.8))
    image = ax.imshow(matrix, cmap="RdYlGn_r", vmin=0, vmax=0.35, aspect="auto")
    ax.set_xticks(range(len(margins)))
    ax.set_xticklabels([f"m={margin:g}" for margin in margins])
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels(labels)
    ax.set_xlabel("Margin")
    ax.set_title("Eligibility map: false-safe rate by system and margin (classical baseline)", fontsize=10)
    for i in range(len(order)):
        for j in range(len(margins)):
            value = matrix[i, j]
            ax.text(j, i, f"{value:.3f}", ha="center", va="center", fontsize=9.5, color="white" if value > 0.18 else "black")
    colorbar = fig.colorbar(image, ax=ax, fraction=0.046, pad=0.04)
    colorbar.set_label("False-safe rate (unsafe-set)", fontsize=9)
    fig.tight_layout()
    save(fig, "figure_6_eligibility_map")


def main() -> None:
    plt.rcParams.update({"font.size": 10})
    rebuild_figure_2()
    rebuild_figure_5_and_6()
    print("Rebuilt final manuscript Figures 2, 5, and 6 from packaged summary tables.")


if __name__ == "__main__":
    main()
