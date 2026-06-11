# Poster Section Text Source

작성일: 2026-06-11 KST  
상태: 포스터 본문 원고 기준 문서

## 0. Purpose

이 문서는 `poster/poster.tex`에 들어갈 **본문 서술의 source of truth**이다.
디자인, 배치, TeX macro, figure 크기는 이 문서의 목적이 아니다. 이 문서는
각 section이 어떤 논리적 역할을 해야 하는지와 실제 포스터에 넣을 문장을 먼저
고정하기 위해 사용한다.

향후 `poster/poster.tex`의 본문 문장을 수정할 때는 먼저 이 문서를 읽고,
여기 있는 section별 서술을 압축하거나 배치한다. TeX 편집 중 새 claim이나 새
해석을 즉흥적으로 만들지 않는다. 문장을 바꿔야 하면 이 문서를 먼저 수정하고
그 다음 `poster/poster.tex`에 반영한다.

## 1. Global Writing Rules

### 1.1 Language Rule

- Title, section headings, table titles, figure titles는 영어로 둔다.
- 현재 production draft의 title block에는 subtitle을 두지 않는다.
- 본문 설명은 한국어 초안으로 작성한다.
- 영어 technical term은 필요하면 그대로 둔다: `calibration`, `OOD detection`,
  `post-hoc`, `feature geometry`, `Mahalanobis`, `kNN`, `L2-normalized control`.
- 최종 영어 포스터로 바꿀 때도 이 문서의 논리 순서를 유지한다.

### 1.2 Evidence Constraints

현재 포스터의 수치는 seed0 diagnostic draft이다. 따라서 본문은 반드시 다음
경계를 유지한다.

- `seed0`, `diagnostic`, `draft`, `preliminary`, `suggests`,
  `is consistent with`, `may contribute to`를 사용한다.
- `proves`, `demonstrates`, `consistently`, `always`, `causes`처럼
  seed 반복 전에는 강한 표현을 쓰지 않는다.
- OOD와 geometry metric은 hyperparameter selection에 쓰지 않았고,
  post-hoc diagnostics로만 쓴다.
- 최종 3-seed 결과가 들어오면 selected 5 configs의 `mean +/- std`로
  table과 figure를 교체한다.
- `DDU`는 원 논문 전체 recipe 재현이 아니라 `DDU-style GMM feature density`로
  표기한다.

### 1.3 Main Message

포스터 전체의 중심 문장은 다음이다.

```text
ID accuracy alone does not guarantee reliable calibration or feature-based OOD detection.
```

한국어 논리:

```text
비슷한 ID accuracy를 달성한 모델이라도, optimizer/LR/weight decay가 만든
feature norm과 covariance-scale geometry 차이 때문에 calibration과 post-hoc
feature OOD detector reliability가 다르게 나타날 수 있다.
```

### 1.4 What This Poster Should Not Say

다음 표현은 피한다.

- `SGD, Adam, AdamW have the same accuracy but different OOD reliability.`
- `AdamW feature OOD fails.`
- `Neural Collapse weakening alone causes Mahalanobis collapse.`
- `Weight decay reduction solves Mahalanobis collapse.`
- `kNN is free from feature norm effects.`
- `Mahalanobis-L2 is a full reproduction of Mahalanobis++.`
- `Seed0 proves optimizer effects are consistent.`

## 2. Fixed Header Text

### Title

```text
Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability
```

### Subtitle

현재 production draft에서는 subtitle을 삭제한다.

### Author Line

```text
GunHak Jin ∙ HyeYoung Jung
Department of Mathematical Data Science, Hanyang University
```

### Header Design Notes

- Title font: Copperplate Gothic Bold, 50pt.
- Author font: Calibri, 28pt.
- Affiliation font: Calibri, 20pt.
- Hangul body draft: Pretendard.
- Math: Cambria Math.
- Upper-right logos: Hanyang University and Korean Statistical Society.

## 3. Section Text

### Layout Intent

왼쪽 열은 문제 정의에서 실험 설계까지 독자가 따라갈 수 있는 개념 흐름으로 둔다.
오른쪽 열은 결과와 해석 중심으로 구성한다. 포스터 하단에는 별도의
2열 spanning 결론 섹션을 두지 않는다. 결론과 한계는
`Mechanism Diagnostic and Poster Conclusion` 및 `Future Work` 안에 흡수한다.

## 3.1 Abstract

### Role

