# Paper-Flow Poster Redesign Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Redesign the A0 poster into a paper-like narrative flow with compact reference-style header, conceptual calibration/OOD diagrams, and the existing two tables plus two empirical figures.

> Production update, 2026-06-11 KST: this plan is a historical implementation
> record. The current production draft has no title-block subtitle, uses
> `Key Question: 비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`,
> and numbers the concept diagram as Figure 1, the reliability scatter as
> Figure 2, and the raw-to-L2 recovery figure as Figure 3. Use
> `docs/research/poster_section_text.md` and `poster/poster.tex` as the current
> source of truth.

**Architecture:** Keep the redesign scoped to `poster/poster.tex` and reuse existing seed0 CSV-derived figure PDFs. Define compact header and conceptual diagram macros locally inside `poster/poster.tex` so the shared design harness is not changed for one draft. Compile through the existing TeX workflow and preserve seed0 evidence boundaries.

**Tech Stack:** LaTeX/pdfLaTeX with `kotex` for Korean text, TikZ for conceptual diagrams, existing `design_harness/templates/wanted_poster_macros.tex`, existing `figures/source/*.pdf`, existing seed0 CSV files.

---

## File Structure

- Modify: `poster/poster.tex`  
  Responsibility: complete poster source, local compact-header macros, local conceptual diagram macros, paper-flow/evidence-wall layout.
- Read: `design_harness/templates/wanted_poster_macros.tex`  
  Responsibility: shared base poster macros, colors, table, figure, section utilities. Do not modify in this plan.
- Read: `docs/superpowers/specs/2026-06-11-paper-flow-poster-redesign.md`  
  Responsibility: approved redesign spec and acceptance criteria.
- Read: `tables/csv/seed0_id_calibration_summary_draft.csv`  
  Responsibility: source of Table 1 values.
- Read: `tables/csv/seed0_dataset_raw_mahalanobis_draft.csv`  
  Responsibility: source of Table 2 values and 4-row source coverage.
- Read: `figures/source/fig1_seed0_reliability_scatter_draft.pdf`  
  Responsibility: existing empirical source PDF now displayed as poster Figure 2.
- Read: `figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf`  
  Responsibility: existing empirical source PDF now displayed as poster Figure 3.
- Output: `poster/build/poster.pdf`  
  Responsibility: compiled one-page A0 poster.

No experiment code is read or modified. Do not touch `/mnt/c/Users/User/Desktop/2027ICLR/code`.

## Implementation Notes

- There are no standalone logo image files currently in the workspace. Use small text labels `Hanyang Univ.` and `Korean Statistical Society` in the compact header logo zone.
- Do not create new CSV files.
- Do not regenerate the empirical source PDFs unless the existing files are missing.
- The conceptual calibration/OOD diagrams should be TikZ inside `poster/poster.tex`; no new figure source PDFs are required.
- This workspace is not a git repository, so commit steps are not possible. Record that fact in the final report instead of attempting `git commit`.

### Task 1: Verify Inputs And TeX Environment

**Files:**
- Read: `poster/poster.tex`
- Read: `figures/source/fig1_seed0_reliability_scatter_draft.pdf`
- Read: `figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf`
- Read: `tables/csv/seed0_id_calibration_summary_draft.csv`
- Read: `tables/csv/seed0_dataset_raw_mahalanobis_draft.csv`

- [ ] **Step 1: Confirm required poster inputs exist**

Run:

```bash
test -s poster/poster.tex
test -s figures/source/fig1_seed0_reliability_scatter_draft.pdf
test -s figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf
test -s tables/csv/seed0_id_calibration_summary_draft.csv
test -s tables/csv/seed0_dataset_raw_mahalanobis_draft.csv
```

Expected: command exits with status 0.

- [ ] **Step 2: Verify seed0 draft CSV row counts**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import csv
checks = {
    'tables/csv/seed0_id_calibration_summary_draft.csv': 5,
    'tables/csv/seed0_dataset_raw_mahalanobis_draft.csv': 4,
    'tables/csv/seed0_raw_l2_recovery_draft.csv': 5,
}
for path, expected in checks.items():
    with Path(path).open(newline='') as f:
        rows = list(csv.DictReader(f))
    print(path, len(rows))
    assert len(rows) == expected, (path, len(rows), expected)
