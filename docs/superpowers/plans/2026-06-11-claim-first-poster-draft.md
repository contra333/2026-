# Claim-First Poster Draft Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a Korean-body, English-heading A0 poster draft that uses confirmed seed0 values to validate the logic and can later be updated with 3-seed `mean +/- std` results.

> Production update, 2026-06-11 KST: this plan is a historical implementation
> record for the earlier claim-first draft. The current production draft uses
> Figure 1 for the reliability failure concept diagram; the generated seed0
> reliability scatter is now Figure 2 and raw-to-L2 recovery is now Figure 3.
> Use `docs/research/poster_section_text.md` and `poster/poster.tex` as the
> current source of truth.

**Architecture:** Keep data, plotting, and TeX layout separate. Small seed0 CSV files under `tables/csv/` feed a plotting script under `analysis/scripts/`, which writes draft figures to `figures/source/`; `poster/poster.tex` consumes the tables and figures through the existing design harness macros.

**Tech Stack:** LaTeX/XeLaTeX or pdfLaTeX fallback, existing `wanted_poster_macros.tex`, Python 3, pandas, matplotlib.

---

## File Structure

- Create `tables/csv/seed0_id_calibration_summary_draft.csv`: confirmed seed0 selected-config ID/ECE values for Table 1.
- Create `tables/csv/seed0_dataset_raw_mahalanobis_draft.csv`: confirmed dataset-specific raw Mahalanobis AUROC values from `WRN seed0 350eps grid-search 실험_0531 371a26cf6e72819bacacd14427eb6614.md`.
- Create `tables/csv/seed0_raw_l2_recovery_draft.csv`: confirmed seed0 raw/L2 Mahalanobis and kNN mean AUROC values for the recovery figure now numbered Figure 3.
- Create `data/manifests/seed0_poster_draft_sources_20260611.md`: provenance note for copied seed0 draft values.
- Create `analysis/scripts/plot_seed0_draft_figures.py`: reads the CSVs and writes empirical source PDFs now displayed as poster Figure 2 and Figure 3.
- Modify `poster/poster.tex`: replace the old optimizer-row draft with the approved claim-first B layout.
- Do not modify experiment code under `/mnt/c/Users/User/Desktop/2027ICLR/code`.

## Data Scope Decisions

The provided local md file contains dataset-specific feature OOD values for:

- `SGD best val` = `sgd_lr1e-1_wd2e-4`
- `Adam wd=0 best val` = `adam_lr1e-3_wd0`
- `Adam wd>0 best val` = `adam_lr1e-3_wd1e-4`
- `AdamW best val` = `adamw_lr5e-3_wd1e-4`

It does not expose dataset-specific rows for `sgd_lr1e-1_wd5e-4_anchor` or `adamw_lr5e-3_wd5e-4_anchor` in the visible markdown table. Therefore the internal seed0 draft Table 2 must use only confirmed dataset-specific rows and include a Korean source note. The final poster Table 2 will be replaced by the selected 5 configs after 3-seed aggregation.

### Task 1: Create Seed0 Draft Data CSVs

**Files:**
- Create: `tables/csv/seed0_id_calibration_summary_draft.csv`
- Create: `tables/csv/seed0_dataset_raw_mahalanobis_draft.csv`
- Create: `tables/csv/seed0_raw_l2_recovery_draft.csv`
- Create: `data/manifests/seed0_poster_draft_sources_20260611.md`

- [ ] **Step 1: Create Table 1 CSV**

Use `apply_patch` to create `tables/csv/seed0_id_calibration_summary_draft.csv` with this exact content:

```csv
short_label,config_label,optimizer,val_acc,test_acc,ece,source_scope
SGD-A,sgd_lr1e-1_wd5e-4_anchor,SGD,0.9586,0.9585,0.0298,selected5_seed0_mean_source
SGD-B,sgd_lr1e-1_wd2e-4,SGD,0.9612,0.9546,0.0331,selected5_seed0_mean_source
Adam,adam_lr1e-3_wd1e-4,Adam,0.9494,0.9447,0.0390,selected5_seed0_mean_source
AdamW-B,adamw_lr5e-3_wd1e-4,AdamW,0.9528,0.9468,0.0451,selected5_seed0_mean_source
AdamW-A,adamw_lr5e-3_wd5e-4_anchor,AdamW,0.9502,0.9437,0.0479,selected5_seed0_mean_source
```

- [ ] **Step 2: Create Table 2 dataset-specific raw Mahalanobis CSV**

Use `apply_patch` to create `tables/csv/seed0_dataset_raw_mahalanobis_draft.csv` with this exact content:

