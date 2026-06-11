# Poster Workshop Folder Design

Date: 2026-06-11 KST

## Goal

Reorganize `/home/contra333/2026통계학회포스터` as a statistics-conference poster production workspace.
The workspace should keep poster writing, design references, small processed results, tables, figures, and TeX deliverables separate from the experiment-code repository.

Experiment code remains the source of truth in:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

The poster workspace must not duplicate or modify experiment code unless explicitly requested.

## Chosen Approach

Use a production-workshop structure:

```text
2026통계학회포스터/
├── AGENTS.md
├── README.md
├── AI_CONTEXT.md
├── PRODUCT.md
├── docs/
│   ├── research/
│   ├── design/
│   └── superpowers/specs/
├── references/
│   ├── poster_layout/
│   └── design_system/
├── design_harness/
│   ├── README.md
│   ├── tokens/
│   ├── prompts/
│   └── templates/
├── data/
│   ├── manifests/
│   ├── processed/
│   └── README.md
├── analysis/
│   ├── scripts/
│   ├── outputs/
│   └── README.md
├── figures/
│   ├── source/
│   └── final/
├── tables/
│   ├── csv/
│   └── tex/
├── poster/
│   ├── poster.tex
│   ├── refs.bib
│   ├── sections/
│   ├── assets/
│   └── build/
└── archive/
```

## File Roles

Root files:

- `AGENTS.md`: operating rules for Codex in this poster workspace.
- `README.md`: human-readable map of the workspace.
- `AI_CONTEXT.md`: short hot cache with current state, path map, next actions, and evidence status.
- `PRODUCT.md`: product/design intent for the A0 poster and related deliverables.

Research docs:

- `docs/research/GPT제안_포스터초안.md`
- `docs/research/통계학회_포스터_실험계획.md`
- `docs/research/추가실험_승인_컨텍스트.md`
- `docs/research/학습후_평가_집계_가이드.md`

Design docs:

- `docs/design/클로드디자인_영상안내.md`

References:

- `references/poster_layout/25_동계_통계학회_포스터_진군학.pptx`
- `references/poster_layout/0603_포스터샘플.ppt`
- `references/design_system/Wanted Design System (Community).fig`
- `references/design_system/Wanted Design System (Community).fig:Zone.Identifier`

Poster deliverable:

- Move `poster.tex` to `poster/poster.tex`.
- Move generated `poster.pdf`, `poster.aux`, `poster.log`, and `poster.out` to `poster/build/`.
- Keep future TeX sections in `poster/sections/`, poster-only image assets in `poster/assets/`, and bibliography in `poster/refs.bib`.

Design harness:

- Keep `design_harness/` as a reusable cross-format production harness.
- It stores shared design tokens, prompts, HTML templates, and TeX macros.
- It should not become a dumping ground for poster-specific outputs.

Data, tables, and figures:

- `data/manifests/`: import/provenance notes for external results.
- `data/processed/`: small processed CSV/JSON result copies only.
- `tables/csv/`: poster table source CSVs.
- `tables/tex/`: TeX table fragments.
- `figures/source/`: editable or script-generated intermediate plots.
- `figures/final/`: PDF/PNG/SVG figures used by the poster.

Analysis:

- `analysis/scripts/`: scripts that aggregate imported processed results and generate tables/figures.
- `analysis/outputs/`: intermediate analysis outputs not directly used in the final poster.

Archive:

- `archive/`: superseded drafts and legacy files that should be preserved but not read by default.

## Evidence And Data Boundary

The poster workspace may contain:

- Small processed CSV/JSON files.
- Import manifests and provenance notes.
- Poster figures and table artifacts.
- TeX, HTML, PPTX, or design handoff deliverables.

The poster workspace must not contain:

- Raw checkpoints.
- Feature dumps or large arrays.
- Full server logs.
- Uncurated raw result directories.
- Duplicated experiment-code source.

Every imported result needs a manifest or provenance note that records source path, import date, config labels, seed coverage, and whether the result is seed0-only or 3-seed aggregated.

## Context Management

`AI_CONTEXT.md` should stay short and should point to detailed docs rather than repeating them.

Required startup read order for Codex:

1. `AI_CONTEXT.md`
2. `README.md`
3. `docs/research/통계학회_포스터_실험계획.md` when interpreting experiment strategy
4. `docs/research/추가실험_승인_컨텍스트.md` and `docs/research/학습후_평가_집계_가이드.md` when importing or aggregating results
5. `design_harness/README.md` and `design_harness/tokens/wanted-inspired.json` when designing or editing poster artifacts

`AGENTS.md` should encode these rules so Codex does not need to rediscover them.

## Design Rules To Preserve

- Main poster format is exactly one A0 portrait page: `841mm x 1189mm`.
- The previous poster PPTX is the primary layout reference.
- The Wanted design system file is secondary; use the Codex-readable token file as the active source.
- Use white background, black text, dark section blue `#2F5597`, accent blue `#0070C0`, and footer blue `#096EB7`.
- Use Pretendard for production output when available.
- Keep the main poster compact. The current production draft uses two tables,
  one conceptual Figure 1, and two empirical Figures 2/3.
- TeX is the primary final poster target; HTML can be used for fast preview.

## Implementation Notes

- Update `poster/poster.tex` input paths after moving it under `poster/`.
- Generated TeX build artifacts belong under `poster/build/`.
- Existing PDF was built with `pdflatex` fallback and is a structural preview, not a final Korean/Pretendard validation.
- This workspace currently is not a valid Git repository despite having an empty `.git/` directory, so the design document cannot be committed unless Git is initialized later.

## Success Criteria

- The root directory contains only high-level context files and major folders.
- A new Codex session can identify the active task state by reading `AI_CONTEXT.md` and `README.md`.
- Design references and heavy binary files are no longer in the root.
- Result import boundaries are explicit.
- TeX source, build products, tables, figures, and design harness assets have separate homes.
- No raw training result, checkpoint, feature dump, or experiment-code copy is introduced into the poster workspace.
