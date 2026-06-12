# Pretendard

Project-local Pretendard font files for Korean poster production.

- Source: https://github.com/orioncactus/pretendard
- Release: v1.3.9
- Download URL: https://github.com/orioncactus/pretendard/releases/download/v1.3.9/Pretendard-1.3.9.zip
- Installed: 2026-06-11
- License: SIL Open Font License 1.1. See `LICENSE.txt`.

## Files

- `static/*.otf`: static desktop fonts used by XeLaTeX/kotex through `design_harness/templates/wanted_poster_macros.tex`.
- `web/variable/PretendardVariable.woff2`: variable webfont used by `design_harness/templates/stat_poster_a0.html`.

Keep these files under `design_harness/fonts/pretendard/` so TeX and HTML builds do not depend on machine-level font installation.
