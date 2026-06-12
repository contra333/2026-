#!/usr/bin/env python3
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "analysis" / "scripts"))

import build_wrn350_metrics_notion_markdown as report


class MetricReportFormattingTests(unittest.TestCase):
    def test_sample_std_uses_ddof_one(self):
        mean, std = report.mean_std([1.0, 2.0, 3.0])
        self.assertAlmostEqual(mean, 2.0)
        self.assertAlmostEqual(std, 1.0)

    def test_ood_aggregation_keeps_datasets_separate(self):
        rows = [
            {
                "config_label": "cfg",
                "optimizer": "sgd",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "0",
                "detector_type": "logit",
                "detector": "msp",
                "ood_dataset": "cifar100",
                "auroc": "0.8",
                "fpr95": "0.2",
                "aupr_in": "0.7",
            },
            {
                "config_label": "cfg",
                "optimizer": "sgd",
                "lr": "0.1",
                "weight_decay": "0.0005",
                "seed": "0",
                "detector_type": "logit",
                "detector": "msp",
                "ood_dataset": "mnist",
                "auroc": "0.4",
                "fpr95": "0.6",
                "aupr_in": "0.3",
            },
        ]
        aggregated = report.aggregate_ood_rows(rows)
        keys = {(row["ood_dataset"], row["metric"]) for row in aggregated}
        self.assertIn(("cifar100", "auroc"), keys)
        self.assertIn(("mnist", "auroc"), keys)
        self.assertNotIn(("all", "auroc"), keys)

    def test_markdown_table_escapes_pipe_and_newline(self):
        rendered = report.markdown_table(
            ["Metric", "Description"],
            [{"Metric": "A|B", "Description": "first\nsecond"}],
        )
        self.assertIn("A\\|B", rendered)
        self.assertIn("first<br>second", rendered)


if __name__ == "__main__":
    unittest.main()