```csv
short_label,config_label,optimizer,cifar100,tiny_imagenet,svhn,mnist,source_scope
SGD-B,sgd_lr1e-1_wd2e-4,SGD,0.8613,0.8569,0.9729,0.9457,dataset_specific_md_confirmed
Adam-0,adam_lr1e-3_wd0,Adam,0.6096,0.5654,0.9003,0.6301,dataset_specific_md_confirmed_supplement
Adam,adam_lr1e-3_wd1e-4,Adam,0.5680,0.5423,0.6604,0.4416,dataset_specific_md_confirmed
AdamW-B,adamw_lr5e-3_wd1e-4,AdamW,0.4353,0.3983,0.7828,0.2712,dataset_specific_md_confirmed
```

- [ ] **Step 3: Create Figure 3 recovery CSV**

Use `apply_patch` to create `tables/csv/seed0_raw_l2_recovery_draft.csv` with this exact content:

```csv
short_label,config_label,optimizer,raw_maha,maha_l2,raw_knn,knn_l2
SGD-A,sgd_lr1e-1_wd5e-4_anchor,SGD,0.9192,0.9300,0.9165,0.9236
SGD-B,sgd_lr1e-1_wd2e-4,SGD,0.9092,0.9242,0.9188,0.9233
Adam,adam_lr1e-3_wd1e-4,Adam,0.5531,0.8148,0.8692,0.8904
AdamW-B,adamw_lr5e-3_wd1e-4,AdamW,0.4719,0.9226,0.6538,0.9418
AdamW-A,adamw_lr5e-3_wd5e-4_anchor,AdamW,0.5311,0.9237,0.6703,0.9411
```

- [ ] **Step 4: Create provenance note**

Use `apply_patch` to create `data/manifests/seed0_poster_draft_sources_20260611.md` with this exact content:

```markdown
# Seed0 Poster Draft Sources

Date: 2026-06-11 KST

This manifest records small seed0 values copied into the poster workspace for the internal draft.

## Source files

- `docs/research/통계학회_포스터_실험계획.md`
- `docs/research/추가실험_승인_컨텍스트.md`
- `WRN seed0 350eps grid-search 실험_0531 371a26cf6e72819bacacd14427eb6614.md`

## Imported files

- `tables/csv/seed0_id_calibration_summary_draft.csv`
- `tables/csv/seed0_dataset_raw_mahalanobis_draft.csv`
- `tables/csv/seed0_raw_l2_recovery_draft.csv`

## Evidence boundary

These are seed0 diagnostic draft values. They are used to validate poster logic and layout before selected seed1/2 results finish. The final poster main tables and error bars should be replaced with selected 5 configs over seed0/1/2 as `mean +/- std`.

The dataset-specific raw Mahalanobis markdown source directly exposes rows for `SGD best val`, `Adam wd=0 best val`, `Adam wd>0 best val`, and `AdamW best val`. It does not expose dataset-specific rows for the SGD anchor or AdamW anchor in the visible markdown table, so the draft dataset-specific table uses confirmed source rows only.
```

- [ ] **Step 5: Verify CSV row counts**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import csv
checks = {
    'tables/csv/seed0_id_calibration_summary_draft.csv': 5,
    'tables/csv/seed0_dataset_raw_mahalanobis_draft.csv': 4,
    'tables/csv/seed0_raw_l2_recovery_draft.csv': 5,
}
for path, expected in checks.items():
    with Path(path).open(newline='') as f:
        rows = list(csv.DictReader(f))
    print(path, len(rows))
    assert len(rows) == expected, (path, len(rows), expected)
print('seed0 draft CSV row counts OK')
PY
```

Expected output:

```text
tables/csv/seed0_id_calibration_summary_draft.csv 5
tables/csv/seed0_dataset_raw_mahalanobis_draft.csv 4
tables/csv/seed0_raw_l2_recovery_draft.csv 5
seed0 draft CSV row counts OK
```

### Task 2: Create Draft Figure Script

**Files:**
- Create: `analysis/scripts/plot_seed0_draft_figures.py`
- Output: `figures/source/fig1_seed0_reliability_scatter_draft.pdf`
- Output: `figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf`

- [ ] **Step 1: Create plotting script**

Use `apply_patch` to create `analysis/scripts/plot_seed0_draft_figures.py` with the following complete script:

```python
#!/usr/bin/env python3
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "tables" / "csv"
FIG_DIR = ROOT / "figures" / "source"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "SGD": "#0070C0",
    "Adam": "#70AD47",
    "AdamW": "#C00000",
}