포스터의 첫 15초를 책임진다. 문제, 방법, 발견을 각각 한 문장으로 제시한다.
추상적인 AI safety 서론이 아니라 이 포스터가 실제로 무엇을 검증하는지 바로
보여준다.

### Reader Question

`이 포스터가 무슨 문제를, 어떤 실험으로, 어떤 예비 결과로 말하려는가?`

### Poster Text

```text
ID accuracy는 정답률을 요약하지만, confidence calibration과 distribution-shift
robustness를 보장하지 않는다. 우리는 CIFAR-10 WRN-28-10을 SGD, Adam, AdamW와
LR–weight decay grid로 학습하고, ID validation accuracy만으로 선택한 후보들의
calibration, post-hoc OOD detection, feature geometry를 진단한다. Seed0 diagnostic
draft는 비슷한 accuracy band 안에서도 raw feature OOD reliability가 갈라질 수
있으며, L2-normalized controls가 그 차이를 feature norm/covariance-scale geometry와
연결해 볼 수 있음을 시사한다.
```

### Ultra-Short Version

```text
높은 ID accuracy는 calibration이나 post-hoc OOD reliability를 보장하지 않는다.
CIFAR-10 WRN-28-10 seed0 diagnostic evidence에서 accuracy band 안에서도 raw
feature OOD AUROC가 크게 갈라지고, L2 control recovery는 feature norm/covariance-scale
geometry 해석과 일관된다.
```

## 3.2 Introduction: Why Accuracy Is Not Reliability

### Role

포스터의 문제 제기를 만든다. `accuracy = correctness summary`이고,
`reliability = confidence + distribution-shift behavior`라는 구분을 독자에게
먼저 심어준다.

### Reader Question

`왜 accuracy가 높으면 충분하다고 말할 수 없는가?`

### Poster Text

```text
ID accuracy는 모델이 test distribution에서 정답을 얼마나 자주 맞히는지를 요약한다.
그러나 실제 배포 환경에서 reliability는 정답률만으로 끝나지 않는다. 모델의
confidence가 믿을 만한지, 그리고 distribution-shift input을 정상 입력처럼
받아들이지 않는지까지 함께 확인해야 한다.

이 포스터의 질문은 한 단계 더 나아간다. 비슷한 ID accuracy를 달성한 모델이라도,
optimizer와 LR–weight decay 선택이 penultimate feature geometry를 다르게 만들면
post-hoc detector가 보는 score landscape도 달라질 수 있다. 따라서 우리는 optimizer를
단순한 training speed 선택이 아니라, calibration과 feature-based OOD reliability를
바꿀 수 있는 실험 요인으로 다룬다.
```

### Key Question

```text
비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을
미치는가?
```

### Ultra-Short Version

```text
Accuracy는 정답률의 요약이다. 배포 reliability는 confidence가 실제 정답률과 맞는지,
그리고 distribution shift에서 OOD input을 정상 입력처럼 받아들이지 않는지까지 포함한다.
```

## 3.3 Reliability Failure: Miscalibration and OOD Acceptance

### Role

Calibration과 OOD detection을 하나의 reliability failure 섹션으로 묶는다.
독자가 `confidence mismatch`와 `OOD acceptance`를 accuracy 표로는 보이지 않는
두 실패 축으로 이해하게 한다.

### Reader Question

`Miscalibration과 OOD acceptance는 실제 배포에서 어떤 문제를 만드는가?`

### Poster Text

```text
Accuracy는 "얼마나 자주 맞혔는가"를 말하지만, reliability는 "모델이 자기 판단을
얼마나 믿을 만하게 표현하는가"까지 묻는다. 각 예측에서 confidence는 보통 모델이
선택한 class의 softmax probability로 정의된다. 반면 actual accuracy는 한 샘플의
값이 아니라, 비슷한 confidence를 받은 샘플 묶음에서 실제로 정답이었던 비율이다.

예를 들어 confidence 90%인 예측들이 100개 있다면, 잘 보정된 모델에서는 그중 약
90개가 맞아야 한다. 이때 confidence와 actual accuracy가 크게 다르면 miscalibration이다.
Overconfident model은 틀릴 때도 높은 confidence를 줄 수 있으므로, "confidence가
높으면 자동 승인하고 낮으면 보류한다" 같은 threshold decision을 불안정하게 만든다.

OOD detection은 모델이 학습 분포 밖 입력을 정상 입력처럼 받아들이지 않게 하는 장치다.
Post-hoc OOD detector는 score s(x)를 이용해 ID sample에는 높은 ID-like score를,
OOD sample에는 낮은 score를 주어야 한다. OOD sample이 ID처럼 높은 score를 받으면,
모델은 지원하지 않는 입력에도 정상 class 예측을 내리고 downstream decision으로 넘길
수 있다.

따라서 신뢰성 실패는 두 축에서 나타난다. Miscalibration은 confidence의 숫자를 믿기
어렵게 만들고, OOD acceptance는 분포 밖 입력을 정상 입력처럼 처리하게 만든다. 이
포스터에서는 ECE로 confidence mismatch를, AUROC로 ID/OOD score ranking 품질을 요약한다.
```

