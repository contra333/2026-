#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import json
import math
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_PACKAGE_DIR = ROOT / "wrn350_selected_3seed_raw_eval_results_20260612"
DEFAULT_OUTPUT = ROOT / "docs" / "research" / "wrn350_selected_3seed_metrics_notion_20260612.md"

OOD_DATASETS = ["cifar100", "tiny_imagenet", "svhn", "mnist"]
OOD_METRICS = ["auroc", "fpr95", "aupr_in"]
LOGIT_DETECTORS = ["msp", "maxlogit", "energy_id_score", "neg_entropy"]
FEATURE_DETECTORS = [
    "mahalanobis",
    "mahalanobis_l2",
    "knn",
    "knn_l2",
    "gmm_ddu_tied",
    "gmm_ddu_diag",
    "gmm_ddu_shrinkage",
]
HYBRID_DETECTORS = ["ncc_distance", "nc_prototype_cosine", "vim_id_score"]
DETECTOR_ORDER = LOGIT_DETECTORS + FEATURE_DETECTORS + HYBRID_DETECTORS
GEOMETRY_METRIC_ORDER = [
    "nc0_width_norm",
    "nc0_by_K",
    "nc1",
    "nc2_mean_cos",
    "nc2_mean_etf",
    "nc2_weight_etf",
    "nc2_product_etf",
    "nc3_cos_alignment",
    "nc3_self_duality",
    "nc3_self_duality_raw",
    "nc4_agreement",
    "within_var",
    "inter_dist_l2",
    "inter_dist_sq",
    "anisotropy_lambda1_trace",
    "effective_rank",
    "condition_number_clipped",
]
FEATURE_SPLIT_ORDER = [
    "id_train",
    "id_val",
    "id_test",
    "ood_test_cifar100",
    "ood_test_tiny_imagenet",
    "ood_test_svhn",
    "ood_test_mnist",
]
FEATURE_STAT_COLUMNS = [
    "feature_dim",
    "num_samples",
    "feature_norm_mean",
    "feature_norm_std",
    "feature_norm_min",
    "feature_norm_q25",
    "feature_norm_median",
    "feature_norm_q75",
    "feature_norm_max",
]


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_float(value) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def mean_std(values: list[float]) -> tuple[float | None, float | None]:
    clean = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    if not clean:
        return None, None
    mean = sum(clean) / len(clean)
    if len(clean) == 1:
        return mean, 0.0
    variance = sum((v - mean) ** 2 for v in clean) / (len(clean) - 1)
    return mean, math.sqrt(variance)


def format_hparam(value: str | float) -> str:
    x = float(value)
    if x == 0:
        return "0"
    if abs(x) < 0.01:
        return f"{x:.0e}".replace("e-0", "e-").replace("e+0", "e+")
    return f"{x:g}"


def format_scalar(value: float | None, metric: str = "") -> str:
    if value is None:
        return "NA"
    if metric in {"feature_dim", "num_samples"}:
        return f"{value:.0f}"
    if value == 0:
        return "0"
    abs_value = abs(value)
    if abs_value >= 1000 or abs_value < 0.0001:
        return f"{value:.4g}"
    return f"{value:.4f}"


def format_mean_std(mean: float | None, std: float | None, metric: str = "") -> str:
    if mean is None or std is None:
        return "NA"
    return f"{format_scalar(mean, metric)} +/- {format_scalar(std, metric)}"


def markdown_escape(value) -> str:
    text = "" if value is None else str(value)
    return text.replace("\\", "\\\\").replace("|", "\\|").replace("\n", "<br>")


