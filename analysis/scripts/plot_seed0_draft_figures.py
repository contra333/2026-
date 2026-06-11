#!/usr/bin/env python3
from pathlib import Path
import csv
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[2]
TABLE_DIR = ROOT / "tables" / "csv"
FIG_DIR = ROOT / "figures" / "source"
FIG_DIR.mkdir(parents=True, exist_ok=True)

COLORS = {
    "SGD": "0070C0",
    "Adam": "70AD47",
    "AdamW": "C00000",
}

FIGURE_FONT_PREAMBLE = r"""
\usepackage{fontspec}
\usepackage{unicode-math}
\setmainfont[
  Path=/mnt/c/Windows/Fonts/,
  UprightFont=calibri.ttf,
  BoldFont=calibrib.ttf,
  ItalicFont=calibrii.ttf,
  BoldItalicFont=calibriz.ttf
]{Calibri}
\setsansfont[
  Path=/mnt/c/Windows/Fonts/,
  UprightFont=calibri.ttf,
  BoldFont=calibrib.ttf,
  ItalicFont=calibrii.ttf,
  BoldItalicFont=calibriz.ttf
]{Calibri}
\setmathfont[
  Path=/mnt/c/Windows/Fonts/,
  FontIndex=1
]{cambria.ttc}
"""


def read_csv(name):
    with (TABLE_DIR / name).open(newline="") as f:
        return list(csv.DictReader(f))


def grouped(rows, key):
    out = {}
    for row in rows:
        out.setdefault(row[key], []).append(row)
    return out


def latex_points(rows, metric):
    return " ".join(f"({float(row['val_acc']):.4f},{float(row[metric]):.4f})" for row in rows)


def latex_nodes(rows, metric):
    return "\n".join(
        rf"\node[anchor=south west,font=\scriptsize] at (axis cs:{float(row['val_acc']):.4f},{float(row[metric]):.4f}) {{{row['short_label']}}};"
        for row in rows
    )


