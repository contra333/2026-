# AI_CONTEXT

Last updated: 2026-06-11 KST

## Role

This folder is the Korean statistics conference poster production workspace. It is not the experiment-code repository.

Experiment code source of truth:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

Local research repo:

```text
/mnt/c/Users/User/Desktop/2027ICLR
```

Server paths mentioned in research docs, such as `/home/ghjin/2027ICLR/2027ICLR`, are server-side paths and may not exist on this machine.

## Current State

- Folder structure was reorganized on 2026-06-11 into a poster production-workshop layout.
- Research docs are under `docs/research/`.
- Heavy poster/Figma references are under `references/`.
- The active TeX source is `poster/poster.tex`.
- Shared design tokens and templates remain under `design_harness/`.
- No 3-seed processed result CSV has been imported into `data/processed/` yet.
- The current TeX draft builds as one A0 portrait page at `poster/build/poster.pdf`.
- The locked draft title is `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`.
- The current header has no subtitle. It uses `GunHak Jin ∙ HyeYoung Jung` and
  `Department of Mathematical Data Science, Hanyang University`, with Hanyang
  University and Korean Statistical Society logos at the upper right.
- The current Key Question is:
  `비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`
- Current figure numbering is:
  Figure 1 = Reliability Failure concept diagram,
  Figure 2 = Accuracy-Matched Reliability Split,
  Figure 3 = Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity.

## Current Evidence

- Existing evidence is seed0 diagnostic WRN-28-10/CIFAR-10 LR-WD grid context from the research docs.
- Selected seed1/seed2 server runs are planned or recorded in `docs/research/추가실험_승인_컨텍스트.md`.
- Do not make mean/std or stability claims until seed0/1/2 aggregation files are imported and checked.

## Next Actions

1. Import small processed CSVs and provenance manifests after server evaluation/aggregation completes.
2. Build `tables/csv/` and `tables/tex/` outputs from imported data.
3. Generate final figures under `figures/final/`.
4. Replace seed0 diagnostic table/figure values in `poster/poster.tex` once repeated-seed summaries are imported.
5. Compile final A0 PDF with XeLaTeX if the environment has Korean TeX support, Pretendard for Hangul, and Cambria Math for formulas.

## Startup Read Order

For general work:

1. this file
2. `README.md`
3. the nearest relevant README or AGENTS file

For research/result interpretation:

1. `docs/research/통계학회_포스터_실험계획.md`
2. `docs/research/추가실험_승인_컨텍스트.md`
3. `docs/research/학습후_평가_집계_가이드.md`
4. relevant files under `data/manifests/`

For poster text editing:

1. `docs/research/poster_section_text.md`
2. then the research/result interpretation documents above
3. `poster/poster.tex`

For design or TeX work:

1. `PRODUCT.md`
2. `design_harness/README.md`
3. `design_harness/tokens/wanted-inspired.json`
4. `poster/poster.tex`