### Figure 1 Caption

```text
Figure 1. Left: confidence no longer matches empirical accuracy, destabilizing
threshold decisions. Right: an OOD input receives a high ID-like score and can
be passed downstream as if it were ID.
```

### Formula

```tex
\mathrm{acc}(B)=\frac{1}{|B|}\sum_{i\in B}\mathbf{1}(\hat y_i=y_i),\qquad
\mathrm{conf}(B)=\frac{1}{|B|}\sum_{i\in B}\max_k p_i(k)
```

```tex
\mathrm{ECE}=\sum_b \frac{|B_b|}{n}\,
|\mathrm{acc}(B_b)-\mathrm{conf}(B_b)|,\qquad
\mathrm{AUROC}=P(s(x_{\mathrm{ID}})>s(x_{\mathrm{OOD}}))
```

### Diagram Requirement

- `figures/final/fig1_reliability_failure_concept.png`를 Figure 1로 사용한다.
- 왼쪽 패널은 confidence와 empirical accuracy가 어긋나는 miscalibration failure를
  보여준다.
- 오른쪽 패널은 OOD sample이 ID feature region에서 high ID-like score를 받는 OOD
  acceptance failure를 보여준다.

### Ultra-Short Version

```text
Miscalibration은 confidence의 숫자를 믿기 어렵게 만들고, OOD acceptance는 분포 밖
입력을 정상 입력처럼 처리하게 만든다. ECE는 confidence mismatch를, AUROC는 ID/OOD
score ranking 품질을 요약한다.
```

## 3.4 Optimizers: Update Rules and Feature Distributions

### Role

SGD, Adam, AdamW가 단순 이름 차이가 아니라 update rule 차이라는 점을 보여준다.
통계학회 포스터에서는 이를 Neural Collapse 용어 자체보다, 마지막 표현층의
class-conditional feature distribution이 달라지는 문제로 설명한다. 논문 수식의 핵심인
last-layer row-sum statistic은 유지하되, 해석은 class mean, within-class dispersion,
covariance scale/anisotropy, between-class separation으로 연결한다.

### Reader Question

`왜 optimizer가 마지막 표현층 feature distribution과 post-hoc detector reliability에 연결될 수 있는가?`

### Poster Text

```text
마지막 표현을 `H=h_theta(X)`로 두면, 각 class는 표현층에서 하나의 조건부분포
`H | Y=k`를 만든다. 이 분포는 class mean `mu_k`, covariance `Sigma_k`,
within-class dispersion, between-class separation으로 요약할 수 있다. Mahalanobis,
kNN, DDU-style GMM 같은 post-hoc feature detector는 바로 이 분포의 위치와
공분산 구조를 본다.

Optimizer가 이 분포를 바꿀 수 있는 이유는 마지막 classifier `W`와 feature `H`가
cross-entropy 학습 중 함께 움직이기 때문이다. 마지막 logit layer를
`z = W h_theta(x)`로 쓰고, classifier row-sum statistic을
`a_t = K^{-1} ||W_t^T 1_K||_2^2`로 둔다. Cross-entropy에서는 마지막층 gradient의
row-sum이 0이다: `(nabla_W L_CE)^T 1_K = 0`. 따라서 이 statistic의 변화는 loss
gradient 자체보다 weight decay가 update 안에서 어떻게 작용하는지에 크게 좌우된다.

SGD/L2에서는 `W_{t+1}=W_t-eta(nabla L + lambda W_t)`이고, row-sum을 취하면
`s_{t+1}=(1-eta lambda)s_t`가 된다. 즉
`a_{t+1} approx (1-eta lambda)^2 a_t`이므로 class 방향의 centering statistic이 0쪽으로
수축한다. 반면 Adam/L2와 AdamW에서는 같은 `lambda W_t` 항이 adaptive scaling 안에
들어가느냐, 밖에서 별도 shrinkage로만 작용하느냐가 다르다. 이 차이는 classifier-feature
alignment와 함께 `H | Y=k`의 mean separation, covariance scale, anisotropy를 다르게
만들 수 있다.

따라서 optimizer/LR/WD는 비슷한 ID accuracy에 도달하더라도 마지막 표현층의
class-conditional feature distribution을 다르게 만들 수 있다. 이 mechanism은
optimizer-induced feature distribution shift를 설명하고, OOD reliability와의 연결은
우리 post-hoc diagnostics로 평가한다.
```

