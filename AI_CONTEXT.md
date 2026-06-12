# AI_CONTEXT

Last updated: 2026-06-13 KST

This workspace is the Korean statistics conference A0 poster production area.
It is not the experiment-code repository.

Experiment code source of truth:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

## Current Source Of Truth

- Poster source: `poster/poster.tex`
- Active poster style: `poster/poster_style.tex`
- Current PDF: `poster/build/poster.pdf`
- Current poster context: `docs/research/current_poster_context.md`
- Current 3-seed metric summary:
  `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`
- Current provenance manifest:
  `data/manifests/wrn350_selected_3seed_poster_assets_20260612.md`

Historical drafts, plans, and the retired design harness are archived under:

```text
archive/context_legacy_20260613/
archive/design_harness_legacy_20260613/
```

Do not read archived material by default.

## Current Poster Snapshot

- Format: one A0 portrait page, `841mm x 1189mm`.
- Title: `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`.
- Evidence: WRN-28-10/CIFAR-10 selected configs, seeds 0/1/2, mean +/- sample std.
- Selection: ID validation accuracy only.
- Diagnostics: calibration, OOD AUROC, and feature geometry are post-hoc.
- OOD convention: higher score means more ID-like.
- DDU wording: use `DDU-style GMM feature density`, not full DDU reproduction.

Current figure/table order:

1. Figure 1: Reliability failure concept.
2. Figure 2: validation-selected reliability scatter.
3. Figure 3: raw-vs-L2 near-OOD AUROC for one representative per optimizer.
4. Table 1: DDU-style GMM classwise covariance regularization.
5. Table 2: feature distribution geometry.

## Startup Read Order

For general workspace work:

1. `AI_CONTEXT.md`
2. `README.md`
3. `AGENTS.md`

For poster logic/content edits:

1. `docs/research/current_poster_context.md`
2. `poster/poster.tex`

For numeric claims:

1. `data/manifests/wrn350_selected_3seed_poster_assets_20260612.md`
2. `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`
3. relevant `tables/csv/` or `tables/tex/` files

For TeX/design edits:

1. `poster/poster.tex`
2. `poster/poster_style.tex`

## Verification

- For TeX/PDF edits, compile the poster and record the exact command or failure.
- For final Korean print PDFs, prefer XeLaTeX with Korean TeX support, local
  Pretendard under `poster/fonts/pretendard/`, and Cambria Math when available.
