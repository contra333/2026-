# Current Poster Context

Last updated: 2026-06-13 KST

This is the single current-context document for the production poster. Treat
`poster/poster.tex` and `poster/build/poster.pdf` as the rendered source of
truth; use this file only to understand the poster logic, evidence boundary,
and current figure/table order.

Historical plans, draft text, and old design-harness notes are archived under
`archive/context_legacy_20260613/` and should not be read by default.

## Current Poster Surface

- Format: one A0 portrait page, `841mm x 1189mm`.
- TeX source: `poster/poster.tex`.
- Active style macros: `poster/poster_style.tex`.
- Built PDF: `poster/build/poster.pdf`.
- Title: `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`.
- Header: no subtitle; `GunHak Jin ∙ HyeYoung Jung`, Department of Mathematical Data Science, Hanyang University.
- Main question: 최적화 방법이 마지막 표현층의 class-conditional distribution을 다르게 만든다면, validation-selected high-accuracy models의 calibration과 feature-based OOD detection은 어떻게 달라지는가?

## Core Message

Accuracy is necessary, not reliability. Across validation-selected
WRN-28-10/CIFAR-10 configurations, similar ID validation accuracy does not imply
similar calibration or feature-based OOD reliability. The observed split is
accompanied by changes in penultimate class-conditional geometry, including
compactness, class separation, feature-norm scale, and covariance structure.

Use bounded language:

- Say `post-hoc diagnostic evidence`, `is accompanied by`, `can differ`, and
  `is consistent with`.
- Do not say `proves`, `always`, `causes`, or `AdamW fails`.
- Do not claim original DDU reproduction. Use `DDU-style GMM feature density`.

## Evidence Boundary

- Model/evidence: WRN-28-10 dropout 0.3 on CIFAR-10.
- Selected configs: 2 SGD, 1 Adam, 2 AdamW.
- Seeds: 0, 1, 2.
- Reported uncertainty: mean +/- sample standard deviation.
- Selection: ID validation accuracy only.
- Post-hoc diagnostics: calibration, OOD AUROC, and feature geometry.
- OOD datasets: CIFAR-100, TinyImageNet, SVHN, MNIST.
- Figure-level near-OOD panels keep CIFAR-100 and TinyImageNet separate.
- OOD score convention: higher score means more ID-like; ID label = 1, OOD label = 0.

Numeric provenance:

- Manifest: `data/manifests/wrn350_selected_3seed_poster_assets_20260612.md`.
- Metric summary: `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`.
- Compact table CSVs: `tables/csv/wrn350_3seed_*.csv`.

## Current Figure And Table Order

1. **Figure 1. Reliability Failure Concept**
   - Asset: `figures/final/fig1_reliability_failure_concept.png`.
   - Role: shows miscalibration and OOD acceptance as two reliability failures
     that accuracy alone does not expose.

2. **Figure 2. Accuracy-Matched Reliability Scatter**
   - Asset: `figures/final/fig2_wrn350_accuracy_matched_reliability_scatter.pdf`.
   - Role: validation-selected configs plotted by best ID validation accuracy,
     ECE, and raw Mahalanobis AUROC on CIFAR-100.
   - Wording boundary: despite the figure title, prose should prefer
     `validation-selected high-accuracy models` or `similar ID validation accuracy`
     over a strong `same accuracy` claim.

3. **Figure 3. Raw vs L2 Feature OOD AUROC on Near-OOD**
   - Asset: `figures/final/fig3_wrn350_3optimizer_near_ood_raw_l2.pdf`.
   - Role: one ID-validation representative per optimizer; shows raw
     Mahalanobis/kNN and detector-side L2 controls on CIFAR-100 and TinyImageNet.
   - Interpretation: L2 normalization is a diagnostic control, not a final
     detector solution or full Mahalanobis++ reproduction.

4. **Table 1. Classwise Covariance Regularization in DDU-Style GMM**
   - Source values: `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`,
     CIFAR-100 `gmm_ddu_diag` and `gmm_ddu_shrinkage` AUROC for representative
     SGD, Adam, and AdamW rows.
   - Role: shows that replacing classwise diagonal covariance with classwise
     shrinkage covariance can partially recover AdamW but does not uniformly
     improve every optimizer.
   - Interpretation: covariance estimation is one diagnostic part of the
     detector split, not a universal fix.

5. **Table 2. Feature Distribution Geometry**
   - Table fragment: `tables/tex/wrn350_3seed_geometry_summary.tex`.
   - Role: reports NC1, InterDist, feature norm, and effective rank for the five
     selected configs.
   - Interpretation: the detector split is accompanied by shifts in class
     compactness, separation, norm scale, and covariance spectrum.

## Poster Logic Flow

Left column:

1. Abstract: reliability includes calibrated confidence and OOD rejection, not
   only ID test accuracy.
2. Introduction: accuracy is necessary, not reliability; Figure 1 defines
   miscalibration and OOD acceptance.
3. Optimizer mechanism: update rules can shift class-conditional feature
   distributions; feature detectors read those distributions.
4. Experiment: CIFAR-10 / WRN-28-10, SGD/Adam/AdamW LR-WD grid, ID-validation
   selection only, post-hoc diagnostics.

Right column:

1. Figure 2: validation-selected reliability scatter.
2. Figure 3: raw-vs-L2 detector split and recovery.
3. Table 1: DDU-style GMM covariance-control diagnostic.
4. Table 2: feature geometry diagnostics.
5. Conclusion and future work.

## Current Conclusion

Accuracy-matched models are not reliability-matched: feature geometry determines
post-hoc detector behavior. Detector-side controls such as L2 normalization and
shrinkage covariance explain part of the gap, but their effects are not uniform;
therefore, they should be treated as diagnostics rather than universal fixes.

Future work currently listed on the poster:

- Broader architectures and datasets.
- Other training interventions such as SAM and mixup.
- Mechanistic analysis of how representation-layer distribution changes
  propagate to the output layer and affect generalization and ECE.

## Editing Rules

- Update `poster/poster.tex` first when changing the actual poster.
- Update this file only after the poster logic changes.
- Do not reintroduce separate poster-section source documents unless the poster
  is being substantially rewritten.
- For numeric claims, check the manifest and metric summary before editing prose.
- Keep old plans and drafts in `archive/context_legacy_20260613/`; do not make
  them default startup reads.