### Formulas

```tex
H=h_\theta(X),\qquad
H\mid Y=k:\quad
\mu_k=\mathbb{E}[H\mid Y=k],\quad
\Sigma_k=\mathrm{Var}(H\mid Y=k)
```

```tex
z=W h_\theta(x),\qquad
s_t=W_t^\top \mathbf{1}_K,\qquad
a_t=\frac{1}{K}\|s_t\|_2^2,\qquad
(\nabla_W L_{\mathrm{CE}})^\top\mathbf{1}_K=0
```

```tex
\text{SGD/L2:}\quad
W_{t+1}=W_t-\eta(\nabla_W L+\lambda W_t)
\Rightarrow
s_{t+1}=(1-\eta\lambda)s_t
\Rightarrow
a_{t+1}\approx(1-\eta\lambda)^2a_t
```

```tex
\text{Adam/L2:}\quad W_{t+1}=W_t-\eta D_t(\nabla_W L+\lambda W_t)
```

```tex
\text{AdamW:}\quad W_{t+1}=(1-\eta\lambda)W_t-\eta D_t\nabla_W L
```

### Ultra-Short Version

```text
마지막 표현층의 `H | Y=k` 분포는 class mean, within-class dispersion, covariance
scale/anisotropy, between-class separation으로 요약된다. Cross-entropy 마지막층
gradient의 row-sum은 0이므로, classifier centering statistic은 weight-decay coupling에
크게 좌우된다. 이 차이가 classifier-feature alignment와 class-conditional feature
distribution을 다르게 만들 수 있다.
```

### Diagram Requirement

- 별도 Figure 번호를 붙이지 않고, Optimizer 섹션 내부에 작은 `Mechanism sketch`로 넣는다.
- 도식은 `feature distribution view`를 상단에 두고, 이어서 `CE zero row-sum`과
  `SGD/L2 contraction`, `Adam/L2 vs AdamW coupling split`을 보여준다.
- 새 도식은 optimizer -> feature distribution shift mechanism만 설명한다. OOD detector
  성능 저하의 직접 증거처럼 보이지 않도록 caption 또는 boundary 문장을 함께 둔다.

## 3.5 Experiment

### Role

실험 경계와 selection rule을 고정한다. OOD metric으로 hyperparameter를 고른 것이
아니라는 점을 분명히 한다.

### Reader Question

`결과가 cherry-picking이 아니라 ID-validation-only selection 위에서 나온 것인가?`

### Poster Text

```text
우리는 ID validation 성능만으로 선택한 모델들이 reliability metric에서도 같은 경향을
보이는지 확인한다. 모든 모델은 CIFAR-10에서 WRN-28-10을 사용해 동일한 학습 protocol로
학습한다. 실험 요인은 SGD, Adam, AdamW에 대한 optimizer별 LR-weight decay grid이다.

후보 모델은 ID validation accuracy만으로 선택한다. OOD detection score와 feature
geometry metric은 hyperparameter selection에 사용하지 않고, 선택 이후의 post-hoc
diagnostic으로만 평가한다.

각 선택 모델에 대해 ID accuracy와 calibration, CIFAR-100, TinyImageNet, SVHN, MNIST에
대한 post-hoc OOD detection, 그리고 penultimate feature geometry를 함께 보고한다.
Feature-based detector는 동일한 feature layer에서 평가하며, 모든 OOD score는 높을수록
ID-like하도록 맞춘다.
```

### Fixed Experimental Facts

| Item | Value |
|---|---|
| ID dataset | CIFAR-10 |
| Architecture | WRN-28-10 |
| Epochs | 350 |
| Optimizers | SGD, Adam, AdamW |
| Grid | LR x weight decay |
| Selection | ID validation accuracy only |
| OOD datasets | CIFAR-100, TinyImageNet, SVHN, MNIST |
| Feature layer | penultimate feature |
| Current status | seed0 diagnostic draft |
| Final target | selected 5 configs, seed0/1/2 mean +/- std |

### Ultra-Short Version

