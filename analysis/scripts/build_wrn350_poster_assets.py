#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
import shutil
import subprocess
import tempfile
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKAGE_DIR = ROOT / "wrn350_selected_3seed_raw_eval_results_20260612"
TABLE_CSV_DIR = ROOT / "tables" / "csv"
TABLE_TEX_DIR = ROOT / "tables" / "tex"
FIGURE_SOURCE_DIR = ROOT / "figures" / "source"
FIGURE_FINAL_DIR = ROOT / "figures" / "final"

CONFIG_ORDER = [
    "sgd_lr1e-1_wd5e-4_anchor",
    "sgd_lr1e-1_wd2e-4",
    "adam_lr1e-3_wd1e-4",
    "adamw_lr5e-3_wd1e-4",
    "adamw_lr5e-3_wd5e-4_anchor",
]
SHORT_LABELS = {
    "sgd_lr1e-1_wd5e-4_anchor": "SGD-5e-4",
    "sgd_lr1e-1_wd2e-4": "SGD-2e-4",
    "adam_lr1e-3_wd1e-4": "Adam",
    "adamw_lr5e-3_wd1e-4": "AdamW-1e-4",
    "adamw_lr5e-3_wd5e-4_anchor": "AdamW-5e-4",
}
NEAR_OOD_DATASETS = ["cifar100", "tiny_imagenet"]
DATASET_LABELS = {
    "cifar100": "CIFAR-100",
    "tiny_imagenet": "TinyImageNet",
}
MAIN_DETECTORS = ["mahalanobis", "mahalanobis_l2", "knn", "knn_l2"]
FIGURE3_REPRESENTATIVES = {
    "sgd_lr1e-1_wd5e-4_anchor",
    "adam_lr1e-3_wd1e-4",
    "adamw_lr5e-3_wd1e-4",
}
DETECTOR_LABELS = {
    "mahalanobis": "Raw Maha",
    "mahalanobis_l2": "Maha-L2",
    "knn": "Raw kNN",
    "knn_l2": "kNN-L2",
}
DETECTOR_COLORS = {
    "mahalanobis": "2F5597",
    "mahalanobis_l2": "5B9BD5",
    "knn": "70AD47",
    "knn_l2": "FFC000",
}


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv_rows(path: Path, rows: list[dict[str, object]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in fieldnames})


def parse_float(value: object) -> float | None:
    if value is None or value == "":
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    if math.isnan(parsed):
        return None
    return parsed


def mean_std(values: list[float]) -> tuple[float, float]:
    clean = [float(value) for value in values]
    if not clean:
        raise ValueError("cannot aggregate an empty value list")
    mean = sum(clean) / len(clean)
    if len(clean) == 1:
        return mean, 0.0
    variance = sum((value - mean) ** 2 for value in clean) / (len(clean) - 1)
    return mean, math.sqrt(variance)


def display_optimizer(value: str) -> str:
    normalized = value.lower()
    if normalized == "sgd":
        return "SGD"
    if normalized == "adamw":
        return "AdamW"
    if normalized == "adam":
        return "Adam"
    return value


def format_hparam(value: object) -> str:
    parsed = float(value)
    if parsed == 0:
        return "0"
    if abs(parsed) < 0.01:
        return f"{parsed:.0e}".replace("e-0", "e-").replace("e+0", "e+")
    return f"{parsed:g}"


def config_rank(label: str) -> int:
    try:
        return CONFIG_ORDER.index(label)
    except ValueError:
        return len(CONFIG_ORDER)


def detector_rank(detector: str) -> int:
    try:
        return MAIN_DETECTORS.index(detector)
    except ValueError:
        return len(MAIN_DETECTORS)


def dataset_rank(dataset: str) -> int:
    try:
        return NEAR_OOD_DATASETS.index(dataset)
    except ValueError:
        return len(NEAR_OOD_DATASETS)


def short_label(config_label: str) -> str:
    return SHORT_LABELS.get(config_label, config_label)


def format_pm(mean: object, std: object, *, scale: float = 1.0, decimals: int = 2) -> str:
    mean_value = parse_float(mean)
    std_value = parse_float(std)
    if mean_value is None or std_value is None:
        return "NA"
    return f"{mean_value * scale:.{decimals}f} $\\pm$ {std_value * scale:.{decimals}f}"


