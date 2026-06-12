# 2026 Korean Statistics Conference Poster

This workspace produces the Korean statistics conference A0 portrait poster and
small related artifacts. Experiment code and raw training outputs remain outside
this workspace.

Experiment code source of truth:

```text
/mnt/c/Users/User/Desktop/2027ICLR/code
```

## Active Files

- `poster/poster.tex`: current poster source.
- `poster/poster_style.tex`: active TeX style/macros for the poster.
- `poster/build/poster.pdf`: current compiled PDF.
- `docs/research/current_poster_context.md`: single current logic/context file.
- `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`: numeric metric summary.
- `data/manifests/wrn350_selected_3seed_poster_assets_20260612.md`: provenance for imported results and poster assets.

## Workspace Map

- `analysis/`: scripts and tests for aggregation and poster asset generation.
- `data/`: small processed result copies and provenance manifests.
- `docs/research/`: current poster context and metric summaries.
- `figures/`: source and final poster figures.
- `poster/`: TeX poster source, style, fonts, references, and build outputs.
- `references/`: heavy PPTX/Figma reference files kept for historical lookup.
- `tables/`: poster table CSVs and TeX fragments.
- `archive/`: historical drafts, plans, and retired design-harness files; do not read by default.

## Current Poster

See `docs/research/current_poster_context.md` for the live narrative, evidence
boundary, and figure/table order. Avoid duplicating that context here.

## Result Import Rule

Only import small processed CSV/JSON files plus provenance manifests. Keep
checkpoints, feature caches, server logs, raw result directories, and large
arrays outside this poster workspace.

## Build

Preferred final build:

```bash
cd poster
latexmk -xelatex -interaction=nonstopmode -halt-on-error -outdir=build poster.tex
```

In the current WSL setup, `latexmk` may need to call Windows MiKTeX's
`xelatex.exe` explicitly:

```bash
cd poster
PATH="/mnt/c/Users/jin/AppData/Local/Programs/MiKTeX/miktex/bin/x64:$PATH" \
  latexmk -g -xelatex -e '$xelatex = q/xelatex.exe %O %S/;' \
  -interaction=nonstopmode -halt-on-error -outdir=build poster.tex
```

If `latexmk` is unavailable but a native XeLaTeX engine exists, use XeLaTeX
directly:

```bash
cd poster
xelatex -interaction=nonstopmode -halt-on-error -output-directory=build poster.tex
```