```text
Hyperparameters are selected by ID validation accuracy only. OOD, calibration,
and geometry metrics are post-hoc diagnostics. Current poster values are seed0
diagnostic draft values.
```

## 3.6 Figure 2: Accuracy-Matched Reliability Split

### Role

Figure 2를 오른쪽 열의 main result로 둔다. ID validation accuracy가 비슷한 후보들이
reliability metric에서는 같은 순서로 정렬되지 않음을 보여준다.

### Caption Text

```text
Seed0 diagnostic draft: ECE and raw Mahalanobis AUROC against ID validation
accuracy. Calibration mismatch and raw feature OOD reliability can split within a
similar ID accuracy band.
```

### Interpretation Text

```text
Figure 2는 ID validation accuracy가 비슷한 후보들이 reliability metric에서는 같은 순서로
정렬되지 않음을 보여준다. 즉, ID accuracy는 필요한 selection criterion이지만
calibration과 feature-based OOD reliability를 대체하지 못한다.

Seed0 diagnostic draft에서 Adam/AdamW 후보는 competitive ID accuracy band에 들어오지만,
ECE와 raw Mahalanobis AUROC는 SGD 후보와 다른 profile을 보인다. 이는 accuracy-matched
regime에서도 reliability axis가 분리될 수 있음을 시사한다.

이 그림의 역할은 "accuracy가 완전히 무너진 모델"을 비교하는 것이 아니다. 비슷한 ID
accuracy band 안에서도 calibration mismatch와 raw feature OOD reliability가 분리될 수
있다는 점을 먼저 고정하는 것이다.
```

### Ultra-Short Version

```text
ID validation accuracy가 비슷해도 ECE와 raw Mahalanobis AUROC는 같은 순서로 정렬되지
않을 수 있다. Accuracy는 필요한 selection criterion이지만 reliability를 대체하지 못한다.
```

## 3.7 Table 1: Dataset-Specific Raw Mahalanobis AUROC

### Role

평균값 하나로 숨기지 않고, raw Mahalanobis AUROC가 OOD dataset별로 어떻게 달라지는지
보여준다. 현재 source에서 직접 확인되는 representative rows가 4개뿐이라는 coverage note를
반드시 보존한다.

### Required Columns

```text
Config, Optimizer, CIFAR-100, TinyImageNet, SVHN, MNIST
```

### Caption Text

```text
Dataset-specific raw Mahalanobis AUROC for four confirmed seed0 representative
rows. Higher is better. Current table is a seed0 diagnostic draft and will be
replaced by repeated-seed summaries.
```

### Interpretation Text

```text
Table 1은 raw Mahalanobis AUROC가 OOD dataset별로 어떻게 달라지는지 보여준다. 낮은 raw
Mahalanobis AUROC는 ID feature와 OOD feature를 score ranking으로 충분히 구분하지 못한다는
뜻이다.

Dataset-specific raw Mahalanobis AUROC는 optimizer/LR/WD config에 따라 크게 달라진다.
예를 들어 seed0 draft에서 SGD 대표 row는 CIFAR-100/TinyImageNet/SVHN/MNIST 전반에서
높은 raw Mahalanobis AUROC를 보이지만, Adam/AdamW 대표 row는 dataset별로 큰 drop을
보인다. 이는 feature-based detector가 ID accuracy와 같은 순서로 정렬되지 않을 수 있음을
보여주는 preliminary signal이다.

현재 표는 source에서 직접 확인되는 4개 representative rows만 사용한다. 따라서 이 표는
seed0 diagnostic evidence이며, 최종본에서는 selected configs의 repeated-seed mean +/- std로
교체한다. 이 표만으로 optimizer별 일관성이나 seed-averaged superiority를 주장하지 않는다.
```

## 3.8 Table 2: Geometry Summary

### Role

Reliability split이 단순한 accuracy 차이만으로 설명되지 않음을 보이기 위한 geometry
diagnostic이다. Table 2는 `raw Mahalanobis가 낮다`에서 끝나지 않고, 그 차이가
penultimate feature geometry와 연결될 수 있다는 해석으로 넘어가는 다리 역할을 한다.

### Required Columns

```text
Config, Optimizer, Val/Test Acc, ECE, Raw Maha, NC1, InterDist, Feature norm / covariance diagnostic
```

### Metric Boundary

- 포스터 표에는 geometry metric을 과하게 넣지 않는다.
- 기본 축은 `NC1`, `InterDist`, `feature norm / covariance diagnostic`으로 제한한다.
- `NC3`, `effective rank`, `condition number`는 값이 확실하고 공간이 허용될 때만
  마지막 diagnostic column 또는 Q&A 보조 자료로 사용한다.