print('seed0 draft CSV row counts OK')
PY
```

Expected output:

```text
tables/csv/seed0_id_calibration_summary_draft.csv 5
tables/csv/seed0_dataset_raw_mahalanobis_draft.csv 4
tables/csv/seed0_raw_l2_recovery_draft.csv 5
seed0 draft CSV row counts OK
```

- [ ] **Step 3: Check available TeX engine**

Run:

```bash
command -v xelatex || command -v pdflatex
```

Expected: prints at least one TeX engine path. This environment has previously used `/usr/bin/pdflatex`.

- [ ] **Step 4: Check Korean TeX package availability**

Run:

```bash
kpsewhich kotex.sty || TEXMFHOME=/tmp/codex-texmf kpsewhich kotex.sty
```

Expected if Korean TeX support is already available:

```text
/tmp/codex-texmf/tex/latex/cjk-ko/kotex.sty
```

or any valid system path ending in `kotex.sty`.

- [ ] **Step 5: Install temporary Korean TeX user tree only if Step 4 fails**

If Step 4 prints no path, run these exact commands. This downloads TeX packages into `/tmp/codex-texmf` only and does not modify system TeX directories.

```bash
tlmgr --usertree /tmp/codex-texmf init-usertree
tlmgr --usertree /tmp/codex-texmf --repository https://ftp.math.utah.edu/pub/tex/historic/systems/texlive/2023/tlnet-final install collection-langkorean
mkdir -p /tmp/codex-texmf-var /tmp/codex-texmf-config
TEXMFHOME=/tmp/codex-texmf TEXMFVAR=/tmp/codex-texmf-var TEXMFCONFIG=/tmp/codex-texmf-config updmap-user --enable Map=nanumfonts.map
TEXMFHOME=/tmp/codex-texmf TEXMFVAR=/tmp/codex-texmf-var TEXMFCONFIG=/tmp/codex-texmf-config updmap-user
```

Expected: `tlmgr` installs `kotex-utf`, `cjk-ko`, `nanumtype1`, `uhc`, and related packages. `updmap-user` writes map files under `/tmp/codex-texmf-var/fonts/map/`.

- [ ] **Step 6: Re-check Korean TeX package after temporary install**

Run:

```bash
TEXMFHOME=/tmp/codex-texmf kpsewhich kotex.sty
```

Expected:

```text
/tmp/codex-texmf/tex/latex/cjk-ko/kotex.sty
```

### Task 2: Replace Poster TeX With Paper-Flow Layout

**Files:**
- Modify: `poster/poster.tex`

- [ ] **Step 1: Replace `poster/poster.tex` with the complete redesigned TeX source**

Use `apply_patch` to replace the whole file with this source:

```tex
\documentclass[final]{article}

\input{../design_harness/templates/wanted_poster_macros.tex}