def plot_fig1():
    df = pd.read_csv(TABLE_DIR / "seed0_id_calibration_summary_draft.csv")
    fig, axes = plt.subplots(1, 2, figsize=(11.2, 4.2), constrained_layout=True)

    for ax, metric, ylabel in [
        (axes[0], "ece", "ECE"),
        (axes[1], "raw_maha", "Raw Mahalanobis AUROC"),
    ]:
        if metric == "raw_maha":
            recovery = pd.read_csv(TABLE_DIR / "seed0_raw_l2_recovery_draft.csv")
            plot_df = df.merge(recovery[["short_label", "raw_maha"]], on="short_label", how="left")
        else:
            plot_df = df.copy()

        for optimizer, group in plot_df.groupby("optimizer"):
            ax.scatter(
                group["val_acc"],
                group[metric],
                s=88,
                color=COLORS.get(optimizer, "#555555"),
                edgecolor="#202020",
                linewidth=0.6,
                label=optimizer,
                zorder=3,
            )
            for _, row in group.iterrows():
                ax.annotate(
                    row["short_label"],
                    (row["val_acc"], row[metric]),
                    xytext=(4, 4),
                    textcoords="offset points",
                    fontsize=8,
                )

        ax.set_xlabel("ID validation accuracy")
        ax.set_ylabel(ylabel)
        ax.grid(True, color="#D9E2EF", linewidth=0.6)
        ax.set_axisbelow(True)

    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", ncol=3, frameon=False)
    fig.suptitle("Figure 2. Accuracy-Matched Reliability Scatter (seed0 draft)", fontsize=13, fontweight="bold")
    fig.savefig(FIG_DIR / "fig1_seed0_reliability_scatter_draft.pdf")
    plt.close(fig)


def plot_fig2():
    df = pd.read_csv(TABLE_DIR / "seed0_raw_l2_recovery_draft.csv")
    metrics = [
        ("raw_maha", "Raw Maha", "#0070C0"),
        ("maha_l2", "Maha-L2", "#5B9BD5"),
        ("raw_knn", "Raw kNN", "#70AD47"),
        ("knn_l2", "kNN-L2", "#FFC000"),
    ]
    x = range(len(df))
    width = 0.18
    offsets = [-1.5 * width, -0.5 * width, 0.5 * width, 1.5 * width]

    fig, ax = plt.subplots(figsize=(11.2, 4.6), constrained_layout=True)
    for offset, (column, label, color) in zip(offsets, metrics):
        ax.bar([i + offset for i in x], df[column], width=width, label=label, color=color)

    ax.set_xticks(list(x))
    ax.set_xticklabels(df["short_label"])
    ax.set_ylim(0.2, 1.02)
    ax.set_ylabel("Near/Far mean AUROC")
    ax.set_title("Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity", fontsize=13, fontweight="bold")
    ax.grid(True, axis="y", color="#D9E2EF", linewidth=0.6)
    ax.set_axisbelow(True)
    ax.legend(ncol=4, loc="upper center", bbox_to_anchor=(0.5, 1.14), frameon=False)

    label_note = "SGD-A: SGD anchor | SGD-B: SGD val-best | Adam: Adam reg. | AdamW-B: AdamW val-best | AdamW-A: AdamW anchor"
    fig.text(0.5, -0.02, label_note, ha="center", fontsize=8, color="#555555")
    fig.savefig(FIG_DIR / "fig2_seed0_raw_to_l2_recovery_draft.pdf", bbox_inches="tight")
    plt.close(fig)


def main():
    plot_fig1()
    plot_fig2()
    print(FIG_DIR / "fig1_seed0_reliability_scatter_draft.pdf")
    print(FIG_DIR / "fig2_seed0_raw_to_l2_recovery_draft.pdf")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Run plotting script**

Run:

```bash
python3 analysis/scripts/plot_seed0_draft_figures.py
```

Expected output:

```text
/home/contra333/2026통계학회포스터/figures/source/fig1_seed0_reliability_scatter_draft.pdf
/home/contra333/2026통계학회포스터/figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf
```

- [ ] **Step 3: Verify figure files exist**

Run:

```bash
test -s figures/source/fig1_seed0_reliability_scatter_draft.pdf
test -s figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf
```

Expected: command exits with status 0.

### Task 3: Rewrite Poster TeX to Claim-First Draft

**Files:**
- Modify: `poster/poster.tex`

- [ ] **Step 1: Replace poster body with claim-first structure**

Use `apply_patch` to replace `poster/poster.tex` with a complete TeX document that uses:

```tex
\WantedHeader
  {Korean Statistical Society}
  {Optimizer-Induced Feature Geometry Shapes\\Post-Hoc OOD Detection Reliability}
  {ID accuracy alone does not guarantee reliable calibration or feature-based OOD detection.}
  {Gun-Hak Jin\\Department of Mathematical Data Science, Hanyang University}
```

The body must follow this section order:

```text
Claim
Experimental Design
Evidence 1. ID / Calibration
Evidence 2. Dataset-Specific Raw Mahalanobis
Figure 2. Accuracy-Matched Reliability Scatter
Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity
Mechanism Diagnostic
Future Work
```