- 수치가 확정되지 않은 norm/covariance metric은 포스터 제작 시 `TBD`로 남기지 않고,
  확인된 값만 넣거나 qualitative diagnostic으로 축약한다.

### Caption Text

```text
Geometry diagnostics for selected accuracy-matched configs. Lower NC1 and larger
InterDist generally indicate more compact and separated class geometry. Additional
norm/covariance diagnostics are included when confirmed.
```

### Interpretation Text

```text
Table 2는 ID accuracy가 비슷하더라도 optimizer/LR/weight decay 조합이 만든 penultimate
feature geometry가 다를 수 있음을 보여주는 diagnostic table이다.

특히 NC1이 커지면 class 내부 feature spread가 class 간 separation에 비해 커졌다는 뜻으로
해석할 수 있고, InterDist가 작아지면 class mean separation이 약해졌다는 뜻으로 해석할
수 있다. 이런 geometry 변화는 Mahalanobis나 kNN처럼 feature distance와 covariance scale에
의존하는 post-hoc detector의 score landscape를 바꿀 수 있다.

이 표는 geometry 하나로 detector gap을 증명하기 위한 표가 아니다. Figure 2의 reliability
split과 Figure 3의 raw-to-L2 recovery를 연결해, feature norm/covariance-scale geometry를
함께 보고해야 한다는 diagnostic 근거를 제공한다.
```

## 3.9 Figure 3: Raw-to-L2 Recovery

### Required Title

```text
Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity
```

### Required X-Axis Short Labels

```text
SGD-A, SGD-B, Adam, AdamW-B, AdamW-A
```

### Role

Table 2 다음에 배치한다. Table 2가 `geometry가 다르다`를 보여주고, Figure 3은
feature scale effect를 줄이면 raw detector drop이 회복되는지를 보여준다.

### Caption Text

```text
Raw-to-L2 recovery suggests norm/covariance-scale sensitivity. L2-normalized
controls reduce feature-scale effects while preserving angular information.
```

### Interpretation Text

```text
Figure 3은 raw Mahalanobis와 raw kNN의 drop이 L2-normalized control에서 얼마나 회복되는지
보여준다. L2 normalization은 feature norm scale을 줄이면서 angular information을 보존하는
post-hoc control이다.

Raw Mahalanobis와 raw kNN은 feature norm, distance, covariance scale에 직접 의존한다.
따라서 Adam/AdamW representative에서 raw detector가 낮고 L2-normalized detector가 회복되는
seed0 pattern은, raw feature OOD reliability gap이 optimizer-induced feature
norm/covariance-scale geometry와 연결될 수 있다는 해석과 일관된다.

이 결과는 "특정 optimizer가 무조건 나쁘다"가 아니라, "optimizer가 만든 geometry와
detector가 의존하는 geometry가 맞지 않을 수 있다"는 메시지로 읽어야 한다. 또한
L2 normalization이 최종 해법이라는 주장이 아니라, raw detector drop이 feature scale
sensitivity와 연결될 수 있음을 보여주는 diagnostic control이다.
```

## 3.10 Mechanism Diagnostic and Poster Conclusion

### Role

결과 해석을 단순한 `AdamW가 나쁘다`가 아니라, detector-side sensitivity와
feature geometry의 상호작용으로 정리한다. 별도의 spanning takeaway 섹션 없이
포스터의 결론도 이 섹션에서 마무리한다.

### Poster Text

```text
핵심 해석은 "optimizer가 accuracy를 낮췄다"가 아니다. Seed0 diagnostic draft는 비슷한
ID accuracy band 안에서도 calibration과 raw feature OOD reliability가 분리될 수 있고,
이 차이가 penultimate feature norm/covariance-scale geometry와 연결될 수 있음을 시사한다.

Post-hoc feature detectors do not see the optimizer directly. They see the feature
space produced by training. Raw Mahalanobis uses class means and covariance-based
distance; raw kNN uses neighborhood distance. Both scores can change when feature
norms, class separation, covariance anisotropy, or effective rank change.

Raw Mahalanobis와 raw kNN은 feature norm, distance, covariance scale에 민감하다. 따라서
post-hoc feature detector를 사용하는 reliability evaluation에서는 ID accuracy와 함께
feature geometry diagnostic을 함께 보고해야 한다.

Accuracy is necessary but not sufficient. In this seed0 diagnostic draft,
ID-validation-matched models can show different calibration, raw feature OOD
reliability, and feature geometry profiles. This suggests that optimizer/LR/WD
choices should be evaluated not only by ID accuracy, but also by the geometry seen
by downstream post-hoc detectors.
```