def build_validation_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    built = []
    for row in sorted(rows, key=lambda item: config_rank(item["config_label"])):
        built.append(
            {
                "label": short_label(row["config_label"]),
                "opt": display_optimizer(row["optimizer"]),
                "config": row["config_label"],
                "lr": format_hparam(row["lr"]),
                "wd": format_hparam(row["weight_decay"]),
                "id_test_acc": format_pm(row["id_test_acc_mean"], row["id_test_acc_std"], scale=100, decimals=2),
                "nll": format_pm(row["nll_mean"], row["nll_std"], decimals=3),
                "ece": format_pm(row["ece_15bin_mean"], row["ece_15bin_std"], scale=100, decimals=2),
                "t_ece": format_pm(
                    row["temperature_scaled_ece_15bin_mean"],
                    row["temperature_scaled_ece_15bin_std"],
                    scale=100,
                    decimals=2,
                ),
                "temp": format_pm(row["temperature_mean"], row["temperature_std"], decimals=2),
                "n_seeds": int(float(row["n_seeds"])),
            }
        )
    return built


def build_near_ood_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str, str, str], list[float]] = defaultdict(list)
    static: dict[tuple[str, str, str, str, str, str], dict[str, object]] = {}

    for row in rows:
        detector = row.get("detector", "")
        dataset = row.get("ood_dataset", "")
        if detector not in MAIN_DETECTORS or dataset not in NEAR_OOD_DATASETS:
            continue
        value = parse_float(row.get("auroc"))
        if value is None:
            continue
        key = (
            row["config_label"],
            row["optimizer"],
            row["lr"],
            row["weight_decay"],
            dataset,
            detector,
        )
        grouped[key].append(value)
        static.setdefault(
            key,
            {
                "label": short_label(row["config_label"]),
                "opt": display_optimizer(row["optimizer"]),
                "config": row["config_label"],
                "lr": format_hparam(row["lr"]),
                "wd": format_hparam(row["weight_decay"]),
                "dataset": dataset,
                "dataset_label": DATASET_LABELS[dataset],
                "detector": detector,
                "detector_label": DETECTOR_LABELS[detector],
            },
        )

    built = []
    for key, values in grouped.items():
        mean, std = mean_std(values)
        item = dict(static[key])
        item.update({"mean": mean, "std": std, "n_seeds": len(values)})
        built.append(item)

    return sorted(
        built,
        key=lambda row: (
            dataset_rank(str(row["dataset"])),
            config_rank(str(row["config"])),
            detector_rank(str(row["detector"])),
        ),
    )


def build_figure3_rows(near_ood_rows: list[dict[str, object]]) -> list[dict[str, object]]:
    return [row for row in near_ood_rows if row["config"] in FIGURE3_REPRESENTATIVES]


def build_geometry_rows(rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[str, dict[str, dict[str, str]]] = defaultdict(dict)
    static: dict[str, dict[str, object]] = {}
    for row in rows:
        config = row["config_label"]
        grouped[config][row["metric"]] = row
        static.setdefault(
            config,
            {
                "label": short_label(config),
                "opt": display_optimizer(row["optimizer"]),
                "config": config,
                "lr": format_hparam(row["lr"]),
                "wd": format_hparam(row["weight_decay"]),
                "n_seeds": int(float(row["n_seeds"])),
            },
        )

    built = []
    for config in sorted(grouped, key=config_rank):
        metrics = grouped[config]

        def metric_pm(metric: str, decimals: int) -> str:
            metric_row = metrics.get(metric)
            if metric_row is None:
                return "NA"
            return format_pm(metric_row["mean"], metric_row["std"], decimals=decimals)

        item = dict(static[config])
        item.update(
            {
                "nc1": metric_pm("nc1", 3),
                "inter_dist": metric_pm("inter_dist_l2", 2),
                "norm": metric_pm("feature_norm_mean", 2),
                "eff_rank": metric_pm("effective_rank", 1),
            }
        )
        built.append(item)
    return built


def latex_escape(text: object) -> str:
    return str(text).replace("_", "\\_")


def render_validation_tex(rows: list[dict[str, object]]) -> str:
    lines = [
        r"\begin{tabularx}{\linewidth}{@{}l l Z Z Z Z Z@{}}",
        r"\toprule",
        r"Config & Opt & ID Acc (\%) & NLL & ECE (\%) & T-ECE (\%) & Temp. \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(row['label'])} & {row['opt']} & {row['id_test_acc']} & {row['nll']} & "
            f"{row['ece']} & {row['t_ece']} & {row['temp']} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabularx}"])
    return "\n".join(lines) + "\n"