def compile_tex(tex_source, output_pdf):
    engine = shutil.which("xelatex") or shutil.which("lualatex")
    if engine is None:
        raise RuntimeError("No XeLaTeX/LuaLaTeX engine found for PGFPlots figure generation.")

    with tempfile.TemporaryDirectory(prefix="poster_fig_", dir="/tmp") as tmp:
        tmp_dir = Path(tmp)
        tex_path = tmp_dir / "figure.tex"
        tex_path.write_text(tex_source, encoding="utf-8")
        result = subprocess.run(
            [engine, "-interaction=nonstopmode", "-halt-on-error", "figure.tex"],
            cwd=tmp_dir,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        if result.returncode != 0:
            raise RuntimeError(result.stdout)
        shutil.copy2(tmp_dir / "figure.pdf", output_pdf)


def plot_fig1():
    summary = read_csv("seed0_id_calibration_summary_draft.csv")
    recovery = {row["short_label"]: row for row in read_csv("seed0_raw_l2_recovery_draft.csv")}
    merged = []
    for row in summary:
        full = dict(row)
        full["raw_maha"] = recovery[row["short_label"]]["raw_maha"]
        merged.append(full)

    def axis_plots(rows, metric):
        parts = []
        for optimizer, opt_rows in grouped(rows, "optimizer").items():
            color = COLORS.get(optimizer, "555555")
            parts.append(
                rf"\addplot+[only marks,mark=*,mark size=3.1pt,draw=black,fill={optimizer}Color,color={optimizer}Color] coordinates {{{latex_points(opt_rows, metric)}}};"
            )
            parts.append(latex_nodes(opt_rows, metric))
        return "\n".join(parts)

    tex = rf"""
\documentclass[tikz,border=3mm]{{standalone}}
{FIGURE_FONT_PREAMBLE}
\usepackage{{pgfplots}}
\usepgfplotslibrary{{groupplots}}
\pgfplotsset{{compat=1.18}}
\definecolor{{SGDColor}}{{HTML}}{{{COLORS['SGD']}}}
\definecolor{{AdamColor}}{{HTML}}{{{COLORS['Adam']}}}
\definecolor{{AdamWColor}}{{HTML}}{{{COLORS['AdamW']}}}
\definecolor{{GridColor}}{{HTML}}{{D9E2EF}}
\begin{{document}}
\begin{{tikzpicture}}
\begin{{groupplot}}[
  group style={{group size=2 by 1,horizontal sep=1.35cm}},
  width=7.3cm,
  height=5.35cm,
  xlabel={{ID validation accuracy}},
  grid=both,
  grid style={{draw=GridColor,line width=0.25pt}},
  tick label style={{font=\small}},
  label style={{font=\small}},
  title style={{font=\bfseries\small}},
  legend style={{at={{(0.5,1.22)}},anchor=south,draw=none,font=\small}},
  legend columns=3
]
\nextgroupplot[title={{ECE}},ylabel={{ECE}}]
{axis_plots(merged, 'ece')}
\legend{{SGD,Adam,AdamW}}

\nextgroupplot[title={{Raw Mahalanobis AUROC}},ylabel={{Raw Mahalanobis AUROC}}]
{axis_plots(merged, 'raw_maha')}
\end{{groupplot}}
\node[anchor=south,font=\bfseries] at (current bounding box.north) {{Figure 2. Accuracy-Matched Reliability Scatter (seed0 draft)}};
\end{{tikzpicture}}
\end{{document}}
"""
    compile_tex(tex, FIG_DIR / "fig1_seed0_reliability_scatter_draft.pdf")


def plot_fig2():
    rows = read_csv("seed0_raw_l2_recovery_draft.csv")
    labels = ",".join(row["short_label"] for row in rows)
    series = [
        ("raw_maha", "Raw Maha", "RawMahaColor", "0070C0"),
        ("maha_l2", "Maha-L2", "MahaLtwoColor", "5B9BD5"),
        ("raw_knn", "Raw kNN", "RawKnnColor", "70AD47"),
        ("knn_l2", "kNN-L2", "KnnLtwoColor", "FFC000"),
    ]
    plots = []
    legends = []
    color_defs = []
    for column, label, color_name, color in series:
        color_defs.append(rf"\definecolor{{{color_name}}}{{HTML}}{{{color}}}")
        coords = " ".join(f"({row['short_label']},{float(row[column]):.4f})" for row in rows)
        plots.append(rf"\addplot+[fill={color_name},draw=none] coordinates {{{coords}}};")
        legends.append(label)

    tex = rf"""
\documentclass[tikz,border=3mm]{{standalone}}
{FIGURE_FONT_PREAMBLE}
\usepackage{{pgfplots}}
\pgfplotsset{{compat=1.18}}
\definecolor{{GridColor}}{{HTML}}{{D9E2EF}}
{chr(10).join(color_defs)}
\begin{{document}}
\begin{{tikzpicture}}
\begin{{axis}}[
  ybar,
  width=15.8cm,
  height=6.2cm,
  ymin=0.2,
  ymax=1.02,
  ylabel={{Near/Far mean AUROC}},
  symbolic x coords={{{labels}}},
  xtick=data,
  xticklabel style={{font=\small}},
  tick label style={{font=\small}},
  label style={{font=\small}},
  title={{Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity}},
  title style={{font=\bfseries}},
  bar width=5.5pt,
  enlarge x limits=0.15,
  grid=major,
  grid style={{draw=GridColor,line width=0.25pt}},
  legend style={{at={{(0.5,1.14)}},anchor=south,legend columns=4,draw=none,font=\small}},
  clip=false
]
{chr(10).join(plots)}
\legend{{{','.join(legends)}}}
\node[anchor=north,font=\scriptsize,align=center,text width=15cm] at (rel axis cs:0.5,-0.18)
{{SGD-A: SGD anchor | SGD-B: SGD val-best | Adam: Adam reg. | AdamW-B: AdamW val-best | AdamW-A: AdamW anchor}};
\end{{axis}}
\end{{tikzpicture}}
\end{{document}}
"""
    compile_tex(tex, FIG_DIR / "fig2_seed0_raw_to_l2_recovery_draft.pdf")


def main():
    plot_fig1()
    plot_fig2()
    print(FIG_DIR / "fig1_seed0_reliability_scatter_draft.pdf")
    print(FIG_DIR / "fig2_seed0_raw_to_l2_recovery_draft.pdf")


if __name__ == "__main__":
    main()
