# Codex Poster Workshop

## Project Purpose

This workspace is the production area for the Korean statistics conference A0 poster and related presentation artifacts.

Use Codex as a design-production and analysis-assistant agent: turn research context and imported processed results into PRDs, figures, tables, TeX, HTML, PPTX, or Figma-oriented handoff instructions.

Experiment code is external and remains the source of truth:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

Do not duplicate or modify experiment code in this poster workspace unless explicitly requested.

## Startup Protocol

Before doing general poster work, read:

1. `AI_CONTEXT.md`
2. `README.md`
3. the nearest relevant README or AGENTS file

For experiment interpretation, also read:

- `docs/research/통계학회_포스터_실험계획.md`
- `docs/research/추가실험_승인_컨텍스트.md`
- `docs/research/학습후_평가_집계_가이드.md`
- relevant files in `data/manifests/`

For poster text/content editing, also read:

- `docs/research/poster_section_text.md`

For poster design or TeX/HTML/PPTX production, also read:

- `PRODUCT.md`
- `design_harness/README.md`
- `design_harness/tokens/wanted-inspired.json`

## Workspace Map

- `docs/research/`: research plan, evidence boundary, aggregation guide, and poster storyline.
- `docs/design/`: design-system notes and handoff context.
- `references/poster_layout/`: heavy PPT/PPTX layout references.
- `references/design_system/`: Figma design-system archive and related metadata.
- `design_harness/`: reusable tokens, prompts, TeX macros, and HTML templates.
- `data/`: small processed result copies and import manifests only.
- `analysis/`: scripts and intermediate outputs for aggregation, tables, and figures.
- `tables/`: poster table CSVs and TeX fragments.
- `figures/`: source and final poster figures.
- `poster/`: A0 TeX poster source, poster assets, bibliography, and build outputs.
- `archive/`: preserved old drafts or superseded material that should not be read by default.

## Design System

- Treat `references/poster_layout/25_동계_통계학회_포스터_진군학.pptx` as the primary poster layout reference.
- Treat `references/design_system/Wanted Design System (Community).fig` as a secondary visual reference.
- Use `design_harness/tokens/wanted-inspired.json` as the active Codex-readable token source.
- The `.fig` archive contains Figma's own `canvas.fig` binary, so do not assume Codex can reliably parse the complete design system directly from the file.
- If exact Figma tokens are later exported, reconcile them with the poster PPTX layout instead of replacing the A0 portrait rules.

## Visual Direction

- Use the previous poster's academic layout: large top title area, dark blue section bars, two-column body, and thin blue footer rule.
- Use white background, black text, dark section blue `#2F5597`, accent blue `#0070C0`, and footer blue `#096EB7`.
- Use Pretendard for Hangul text in Korean production drafts. Keep Latin/body fonts separable for the final English version, and use Cambria Math for formulas when available.
- Use an 8-point spacing rhythm. Keep cards at 8px radius or less.
- Avoid decorative gradients, floating blobs, nested cards, marketing hero layouts, rounded card-heavy layouts, and color palettes dominated by a single hue.
- For posters, prioritize readability at distance: clear title, strong section labels, dense but organized tables, and no cramped paragraphs.

## Poster Content Defaults

- Default poster format: exactly one A0 portrait page, `841mm x 1189mm`.
- Do not use A0 landscape for the conference poster unless the user explicitly changes the submission rule.
- Keep the main poster compact. The current production draft uses two tables,
  one conceptual Figure 1, and two empirical Figures 2/3.
- Use the research message from `docs/research/GPT제안_포스터초안.md` as the default:
  "Test accuracy alone is not enough: optimizer-induced feature geometry can change calibration and post-hoc OOD detection reliability."
- Current fixed title: `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`.
- Current Key Question: `비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`
- Prefer this layout:
  1. Problem and contribution.
  2. Experiment setup.
  3. Accuracy/calibration/OOD summary table.
  4. Geometry summary table.
  5. Reliability failure concept figure.
  6. Accuracy-matched reliability and raw-to-L2 recovery figures.
  7. Takeaway and limitations.

## Evidence Boundaries

- Main poster evidence is WRN-28-10/CIFAR-10 LR x weight decay grid evidence.
- Hyperparameter selection is ID-validation-only.
- OOD and geometry metrics are post-hoc diagnostics.
- Do not claim seed-averaged conclusions until seed0/1/2 are aggregated.
- Use `DDU-style GMM feature density`, not original DDU reproduction.
- Separate confirmed metrics, interpretation, and hypotheses.

## Data Boundaries

- This folder stores poster logic, small processed CSV/JSON files, manifests, figures, tables, and TeX deliverables.
- Do not store raw checkpoints, feature dumps, cache `.pt` files, full server logs, raw server result directories, or large arrays here.
- Raw training outputs belong on the server or in the external 2027ICLR results area.
- Every imported result must have a manifest or provenance note under `data/manifests/`.

## Output Discipline

- Figures used in the poster go in `figures/final/`.
- Source plotting outputs go in `figures/source/`.
- Poster table CSVs go in `tables/csv/`; TeX table fragments go in `tables/tex/`.
- TeX source lives in `poster/poster.tex`.
- TeX build artifacts go in `poster/build/`.
- Shared design tokens and templates stay in `design_harness/`.

## Verification

- For HTML deliverables, inspect layout at desktop and print dimensions when possible. Make sure text does not overlap or overflow.
- For TeX/PDF deliverables, verify that the generation command completes successfully or record the exact dependency failure.
- For final Korean print PDFs, prefer XeLaTeX with Korean TeX support, Pretendard for Hangul, and Cambria Math for formulas.
- Do not delete downloaded Figma files unless the user explicitly asks.
