# 2026 Korean Statistics Conference Poster

This workspace is the production area for an A0 portrait statistics conference poster and related presentation artifacts.

Experiment code is external:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

This workspace stores research context, small processed result copies, manifests, figures, tables, design harness assets, and TeX/PDF deliverables.

## Map

- `AI_CONTEXT.md`: short hot cache for new Codex sessions.
- `AGENTS.md`: operating rules for AI agents.
- `PRODUCT.md`: poster product and design intent.
- `docs/research/`: experiment plan, evidence boundary, aggregation guide, and storyline.
- `docs/design/`: design-system notes and handoff guidance.
- `references/`: heavy PPTX and Figma reference files.
- `design_harness/`: reusable design tokens, prompts, and templates.
- `data/`: small processed result copies and import manifests.
- `analysis/`: aggregation and plotting scripts plus intermediate outputs.
- `tables/`: poster table source CSVs and TeX fragments.
- `figures/`: source and final poster figures.
- `poster/`: TeX poster source, assets, references, and build outputs.
- `archive/`: preserved superseded drafts.

## Current Poster Target

- Format: one A0 portrait page, `841mm x 1189mm`.
- Locked title: `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`.
- Header: no subtitle; `GunHak Jin ∙ HyeYoung Jung` plus `Department of Mathematical Data Science, Hanyang University`; Hanyang University and Korean Statistical Society logos at the upper right.
- Key question: `비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`
- Main story: test accuracy alone is not enough; optimizer-induced feature geometry can change calibration and post-hoc OOD detection reliability.
- Current figure structure: Figure 1 is the Reliability Failure concept diagram, Figure 2 is the accuracy-matched reliability split, and Figure 3 is the raw-to-L2 recovery figure.
- Primary evidence plan: WRN-28-10/CIFAR-10 selected 5 configs, seed0/1/2 aggregation.
- Final deliverable target: `poster/poster.tex` compiled to PDF, preferably with XeLaTeX, Korean TeX support, Pretendard for Hangul, and Cambria Math for formulas.

## Result Import Rule

Only import small processed CSV/JSON files plus provenance manifests. Keep checkpoints, feature caches, server logs, raw result directories, and large arrays outside this poster workspace.