def render_geometry_tex(rows: list[dict[str, object]]) -> str:
    lines = [
        r"\begin{tabularx}{\linewidth}{@{}l l Z Z Z Z@{}}",
        r"\toprule",
        r"Config & Opt & NC1 $\downarrow$ & InterDist $\uparrow$ & $\|h\|_2$ & Eff. rank \\",
        r"\midrule",
    ]
    for row in rows:
        lines.append(
            f"{latex_escape(row['label'])} & {row['opt']} & {row['nc1']} & {row['inter_dist']} & "
            f"{row['norm']} & {row['eff_rank']} \\\\"
        )
    lines.extend([r"\bottomrule", r"\end{tabularx}"])
    return "\n".join(lines) + "\n"


def render_near_ood_figure_tex(rows: list[dict[str, object]]) -> str:
    config_labels = [short_label(label) for label in CONFIG_ORDER]
    color_defs = "\n".join(
        rf"\definecolor{{{detector}Color}}{{HTML}}{{{DETECTOR_COLORS[detector]}}}"
        for detector in MAIN_DETECTORS
    )
    plots = []
    for dataset in NEAR_OOD_DATASETS:
        plots.append(rf"\nextgroupplot[title={{{DATASET_LABELS[dataset]}}}]")
        for detector in MAIN_DETECTORS:
            detector_rows = [
                row
                for row in rows
                if row["dataset"] == dataset and row["detector"] == detector
            ]
            by_config = {row["config"]: row for row in detector_rows}
            coordinates = []
            for config in CONFIG_ORDER:
                row = by_config.get(config)
                if row is None:
                    continue
                coordinates.append(f"({short_label(config)},{row['mean']:.4f}) +- (0,{row['std']:.4f})")
            plots.append(
                rf"\addplot+[fill={detector}Color,draw=none,error bars/.cd,y dir=both,y explicit] "
                rf"coordinates {{{' '.join(coordinates)}}};"
            )
        if dataset == NEAR_OOD_DATASETS[0]:
            plots.append(r"\legend{Raw Maha,Maha-L2,Raw kNN,kNN-L2}")

    symbolic_coords = ",".join(config_labels)
    return rf"""
\documentclass[tikz,border=3mm]{{standalone}}
\usepackage{{pgfplots}}
\usepgfplotslibrary{{groupplots}}
\pgfplotsset{{compat=1.18}}
\definecolor{{GridColor}}{{HTML}}{{D9E2EF}}
{color_defs}
\begin{{document}}
\begin{{tikzpicture}}
\begin{{groupplot}}[
  group style={{group size=2 by 1,horizontal sep=1.2cm}},
  ybar,
  width=8.0cm,
  height=6.15cm,
  ymin=0.34,
  ymax=0.94,
  ylabel={{AUROC}},
  symbolic x coords={{{symbolic_coords}}},
  xtick=data,
  xticklabel style={{font=\scriptsize,rotate=18,anchor=east}},
  tick label style={{font=\scriptsize}},
  label style={{font=\small}},
  title style={{font=\bfseries\small}},
  enlarge x limits=0.13,
  grid=major,
  grid style={{draw=GridColor,line width=0.25pt}},
  legend style={{at={{(1.03,1.22)}},anchor=south,legend columns=4,draw=none,font=\scriptsize}},
  error bars/error bar style={{line width=0.35pt}},
  error bars/error mark options={{rotate=90,mark size=1.4pt,line width=0.35pt}},
  clip=false
]
{chr(10).join(plots)}
\end{{groupplot}}
\node[anchor=south,font=\bfseries\small] at (current bounding box.north)
{{Raw feature detectors can split; L2 controls recover much of the near-OOD ranking}};
\end{{tikzpicture}}
\end{{document}}
""".strip() + "\n"


