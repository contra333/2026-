# WRN-28-10 selected 3-seed raw evaluation results

This package collects the raw evaluation files for the Korean Statistical Society poster experiment.

Experiment summary:

- ID dataset: CIFAR-10
- Model: WideResNet-28-10, dropout 0.3
- Selected configs: SGD x 2, Adam x 1, AdamW x 2
- Seeds: 0, 1, 2
- OOD datasets: cifar100, tiny_imagenet, svhn, mnist
- Seed1/seed2 checkpoint: epoch_0350
- Seed0 source: WRN_seed0_350eps_girdsearch_0531.zip

Directory structure:

```text
runs/<config_label>/seed<0|1|2>/
  eval/<checkpoint_tag>/
    metrics_classification.json   # ID test accuracy, NLL
    metrics_calibration.json      # ECE, temperature, T-ECE
    metrics_ood_logit.json        # MSP, maxlogit, energy_id_score, neg_entropy per OOD dataset
    metrics_ood_feature.json      # Mahalanobis, kNN, DDU-style GMM variants per OOD dataset
    metrics_ood_nc_hybrid.json    # NCC/prototype/VIM diagnostics
    metrics_geometry.json         # NC and geometry metrics, mainly under id_train
    detector_params.json          # detector fitting and score-direction metadata
    feature_stats.json            # feature norm stats by split
  run_metadata/
    training_summary.json         # best validation accuracy/epoch and final validation metrics
    train_metrics.jsonl           # epoch-wise training metrics
    val_metrics.jsonl             # epoch-wise validation metrics
    config_snapshot.yaml          # training config used for the run
  cache_metadata/<checkpoint_tag>/cache_metadata.json
```

Convenience tables are in `analysis_tables/`. These are derived from the same JSON files and are included only to make quick analysis easier.

Important conventions:

- Scores in OOD JSON follow the project convention: higher score is more ID-like.
- ID label is 1 and OOD label is 0 for AUROC/AUPR/FPR95 calculations.
- `mahalanobis_l2` and `knn_l2` are detector-side L2-normalization controls.
- `gmm_ddu_*` files should be described as DDU-style GMM feature density diagnostics, not full DDU reproduction.