% Local draft layout macros for the paper-flow redesign.
\newcommand{\PaperHeader}[4]{%
  \begin{minipage}[t][112mm][t]{\PosterContentWidth}
    \vspace*{1mm}
    \begin{minipage}[t]{635mm}
      {\WantedMetaFont\bfseries\color{WantedAccent}#1\par}
      \vspace{3mm}
      {\fontsize{50pt}{57pt}\selectfont\bfseries\color{WantedInk}\RaggedRight #2\par}
      \vspace{4mm}
      {\fontsize{21pt}{29pt}\selectfont\color{WantedMuted}\RaggedRight #3\par}
      \vspace{4mm}
      {\WantedMetaFont\color{WantedText}#4\par}
    \end{minipage}%
    \hfill
    \begin{minipage}[t]{165mm}
      \raggedleft
      \begin{tabular}{@{}c@{\hspace{5mm}}c@{}}
        \begin{tikzpicture}
          \node[
            draw=WantedAccent,
            line width=0.7pt,
            circle,
            minimum size=31mm,
            align=center,
            text=WantedAccent,
            font=\fontsize{8.5pt}{10pt}\selectfont\bfseries
          ] {Hanyang\\Univ.};
        \end{tikzpicture}
        &
        \begin{tikzpicture}
          \node[
            draw=WantedPrimary,
            line width=0.7pt,
            rounded corners=1mm,
            minimum width=38mm,
            minimum height=28mm,
            align=center,
            text=WantedPrimary,
            font=\fontsize{8pt}{9.5pt}\selectfont\bfseries
          ] {Korean\\Statistical\\Society};
        \end{tikzpicture}
      \end{tabular}
    \end{minipage}
    \vfill
    {\color{WantedPrimary}\rule{\PosterContentWidth}{2.4mm}}\par
  \end{minipage}
  \vspace{4mm}
}

\newcommand{\PaperSection}[2]{%
  \WantedSectionBar{#1}%
  \vspace{3.2mm}
  {\WantedBodyFont\color{WantedText}#2}%
  \vspace{6.2mm}
}

\newcommand{\PaperTinySection}[2]{%
  \WantedSectionBar{#1}%
  \vspace{2.6mm}
  {\fontsize{16.5pt}{23pt}\selectfont\color{WantedText}#2}%
  \vspace{5.2mm}
}

\newcommand{\PaperTightTable}[2]{%
  \begingroup
    \fontsize{14.2pt}{19pt}\selectfont
    \color{WantedText}
    \setlength{\tabcolsep}{4.5pt}
    \renewcommand{\arraystretch}{1.18}
    #1
    \par\vspace{2mm}
    {\WantedCaptionFont\color{WantedMuted}#2}
  \endgroup
}

\newcommand{\CalibrationMiniDiagram}{%
  \begin{tikzpicture}[x=13mm,y=13mm]
    \draw[WantedLineStrong, line width=0.55pt] (0,0) -- (4.2,0);
    \draw[WantedLineStrong, line width=0.55pt] (0,0) -- (0,4.1);
    \draw[WantedLine, line width=0.45pt] (0,0) -- (4,4);
    \foreach \x/\h in {0.45/0.35,1.15/0.75,1.85/1.25,2.55/1.85,3.25/2.35} {
      \fill[WantedStatBlue!70] (\x,0) rectangle ++(0.38,\h);
      \draw[WantedStatRed, line width=0.9pt] (\x,{\x+0.35}) -- ++(0.38,0);
    }
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedMuted] at (2.1,-0.45) {confidence};
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedMuted, rotate=90] at (-0.5,2.05) {accuracy};
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedAccent, anchor=west] at (2.5,3.35) {ideal};
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedStatRed, anchor=west] at (2.5,2.75) {overconfident};
  \end{tikzpicture}%
}

\newcommand{\OODMiniDiagram}{%
  \begin{tikzpicture}[x=12mm,y=12mm]
    \fill[WantedPrimarySoft] (0,0) ellipse (1.35 and 1.0);
    \foreach \x/\y in {-0.9/0.1,-0.5/0.55,-0.35/-0.35,0.15/0.3,0.45/-0.15,0.75/0.45,0.95/-0.45} {
      \fill[WantedStatBlue] (\x,\y) circle (0.075);
    }
    \draw[WantedAccent, line width=0.8pt] (0,0) ellipse (1.35 and 1.0);
    \fill[WantedStatRed] (1.05,0.12) circle (0.12);
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedStatRed, anchor=west] at (1.2,0.18) {OOD scored ID-like};
    \draw[WantedStatRed, line width=0.6pt, ->] (1.18,0.12) -- (0.98,0.12);
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedAccent] at (0,-1.25) {ID feature region};
    \node[font=\fontsize{7.5pt}{8.5pt}\selectfont, text=WantedMuted, anchor=west] at (-1.35,1.35) {$s(x)$ should rank ID $>$ OOD};
  \end{tikzpicture}%
}

\newcommand{\EquationLine}[2]{%
  \begin{minipage}[t]{42mm}
    {\WantedLabelFont\color{WantedAccent}#1}
  \end{minipage}%
  \hspace{3mm}%
  \begin{minipage}[t]{\dimexpr\linewidth-45mm\relax}
    {\fontsize{16pt}{22pt}\selectfont #2}
  \end{minipage}\par\vspace{2mm}
}

\begin{document}
\begin{WantedPoster}

\PaperHeader
  {Korean Statistical Society}
  {Optimizer-Induced Feature Geometry Shapes\\Post-Hoc OOD Detection Reliability}
  {ID accuracy alone does not guarantee reliable calibration or feature-based OOD detection.}
  {Gun-Hak Jin, Department of Mathematical Data Science, Hanyang University}

\WantedTwoColumns
{%
  \PaperSection{Abstract}{%
    High ID accuracy measures classification correctness, but it does not guarantee reliable confidence or robust behavior under distribution shift.

    \vspace{2mm}
    We study WRN-28-10/CIFAR-10 models trained with SGD, Adam, and AdamW over an LR-weight decay grid, selecting models only by ID validation accuracy and evaluating calibration, post-hoc OOD detection, and feature geometry after training.

    \vspace{2mm}
    Seed0 diagnostic evidence suggests that optimizer-induced feature geometry can strongly change raw feature-based OOD reliability, while L2-normalized controls recover much of the detector drop.
  }

  \PaperTinySection{Introduction: Why Accuracy Is Not Reliability}{%
    ID test accuracy는 모델이 정답을 얼마나 자주 맞혔는지를 요약한다. 그러나 실제 AI 시스템에서는 모델이 자신의 예측 확률을 믿을 만하게 말하는지, 그리고 학습 분포 밖의 입력을 만났을 때 위험 신호를 줄 수 있는지도 중요하다. 따라서 calibration과 OOD detection은 accuracy와 다른 reliability axis로 보아야 한다.
  }

  \PaperTinySection{Calibration: What Miscalibration Means}{%
    \begin{minipage}[t]{0.62\linewidth}
      잘 보정된 모델은 confidence가 실제 정답률과 맞는다. Confidence 90\%라고 말한 샘플들이 실제로도 약 90\% 맞아야 한다. Miscalibrated model은 틀릴 때도 높은 confidence를 줄 수 있어 threshold decision이나 reject option을 불안정하게 만든다.

      \vspace{2mm}
      {\fontsize{15pt}{20pt}\selectfont
      \[
      \mathrm{ECE}=\sum_b \frac{|B_b|}{n}\,|\mathrm{acc}(B_b)-\mathrm{conf}(B_b)|
      \]
      }
    \end{minipage}%
    \hfill
    \begin{minipage}[t]{0.33\linewidth}
      \centering
      \CalibrationMiniDiagram
    \end{minipage}
  }

  \PaperTinySection{OOD Detection: What Goes Wrong Under Distribution Shift}{%
    \begin{minipage}[t]{0.60\linewidth}
      OOD detector는 post-hoc score $s(x)$를 사용해 ID input과 distribution-shift input을 구분한다. 좋은 detector는 ID sample에 더 높은 ID-like score를 주고 OOD sample에는 낮은 score를 주어야 한다. OOD sample을 ID처럼 높은 score로 평가하면 분포 밖 입력을 정상 입력처럼 처리하게 된다.

      \vspace{2mm}
      {\fontsize{15pt}{20pt}\selectfont
      \[
      \mathrm{AUROC}=P(s(x_{\mathrm{ID}})>s(x_{\mathrm{OOD}}))
      \]
      }
    \end{minipage}%
    \hfill
    \begin{minipage}[t]{0.35\linewidth}
      \centering
      \OODMiniDiagram
    \end{minipage}
  }

  \PaperTinySection{Optimizers: Update Rules And Intuition}{%
    \EquationLine{SGD}{$w_{t+1}=w_t-\eta g_t$}
    \EquationLine{Adam}{$w_{t+1}=w_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}$}
    \EquationLine{AdamW}{$w_{t+1}=(1-\eta\lambda)w_t-\eta\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}$}
    SGD는 gradient 방향을 직접 따르고, Adam은 first/second moment로 좌표별 adaptive scaling을 적용한다. AdamW는 adaptive update와 weight decay를 분리한다. 이러한 update rule 차이는 feature norm, covariance scale, class mean separation의 형성 방식에 영향을 줄 수 있다.
  }

  \PaperTinySection{Experiment}{%
    CIFAR-10 WRN-28-10을 350 epochs로 학습하고, 동일한 post-hoc evaluation protocol을 사용한다. Hyperparameter selection은 ID validation accuracy만 사용한다. OOD와 geometry metrics는 선택 기준이 아니라 사후 진단이다. 현재 수치는 seed0 diagnostic draft이며, 최종본에서는 selected 5 configs의 seed0/1/2 mean $\pm$ std로 교체한다.
  }
}
{%
  \PaperTinySection{Table 1. ID and Calibration Summary}{%
    \PaperTightTable{%
      \begin{tabularx}{\linewidth}{@{}l l Z Z Z@{}}
        \toprule
        Config & Optimizer & Val Acc & Test Acc & ECE \\
        \midrule
        SGD-A & SGD & 95.86 & 95.85 & 2.98 \\
        SGD-B & SGD & 96.12 & 95.46 & 3.31 \\
        Adam & Adam & 94.94 & 94.47 & 3.90 \\
        AdamW-B & AdamW & 95.28 & 94.68 & 4.51 \\
        AdamW-A & AdamW & 95.02 & 94.37 & 4.79 \\
        \bottomrule
      \end{tabularx}%
    }{Values are percentages from seed0 diagnostic draft evidence.}
  }

  \PaperTinySection{Table 2. Dataset-Specific Raw Mahalanobis AUROC}{%
    \PaperTightTable{%
      \begin{tabularx}{\linewidth}{@{}l l Z Z Z Z@{}}
        \toprule
        Config & Optimizer & CIFAR-100 & TinyImageNet & SVHN & MNIST \\
        \midrule
        SGD-B & SGD & 0.861 & 0.857 & 0.973 & 0.946 \\
        Adam-0 & Adam & 0.610 & 0.565 & 0.900 & 0.630 \\
        Adam & Adam & 0.568 & 0.542 & 0.660 & 0.442 \\
        AdamW-B & AdamW & 0.435 & 0.398 & 0.783 & 0.271 \\
        \bottomrule
      \end{tabularx}%
    }{Seed0 dataset-specific source directly exposes four representative rows. Final poster replaces this with selected 5 configs over 3 seeds.}
  }

  \PaperTinySection{Figure 2. Accuracy-Matched Reliability Scatter}{%
    \includegraphics[width=\linewidth]{../figures/source/fig1_seed0_reliability_scatter_draft.pdf}

    \vspace{1mm}
    {\WantedCaptionFont\color{WantedMuted}Seed0 draft: ID validation accuracy 대비 ECE와 raw Mahalanobis AUROC. 최종본에서는 seed0 grid background와 selected 5 configs의 3-seed error bar를 함께 표시한다.}
  }

  \PaperTinySection{Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity}{%
    \includegraphics[width=\linewidth]{../figures/source/fig2_seed0_raw_to_l2_recovery_draft.pdf}

    \vspace{1mm}
    {\WantedCaptionFont\color{WantedMuted}L2-normalized controls reduce feature-scale effects while preserving angular information. Raw-to-L2 recovery suggests norm/covariance-scale sensitivity.}
  }

  \PaperTinySection{Mechanism Diagnostic / Future Work}{%
    Raw Mahalanobis and raw kNN depend on feature norms, distances, and covariance scale. L2-normalized controls reduce feature-scale effects while preserving angular information. Raw-to-L2 recovery is consistent with optimizer-induced norm/covariance-scale geometry contributing to detector reliability gaps.

    \vspace{3mm}
    {\WantedSubsectionFont\textcolor{WantedAccent}{Future Work}}\par\vspace{1mm}
    \begin{enumerate}[leftmargin=8mm,itemsep=1mm,topsep=0mm]
      \item Adam-AdamW interpolation
      \item dataset / architecture expansion
      \item SAM, Mixup 등 다른 training methods 확장
    \end{enumerate}
  }
}

\WantedFooter
  {Seed0 diagnostic draft. Main claims avoid seed-averaged consistency language until selected seed0/1/2 aggregation is imported.}
  {Poster source: poster/poster.tex}

\end{WantedPoster}
\end{document}
```

- [ ] **Step 2: Confirm old header placeholder text is gone from `poster.tex`**

Run:

```bash
rg -n "Logo / QR code|A0 portrait|XeLaTeX / Pretendard|WantedHeader" poster/poster.tex
```

Expected: no matches.

- [ ] **Step 3: Confirm required narrative sections exist**

Run:

```bash
rg -n "Abstract|Introduction: Why Accuracy Is Not Reliability|Calibration: What Miscalibration Means|OOD Detection: What Goes Wrong Under Distribution Shift|Optimizers: Update Rules And Intuition|Experiment" poster/poster.tex
```

Expected: each section title appears at least once.

- [ ] **Step 4: Confirm required evidence sections exist**

Run:

```bash
rg -n "Table 1. ID and Calibration Summary|Table 2. Dataset-Specific Raw Mahalanobis AUROC|Figure 2. Accuracy-Matched Reliability Scatter|Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity|Mechanism Diagnostic / Future Work" poster/poster.tex
```

Expected: each section title appears at least once.

- [ ] **Step 5: Confirm conceptual diagram macros exist**

Run:

```bash
rg -n "CalibrationMiniDiagram|OODMiniDiagram|ECE|AUROC" poster/poster.tex
```

Expected: `CalibrationMiniDiagram`, `OODMiniDiagram`, `ECE`, and `AUROC` all appear.

### Task 3: Compile Poster And Fix Layout-Blocking TeX Errors

**Files:**
- Read: `poster/poster.tex`
- Output: `poster/build/poster.pdf`

- [ ] **Step 1: Compile with Korean-capable pdflatex environment**

Run:

```bash
cd poster
TEXMFHOME=/tmp/codex-texmf TEXMFVAR=/tmp/codex-texmf-var TEXMFCONFIG=/tmp/codex-texmf-config pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build poster.tex
```

Expected: command exits with status 0 and prints:

```text
Output written on build/poster.pdf
```

- [ ] **Step 2: If compile fails with missing `kotex.sty`, return to Task 1 Step 5**

Expected missing package symptom:

```text
kotex.sty not found
Unicode character ... not set up for use with LaTeX
```

Do not edit content to remove Korean text. Install the temporary Korean TeX user tree from Task 1 Step 5 and rerun Task 3 Step 1.

- [ ] **Step 3: If compile fails with undefined macro from local TeX source, fix only the named macro**

Expected macro-error pattern:

```text
! Undefined control sequence.
l.<line> \<macro-name>
```

Fix rule:

- If the missing macro is one of `PaperHeader`, `PaperSection`, `PaperTinySection`, `PaperTightTable`, `CalibrationMiniDiagram`, `OODMiniDiagram`, or `EquationLine`, compare the local macro block in `poster/poster.tex` against Task 2 Step 1 and restore the missing definition.
- If the missing macro is from the design harness, inspect `design_harness/templates/wanted_poster_macros.tex` before editing. Do not invent a new replacement without checking existing macros.

- [ ] **Step 4: Rerun compile after any TeX fix**

Run:

```bash
cd poster
TEXMFHOME=/tmp/codex-texmf TEXMFVAR=/tmp/codex-texmf-var TEXMFCONFIG=/tmp/codex-texmf-config pdflatex -interaction=nonstopmode -halt-on-error -output-directory=build poster.tex
```

Expected: command exits with status 0.

### Task 4: Verify Poster Output

**Files:**
- Read: `poster/poster.tex`
- Read: `poster/build/poster.pdf`
- Read: `poster/build/poster.log`

- [ ] **Step 1: Verify PDF exists and is non-empty**

Run:

```bash
test -s poster/build/poster.pdf
ls -lh poster/build/poster.pdf
```

Expected: `poster/build/poster.pdf` exists and has non-zero file size.

- [ ] **Step 2: Verify PDF is exactly one page**

Run:

```bash
pdfinfo poster/build/poster.pdf | rg '^Pages:'
```

Expected output:

```text
Pages:           1
```

- [ ] **Step 3: Verify page size is A0**

Run:

```bash
pdfinfo poster/build/poster.pdf | rg '^Page size:'
```

Expected output includes:

```text
(A0)
```

- [ ] **Step 4: Check TeX log for hard errors and overfull boxes**

Run:

```bash
rg -n "Fatal|Emergency stop|Undefined control sequence|LaTeX Error|Package .* Error|Overfull" poster/build/poster.log
```

Expected: no matches.

If `Overfull` appears, reduce local section spacing in `poster/poster.tex` by changing `\vspace{6.2mm}` in `\PaperSection` to `\vspace{5mm}` and `\vspace{5.2mm}` in `\PaperTinySection` to `\vspace{4mm}`, then rerun Task 3 Step 1 and Task 4.

- [ ] **Step 5: Verify required text appears in PDF**

Run:

```bash
pdftotext poster/build/poster.pdf - | rg -n "Optimizer-Induced Feature Geometry Shapes|Post-Hoc OOD Detection Reliability|ID accuracy alone|Abstract|Calibration|OOD Detection|Optimizers|Raw-to-L2 Recovery|Adam-AdamW"
```

Expected: all listed concepts appear in extracted PDF text.

- [ ] **Step 6: Verify stale title/wording does not appear in TeX**

Run:

```bash
rg -n "Changes Post-Hoc|A matched-accuracy optimizer comparison|WRN-28-10 or ResNet-18|Optimizer & Acc|Test accuracy alone is not enough|Logo / QR code" poster/poster.tex
```

Expected: no matches.

- [ ] **Step 7: Verify stale title/wording does not appear in PDF text**

Run:

```bash
pdftotext poster/build/poster.pdf - | rg -n "Changes Post-Hoc|A matched-accuracy optimizer comparison|WRN-28-10 or ResNet-18|Optimizer & Acc|Test accuracy alone is not enough|Logo / QR code"
```

Expected: no matches.

- [ ] **Step 8: Verify Table 2 source coverage note remains**

Run:

```bash
rg -n "four representative rows|4개 대표 후보|3-seed 집계값" poster/poster.tex
pdftotext poster/build/poster.pdf - | rg -n "four representative rows|3-seed"
```

Expected: both commands find the source coverage note or its English equivalent.

### Task 5: Final Implementation Report

**Files:**
- Read: `poster/poster.tex`
- Read: `poster/build/poster.pdf`
- Read: `poster/build/poster.log`

- [ ] **Step 1: Confirm workspace is not a git repository**

Run:

```bash
git rev-parse --git-dir
```

Expected:

```text
fatal: not a git repository (or any of the parent directories): .git
```

Do not attempt `git add` or `git commit`.

- [ ] **Step 2: Report modified/generated files**

Include these paths in the final report:

```text
poster/poster.tex
poster/build/poster.pdf
```

If Task 1 Step 5 was needed, also report temporary TeX environment paths:

```text
/tmp/codex-texmf
/tmp/codex-texmf-var
/tmp/codex-texmf-config
```

- [ ] **Step 3: Report verification commands and results**

The final report must include:

```text
- TeX compile: exit 0
- PDF page count: Pages: 1
- PDF page size: A0
- CSV row counts: 5 / 4 / 5
- Figure PDF existence: both source PDFs non-empty
- Hard TeX error/Overfull check: no matches
- Stale title/wording check: no matches
```

- [ ] **Step 4: Report remaining data limitations**

Use this wording:

```text
현재 수치는 seed0 diagnostic draft이다. Table 2 dataset-specific markdown source는 4개 대표 후보만 직접 제공하므로, 최종본에서는 selected 5 configs의 seed0/1/2 mean +/- std와 dataset-specific values로 교체해야 한다.
```

## Self-Review Checklist

- Spec coverage: compact header, abstract, introduction, reliability failure concept diagram, optimizer equations, experiment boundary, two tables, two empirical figures, mechanism, future work, one-page PDF verification are all covered.
- Placeholder scan: plan uses no `TBD`, `TODO`, or unresolved placeholder work. The header uses concrete text labels because no logo image assets are present.
- Type/name consistency: local macros referenced in body are defined before `\begin{document}`; section titles match the approved spec; Figure 3 title and x-axis short labels are preserved through the existing source PDF and caption.