def compile_tex(tex_source: str, output_pdf: Path) -> None:
    engine = shutil.which("xelatex")
    if engine is None:
        raise RuntimeError("xelatex is required to build poster figures")

    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="wrn_poster_fig_", dir="/tmp") as tmp:
        tmp_dir = Path(tmp)
        tex_path = tmp_dir / "figure.tex"
        tex_path.write_text(tex_source, encoding="utf-8")
        result = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
            cwd=tmp_dir,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stdout)
        shutil.copy2(tmp_dir / "figure.pdf", output_pdf)


def build_assets(package_dir: Path = DEFAULT_PACKAGE_DIR, *, compile_figure: bool = True) -> dict[str, Path]:
    analysis_dir = package_dir / "analysis_tables"
    validation_rows = build_validation_rows(read_csv_rows(analysis_dir / "mean_std.csv"))
    near_ood_rows = build_near_ood_rows(read_csv_rows(analysis_dir / "ood_by_dataset_long.csv"))
    geometry_rows = build_geometry_rows(read_csv_rows(analysis_dir / "geometry_mean_std_long.csv"))

    TABLE_CSV_DIR.mkdir(parents=True, exist_ok=True)
    TABLE_TEX_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    FIGURE_FINAL_DIR.mkdir(parents=True, exist_ok=True)

    validation_csv = TABLE_CSV_DIR / "wrn350_3seed_validation_calibration.csv"
    near_ood_csv = TABLE_CSV_DIR / "wrn350_3seed_near_ood_raw_l2.csv"
    geometry_csv = TABLE_CSV_DIR / "wrn350_3seed_geometry_summary.csv"
    validation_tex = TABLE_TEX_DIR / "wrn350_3seed_validation_calibration.tex"
    geometry_tex = TABLE_TEX_DIR / "wrn350_3seed_geometry_summary.tex"
    figure_tex = FIGURE_SOURCE_DIR / "fig3_wrn350_3optimizer_near_ood_raw_l2.tex"
    figure_pdf = FIGURE_FINAL_DIR / "fig3_wrn350_3optimizer_near_ood_raw_l2.pdf"

    write_csv_rows(
        validation_csv,
        validation_rows,
        ["label", "opt", "config", "lr", "wd", "id_test_acc", "nll", "ece", "t_ece", "temp", "n_seeds"],
    )
    write_csv_rows(
        near_ood_csv,
        near_ood_rows,
        [
            "label",
            "opt",
            "config",
            "lr",
            "wd",
            "dataset",
            "dataset_label",
            "detector",
            "detector_label",
            "mean",
            "std",
            "n_seeds",
        ],
    )
    write_csv_rows(
        geometry_csv,
        geometry_rows,
        ["label", "opt", "config", "lr", "wd", "nc1", "inter_dist", "norm", "eff_rank", "n_seeds"],
    )
    validation_tex.write_text(render_validation_tex(validation_rows), encoding="utf-8")
    geometry_tex.write_text(render_geometry_tex(geometry_rows), encoding="utf-8")

    figure_rows = build_figure3_rows(near_ood_rows)
    figure_source = render_near_ood_figure_tex(figure_rows)
    figure_tex.write_text(figure_source, encoding="utf-8")
    if compile_figure:
        compile_tex(figure_source, figure_pdf)

    return {
        "validation_csv": validation_csv,
        "near_ood_csv": near_ood_csv,
        "geometry_csv": geometry_csv,
        "validation_tex": validation_tex,
        "geometry_tex": geometry_tex,
        "figure_tex": figure_tex,
        "figure_pdf": figure_pdf,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build compact WRN350 3-seed poster tables and figures.")
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    parser.add_argument("--skip-figure", action="store_true", help="Write figure TeX but do not compile the PDF.")
    args = parser.parse_args()

    outputs = build_assets(args.package_dir, compile_figure=not args.skip_figure)
    for path in outputs.values():
        print(path)


if __name__ == "__main__":
    main()
