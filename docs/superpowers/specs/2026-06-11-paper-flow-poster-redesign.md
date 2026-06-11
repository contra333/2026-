# Paper-Flow Poster Redesign Spec

작성일: 2026-06-11 KST

> Production update, 2026-06-11 KST: 이 spec은 paper-flow redesign의 당시 결정 기록이다.
> 현재 production draft에서는 title block subtitle을 삭제했고, `Key Question`은
> `비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`이다.
> Conceptual calibration/OOD material은 Figure 1 `Reliability Failure:
> Miscalibration and OOD Acceptance`로 승격되었고, 기존 empirical figures는
> 각각 Figure 2/3으로 이동했다. 최신 source of truth는
> `docs/research/poster_section_text.md`이다.

## 목적

현재 `poster/poster.tex`와 `poster/build/poster.pdf`는 seed0 결과 표와 그림을
넣는 데는 성공했지만, 포스터를 읽는 사람이 왜 이 문제가 중요한지 따라가기에는
설명량이 부족하다. 특히 calibration, OOD detection, optimizer update rule,
feature geometry mechanism 사이의 논리 연결이 짧게만 제시되어 있어, 결과가
갑자기 등장하는 인상을 준다.

이번 redesign의 목표는 포스터를 짧은 논문처럼 읽히게 만드는 것이다. 다만
통계학회 A0 포스터라는 형식은 유지한다. 즉, 표 2개와 empirical 그림 2개를
유지하고, calibration/OOD concept을 Figure 1로 별도 배치한다. 상단 header를
줄여 확보한 공간에는 abstract-like summary, introduction, reliability failure
개념 설명, optimizer 직관을 추가한다.

## 결정된 방향

채택한 접근은 **Paper-Flow With Evidence Wall**이다.

- 왼쪽 열은 논문형 흐름:
  `Abstract -> Introduction -> Reliability Failure -> Optimizers -> Experiment`
- 오른쪽 열은 evidence wall:
  `Figure 2 -> Table 1 -> Table 2 -> Figure 3 -> Mechanism / Future Work`
- 본문 설명은 한국어 초안으로 작성한다.
- title, section headings, table/figure titles는 영어로 유지한다.
- title block subtitle은 사용하지 않는다.
- 표 2개, concept Figure 1, empirical Figures 2/3를 유지한다.
- Calibration reliability diagram과 OOD miss-detection schematic은 Figure 1
  concept diagram으로 통합한다.

## Reference Poster Lessons

다음 reference를 새 상단 구성의 기준으로 사용한다.

- `references/poster_layout/24_하계_통계학회_포스터_양준성_최종제출본_v3.pptx`
- `references/poster_layout/4. 25_하계_통계학회_포스터.pdf`

확인한 layout rule:

1. Header는 현재 `poster.tex`보다 훨씬 compact하다.
2. 큰 QR 임시 박스 또는 큰 빈 logo box는 없다.
3. 제목은 상단에 크게 두되, 저자/소속은 제목 아래 한 줄 또는 두 줄로 압축한다.
4. 한양대학교 로고와 통계학회 로고는 작은 크기로 상단 가장자리 영역에 배치한다.
5. Header 아래에는 얇은 blue rule이 있고, 바로 첫 section bar가 시작한다.
6. A1 reference에서는 첫 section이 상단 약 10% 부근에서 시작하므로, A0 poster에서도
   header가 body를 과도하게 밀어내면 안 된다.

새 header rule:

- `Logo / QR code` 큰 임시 박스는 제거한다.
- Header height는 A0 기준 약 `105-120mm`를 목표로 한다.
- 제목은 2줄 이하로 유지한다.
- Subtitle은 사용하지 않는다.
- 저자/소속은 compact하게 둔다.
- 우측 상단에는 작은 logo zone을 둔다. 실제 로고 파일이 있으면 한양대와 통계학회
  로고를 넣고, 없으면 작은 text label만 둔다.

## Fixed Title And Header

Title:

```text
Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability
```

Subtitle:

```text
None. The current production title block has no subtitle.
```

## Final Narrative Flow

### 1. Abstract

상단 header 바로 아래에 `Abstract` section을 둔다. 3문장으로 고정한다.
각 문장은 problem, method, finding 역할을 한다.

Draft text:

```text
High ID accuracy measures classification correctness, but it does not guarantee reliable confidence or robust behavior under distribution shift.

We study WRN-28-10/CIFAR-10 models trained with SGD, Adam, and AdamW over an LR-weight decay grid, selecting models only by ID validation accuracy and evaluating calibration, post-hoc OOD detection, and feature geometry after training.

Seed0 diagnostic evidence suggests that optimizer-induced feature geometry can strongly change raw feature-based OOD reliability, while L2-normalized controls recover much of the detector drop.
```

### 2. Introduction: Why Accuracy Is Not Reliability

역할:

- 포스터의 문제 제기를 담당한다.
- `accuracy = correctness summary`이고, `reliability = confidence + distribution-shift
  behavior`라는 구분을 만든다.
- 지나치게 일반적인 AI safety 서론으로 흐르지 않는다.

Draft Korean text:

```text
ID test accuracy는 모델이 정답을 얼마나 자주 맞혔는지를 요약한다. 그러나 실제
AI 시스템에서는 모델이 자신의 예측 확률을 믿을 만하게 말하는지, 그리고 학습
분포 밖의 입력을 만났을 때 위험 신호를 줄 수 있는지도 중요하다. 따라서
calibration과 OOD detection은 accuracy와 다른 reliability axis로 보아야 한다.
```

### 3. Calibration: What Miscalibration Means

역할:

- calibration이 무엇인지 짧게 정의한다.
- reliability diagram이 왜 필요한지 설명한다.
- miscalibration의 실제 문제를 한 줄로 연결한다.

Draft content:

```text
잘 보정된 모델은 confidence가 실제 정답률과 맞는다. 예를 들어 confidence 90%
라고 말한 샘플들이 실제로도 약 90% 맞아야 한다. Miscalibrated model은 틀릴 때도
높은 confidence를 줄 수 있어 threshold decision이나 reject option을 불안정하게
만든다.
```

Formula:

```tex
ECE = \sum_b \frac{|B_b|}{n}\, |\mathrm{acc}(B_b)-\mathrm{conf}(B_b)|
```

Conceptual diagram requirement:

- 작은 reliability diagram을 넣는다.
- x-axis: confidence bin
- y-axis: empirical accuracy
- diagonal line: ideal calibration
- bars/points: overconfident model이 diagonal 아래에 있는 상황
- 목적: `confidence != accuracy`를 시각적으로 보여준다.

### 4. OOD Detection: What Goes Wrong Under Distribution Shift

역할:

- OOD detection이 무엇인지 짧게 정의한다.
- post-hoc detector가 score ranking 문제임을 보여준다.
- OOD sample을 ID처럼 처리하는 위험을 설명한다.

Draft content:

```text
OOD detector는 post-hoc score s(x)를 사용해 ID input과 distribution-shift input을
구분한다. 좋은 detector는 ID sample에 더 높은 ID-like score를 주고, OOD sample에는
낮은 score를 주어야 한다. OOD sample을 ID처럼 높은 score로 평가하면, 모델은
분포 밖 입력을 정상 입력처럼 처리하게 된다.
```

Formula:

```tex
AUROC = P(s(x_{\mathrm{ID}}) > s(x_{\mathrm{OOD}}))
```

Conceptual diagram requirement:

- 작은 schematic을 넣는다.
- ID cluster는 blue points로 표현한다.
- OOD point는 red/orange point로 표현한다.
- 실패 상황은 OOD point가 ID-like high score 영역 안에 들어온 모습으로 표현한다.
- 목적: OOD detection failure가 단순 숫자 저하가 아니라 safety/reliability guard
  failure임을 보여준다.

### 5. Optimizers: Update Rules And Intuition

역할:

- SGD, Adam, AdamW가 단순 label 차이가 아니라 update rule 차이라는 점을 보여준다.
- optimizer가 feature geometry에 영향을 줄 수 있는 직관을 제공한다.
- 너무 긴 optimizer tutorial이 되지 않게 한다.

Draft formulas:

```tex
\text{SGD:}\quad w_{t+1}=w_t-\eta g_t
```

```tex
\text{Adam:}\quad w_{t+1}=w_t-\eta \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
```

```tex
\text{AdamW:}\quad w_{t+1}=(1-\eta\lambda)w_t-\eta \frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
```

Draft Korean text:

```text
SGD는 gradient 방향을 직접 따른다. Adam은 first/second moment를 사용해 좌표별로
adaptive scaling을 적용한다. AdamW는 adaptive update와 weight decay를 분리한다.
이러한 update rule 차이는 feature norm, covariance scale, class mean separation의
형성 방식에 영향을 줄 수 있다.
```

주의:

- optimizer가 feature geometry를 반드시 `causes`한다고 강하게 쓰지 않는다.
- `can shape`, `suggests`, `is consistent with`, `may contribute to`를 사용한다.

### 6. Experiment

역할:

- 결과 해석의 boundary를 고정한다.
- hyperparameter selection이 OOD를 보지 않았음을 명시한다.
- seed0 draft와 final 3-seed 구조를 분리한다.

Draft content:

```text
We use CIFAR-10 WRN-28-10 models trained for 350 epochs with a fixed evaluation
protocol. Hyperparameter selection uses ID validation accuracy only. OOD and
geometry metrics are post-hoc diagnostics. Current values are seed0 diagnostic
draft values; the final poster will replace selected rows with 3-seed mean
\pm std over seed0/1/2.
```

Selected configs:

| Short label | Config label | Role |
|---|---|---|
| `SGD-A` | `sgd_lr1e-1_wd5e-4_anchor` | SGD anchor |
| `SGD-B` | `sgd_lr1e-1_wd2e-4` | SGD validation-best control |
| `Adam` | `adam_lr1e-3_wd1e-4` | regularized Adam representative |
| `AdamW-B` | `adamw_lr5e-3_wd1e-4` | AdamW validation-best representative |
| `AdamW-A` | `adamw_lr5e-3_wd5e-4_anchor` | AdamW anchor |

## Evidence Wall

오른쪽 열은 기존 evidence 구조를 유지한다.

### Table 1. ID and Calibration Summary

유지할 columns:

```text
Config
Optimizer
Val Acc
Test Acc
ECE
```

역할:

- selected 5 configs가 비슷한 ID performance band에 있음을 보여준다.
- calibration은 accuracy와 다른 reliability axis임을 보여준다.

### Table 2. Dataset-Specific Raw Mahalanobis AUROC

유지할 columns:

```text
Config
Optimizer
CIFAR-100
TinyImageNet
SVHN
MNIST
```

Source coverage note:

```text
Table 2의 seed0 dataset-specific source는 현재 4개 대표 후보만 직접 제공한다.
최종본에서는 selected 5 configs의 3-seed 집계값으로 교체한다.
```

### Figure 1. Reliability Failure: Miscalibration and OOD Acceptance

역할:

- Miscalibration과 OOD acceptance를 concept diagram으로 설명한다.
- ECE와 AUROC 정의를 같은 섹션에 둔다.

### Figure 2. Accuracy-Matched Reliability Scatter

역할:

- ID validation accuracy가 비슷한 영역에서도 ECE와 raw Mahalanobis AUROC가
  갈라질 수 있음을 보여준다.

### Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity

유지할 title:

```text
Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity
```

유지할 x-axis short labels:

```text
SGD-A, SGD-B, Adam, AdamW-B, AdamW-A
```

역할:

- raw detector drop이 L2-normalized control에서 회복되는 패턴을 보여준다.
- feature norm/covariance-scale sensitivity 해석으로 연결한다.

### Mechanism Diagnostic

Draft content:

```text
Raw Mahalanobis and raw kNN depend on feature norms, distances, and covariance
scale. L2-normalized controls reduce feature-scale effects while preserving
angular information. Raw-to-L2 recovery is consistent with optimizer-induced
norm/covariance-scale geometry contributing to detector reliability gaps.
```

한국어 해석 문장:

```text
이 결과는 Adam/AdamW에서 feature-based OOD가 단순히 실패한다는 뜻이 아니다.
더 정확히는 raw norm/covariance-sensitive detector가 optimizer-induced feature
geometry와 충돌하고, detector-side normalization이 그 영향을 상당 부분 완화할 수
있다는 신호로 해석한다.
```

## Future Work

순서는 유지한다.

1. Adam-AdamW interpolation
2. dataset / architecture expansion
3. SAM, Mixup 등 다른 training methods 확장

## TeX Redesign Requirements

다음 구현 계획에서 다룰 TeX 변경 범위:

- `poster/poster.tex`를 Paper-Flow With Evidence Wall 구조로 재배치한다.
- `WantedHeader` 또는 별도 compact header macro를 사용해 상단 높이를 줄인다.
- 큰 `Logo / QR code` 임시 박스를 제거한다.
- 실제 로고 파일이 있으면 작은 logo zone에 넣고, 없으면 작은 text label만 둔다.
- Calibration reliability diagram을 TeX/TikZ 또는 figure PDF로 생성한다.
- OOD miss-detection schematic을 TeX/TikZ 또는 figure PDF로 생성한다.
- 기존 seed0 CSV, Table 1/2, empirical Figure 2/3 값과 provenance boundary를 유지한다.
- `poster/build/poster.pdf`를 A0 portrait 1페이지로 컴파일한다.

## Data And Evidence Boundaries

- 실험 코드는 수정하지 않는다.
- `/mnt/c/Users/User/Desktop/2027ICLR/code`는 source of truth이므로 건드리지 않는다.
- 현재 포스터 workspace 안에서만 TeX, CSV, provenance manifest, figure source PDF,
  build PDF를 생성/수정한다.
- seed0-only 결과로 seed-averaged consistency claim을 쓰지 않는다.
- DDU는 `DDU-style GMM feature density`로 표현한다.
- Table 2 dataset-specific row coverage note를 유지한다.
- 최종 3-seed 결과가 오면 selected 5 configs `mean +/- std`로 교체 가능한 구조를
  유지한다.

## Acceptance Criteria

새 poster draft는 다음을 만족해야 한다.

1. Title은 확정 문구와 정확히 일치하고 title block subtitle은 없다.
2. Header는 reference처럼 compact해야 하며, 큰 QR/logo 임시 박스가 없어야 한다.
3. 첫 section `Abstract`가 현재 draft보다 훨씬 위에서 시작해야 한다.
4. Abstract는 problem/method/finding 3문장 구조다.
5. Introduction은 `accuracy is not reliability` 메시지를 분명히 설명한다.
6. Calibration section은 ECE 직관식과 작은 reliability diagram을 포함한다.
7. OOD Detection section은 AUROC 직관식과 작은 OOD failure schematic을 포함한다.
8. Optimizers section은 SGD, Adam, AdamW update 식과 짧은 직관을 포함한다.
9. Table 1과 Table 2는 유지한다.
10. Figure 1 concept diagram과 empirical Figure 2/3를 유지한다.
11. Figure 3 title은 `Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity`이다.
12. Figure 3 x-axis short labels는 `SGD-A`, `SGD-B`, `Adam`, `AdamW-B`, `AdamW-A`이다.
13. Future Work 순서는 Adam-AdamW interpolation, dataset / architecture expansion,
    SAM/Mixup 확장 순서다.
14. 본문 설명은 한국어 초안이고, section/table/figure titles는 영어다.
15. `poster/build/poster.pdf`는 1페이지여야 한다.
16. 기존 잘못된 제목/문구가 `poster.tex`와 PDF에 남아 있지 않아야 한다.
