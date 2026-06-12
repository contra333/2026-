# Poster Workshop Reorganization Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Reorganize the statistics conference poster workspace into the approved production-workshop folder structure.

**Architecture:** Keep the poster workspace focused on research context, small processed results, design harness assets, figures, tables, and TeX deliverables. Experiment code remains external in `/mnt/c/Users/User/Desktop/2027ICLR/code`; this workspace records paths and provenance but does not duplicate code.

**Tech Stack:** Markdown documentation, TeX/XeLaTeX-compatible poster source, shell file operations, `rg`/`find` path verification.

---

## File Structure

- Modify: `AGENTS.md`
  - Encode startup read order, folder boundaries, design rules, and data import rules after reorganization.
- Create: `README.md`
  - Human-facing map of the poster production workspace.
- Create: `AI_CONTEXT.md`
  - Short hot cache with current state, path map, evidence status, and next actions.
- Move into `docs/research/`
  - `GPT제안_포스터초안.md`
  - `통계학회_포스터_실험계획.md`
  - `추가실험_승인_컨텍스트.md`
  - `학습후_평가_집계_가이드.md`
- Move into `docs/design/`
  - `클로드디자인_영상안내` as `클로드디자인_영상안내.md`
- Move into `references/poster_layout/`
  - `25_동계_통계학회_포스터_진군학.pptx`
  - `0603_포스터샘플.ppt`
- Move into `references/design_system/`
  - `Wanted Design System (Community).fig`
  - `Wanted Design System (Community).fig:Zone.Identifier`
- Move into `poster/`
  - `poster.tex`
- Move into `poster/build/`
  - `poster.pdf`
  - `poster.aux`
  - `poster.log`
  - `poster.out`
- Create:
  - `data/README.md`
  - `analysis/README.md`
  - `poster/refs.bib`
  - empty structural directories: `data/manifests`, `data/processed`, `analysis/scripts`, `analysis/outputs`, `figures/source`, `figures/final`, `tables/csv`, `tables/tex`, `poster/sections`, `poster/assets`, `archive`
- Modify: `poster/poster.tex`
  - Change `\input{design_harness/templates/wanted_poster_macros.tex}` to `\input{../design_harness/templates/wanted_poster_macros.tex}` after moving it into `poster/`.
- Modify: `design_harness/README.md`
  - Update references to moved files, especially `../poster.tex`, `../25_동계_통계학회_포스터_진군학.pptx`, and root-level research docs.
- Modify: `design_harness/prompts/*.md`
  - Update paths from root-level docs to `docs/research/*` and poster source to `poster/poster.tex`.

## Task 1: Create Directory Skeleton

**Files:**
- Create directories only.

- [ ] **Step 1: Create approved directories**

Run:

```bash
mkdir -p docs/research docs/design references/poster_layout references/design_system data/manifests data/processed analysis/scripts analysis/outputs figures/source figures/final tables/csv tables/tex poster/sections poster/assets poster/build archive
```

Expected: command exits with status `0`.

- [ ] **Step 2: Verify skeleton**

Run:

```bash
find . -maxdepth 3 -type d | sort
```

Expected: output includes `./docs/research`, `./references/poster_layout`, `./poster/build`, `./figures/final`, and `./tables/tex`.

## Task 2: Move Existing Files

**Files:**
- Move the files listed in the File Structure section.

- [ ] **Step 1: Move research docs**

Run:

```bash
mv GPT제안_포스터초안.md 통계학회_포스터_실험계획.md 추가실험_승인_컨텍스트.md 학습후_평가_집계_가이드.md docs/research/
```

Expected: command exits with status `0`.

- [ ] **Step 2: Move design note**

Run:

```bash
mv 클로드디자인_영상안내 docs/design/클로드디자인_영상안내.md
```

Expected: command exits with status `0`.

- [ ] **Step 3: Move binary references**

Run:

```bash
mv 25_동계_통계학회_포스터_진군학.pptx 0603_포스터샘플.ppt references/poster_layout/
mv 'Wanted Design System (Community).fig' 'Wanted Design System (Community).fig:Zone.Identifier' references/design_system/
```

Expected: both commands exit with status `0`.

- [ ] **Step 4: Move poster source and build artifacts**

Run:

```bash
mv poster.tex poster/poster.tex
mv poster.pdf poster.aux poster.log poster.out poster/build/
```

Expected: both commands exit with status `0`.

- [ ] **Step 5: Verify root cleanup**

Run:

```bash
find . -maxdepth 1 -type f | sort
```

Expected: root files are limited to high-level context files such as `./AGENTS.md`, `./AI_CONTEXT.md`, `./PRODUCT.md`, `./README.md`, and no poster build artifacts or binary design references remain at root.

## Task 3: Update Path References

**Files:**
- Modify: `poster/poster.tex`
- Modify: `design_harness/README.md`
- Modify: `design_harness/prompts/stat_poster_prd.md`
- Modify: `design_harness/prompts/build_from_design_harness.md`

- [ ] **Step 1: Update TeX macro input**

Edit `poster/poster.tex`:

```tex
\input{../design_harness/templates/wanted_poster_macros.tex}
```

Expected: `poster/poster.tex` can find the TeX macro file when compiled from the `poster/` directory.

- [ ] **Step 2: Update design harness README paths**