### Ultra-Short Version

```text
Accuracy is necessary but not sufficient. Seed0 diagnostic evidence suggests that
ID-validation-matched models can show different calibration, raw feature OOD
reliability, and feature geometry profiles. This is a diagnostic signal, not a
causal proof or seed-averaged conclusion.
```

## 3.11 Future Work

### Required Order

1. Adam-AdamW interpolation
2. dataset / architecture expansion
3. SAM, Mixup 등 다른 training methods 확장

### Poster Text

```text
1. Adam-AdamW interpolation: coupled weight decay와 decoupled weight decay 사이를
연속적으로 조절해, adaptive update와 norm shrinkage가 feature geometry와 OOD reliability를
어떻게 바꾸는지 더 직접적으로 확인한다.

2. Dataset / architecture expansion: CIFAR-10 WRN-28-10에서 보인 seed0 diagnostic pattern이
다른 ID dataset과 architecture에서도 유지되는지 확인한다.

3. SAM, Mixup 등 다른 training methods 확장: optimizer뿐 아니라 training method 선택도
feature norm, covariance scale, post-hoc OOD detector reliability를 바꾸는지 평가한다.
```

### Expanded Meaning For Q&A

```text
Adam-AdamW interpolation은 coupled/decoupled weight decay의 효과를 연속적으로
조정해 feature geometry와 OOD reliability의 변화를 더 직접적으로 확인하기 위한
후속 실험이다.

Dataset / architecture expansion은 CIFAR-10 WRN-28-10에서 관찰한 패턴이 다른
ID dataset과 architecture에서도 유지되는지 확인하기 위한 일반화 실험이다.

SAM, Mixup 등 다른 training methods 확장은 optimizer 이외의 training choice도
feature norm, covariance scale, post-hoc OOD detector reliability를 바꿀 수 있는지
확인하기 위한 확장이다.
```

## 3.12 Poster-Ready Compact Text

현재 `poster/poster.tex`는 아래의 압축 원고를 우선 사용한다. 목적은 논문식
문단을 그대로 넣는 것이 아니라, A0 포스터에서 10초 안에 논리 구조가 보이게
하는 것이다. 각 섹션은 `Claim / Evidence / Boundary / Implication` 중 필요한
라벨만 사용한다.

### Abstract

```text
Problem: 높은 ID accuracy는 정답률만 요약한다. Calibration과 post-hoc OOD
reliability는 별도 진단이 필요하다.

Method: CIFAR-10 WRN-28-10을 SGD/Adam/AdamW LR-WD grid로 학습하고, ID validation
accuracy만으로 후보를 선택했다.

Finding: Seed0 draft에서 accuracy band 안에서도 ECE와 raw Mahalanobis AUROC가
갈라지고, L2 control recovery는 norm/covariance-scale sensitivity 해석과 일관된다.
```

### Introduction

```text
Claim: Accuracy is necessary, not reliability.

Evidence:
- ID accuracy는 test distribution에서의 correctness summary이다.
- Reliability는 calibrated confidence와 OOD input rejection까지 포함한다.
- Optimizer/LR/WD가 penultimate geometry를 바꾸면 post-hoc detector의 score
  landscape도 달라질 수 있다.

Key Question: 비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에
어떤 영향을 미치는가?
```

### Reliability Failure

```text
Claim: 신뢰성 실패는 높은 confidence를 믿고 넘기거나 OOD 입력을 정상 입력처럼 넘기는
순간 downstream decision을 흔든다.

Miscalibration: Confidence와 actual accuracy가 크게 다르면 confidence-threshold 기반
승인/보류 결정이 불안정해진다.

OOD acceptance: OOD sample이 높은 ID-like score를 받으면, 지원하지 않는 입력도 정상
class prediction으로 downstream decision에 넘어갈 수 있다.

Metrics: ECE는 confidence mismatch를, AUROC는 ID/OOD score ranking 품질을 요약한다.

Figure 1: Left panel은 miscalibration, right panel은 OOD acceptance를 보여준다.
```

### Optimizers

