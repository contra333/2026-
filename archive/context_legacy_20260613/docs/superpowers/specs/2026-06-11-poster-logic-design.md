# 통계학회 포스터 논리/레이아웃 설계

작성일: 2026-06-11 KST

> Production update, 2026-06-11 KST: 이 설계 문서는 초기 구현 기준을 기록한다.
> 현재 `poster/poster.tex` production draft는 title block에서 subtitle을 삭제했고,
> `Key Question`은 `비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`로 바뀌었다.
> Figure numbering도 바뀌어 Figure 1은 reliability failure concept diagram,
> 기존 reliability scatter는 Figure 2, raw-to-L2 recovery는 Figure 3이다.
> 최신 source of truth는 `docs/research/poster_section_text.md`이다.

## 목적

현재 `poster/poster.tex` 초안은 최신 연구 계획과 맞지 않는다. 기존 초안은
`SGD / Adam / AdamW` 3행 평균 비교처럼 보이고, "optimizer만 바꾼
matched-accuracy comparison"으로 읽힐 수 있다. 최신 포스터는 seed0
WRN-28-10/CIFAR-10 LR-WD grid 결과를 바탕으로 논리 뼈대를 먼저 잡고,
selected 5 configs의 seed1/2 결과가 나오면 같은 구조에 3-seed
`mean +/- std`를 교체해 완성한다.

이 설계 문서는 구현 전에 포스터의 주장, evidence hierarchy, table/figure
역할, 언어 규칙, future work를 고정한다.

## 최종 방향

채택한 포스터 구조는 claim-first evidence poster다. 전통적인
`Problem -> Experiment -> Results -> Mechanism -> Limitations` 흐름보다
주장을 먼저 제시하고, 바로 아래에 증거와 메커니즘을 배치한다. 다만 실험
설계와 연구 한계는 작은 박스로 보강해 과장된 주장처럼 보이지 않게 한다.

최종 흐름:

1. Claim
2. Evidence 1: ID accuracy / calibration
3. Evidence 2: dataset-specific raw feature OOD reliability
4. Mechanism: raw-to-L2 detector recovery and feature geometry
5. Future Work

## 제목과 헤더

Title:

```text
Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability
```

Subtitle:

```text
None. The current production title block has no subtitle.
```

제목은 제출 초록의 "최적화 방법에 따른 표현기하 변화와 분포외 탐지기 성능
불일치에 관한 연구"와 대응한다. `Optimizer-Induced Feature Geometry`를
전면에 두되, 동사는 `Shapes`로 두어 `Changes`보다 인과 강도를 낮춘다.

## 언어 규칙

초안 단계에서는 논리 검토가 우선이므로 본문을 한국어로 작성한다. 최종 컨펌
후 영어 포스터 문체로 번역한다.

- Title: 영어
- Subtitle: 사용하지 않음
- Section headers: 영어
- Table / Figure titles: 영어
- 본문 해석: 한국어 초안
- 최종 제출본: 컨펌 후 영어로 번역

## 중심 주장

포스터의 핵심 문장:

```text
ID accuracy만으로는 calibration/OOD reliability를 보장하지 않는다.
```

더 구체적으로는 다음을 주장한다.

동일한 WRN-28-10/CIFAR-10 설정에서 비슷한 ID accuracy를 달성하더라도,
optimizer-induced feature geometry 차이 때문에 raw feature-based OOD
detector reliability가 크게 달라질 수 있다. 특히 raw Mahalanobis와 raw kNN은
feature norm 및 covariance-scale geometry에 민감하며, L2-normalized control은
이 차이를 해석하는 단서를 제공한다. Calibration 지표는 보조 신뢰성 지표로
함께 보고한다.

## Evidence hierarchy

포스터는 seed0과 3-seed 결과의 역할을 분리한다.

- seed0 full LR-WD grid: 현상 발견과 selected configs 선택 맥락
- selected 5 configs, 3 seeds: 최종 main quantitative evidence