Use Korean body text for explanations. Use English section bars and table/figure titles. Do not include LR/WD columns in Table 1 or Table 2. Include the draft data note:

```tex
{\WantedCaptionFont\color{WantedMuted}Draft values use seed0 diagnostic grid results. Final poster replaces selected rows with 3-seed mean $\pm$ std.}
```

- [ ] **Step 2: Add Table 1 manually from CSV values**

In `poster/poster.tex`, Table 1 rows must be:

```tex
SGD-A & SGD & 95.86 & 95.85 & 2.98 \\
SGD-B & SGD & 96.12 & 95.46 & 3.31 \\
Adam & Adam & 94.94 & 94.47 & 3.90 \\
AdamW-B & AdamW & 95.28 & 94.68 & 4.51 \\
AdamW-A & AdamW & 95.02 & 94.37 & 4.79 \\
```

Use percentage formatting for readability.

- [ ] **Step 3: Add Table 2 manually from confirmed dataset-specific md values**

In `poster/poster.tex`, Table 2 rows must be:

```tex
SGD-B & SGD & 0.861 & 0.857 & 0.973 & 0.946 \\
Adam-0 & Adam & 0.610 & 0.565 & 0.900 & 0.630 \\
Adam & Adam & 0.568 & 0.542 & 0.660 & 0.442 \\
AdamW-B & AdamW & 0.435 & 0.398 & 0.783 & 0.271 \\
```

Add a caption note in Korean:

```tex
Table 2의 seed0 dataset-specific source는 현재 4개 대표 후보만 직접 제공한다. 최종본에서는 selected 5 configs의 3-seed 집계값으로 교체한다.
```

- [ ] **Step 4: Include generated figure PDFs**

Use `\WantedFigureFile` to include:

```tex
\WantedFigureFile
  {Figure 2. Accuracy-Matched Reliability Scatter}
  {../figures/source/fig1_seed0_reliability_scatter_draft.pdf}
  {Seed0 draft: ID validation accuracy 대비 ECE와 raw Mahalanobis AUROC. 최종본에서는 seed0 grid background와 selected 5 configs의 3-seed error bar를 함께 표시한다.}

\WantedFigureFile
  {Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity}
  {../figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf}
  {L2-normalized controls reduce feature-scale effects while preserving angular information. Raw-to-L2 recovery suggests norm/covariance-scale sensitivity.}
```

### Task 4: Compile and Verify Poster Draft

**Files:**
- Read: `poster/poster.tex`
- Output: `poster/build/poster.pdf`

- [ ] **Step 1: Check TeX engine availability**

Run:

```bash
command -v xelatex || command -v pdflatex
```

Expected: prints at least one TeX engine path. Prefer `xelatex` for final Korean/Pretendard validation; use `pdflatex` only for structural fallback.

- [ ] **Step 2: Compile with the available engine**

If `xelatex` exists, run:

```bash
cd poster
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build poster.tex
```

If only `pdflatex` exists, run:

```bash
cd poster
pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build poster.tex
```

Expected: command exits with status 0 and writes `poster/build/poster.pdf`.

- [ ] **Step 3: Verify one-page PDF output**

Run:

```bash
pdfinfo poster/build/poster.pdf | rg '^Pages:'
```

Expected output:

```text
Pages:           1
```

- [ ] **Step 4: Inspect TeX log for hard errors**

Run:

```bash
rg -n "Overfull|LaTeX Warning|Package Warning|Error" poster/build/poster.log
```

Expected: no fatal `Error` lines. Overfull/Warning lines should be reviewed and either fixed or recorded in the final report.

### Task 5: Final Review Notes

**Files:**
- Read: `poster/poster.tex`
- Read: `tables/csv/*.csv`
- Read: `figures/source/*.pdf`

- [ ] **Step 1: Confirm spec coverage**

Run:

```bash
rg -n "Optimizer-Induced Feature Geometry Shapes|Raw-to-L2 Recovery|Future Work|Adam-AdamW|SGD-A|AdamW-A" poster/poster.tex
```

Expected: each phrase appears at least once.

- [ ] **Step 2: Confirm no old title remains**

Run:

```bash
rg -n "Changes Post-Hoc|A matched-accuracy optimizer comparison|WRN-28-10 or ResNet-18|Optimizer & Acc" poster/poster.tex
```

Expected: no matches.

- [ ] **Step 3: Report final status**

Final implementation report must include:

```text
- Updated poster/poster.tex to claim-first B layout.
- Added seed0 draft CSVs and provenance manifest.
- Generated empirical draft PDFs now displayed as Figure 2 and Figure 3.
- Built poster/build/poster.pdf.
- Data limitation: current dataset-specific seed0 markdown source directly exposes four representative rows; final selected-5 Table 2 should be replaced after 3-seed aggregation.
```