def markdown_table(headers: list[str], rows: list[dict[str, object]]) -> str:
    lines = [
        "| " + " | ".join(markdown_escape(header) for header in headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    for row in rows:
        lines.append("| " + " | ".join(markdown_escape(row.get(header, "")) for header in headers) + " |")
    return "\n".join(lines)


def detector_type(detector: str) -> str:
    if detector in LOGIT_DETECTORS:
        return "logit"
    if detector in FEATURE_DETECTORS:
        return "feature"
    if detector in HYBRID_DETECTORS:
        return "nc_hybrid"
    return "other"


def display_optimizer(value: str) -> str:
    normalized = value.lower()
    if normalized == "sgd":
        return "SGD"
    if normalized == "adamw":
        return "AdamW"
    if normalized == "adam":
        return "Adam"
    return value


def eval_dir_for(package_dir: Path, run_row: dict[str, str]) -> Path:
    return package_dir / run_row["package_path"] / "eval" / run_row["checkpoint_tag"]


def config_order(run_rows: list[dict[str, str]]) -> list[str]:
    order = []
    for row in run_rows:
        label = row["config_label"]
        if label not in order:
            order.append(label)
    return order


def config_rank(order: list[str], label: str) -> int:
    try:
        return order.index(label)
    except ValueError:
        return len(order)


def detector_rank(detector: str) -> int:
    try:
        return DETECTOR_ORDER.index(detector)
    except ValueError:
        return len(DETECTOR_ORDER)


def dataset_rank(dataset: str) -> int:
    try:
        return OOD_DATASETS.index(dataset)
    except ValueError:
        return len(OOD_DATASETS)


def geometry_rank(metric: str) -> int:
    try:
        return GEOMETRY_METRIC_ORDER.index(metric)
    except ValueError:
        return len(GEOMETRY_METRIC_ORDER)


def split_rank(split: str) -> int:
    try:
        return FEATURE_SPLIT_ORDER.index(split)
    except ValueError:
        return len(FEATURE_SPLIT_ORDER)


def aggregate_metric_rows(
    rows: list[dict[str, object]],
    key_fields: list[str],
    metric_field: str,
    value_field: str,
) -> list[dict[str, object]]:
    groups: dict[tuple, list[float]] = defaultdict(list)
    static: dict[tuple, dict[str, object]] = {}
    for row in rows:
        value = parse_float(row.get(value_field))
        if value is None:
            continue
        key = tuple(row.get(field, "") for field in key_fields + [metric_field])
        groups[key].append(value)
        static.setdefault(key, {field: row.get(field, "") for field in key_fields + [metric_field]})

    aggregated = []
    for key, values in groups.items():
        mean, std = mean_std(values)
        item = dict(static[key])
        item.update({"mean": mean, "std": std, "n_seeds": len(values)})
        aggregated.append(item)
    return aggregated


def aggregate_wide_rows(
    rows: list[dict[str, object]],
    key_fields: list[str],
    value_fields: list[str],
) -> list[dict[str, object]]:
    grouped: dict[tuple, list[dict[str, object]]] = defaultdict(list)
    for row in rows:
        key = tuple(row.get(field, "") for field in key_fields)
        grouped[key].append(row)

    out = []
    for key, group_rows in grouped.items():
        item = {field: key[index] for index, field in enumerate(key_fields)}
        seed_count = len({row.get("seed") for row in group_rows})
        item["n_seeds"] = seed_count
        for field in value_fields:
            values = [parse_float(row.get(field)) for row in group_rows]
            mean, std = mean_std([v for v in values if v is not None])
            item[f"{field}_mean"] = mean
            item[f"{field}_std"] = std
        out.append(item)
    return out


def aggregate_ood_rows(rows: list[dict[str, object]]) -> list[dict[str, object]]:
    key_fields = [
        "config_label",
        "optimizer",
        "lr",
        "weight_decay",
        "detector_type",
        "detector",
        "ood_dataset",
    ]
    long_rows = []
    for row in rows:
        for metric in OOD_METRICS:
            if metric not in row:
                continue
            value = parse_float(row.get(metric))
            if value is None:
                continue
            long_row = {field: row.get(field, "") for field in key_fields}
            long_row.update({"metric": metric, "value": value, "seed": row.get("seed", "")})
            long_rows.append(long_row)
    aggregated = aggregate_metric_rows(long_rows, key_fields, "metric", "value")
    return sorted(
        aggregated,
        key=lambda row: (
            dataset_rank(str(row["ood_dataset"])),
            detector_rank(str(row["detector"])),
            config_rank(CURRENT_CONFIG_ORDER, str(row["config_label"])),
            str(row["metric"]),
        ),
    )


CURRENT_CONFIG_ORDER: list[str] = []


def collect_training_eval_rows(package_dir: Path, run_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for run in run_rows:
        base = package_dir / run["package_path"]
        eval_dir = eval_dir_for(package_dir, run)
        training = read_json(base / "run_metadata" / "training_summary.json")
        classification = read_json(eval_dir / "metrics_classification.json")
        calibration = read_json(eval_dir / "metrics_calibration.json")
        row = {
            "config_label": run["config_label"],
            "optimizer": run["optimizer"],
            "lr": run["lr"],
            "weight_decay": run["weight_decay"],
            "seed": run["seed"],
            "best_val_epoch": training.get("best_val_epoch"),
            "best_val_acc": training.get("best_val_value"),
            "final_val_acc": training.get("final_val_metrics", {}).get("accuracy"),
            "final_val_nll": training.get("final_val_metrics", {}).get("nll"),
            "id_test_acc": classification.get("id_test", {}).get("accuracy"),
            "id_test_nll": classification.get("id_test", {}).get("nll"),
            "ece_15bin": calibration.get("id_test", {}).get("ece_15bin"),
            "temperature_scaled_ece_15bin": calibration.get("id_test", {}).get("temperature_scaled_ece_15bin"),
            "temperature": calibration.get("id_test", {}).get("temperature"),
        }
        rows.append(row)
    return rows


def collect_ood_rows(package_dir: Path, run_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    files = [
        ("metrics_ood_logit.json", "logit"),
        ("metrics_ood_feature.json", "feature"),
        ("metrics_ood_nc_hybrid.json", "nc_hybrid"),
    ]
    for run in run_rows:
        eval_dir = eval_dir_for(package_dir, run)
        for filename, fallback_type in files:
            data = read_json(eval_dir / filename)
            for detector, by_dataset in data.items():
                if detector in {"implemented_detectors", "ncc_accuracy"}:
                    continue
                if not isinstance(by_dataset, dict):
                    continue
                for dataset, metrics in by_dataset.items():
                    if dataset not in OOD_DATASETS or not isinstance(metrics, dict):
                        continue
                    row = {
                        "config_label": run["config_label"],
                        "optimizer": run["optimizer"],
                        "lr": run["lr"],
                        "weight_decay": run["weight_decay"],
                        "seed": run["seed"],
                        "detector_type": detector_type(detector) if detector_type(detector) != "other" else fallback_type,
                        "detector": detector,
                        "ood_dataset": dataset,
                    }
                    for metric in OOD_METRICS:
                        row[metric] = metrics.get(metric)
                    rows.append(row)
    return rows


def collect_ncc_accuracy_rows(package_dir: Path, run_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for run in run_rows:
        data = read_json(eval_dir_for(package_dir, run) / "metrics_ood_nc_hybrid.json")
        rows.append(
            {
                "config_label": run["config_label"],
                "optimizer": run["optimizer"],
                "lr": run["lr"],
                "weight_decay": run["weight_decay"],
                "seed": run["seed"],
                "metric": "ncc_accuracy_id_test",
                "value": data.get("ncc_accuracy", {}).get("id_test"),
            }
        )
    return rows


def collect_geometry_rows(package_dir: Path, run_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for run in run_rows:
        data = read_json(eval_dir_for(package_dir, run) / "metrics_geometry.json")
        id_train = data.get("id_train", {})
        for metric, value in id_train.items():
            if isinstance(value, (int, float)):
                rows.append(
                    {
                        "config_label": run["config_label"],
                        "optimizer": run["optimizer"],
                        "lr": run["lr"],
                        "weight_decay": run["weight_decay"],
                        "seed": run["seed"],
                        "metric": metric,
                        "value": value,
                    }
                )
    return rows


def collect_feature_stat_rows(package_dir: Path, run_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    rows = []
    for run in run_rows:
        data = read_json(eval_dir_for(package_dir, run) / "feature_stats.json")
        for split, stats in data.items():
            if not isinstance(stats, dict):
                continue
            quantiles = stats.get("feature_norm_quantiles", {})
            row = {
                "config_label": run["config_label"],
                "optimizer": run["optimizer"],
                "lr": run["lr"],
                "weight_decay": run["weight_decay"],
                "seed": run["seed"],
                "split": split,
                "feature_dim": stats.get("feature_dim"),
                "num_samples": stats.get("num_samples"),
                "feature_norm_mean": stats.get("feature_norm_mean"),
                "feature_norm_std": stats.get("feature_norm_std"),
                "feature_norm_min": quantiles.get("min"),
                "feature_norm_q25": quantiles.get("q25"),
                "feature_norm_median": quantiles.get("median"),
                "feature_norm_q75": quantiles.get("q75"),
                "feature_norm_max": quantiles.get("max"),
            }
            rows.append(row)
    return rows


def render_config_table(run_rows: list[dict[str, str]]) -> str:
    rows = []
    for label in config_order(run_rows):
        matching = [row for row in run_rows if row["config_label"] == label]
        first = matching[0]
        checkpoint_tags = ", ".join(sorted({row["checkpoint_tag"] for row in matching}))
        rows.append(
            {
                "Optimizer": display_optimizer(first["optimizer"]),
                "Config": label,
                "LR": format_hparam(first["lr"]),
                "WD": format_hparam(first["weight_decay"]),
                "Seeds": ", ".join(row["seed"] for row in matching),
                "Checkpoint tags": checkpoint_tags,
            }
        )
    return markdown_table(["Optimizer", "Config", "LR", "WD", "Seeds", "Checkpoint tags"], rows)


def render_training_eval_table(rows: list[dict[str, object]]) -> str:
    metrics = [
        "best_val_epoch",
        "best_val_acc",
        "final_val_acc",
        "id_test_acc",
        "id_test_nll",
        "ece_15bin",
        "temperature_scaled_ece_15bin",
        "temperature",
    ]
    aggregated = aggregate_wide_rows(
        rows,
        ["config_label", "optimizer", "lr", "weight_decay"],
        metrics,
    )
    aggregated.sort(key=lambda row: config_rank(CURRENT_CONFIG_ORDER, str(row["config_label"])))
    table_rows = []
    for row in aggregated:
        table_rows.append(
            {
                "Opt": display_optimizer(str(row["optimizer"])),
                "Config": row["config_label"],
                "LR": format_hparam(row["lr"]),
                "WD": format_hparam(row["weight_decay"]),
                "Best val epoch": format_mean_std(row["best_val_epoch_mean"], row["best_val_epoch_std"]),
                "Best val acc": format_mean_std(row["best_val_acc_mean"], row["best_val_acc_std"]),
                "Final val acc": format_mean_std(row["final_val_acc_mean"], row["final_val_acc_std"]),
                "ID test acc": format_mean_std(row["id_test_acc_mean"], row["id_test_acc_std"]),
                "ID test NLL": format_mean_std(row["id_test_nll_mean"], row["id_test_nll_std"]),
                "ECE": format_mean_std(row["ece_15bin_mean"], row["ece_15bin_std"]),
                "T-ECE": format_mean_std(
                    row["temperature_scaled_ece_15bin_mean"],
                    row["temperature_scaled_ece_15bin_std"],
                ),
                "Temp.": format_mean_std(row["temperature_mean"], row["temperature_std"]),
            }
        )
    headers = [
        "Opt",
        "Config",
        "LR",
        "WD",
        "Best val epoch",
        "Best val acc",
        "Final val acc",
        "ID test acc",
        "ID test NLL",
        "ECE",
        "T-ECE",
        "Temp.",
    ]
    return markdown_table(headers, table_rows)


def render_ncc_accuracy_table(rows: list[dict[str, object]]) -> str:
    aggregated = aggregate_metric_rows(
        rows,
        ["config_label", "optimizer", "lr", "weight_decay"],
        "metric",
        "value",
    )
    aggregated.sort(key=lambda row: config_rank(CURRENT_CONFIG_ORDER, str(row["config_label"])))
    table_rows = []
    for row in aggregated:
        table_rows.append(
            {
                "Opt": display_optimizer(str(row["optimizer"])),
                "Config": row["config_label"],
                "LR": format_hparam(row["lr"]),
                "WD": format_hparam(row["weight_decay"]),
                "NCC ID-test accuracy": format_mean_std(row["mean"], row["std"]),
                "n": row["n_seeds"],
            }
        )
    return markdown_table(["Opt", "Config", "LR", "WD", "NCC ID-test accuracy", "n"], table_rows)


def render_ood_tables(aggregated: list[dict[str, object]]) -> str:
    sections = []
    by_dataset: dict[str, list[dict[str, object]]] = defaultdict(list)
    for row in aggregated:
        by_dataset[str(row["ood_dataset"])].append(row)

    for dataset in OOD_DATASETS:
        rows = by_dataset.get(dataset, [])
        rows.sort(
            key=lambda row: (
                detector_rank(str(row["detector"])),
                config_rank(CURRENT_CONFIG_ORDER, str(row["config_label"])),
                str(row["metric"]),
            )
        )
        grouped: dict[tuple, dict[str, object]] = {}
        for row in rows:
            key = (
                row["detector_type"],
                row["detector"],
                row["optimizer"],
                row["config_label"],
                row["lr"],
                row["weight_decay"],
            )
            grouped.setdefault(
                key,
                {
                    "Family": row["detector_type"],
                    "Detector": row["detector"],
                    "Opt": display_optimizer(str(row["optimizer"])),
                    "Config": row["config_label"],
                    "LR": format_hparam(row["lr"]),
                    "WD": format_hparam(row["weight_decay"]),
                    "AUROC": "NA",
                    "FPR95": "NA",
                    "AUPR-IN": "NA",
                    "n": row["n_seeds"],
                },
            )
            metric_label = {"auroc": "AUROC", "fpr95": "FPR95", "aupr_in": "AUPR-IN"}[str(row["metric"])]
            grouped[key][metric_label] = format_mean_std(row["mean"], row["std"], str(row["metric"]))

        table_rows = list(grouped.values())
        table_rows.sort(
            key=lambda row: (
                detector_rank(str(row["Detector"])),
                config_rank(CURRENT_CONFIG_ORDER, str(row["Config"])),
            )
        )
        sections.append(f"### OOD dataset: `{dataset}`\n\n" + markdown_table(
            ["Family", "Detector", "Opt", "Config", "LR", "WD", "AUROC", "FPR95", "AUPR-IN", "n"],
            table_rows,
        ))
    return "\n\n".join(sections)


def render_geometry_table(rows: list[dict[str, object]]) -> str:
    aggregated = aggregate_metric_rows(
        rows,
        ["config_label", "optimizer", "lr", "weight_decay"],
        "metric",
        "value",
    )
    aggregated.sort(
        key=lambda row: (
            geometry_rank(str(row["metric"])),
            config_rank(CURRENT_CONFIG_ORDER, str(row["config_label"])),
        )
    )
    table_rows = []
    for row in aggregated:
        table_rows.append(
            {
                "Metric": row["metric"],
                "Opt": display_optimizer(str(row["optimizer"])),
                "Config": row["config_label"],
                "LR": format_hparam(row["lr"]),
                "WD": format_hparam(row["weight_decay"]),
                "Value": format_mean_std(row["mean"], row["std"], str(row["metric"])),
                "n": row["n_seeds"],
            }
        )
    return markdown_table(["Metric", "Opt", "Config", "LR", "WD", "Value", "n"], table_rows)


def render_feature_stats_table(rows: list[dict[str, object]]) -> str:
    aggregated = aggregate_wide_rows(
        rows,
        ["config_label", "optimizer", "lr", "weight_decay", "split"],
        FEATURE_STAT_COLUMNS,
    )
    aggregated.sort(
        key=lambda row: (
            split_rank(str(row["split"])),
            config_rank(CURRENT_CONFIG_ORDER, str(row["config_label"])),
        )
    )
    table_rows = []
    for row in aggregated:
        item = {
            "Split": row["split"],
            "Opt": display_optimizer(str(row["optimizer"])),
            "Config": row["config_label"],
            "LR": format_hparam(row["lr"]),
            "WD": format_hparam(row["weight_decay"]),
            "Dim": format_mean_std(row["feature_dim_mean"], row["feature_dim_std"], "feature_dim"),
            "N": format_mean_std(row["num_samples_mean"], row["num_samples_std"], "num_samples"),
            "Norm mean": format_mean_std(row["feature_norm_mean_mean"], row["feature_norm_mean_std"]),
            "Norm std": format_mean_std(row["feature_norm_std_mean"], row["feature_norm_std_std"]),
            "Min": format_mean_std(row["feature_norm_min_mean"], row["feature_norm_min_std"]),
            "Q25": format_mean_std(row["feature_norm_q25_mean"], row["feature_norm_q25_std"]),
            "Median": format_mean_std(row["feature_norm_median_mean"], row["feature_norm_median_std"]),
            "Q75": format_mean_std(row["feature_norm_q75_mean"], row["feature_norm_q75_std"]),
            "Max": format_mean_std(row["feature_norm_max_mean"], row["feature_norm_max_std"]),
            "n": row["n_seeds"],
        }
        table_rows.append(item)
    headers = ["Split", "Opt", "Config", "LR", "WD", "Dim", "N", "Norm mean", "Norm std", "Min", "Q25", "Median", "Q75", "Max", "n"]
    return markdown_table(headers, table_rows)


def render_metric_dictionary() -> str:
    classification_rows = [
        {"Metric": "best_val_epoch", "Meaning": "Validation accuracy가 가장 높았던 epoch.", "Direction": "descriptive"},
        {"Metric": "best_val_acc", "Meaning": "ID validation split에서 관측된 최고 accuracy.", "Direction": "higher better"},
        {"Metric": "final_val_acc", "Meaning": "최종 checkpoint 기준 ID validation accuracy.", "Direction": "higher better"},
        {"Metric": "id_test_acc", "Meaning": "ID test split에서의 classification accuracy.", "Direction": "higher better"},
        {"Metric": "id_test_nll", "Meaning": "ID test split negative log-likelihood.", "Direction": "lower better"},
        {"Metric": "ece_15bin", "Meaning": "15-bin Expected Calibration Error.", "Direction": "lower better"},
        {"Metric": "temperature_scaled_ece_15bin", "Meaning": "ID validation에서 fit한 temperature를 적용한 뒤의 15-bin ECE.", "Direction": "lower better"},
        {"Metric": "temperature", "Meaning": "Temperature scaling에서 학습된 scalar temperature.", "Direction": "diagnostic"},
        {"Metric": "ncc_accuracy_id_test", "Meaning": "ID train class mean으로 만든 nearest-class-center classifier의 ID test accuracy.", "Direction": "higher better"},
    ]
    ood_rows = [
        {"Metric": "AUROC", "Meaning": "ID score가 OOD score보다 높게 rank될 확률. ID label=1, OOD label=0.", "Direction": "higher better"},
        {"Metric": "FPR95", "Meaning": "ID recall을 95%로 맞추는 threshold에서 OOD가 ID로 통과하는 비율.", "Direction": "lower better"},
        {"Metric": "AUPR-IN", "Meaning": "ID를 positive class로 둔 precision-recall curve 아래 면적.", "Direction": "higher better"},
    ]
    detector_rows = [
        {"Detector": "msp", "Family": "logit", "Score": "maximum softmax probability.", "Note": "higher means more ID-like"},
        {"Detector": "maxlogit", "Family": "logit", "Score": "maximum logit.", "Note": "higher means more ID-like"},
        {"Detector": "energy_id_score", "Family": "logit", "Score": "T logsumexp(z / T), project ID-like sign.", "Note": "not negative energy in storage"},
        {"Detector": "neg_entropy", "Family": "logit", "Score": "negative predictive entropy.", "Note": "higher means lower entropy and more ID-like"},
        {"Detector": "mahalanobis", "Family": "feature", "Score": "negative tied-covariance class Mahalanobis distance.", "Note": "fit on ID train features"},
        {"Detector": "mahalanobis_l2", "Family": "feature", "Score": "Mahalanobis after detector-side L2 feature normalization.", "Note": "Mahalanobis++-motivated control, not full reproduction"},
        {"Detector": "knn", "Family": "feature", "Score": "negative k-th nearest-neighbor distance, k=50.", "Note": "fit on ID train features"},
        {"Detector": "knn_l2", "Family": "feature", "Score": "kNN after detector-side L2 feature normalization.", "Note": "feature-scale control"},
        {"Detector": "gmm_ddu_tied", "Family": "feature", "Score": "DDU-style GMM log density with tied covariance.", "Note": "not full DDU reproduction"},
        {"Detector": "gmm_ddu_diag", "Family": "feature", "Score": "DDU-style GMM log density with classwise diagonal covariance.", "Note": "not full DDU reproduction"},
        {"Detector": "gmm_ddu_shrinkage", "Family": "feature", "Score": "DDU-style GMM log density with classwise shrinkage covariance.", "Note": "alpha selected on ID val likelihood"},
        {"Detector": "ncc_distance", "Family": "nc_hybrid", "Score": "negative distance to nearest ID train class mean.", "Note": "prototype distance diagnostic"},
        {"Detector": "nc_prototype_cosine", "Family": "nc_hybrid", "Score": "maximum cosine between L2 feature and L2 class mean.", "Note": "prototype angular diagnostic"},
        {"Detector": "vim_id_score", "Family": "nc_hybrid", "Score": "ViM-derived ID-like score after project transform.", "Note": "diagnostic only"},
    ]
    geometry_rows = [
        {"Metric": "nc0_width_norm", "Meaning": "global mean / class-mean centering 관련 NC0 width statistic.", "Direction": "diagnostic"},
        {"Metric": "nc0_by_K", "Meaning": "NC0 statistic scaled by number of classes.", "Direction": "diagnostic"},
        {"Metric": "nc1", "Meaning": "within-class variability relative to class separation.", "Direction": "lower often means more collapsed class geometry"},
        {"Metric": "nc2_mean_cos", "Meaning": "class mean cosine structure statistic.", "Direction": "diagnostic"},
        {"Metric": "nc2_mean_etf", "Meaning": "class means의 ETF deviation.", "Direction": "lower means closer to ETF"},
        {"Metric": "nc2_weight_etf", "Meaning": "classifier weights의 ETF deviation.", "Direction": "lower means closer to ETF"},
        {"Metric": "nc2_product_etf", "Meaning": "class mean / weight product geometry ETF deviation.", "Direction": "diagnostic"},
        {"Metric": "nc3_cos_alignment", "Meaning": "classifier weight와 class mean direction의 cosine alignment.", "Direction": "higher means stronger alignment"},
        {"Metric": "nc3_self_duality", "Meaning": "normalized self-duality distance.", "Direction": "lower means closer self-duality"},
        {"Metric": "nc3_self_duality_raw", "Meaning": "raw Frobenius self-duality distance before paper normalization.", "Direction": "lower means closer self-duality"},
        {"Metric": "nc4_agreement", "Meaning": "classifier prediction and nearest-class-center prediction agreement.", "Direction": "higher means stronger agreement"},
        {"Metric": "within_var", "Meaning": "ID train within-class feature variance.", "Direction": "diagnostic"},
        {"Metric": "inter_dist_l2", "Meaning": "off-diagonal class mean pair L2 distance.", "Direction": "higher means larger class-mean separation"},
        {"Metric": "inter_dist_sq", "Meaning": "squared class mean pair distance.", "Direction": "higher means larger class-mean separation"},
        {"Metric": "anisotropy_lambda1_trace", "Meaning": "largest covariance eigenvalue divided by covariance trace.", "Direction": "higher means more anisotropic covariance"},
        {"Metric": "effective_rank", "Meaning": "entropy-based effective rank of within-class covariance spectrum.", "Direction": "higher means covariance energy is spread over more directions"},
        {"Metric": "condition_number_clipped", "Meaning": "clipped covariance condition-number diagnostic.", "Direction": "higher means more ill-conditioned covariance"},
        {"Metric": "covariance_eigenspectrum", "Meaning": "640-dimensional sorted within-class covariance eigenvalue vector.", "Direction": "vector diagnostic; not expanded in table"},
    ]
    feature_rows = [
        {"Metric": "feature_dim", "Meaning": "feature dimensionality.", "Direction": "metadata"},
        {"Metric": "num_samples", "Meaning": "samples in the split used for feature statistics.", "Direction": "metadata"},
        {"Metric": "feature_norm_mean", "Meaning": "mean L2 norm of penultimate features.", "Direction": "diagnostic"},
        {"Metric": "feature_norm_std", "Meaning": "standard deviation of feature L2 norm.", "Direction": "diagnostic"},
        {"Metric": "feature_norm_min/q25/median/q75/max", "Meaning": "feature L2 norm quantiles.", "Direction": "diagnostic"},
    ]
    parts = [
        "### Classification, Validation, and Calibration Metrics\n\n" + markdown_table(["Metric", "Meaning", "Direction"], classification_rows),
        "### OOD Aggregate Metrics\n\n" + markdown_table(["Metric", "Meaning", "Direction"], ood_rows),
        "### OOD Detectors\n\n" + markdown_table(["Detector", "Family", "Score", "Note"], detector_rows),
        "### Geometry Metrics\n\n" + markdown_table(["Metric", "Meaning", "Direction"], geometry_rows),
        "### Feature Statistics\n\n" + markdown_table(["Metric", "Meaning", "Direction"], feature_rows),
    ]
    return "\n\n".join(parts)


def render_equations() -> str:
    return """
## 수식 정의

수식은 Notion 가져오기에서 깨지지 않도록 표 안에 넣지 않고, 각각 독립된 block equation으로 둔다.

Accuracy:

$$
\\mathrm{Accuracy}=\\frac{1}{n}\\sum_{i=1}^{n}\\mathbf{1}(\\hat{y}_i=y_i)
$$

Negative log-likelihood:

$$
\\mathrm{NLL}=-\\frac{1}{n}\\sum_{i=1}^{n}\\log p_i(y_i)
$$

ECE with bins:

$$
\\mathrm{ECE}=\\sum_{b=1}^{B}\\frac{|B_b|}{n}\\left|\\mathrm{acc}(B_b)-\\mathrm{conf}(B_b)\\right|
$$

AUROC under the project convention, where higher score is more ID-like:

$$
\\mathrm{AUROC}=P(s(x_{\\mathrm{ID}})>s(x_{\\mathrm{OOD}}))
$$

Mahalanobis ID-like score:

$$
s(x)=-\\min_k (h(x)-\\mu_k)^T\\Sigma^{-1}(h(x)-\\mu_k)
$$

kNN ID-like score:

$$
s(x)=-d_k(h(x),\\mathcal{H}_{\\mathrm{ID\\ train}})
$$

Feature norm:

$$
\\|h(x)\\|_2=\\sqrt{\\sum_j h_j(x)^2}
$$

Sample standard deviation used in all `mean +/- std` cells:

$$
s=\\sqrt{\\frac{1}{m-1}\\sum_{r=1}^{m}(x_r-\\bar{x})^2}
$$
""".strip()


def render_report(package_dir: Path) -> str:
    global CURRENT_CONFIG_ORDER
    run_rows = read_csv_rows(package_dir / "run_index.csv")
    CURRENT_CONFIG_ORDER = config_order(run_rows)
    manifest = read_json(package_dir / "package_manifest.json")

    training_eval = collect_training_eval_rows(package_dir, run_rows)
    ood_rows = collect_ood_rows(package_dir, run_rows)
    ood_aggregated = aggregate_ood_rows(ood_rows)
    ncc_rows = collect_ncc_accuracy_rows(package_dir, run_rows)
    geometry_rows = collect_geometry_rows(package_dir, run_rows)
    feature_stats = collect_feature_stat_rows(package_dir, run_rows)

    source_rows = [
        {"Item": "Package", "Value": manifest.get("package_name", package_dir.name)},
        {"Item": "Created at", "Value": manifest.get("created_at_kst", "NA")},
        {"Item": "Model", "Value": manifest.get("experiment", {}).get("model", "NA")},
        {"Item": "ID dataset", "Value": manifest.get("experiment", {}).get("id_dataset", "NA")},
        {"Item": "OOD datasets", "Value": ", ".join(manifest.get("experiment", {}).get("ood_datasets", []))},
        {"Item": "Seed0 source", "Value": manifest.get("source_files", {}).get("seed0_zip", "NA")},
        {"Item": "Seed1/2 manifest", "Value": manifest.get("source_files", {}).get("seed1_seed2_manifest", "NA")},
    ]

    sections = [
        "# WRN-28-10 Selected 3-Seed Metric Summary for Notion",
        "작성일: 2026-06-12 KST",
        "",
        "이 문서는 `wrn350_selected_3seed_raw_eval_results_20260612`의 raw evaluation JSON을 기준으로, 선택된 5개 WRN-28-10/CIFAR-10 config의 metric을 3 seeds `mean +/- std`로 정리한 Notion import용 markdown이다.",
        "",
        "핵심 원칙:",
        "",
        "- 모든 `std`는 sample standard deviation, 즉 `ddof=1`이다.",
        "- OOD metric은 `cifar100`, `tiny_imagenet`, `svhn`, `mnist`별로만 정리한다. 서로 다른 OOD dataset 간 평균은 이 문서의 OOD 표에 넣지 않는다.",
        "- SGD와 AdamW는 선택 config가 각각 2개이므로 optimizer 안에서 LR/WD config별 행을 유지한다. config끼리 추가 평균내지 않는다.",
        "- 모든 OOD score convention은 `higher score = more ID-like`, `ID label = 1`, `OOD label = 0`이다.",
        "- `gmm_ddu_*`는 `DDU-style GMM feature density` 진단으로만 해석한다. 원 DDU 전체 reproduction이라고 쓰지 않는다.",
        "",
        "## Source and Evidence Boundary",
        markdown_table(["Item", "Value"], source_rows),
        "",
        "## Configs Included",
        render_config_table(run_rows),
        "",
        "## Validation, ID Test, and Calibration",
        render_training_eval_table(training_eval),
        "",
        "## OOD Metrics by Dataset",
        "아래 표들은 OOD dataset별로 분리되어 있다. `AUROC`, `FPR95`, `AUPR-IN` 각각은 같은 OOD dataset 안에서만 seed0/1/2 평균과 표준편차를 계산했다.",
        render_ood_tables(ood_aggregated),
        "",
        "## NCC Classifier Accuracy",
        "이 값은 OOD AUROC가 아니라 ID test에서 nearest-class-center classifier label accuracy를 측정한 hybrid diagnostic이다.",
        render_ncc_accuracy_table(ncc_rows),
        "",
        "## Geometry Scalars on `id_train`",
        "아래 scalar들은 `metrics_geometry.json`의 `id_train` 아래에 있는 numeric metric을 모두 집계한 것이다. `covariance_eigenspectrum`은 길이 640의 vector라서 표에는 펼치지 않고, metric dictionary에 별도로 적었다.",
        render_geometry_table(geometry_rows),
        "",
        "## Feature Norm Statistics by Split",
        "Feature norm 통계는 ID split과 각 OOD split을 분리해서 정리한다.",
        render_feature_stats_table(feature_stats),
        "",
        "## Metric Dictionary",
        render_metric_dictionary(),
        "",
        render_equations(),
        "",
        "## Notes for Later Analysis",
        "",
        "- Poster용 `near` 또는 `far` 평균이 필요하면 별도 분석 단계에서 명시적으로 만들 수 있다. 다만 이 Notion import 문서의 OOD 표는 사용자의 요청에 맞춰 dataset별 값만 둔다.",
        "- `train_metrics.jsonl`과 `val_metrics.jsonl`에는 epoch-wise logs가 보존되어 있다. 이 문서에서는 `training_summary.json`의 best/final validation summary만 3-seed 표로 집계했다.",
        "- `sgd_lr1e-1_wd5e-4_anchor`의 seed0은 package convention상 `final` checkpoint이며, 나머지 seed/config는 `epoch_0350` 평가다.",
    ]
    return "\n\n".join(sections) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Build Notion-safe WRN350 3-seed metric markdown.")
    parser.add_argument("--package-dir", type=Path, default=DEFAULT_PACKAGE_DIR)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    report = render_report(args.package_dir)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(report, encoding="utf-8")
    print(args.output)


if __name__ == "__main__":
    main()