Edit `design_harness/README.md` so it refers to:

```text
../references/poster_layout/25_동계_통계학회_포스터_진군학.pptx
../references/design_system/Wanted Design System (Community).fig
../poster/poster.tex
../docs/research/GPT제안_포스터초안.md
../docs/research/통계학회_포스터_실험계획.md
../docs/research/학습후_평가_집계_가이드.md
../docs/research/추가실험_승인_컨텍스트.md
```

Expected: no root-level doc path remains in `design_harness/README.md` except `../AGENTS.md`.

- [ ] **Step 3: Update prompt paths**

Edit `design_harness/prompts/stat_poster_prd.md` and `design_harness/prompts/build_from_design_harness.md` so all input docs use `docs/research/*` paths and the TeX source path is `poster/poster.tex`.

Expected: prompts no longer refer to `GPT제안_포스터초안.md` or `통계학회_포스터_실험계획.md` as root-level files.

- [ ] **Step 4: Scan stale root paths**

Run:

```bash
rg -n "GPT제안_포스터초안|통계학회_포스터_실험계획|추가실험_승인_컨텍스트|학습후_평가_집계_가이드|25_동계_통계학회_포스터_진군학|Wanted Design System|poster\\.tex" AGENTS.md README.md AI_CONTEXT.md PRODUCT.md design_harness docs poster
```

Expected: every match either points to the new location or intentionally describes a moved legacy path.

## Task 4: Write Context And Folder README Files

**Files:**
- Create: `README.md`
- Create: `AI_CONTEXT.md`
- Modify: `AGENTS.md`
- Create: `data/README.md`
- Create: `analysis/README.md`
- Create: `poster/refs.bib`

- [ ] **Step 1: Write root README**

Create `README.md` with:

```markdown
# 2026 Korean Statistics Conference Poster

This workspace is the production area for an A0 portrait statistics conference poster and related presentation artifacts.

Experiment code is external:

`/mnt/c/Users/User/Desktop/2027ICLR/code`

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
- Main story: test accuracy alone is not enough; optimizer-induced feature geometry can change calibration and post-hoc OOD detection reliability.
- Primary evidence plan: WRN-28-10/CIFAR-10 selected 5 configs, seed0/1/2 aggregation.
```

Expected: root README exists and maps the workspace.

- [ ] **Step 2: Write short AI_CONTEXT**

Create `AI_CONTEXT.md` with current state, path map, evidence status, next actions, and startup read order.

Expected: the file is short enough to read at session start and points to detailed docs rather than duplicating them.

- [ ] **Step 3: Update AGENTS**

Modify `AGENTS.md` to reflect the new folder structure, moved reference paths, result-import boundary, TeX target, and startup read order.

Expected: future Codex sessions read the right files and avoid raw result/checkpoint imports.

- [ ] **Step 4: Add data README**

Create `data/README.md` explaining:

```markdown
# Data

Store only small processed CSV/JSON result copies and provenance manifests here.

Do not store raw checkpoints, feature dumps, cache `.pt` files, full server logs, or raw server result directories.

- `manifests/`: import/provenance notes.
- `processed/`: small processed files used by analysis scripts and poster tables.
```

Expected: data boundary is explicit.

- [ ] **Step 5: Add analysis README**

Create `analysis/README.md` explaining:

```markdown
# Analysis

Use this folder for scripts that convert imported processed results into poster tables and figures.

- `scripts/`: aggregation and plotting scripts.
- `outputs/`: intermediate analysis outputs.

Final poster tables belong in `tables/`; final poster figures belong in `figures/final/`.
```

Expected: analysis output boundary is explicit.

- [ ] **Step 6: Add empty bibliography file**

Create `poster/refs.bib` with:

```bibtex
% Bibliography entries for the A0 poster.
% Add WRN, Adam, AdamW, Neural Collapse optimizer, and OOD detector references here.
```

Expected: TeX bibliography target exists without inventing citations.

## Task 5: Verify Reorganization

**Files:**
- Inspect workspace after changes.

- [ ] **Step 1: Check final file list**

Run:

```bash
find . -maxdepth 3 -type f | sort
```

Expected: moved files appear under the approved folders.

- [ ] **Step 2: Check stale root clutter**

Run:

```bash
find . -maxdepth 1 -type f | sort
```

Expected: no `poster.pdf`, `poster.aux`, `poster.log`, `poster.out`, `.ppt`, `.pptx`, `.fig`, or root-level research docs remain.

- [ ] **Step 3: Check TeX compile from `poster/`**

Run:

```bash
cd poster
pdflatex -interaction=nonstopmode -halt-on-error -output-directory build poster.tex
```

Expected: command produces `poster/build/poster.pdf` or fails only because local TeX lacks Korean/XeLaTeX dependencies. Record the exact result.

- [ ] **Step 4: Search for stale references**

Run:

```bash
rg -n "\\.\\./poster\\.tex|../25_|../Wanted|GPT제안_포스터초안.md|통계학회_포스터_실험계획.md" .
```

Expected: any matches are either current new paths or intentional historical notes in specs.

- [ ] **Step 5: Report outcome**

Summarize:

```text
Changed:
- ...

Verified:
- ...

Not verified:
- ...
```

Expected: user knows exactly what moved, what was checked, and any remaining risk.
