# Codex Poster Workshop

## Project Purpose

This workspace is the production area for the Korean statistics conference A0
poster and related small presentation artifacts.

Use Codex as a design-production and analysis-assistant agent: turn research
context and imported processed results into figures, tables, TeX, PDF, or
handoff instructions.

Experiment code is external and remains the source of truth:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

Do not duplicate or modify experiment code in this poster workspace unless
explicitly requested.

## Startup Protocol

Before general workspace work, read:

1. `AI_CONTEXT.md`
2. `README.md`
3. this file

For poster logic/content edits, also read:

- `docs/research/current_poster_context.md`
- `poster/poster.tex`

For numeric claims or result interpretation, also read:

- `data/manifests/wrn350_selected_3seed_poster_assets_20260612.md`
- `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`
- relevant files in `tables/csv/` or `tables/tex/`

For TeX/style edits, also read:

- `poster/poster.tex`
- `poster/poster_style.tex`

Historical drafts, plans, and retired design-harness files live under
`archive/`. Do not read archived material by default.

## Workspace Map

- `docs/research/`: current poster context and metric summaries.
- `references/`: heavy PPT/PPTX/Figma reference files retained for lookup.
- `data/`: small processed result copies and import manifests only.
- `analysis/`: scripts, tests, and intermediate outputs for aggregation, tables, and figures.
- `tables/`: poster table CSVs and TeX fragments.
- `figures/`: source and final poster figures.
- `poster/`: A0 TeX poster source, active style, fonts, bibliography, and build outputs.
- `archive/`: historical drafts, plans, and retired design-harness material.

## Visual Direction

- Use the previous academic poster structure: large top title area, dark blue
  section bars, two-column body, and thin blue footer rule.
- Use white background, black text, dark section blue `#2F5597`, accent blue
  `#0070C0`, and footer blue `#096EB7`.
- Use Pretendard for Hangul text in Korean production drafts. Keep Latin/body
  fonts separable for the final English version, and use Cambria Math for
  formulas when available.
- Use an 8-point spacing rhythm. Keep cards at 8px radius or less.
- Avoid decorative gradients, floating blobs, nested cards, marketing hero
  layouts, rounded card-heavy layouts, and color palettes dominated by a single hue.
- For posters, prioritize readability at distance: clear title, strong section
  labels, dense but organized tables, and no cramped paragraphs.

## Current Poster Defaults

- Default format: exactly one A0 portrait page, `841mm x 1189mm`.
- Current title: `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`.
- Current source of truth: `poster/poster.tex`, `poster/build/poster.pdf`, and
  `docs/research/current_poster_context.md`.
- Main evidence: WRN-28-10/CIFAR-10 selected configs over seeds 0/1/2, reported
  as mean +/- sample standard deviation.
- Hyperparameter selection is ID-validation-only.
- Calibration, OOD, and geometry metrics are post-hoc diagnostics.
- Use `DDU-style GMM feature density`, not original DDU reproduction.
- Separate confirmed metrics, interpretation, and hypotheses.

## Data Boundaries

- This folder stores poster logic, small processed CSV/JSON files, manifests,
  figures, tables, and TeX deliverables.
- Do not store raw checkpoints, feature dumps, cache `.pt` files, full server
  logs, raw server result directories, or large arrays here.
- Raw training outputs belong on the server or in the external 2027ICLR results
  area.
- Every imported result must have a manifest or provenance note under
  `data/manifests/`.

## Output Discipline

- Figures used in the poster go in `figures/final/`.
- Source plotting outputs go in `figures/source/`.
- Poster table CSVs go in `tables/csv/`; TeX table fragments go in `tables/tex/`.
- TeX source lives in `poster/poster.tex`.
- Active TeX style lives in `poster/poster_style.tex`.
- TeX build artifacts go in `poster/build/`.
- Historical or retired context belongs in `archive/`, not in the default read path.

## Verification

- For TeX/PDF deliverables, verify that the generation command completes
  successfully or record the exact dependency failure.
- For final Korean print PDFs, prefer XeLaTeX with Korean TeX support,
  `poster/fonts/pretendard/`, and Cambria Math for formulas.
- Do not delete downloaded Figma/PPTX reference files unless explicitly asked.
