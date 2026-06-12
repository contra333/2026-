#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

import build_wrn350_poster_assets as poster_assets


class PosterAssetBuilderTests(unittest.TestCase):
    def test_near_ood_rows_keep_datasets_separate_and_filter_main_detectors(self):
        rows = [
            {
                "config_label": "cfg_a",
                "optimizer": "SGD",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "0",
                "detector": "mahalanobis",
                "ood_dataset": "cifar100",
                "auroc": "0.80",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "SGD",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "1",
                "detector": "mahalanobis",
                "ood_dataset": "cifar100",
                "auroc": "0.90",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "SGD",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "0",
                "detector": "mahalanobis",
                "ood_dataset": "tiny_imagenet",
                "auroc": "0.70",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "SGD",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "0",
                "detector": "msp",
                "ood_dataset": "cifar100",
                "auroc": "0.99",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "SGD",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "0",
                "detector": "knn_l2",
                "ood_dataset": "mnist",
                "auroc": "0.20",
            },
        ]

        built = poster_assets.build_near_ood_rows(rows)
        keys = {(row["dataset"], row["detector"]) for row in built}

        self.assertEqual(keys, {("cifar100", "mahalanobis"), ("tiny_imagenet", "mahalanobis")})
        cifar = next(row for row in built if row["dataset"] == "cifar100")
        self.assertAlmostEqual(cifar["mean"], 0.85)
        self.assertAlmostEqual(cifar["std"], 0.0707106781)
        self.assertEqual(cifar["n_seeds"], 2)

    def test_validation_rows_format_accuracy_as_percent_and_ece_as_points(self):
        rows = [
            {
                "config_label": "cfg_a",
                "optimizer": "adamw",
                "lr": "0.005",
                "weight_decay": "0.0001",
                "n_seeds": "3",
                "id_test_acc_mean": "0.9447333",
                "id_test_acc_std": "0.0024007",
                "nll_mean": "0.5268420",
                "nll_std": "0.0047578",
                "ece_15bin_mean": "0.0464925",
                "ece_15bin_std": "0.0019710",
                "temperature_scaled_ece_15bin_mean": "0.0062494",
                "temperature_scaled_ece_15bin_std": "0.0014967",
                "temperature_mean": "5.0190930",
                "temperature_std": "0.1098036",
            }
        ]

        built = poster_assets.build_validation_rows(rows)

        self.assertEqual(built[0]["opt"], "AdamW")
        self.assertEqual(built[0]["id_test_acc"], "94.47 $\\pm$ 0.24")
        self.assertEqual(built[0]["ece"], "4.65 $\\pm$ 0.20")
        self.assertEqual(built[0]["t_ece"], "0.62 $\\pm$ 0.15")
        self.assertEqual(built[0]["temp"], "5.02 $\\pm$ 0.11")

    def test_geometry_rows_pivot_selected_metrics(self):
        rows = [
            {
                "config_label": "cfg_a",
                "optimizer": "sgd",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "metric": "nc1",
                "mean": "0.051239",
                "std": "0.002452",
                "n_seeds": "3",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "sgd",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "metric": "inter_dist_l2",
                "mean": "16.6181",
                "std": "0.1942",
                "n_seeds": "3",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "sgd",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "metric": "feature_norm_mean",
                "mean": "14.2310",
                "std": "0.1504",
                "n_seeds": "3",
            },
            {
                "config_label": "cfg_a",
                "optimizer": "sgd",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "metric": "effective_rank",
                "mean": "59.5493",
                "std": "1.7959",
                "n_seeds": "3",
            },
        ]

        built = poster_assets.build_geometry_rows(rows)

        self.assertEqual(built[0]["nc1"], "0.051 $\\pm$ 0.002")
        self.assertEqual(built[0]["inter_dist"], "16.62 $\\pm$ 0.19")
        self.assertEqual(built[0]["norm"], "14.23 $\\pm$ 0.15")
        self.assertEqual(built[0]["eff_rank"], "59.5 $\\pm$ 1.8")

    def test_figure3_rows_keep_one_representative_per_optimizer(self):
        rows = [
            {"config": "sgd_lr1e-1_wd5e-4_anchor", "label": "SGD-5e-4"},
            {"config": "sgd_lr1e-1_wd2e-4", "label": "SGD-2e-4"},
            {"config": "adam_lr1e-3_wd1e-4", "label": "Adam"},
            {"config": "adamw_lr5e-3_wd1e-4", "label": "AdamW-1e-4"},
            {"config": "adamw_lr5e-3_wd5e-4_anchor", "label": "AdamW-5e-4"},
        ]

        built = poster_assets.build_figure3_rows(rows)

        self.assertEqual(
            [row["label"] for row in built],
            ["SGD-5e-4", "Adam", "AdamW-1e-4"],
        )


if __name__ == "__main__":
    unittest.main()
