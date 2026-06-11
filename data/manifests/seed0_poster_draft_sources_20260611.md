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
- `tables/csv/seed0_geometry_summary_draft.csv`
- `tables/csv/seed0_raw_l2_recovery_draft.csv`

## Evidence boundary

These are seed0 diagnostic draft values. They are used to validate poster logic and layout before selected seed1/2 results finish. The final poster main tables and error bars should be replaced with selected 5 configs over seed0/1/2 as `mean +/- std`.

The dataset-specific raw Mahalanobis markdown source directly exposes rows for `SGD best val`, `Adam wd=0 best val`, `Adam wd>0 best val`, and `AdamW best val`. It does not expose dataset-specific rows for the SGD anchor or AdamW anchor in the visible markdown table, so the draft dataset-specific table uses confirmed source rows only.

The geometry summary draft uses selected seed0 rows recorded in `docs/research/통계학회_포스터_실험계획.md` and `docs/research/추가실험_승인_컨텍스트.md`. It includes confirmed `NC1` and `InterDist` values only; norm/covariance diagnostics are qualitative labels until processed repeated-seed geometry summaries are imported.