현재 내부 검토용 초안은 seed0 실제 수치를 넣어 포스터 논리가 실제 수치 위에서
작동하는지 확인한다. 최종 포스터에서는 selected 5 configs의 seed0/1/2 집계
결과를 `mean +/- std`로 보고하고, figure에는 error bar를 추가한다.

## Selected configs

Main 5 configs는 다음으로 고정한다.

| Short label | Config label | 역할 |
|---|---|---|
| SGD anchor | `sgd_lr1e-1_wd5e-4_anchor` | 표준 WRN/SGD 기준점 |
| SGD val-best | `sgd_lr1e-1_wd2e-4` | SGD validation-best 근처 control |
| Adam reg. | `adam_lr1e-3_wd1e-4` | regularized Adam 대표 |
| AdamW val-best | `adamw_lr5e-3_wd1e-4` | AdamW validation-best 대표 |
| AdamW anchor | `adamw_lr5e-3_wd5e-4_anchor` | AdamW 내부 robustness check |

`adam_lr1e-3_wd0`은 seed0-only supplementary 또는 Q&A용 control로 남긴다.
seed1/2 반복 대상이 아니므로 main table에는 넣지 않는다.

## Layout

채택한 시각 구조는 "B. 주장 우선형"이다.

- 상단: 영어 title, no subtitle
- 큰 claim band: "ID accuracy alone does not guarantee reliable calibration or
  feature-based OOD detection."
- 왼쪽 좁은 열: experimental design, Table 1, Table 2
- 왼쪽 열: Figure 1 reliability failure concept diagram
- 오른쪽 넓은 열: Figure 2, Figure 3 empirical evidence
- 하단 또는 오른쪽 작은 박스: mechanism diagnostic, future work

이 구조는 강한 optimizer-induced 메시지를 먼저 보이고, 표는 방어 장치,
그림은 주 증거로 사용한다.

## Table design

### Table 1. ID and Calibration Summary

역할: selected 5 configs가 비슷한 ID performance band에 있음을 보여주고,
calibration은 보조 신뢰성 지표로 함께 보고한다.

Columns:

```text
Config
Optimizer
Val Acc
Test Acc
ECE
```

LR/WD column은 결과표에서 제외한다. LR/WD는 실험 설정 설명에서 grid search와
selected configs 맥락으로 설명한다.

### Table 2. Dataset-Specific Raw Mahalanobis AUROC

역할: OOD AUROC를 near/far 평균으로 섞지 않고 dataset별로 보여준다.

Columns:

```text
Config
Optimizer
CIFAR-100
TinyImageNet
SVHN
MNIST
```

Table 2는 raw Mahalanobis AUROC만 다룬다. raw kNN은 Figure 3에서
L2-normalized control과 함께 보여준다.

## Figure design

### Figure 1. Reliability Failure: Miscalibration and OOD Acceptance

역할: accuracy만으로 보이지 않는 두 reliability failure mode를 개념적으로 설명한다.

구성:

- left panel: confidence와 empirical accuracy가 어긋나는 miscalibration.
- right panel: OOD sample이 high ID-like score를 받아 정상 입력처럼 처리되는 OOD acceptance.
- metrics: ECE와 AUROC 정의를 함께 둔다.

### Figure 2. Accuracy-Matched Reliability Scatter

역할: 비슷한 ID validation accuracy 영역에서도 reliability metric이 갈라짐을
보여준다.

구성:

- x-axis: ID validation accuracy
- facet 1 y-axis: ECE
- facet 2 y-axis: raw Mahalanobis AUROC
- background: seed0 15-run LR-WD grid, pale points
- foreground: selected 5 configs, final version uses 3-seed mean +/- std and
  error bars

내부 검토용 초안에서는 seed0 실제 수치를 사용해 구조를 확인한다.

### Figure 3. Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity

역할: raw feature detector drop이 L2-normalized control에서 회복되는지를 보여
feature norm / covariance-scale geometry 해석으로 연결한다.

구성:

- x-axis: selected 5 configs
- short labels: `SGD-A`, `SGD-B`, `Adam`, `AdamW-B`, `AdamW-A`
- legend 또는 caption에서 full label을 설명한다.
- bars: raw Mahalanobis, Mahalanobis-L2, raw kNN, kNN-L2
- final version: 3-seed mean +/- std error bars