```text
Claim: Update rule 차이는 마지막 표현층의 class-conditional feature distribution을 바꿀 수 있다.

Mechanism sketch:
- H | Y=k has mean mu_k and covariance Sigma_k.
- z = W h_theta(x), s_t = W_t^T 1_K, a_t = K^{-1} ||s_t||^2.
- CE fact: (nabla_W L_CE)^T 1_K = 0.
- SGD/L2: s_{t+1} = (1 - eta lambda) s_t, so the classifier centering statistic contracts.
- Adam/L2 vs AdamW: lambda W is either inside adaptive scaling or outside as
  decoupled shrinkage, changing the feature distribution trajectory.

Implication: Accuracy가 비슷해도 class mean separation, within-class dispersion,
covariance scale/anisotropy, classifier-feature alignment가 달라질 수 있다.

Boundary: OOD reliability link is evaluated by our post-hoc diagnostics.
```

### Experiment

```text
Claim: Selection uses ID validation accuracy only.

Setup:
- ID / model: CIFAR-10 / WRN-28-10
- Train factors: SGD, Adam, AdamW x LR-WD grid
- Selection: ID validation accuracy only
- Post-hoc diagnostics: ECE, OOD AUROC, NC1, InterDist
- OOD datasets: CIFAR-100, TinyImageNet, SVHN, MNIST
- Status: seed0 diagnostic draft
```

### Figure 2

```text
Read: Similar ID validation accuracy does not imply similar reliability.

Evidence: Seed0 candidates in a competitive accuracy band split in ECE and raw
Mahalanobis AUROC.

Boundary: Diagnostic draft; repeated-seed summaries will replace this view.
```

### Table 1

```text
Read: Raw Mahalanobis AUROC differs by OOD dataset and config.

Evidence: Confirmed seed0 representative rows show large dataset-specific drops
for Adam/AdamW rows relative to SGD-B.

Boundary: The table uses four directly confirmed representative rows only. It
does not establish seed-averaged optimizer ranking.
```

### Table 2

```text
Read: Reliability split is accompanied by different penultimate geometry.

Evidence: Higher NC1 indicates larger within-class spread relative to separation;
smaller InterDist indicates weaker class-mean separation.

Implication: Distance/covariance-based post-hoc detectors can see a different
score landscape even when ID accuracy is similar.
```

### Figure 3

```text
Read: Raw-to-L2 recovery suggests norm/scale sensitivity.

Evidence: L2-normalized controls reduce feature-scale effects while preserving
angular information.

Boundary: This is a diagnostic control, not a claim that L2 normalization is the
final detector solution.
```

### Mechanism and Conclusion

```text
Claim: Detector reliability depends on the geometry it sees, not the optimizer
name directly.

Mechanism: Raw Mahalanobis uses class means and covariance-based distance; raw
kNN uses neighborhood distance. Both can change with feature norms, class
separation, covariance anisotropy, and effective rank.

Conclusion: Accuracy is necessary but not sufficient. ID-validation-matched
models can show different calibration, raw feature OOD reliability, and feature
geometry profiles. This remains seed0 diagnostic evidence.
```

### Future Work

```text
- Adam-AdamW interpolation: coupled/decoupled weight decay 비율을 연속적으로 조정한다.
- Dataset / architecture expansion: CIFAR-10 WRN-28-10 밖에서도 패턴을 확인한다.
- Other training methods: SAM, Mixup 등이 feature norm/covariance scale과 detector
  reliability를 바꾸는지 확장한다.
```

## 4. TeX Editing Rule

`poster/poster.tex`를 수정할 때는 다음 순서를 따른다.

1. 이 문서에서 수정할 section의 `Poster Text`, `Caption Text`,
   `Interpretation Text`, `Ultra-Short Version`을 먼저 읽는다.
2. 포스터 공간이 충분하면 `Poster Text`를 사용한다.
3. 공간이 부족하면 `Ultra-Short Version`을 사용하되 evidence constraints는 약화하지 않는다.
4. TeX 안에서 새로운 scientific claim을 만들지 않는다.
5. 새 claim이 필요하면 이 문서를 먼저 수정하고, 관련 research/evidence 문서와 대조한다.
6. 수치가 들어가는 문장은 CSV와 provenance manifest를 확인한 뒤 반영한다.

## 5. Source Documents To Check Before Changing Claims

- `docs/research/통계학회_포스터_실험계획.md`
- `docs/research/추가실험_승인_컨텍스트.md`
- `docs/research/학습후_평가_집계_가이드.md`
- `data/manifests/seed0_poster_draft_sources_20260611.md`
- `WRN seed0 350eps grid-search 실험_0531 371a26cf6e72819bacacd14427eb6614.md`