Full label mapping:

| Short label | Full label |
|---|---|
| `SGD-A` | SGD anchor |
| `SGD-B` | SGD validation-best control |
| `Adam` | regularized Adam representative |
| `AdamW-B` | AdamW validation-best representative |
| `AdamW-A` | AdamW anchor |

## Mechanism diagnostic

큰 geometry table은 두지 않는다. 대신 작은 mechanism box에서 raw-to-L2 recovery와
feature geometry를 연결한다.

포함할 내용은 3줄 구조로 압축한다.

1. Raw Mahalanobis/kNN depend on feature norms, distances, and covariance scale.
2. L2-normalized controls reduce feature-scale effects while preserving angular information.
3. Raw-to-L2 recovery suggests that optimizer-induced norm/covariance-scale geometry contributes to detector reliability gaps.

`causes` 같은 강한 인과 표현은 피하고, `suggests`, `is consistent with`,
`contributes to`를 사용한다. Covariance expansion은 조건부 메커니즘으로
해석하며, 모든 경우의 보편적 원인이라고 주장하지 않는다.

## Future Work

하단의 한계/다음 단계 박스는 짜잘한 evidence boundary가 아니라 연구 확장 방향을
보여준다.

순서:

1. Adam-AdamW interpolation으로 optimizer-induced geometry를 연속적으로 조정하고
   OOD reliability 변화를 분석
2. CIFAR-100 등 다양한 ID dataset과 ResNet/ViT 계열 architecture로 일반화 검증
3. SAM, Mixup 등 optimization/regularization/augmentation 방법이 feature norm,
   covariance-scale geometry, OOD reliability에 미치는 영향 분석

## Draft and final data policy

내부 검토용 초안:

- seed0 실제 수치를 넣는다.
- draft marker로 seed0 diagnostic grid 기반임을 표시한다.
- 최종 수치와 figure/table은 3-seed 결과로 교체할 것을 전제로 한다.
- dataset-specific seed0 raw Mahalanobis 값은
  `WRN seed0 350eps grid-search 실험_0531 371a26cf6e72819bacacd14427eb6614.md`의
  dataset별 Feature 표를 source로 사용한다. 이 파일에서 직접 확인되는
  dataset-specific 행은 `SGD best val`, `Adam wd=0 best val`,
  `Adam wd>0 best val`, `AdamW best val`이므로, 내부 검토용 Table 2는
  확인 가능한 row만 사용하거나 source coverage note를 단다.

최종 포스터:

- selected 5 configs의 seed0/1/2 `mean +/- std`를 main table에 사용한다.
- Empirical Figures 2/3에는 3-seed error bar를 추가한다.
- seed0 full grid는 Figure 2의 background evidence로 남긴다.

## Non-goals

이번 포스터 초안에서 하지 않을 것:

- optimizer 3개 평균 행만 놓는 단순 `SGD vs Adam vs AdamW` 표
- geometry full table
- `adam_lr1e-3_wd0`을 main table에 포함
- original DDU reproduction이라고 표기
- seed0-only 결과로 consistency claim 작성

## Acceptance criteria

포스터 초안은 다음을 만족해야 한다.

- Title은 확정 문구와 일치하고 title block subtitle은 없다.
- section headers와 figure/table title은 영어다.
- 본문 설명은 한국어 초안으로 읽힌다.
- Table 1은 ID/calibration summary만 담는다.
- Table 2는 dataset-specific raw Mahalanobis AUROC만 담는다.
- Figure 1은 miscalibration/OOD acceptance concept diagram이다.
- Figure 2는 ID validation accuracy 대비 ECE/raw Mahalanobis AUROC 구조다.
- Figure 3은 `Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity` 제목과
  `SGD-A`, `SGD-B`, `Adam`, `AdamW-B`, `AdamW-A` short labels를 사용한다.
- selected 5 configs의 역할이 포스터 안에서 드러난다.
- Future Work는 Adam-AdamW interpolation, dataset/architecture expansion,
  SAM/Mixup 확장 순서로 제시된다.
