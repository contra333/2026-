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

현재 포스터의 수치는 selected 5 configs의 seed0/1/2 mean +/- sample std이다.
따라서 본문은 반드시 다음 경계를 유지한다.

- `post-hoc diagnostic evidence`, `is associated with`, `can differ`,
  `is consistent with`처럼 bounded claim을 사용한다.
- `proves`, `always`, `causes`처럼 causal proof 또는 보편 명제로 읽히는
  강한 표현은 쓰지 않는다.
- OOD와 geometry metric은 hyperparameter selection에 쓰지 않았고,
  post-hoc diagnostics로만 쓴다.
- OOD dataset 간 평균은 포스터 본문 figure에 만들지 않고, CIFAR-100과
  TinyImageNet을 별도 패널로 보여준다.
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
실제 배포환경에서 신뢰성은 단순한 정답률이 아니라 confidence가 실제 정답 가능성과
맞는지, 그리고 학습 분포 밖 입력을 안전하게 거절할 수 있는지까지 포함한다.
그러나 높은 ID test accuracy는 calibrated confidence나 OOD rejection을 보장하지
않는다. 본 포스터는 optimizer가 마지막 표현층의 class-conditional feature
distribution을 어떻게 바꾸고, Mahalanobis/kNN/GMM 같은 feature-based detector가
그 분포를 읽으면서 OOD score ranking이 어떻게 달라질 수 있는지 진단한다.
결과적으로 validation-selected high-accuracy model이라도 optimizer/config 선택에
따라 calibration과 feature-based OOD reliability가 달라질 수 있으므로, 배포 전에는
accuracy와 함께 feature distribution-based diagnostics를 확인해야 한다.
```

### Ultra-Short Version

```text
높은 ID accuracy는 calibration이나 post-hoc OOD reliability를 보장하지 않는다.
CIFAR-10 WRN-28-10 selected 5 configs의 seed0/1/2 evidence에서 validation-selected
high-accuracy models can differ in ECE and feature-based near-OOD AUROC, and
L2 control recovery links the split to feature norm/covariance-scale geometry.
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
\textbf{Figure 1.} Accuracy만 높은 모델도 두 방식으로 실패할 수 있다.
Left: confidence가 empirical accuracy보다 높으면 overconfident decision이 발생한다.
Right: OOD input이 높은 ID-like score를 받으면 정상 입력처럼 downstream으로 전달될 수 있다.
Throughout the poster, higher OOD score means more ID-like.
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
마지막 표현층의 geometry를 class-conditional feature distribution으로 요약한다.
Let X be an input, Y in {1,...,K} its ID class label, and H=h_theta(X) in R^p the
penultimate feature. For class k, H | Y=k is summarized by its center, spread,
anisotropy, and norm scale.

Mahalanobis, kNN, DDU-style GMM 같은 post-hoc feature detector는 이 분포를 서로
다른 방식으로 읽는다. Mahalanobis high score는 h가 pooled covariance ellipsoid에서
어떤 class mean에 가깝다는 뜻이고, kNN high score는 h가 ID feature bank 안에 가까운
neighbor를 갖는다는 뜻이다. DDU-style GMM high score는 fitted class-conditional
Gaussian mixture 아래에서 h의 likelihood가 높다는 뜻이다.

Optimizer가 이 분포를 바꿀 수 있는 이유는 마지막 classifier W와 feature H가
cross-entropy 학습 중 함께 움직이기 때문이다. 마지막 logit layer를 z=W h_theta(x)로
쓰고, g_t=nabla_{W_t} L_CE, s_t=W_t^T 1_K, a_t=K^{-1}||s_t||_2^2로 둔다.
Cross-entropy에서는 g_t^T 1_K=0이고, s_t는 classifier row-sum direction이다.

SGD/L2에서는 row-sum zero gradient 때문에 weight decay가 s_t를 주로 수축한다. Adam/L2는
decay term이 adaptive direction 안에 들어가고, AdamW는 decoupled decay가 adaptive
direction 밖에서 shrinkage로 작용한다. Adaptive scaling은 centered gradient를
non-centered update로 바꿀 수 있으므로, coupled/decoupled weight decay는 classifier
centering과 feature-distribution geometry에서 서로 다른 경로를 만들 수 있다.

NC2/NC3 alignment는 classifier rows와 centered class means가 맞물려야 하며, 이를 위해
W^T 1_K -> 0이 필요하다. 따라서 다른 s_t 경로는 class-mean alignment와 feature
distribution geometry 차이로 이어질 수 있다. Mahalanobis/kNN/GMM은 mu_k, Sigma_k,
||H||, class separation을 읽으므로, optimizer-induced geometry changes는 같은 detector
formula에서도 OOD score ranking을 바꿀 수 있다.
```

### Formulas

```tex
H\mid Y=k,\qquad
\mu_k=\mathbb{E}[H\mid Y=k],\qquad
\Sigma_k=\mathbb{E}\{(H-\mu_k)(H-\mu_k)^\top\mid Y=k\}
```

```tex
z=W h_\theta(x),\qquad
g_t=\nabla_{W_t}L_{\rm CE},\qquad
s_t=W_t^\top \mathbf{1}_K,\qquad
a_t=\frac{1}{K}\|s_t\|_2^2,\qquad
g_t^\top\mathbf{1}_K=0
```

```tex
\text{SGD/L2:}\quad
V_{t+1}=\beta V_t+g_t,\qquad
W_{t+1}=(1-\eta\lambda)W_t-\eta V_{t+1},\qquad
s_{t+1}\approx(1-\eta\lambda)s_t
```

```tex
\text{Adam/L2:}\quad
g_t^{\rm L2}=g_t+\lambda W_t,\qquad
W_{t+1}=W_t-\eta D_t g_t^{\rm L2}
```

```tex
\text{AdamW:}\quad
W_{t+1}=W_t-\eta D_tg_t-\eta\lambda W_t,\qquad
(D_tg_t)^\top\mathbf{1}_K\not\equiv0
```

### Ultra-Short Version

```text
`H | Y=k`는 center, spread, anisotropy, norm scale로 요약된다. CE gradients are
row-sum zero, so SGD/L2 mainly contracts classifier row-sum `s_t`; adaptive scaling
and coupled/decoupled weight decay can follow different centering paths. Because
Mahalanobis/kNN/GMM read `mu_k`, `Sigma_k`, `||H||`, and class separation, those
geometry paths can change OOD score ranking.
```

### Diagram Requirement

- 별도 Figure 번호를 붙이지 않고, Optimizer 섹션 내부에 작은 `Mechanism sketch`로 넣는다.
- 도식은 `feature distribution view`를 상단에 두고, 이어서 detector가 읽는
  distribution quantities, `CE zero row-sum`, `SGD/L2`, `Adam/L2`, `AdamW`, 그리고
  stepwise geometry chain을 보여준다.
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
| Current status | selected 5 configs, seed0/1/2 mean +/- sample std |
| Main result assets | validation/calibration table, near-OOD raw-vs-L2 figure, geometry table |

### Ultra-Short Version

```text
Hyperparameters are selected by ID validation accuracy only. OOD, calibration,
and geometry metrics are post-hoc diagnostics. Poster values are selected
seed0/1/2 mean +/- sample std.
```

## 3.6 Table 1: Validation-Selected Models

### Role

오른쪽 열의 첫 evidence panel이다. ID validation accuracy로 선택한 5개 config가
높은 accuracy band에 있더라도 calibration diagnostic은 달라질 수 있음을 보여준다.

### Required Columns

```text
Config, Optimizer, ID test acc, ID test NLL, ECE, Temperature-scaled ECE, Temperature
```

### Caption Text

```text
Selected WRN-28-10/CIFAR-10 configs, seeds 0/1/2. Selection uses ID validation
accuracy only; calibration metrics are post-hoc diagnostics.
```

### Interpretation Text

```text
Table 1은 high ID accuracy가 calibration identity를 보장하지 않음을 보여준다.
SGD rows는 ID test accuracy가 더 높고 ECE가 낮으며, AdamW rows는 competitive
accuracy band에 있지만 ECE와 temperature scaling 값이 더 크다.

이 표는 optimizer ranking을 단독으로 주장하기 위한 표가 아니다. Selection은 ID
validation accuracy만 사용했고, ECE/NLL/temperature는 post-hoc diagnostic으로
읽는다.
```

### Ultra-Short Version

```text
Validation-selected high-accuracy models can differ in ECE and temperature
scaling; accuracy alone does not determine calibration reliability.
```

## 3.7 Figure 2: Raw vs L2 Feature OOD AUROC on Near-OOD

### Role

오른쪽 열의 main empirical figure이다. CIFAR-100과 TinyImageNet을 별도 패널로
표시해 OOD dataset 간 평균을 만들지 않으면서 raw feature detector split과
L2-normalized diagnostic recovery를 보여준다.

### Required Figure Structure

```text
Panels: CIFAR-100, TinyImageNet
X-axis: SGD-5e-4, SGD-2e-4, Adam, AdamW-1e-4, AdamW-5e-4
Series: raw Mahalanobis, Mahalanobis-L2, raw kNN, kNN-L2
Y-axis: AUROC, higher is better
Error bars: sample std over seeds 0/1/2
```

### Caption Text

```text
CIFAR-100 and TinyImageNet are shown separately. Bars are AUROC mean +/- sample
std over seeds 0/1/2. Higher is better; no average across OOD datasets is used.
```

### Interpretation Text

```text
Feature detectors split sharply on raw features, especially for AdamW rows.
Raw Mahalanobis drops on CIFAR-100/TinyImageNet for Adam/AdamW, while
detector-side L2 controls recover much of the ranking.

This figure should not be read as "L2 normalization solves OOD detection."
L2 normalization is a diagnostic control that reduces feature-scale effects while
preserving angular information.
```

## 3.8 Table 2: Feature Distribution Geometry

### Role

Figure 2의 detector split이 단순한 detector artifact가 아니라 penultimate feature
distribution의 차이와 함께 나타난다는 것을 보여주는 geometry evidence panel이다.

### Required Columns

```text
Config, Optimizer, NC1, InterDist, feature norm mean, effective rank
```

### Metric Boundary

- 포스터 표에는 geometry metric을 과하게 넣지 않는다.
- 기본 축은 `NC1`, `InterDist`, `feature_norm_mean`, `effective_rank`로 제한한다.
- `NC3`, `condition number`, full covariance spectrum은 Q&A 보조 자료로 남긴다.
- 표 caption에서는 낮은 NC1과 큰 InterDist가 더 compact/separated geometry와
  관련된다는 정도로만 설명한다.

### Caption Text

```text
ID-train penultimate feature diagnostics, seeds 0/1/2. Lower NC1 and larger
InterDist indicate more compact and separated class-conditional geometry.
```

### Interpretation Text

```text
Table 2는 optimizer/LR/weight decay 조합이 만든 penultimate feature distribution이
다를 수 있음을 보여준다. AdamW rows는 class-mean separation과 feature norm이 작고,
Adam row는 SGD보다 NC1이 크면서 effective rank가 낮다.

이 표는 geometry 하나로 detector gap을 증명하기 위한 표가 아니다. Figure 2의 raw-vs-L2
split과 함께 읽어, feature-based detector가 읽는 class-conditional distribution이
optimizer choice와 함께 달라질 수 있음을 보여주는 diagnostic evidence이다.
```

## 3.9 Takeaway and Limitations

### Role

결과 해석을 단순한 `AdamW가 나쁘다`가 아니라, detector-side sensitivity와
feature distribution의 상호작용으로 정리한다.

### Poster Text

```text
Detector reliability depends on the feature distribution it sees, not the
optimizer name directly. Accuracy is necessary but not sufficient:
validation-selected high-accuracy models can differ in calibration and
feature-based OOD behavior.

Optimizer update rules can shift class-conditional feature location, dispersion,
norm scale, and covariance structure. This is post-hoc diagnostic evidence on
WRN-28-10/CIFAR-10 selected configs, not a causal proof or full DDU reproduction.
```

### Ultra-Short Version

```text
Accuracy is necessary but not sufficient. Validation-selected high-accuracy
models can differ in calibration, feature-based OOD behavior, and feature
distribution geometry. This is bounded post-hoc diagnostic evidence.
```

## 3.10 Future Work

### Required Order

1. Adam-AdamW interpolation
2. dataset / architecture expansion
3. SAM, Mixup 등 다른 training methods 확장

### Poster Text

```text
1. Adam-AdamW interpolation: coupled weight decay와 decoupled weight decay 사이를
연속적으로 조절해, adaptive update와 norm shrinkage가 feature geometry와 OOD reliability를
어떻게 바꾸는지 더 직접적으로 확인한다.

2. Dataset / architecture expansion: CIFAR-10 WRN-28-10에서 보인 diagnostic pattern이
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

## 3.11 Poster-Ready Compact Text

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

Finding: Selected seed0/1/2 evidence에서 validation-selected high-accuracy models가
ECE와 feature-based near-OOD AUROC에서 갈라지고, L2 control recovery는
norm/covariance-scale sensitivity 해석과 일관된다.
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
- H | Y=k has center mu_k, covariance Sigma_k, anisotropy, and norm scale.
- Mahalanobis/kNN/GMM read mu_k, Sigma_k, ||H||, and class separation.
- z = W h_theta(x), g_t = nabla_{W_t} L_CE, s_t = W_t^T 1_K,
  a_t = K^{-1} ||s_t||^2, and g_t^T 1_K = 0.
- SGD/L2 mainly contracts the classifier row-sum s_t.
- Adam/L2 and AdamW place weight decay inside or outside the adaptive direction,
  so coordinate-wise scaling can create different centering paths.
- Different s_t paths can support different NC2/NC3 alignment, class-mean
  alignment, and feature-distribution geometry.

Implication: Accuracy가 비슷해도 class mean separation, within-class dispersion,
covariance scale/anisotropy, feature norm, classifier-feature alignment가 달라질 수 있다.

Boundary: This mechanism supports optimizer-induced geometry shifts; OOD
reliability is evaluated by the post-hoc diagnostics on the right.
```

### Experiment

```text
Claim: Selection uses ID validation accuracy only.

Setup:
- ID / model: CIFAR-10 / WRN-28-10
- Train factors: SGD, Adam, AdamW over LR-WD grid
- Selection: no OOD/geometry metric used
- Post-hoc diagnostics: ECE, OOD AUROC, NC1, InterDist
- OOD datasets: CIFAR-100, TinyImageNet, SVHN, MNIST
- Reported: seed 0/1/2 mean +/- sample std
```

### Table 1

```text
Read: High ID accuracy does not make calibration identical.

Evidence: SGD rows have higher ID test accuracy and lower ECE; AdamW rows remain
competitive in accuracy but require much larger temperature scaling.

Boundary: No OOD or geometry metric was used for hyperparameter selection.
```

### Figure 2

```text
Read: Feature detectors split sharply on raw features, especially for AdamW rows.

Evidence: Raw Mahalanobis drops on CIFAR-100/TinyImageNet for Adam/AdamW, while
detector-side L2 controls recover much of the ranking.

Boundary: L2 normalization is a diagnostic control, not a final detector solution.
```

### Table 2

```text
Read: The detector split is accompanied by different feature distributions.

Evidence: AdamW rows show smaller class-mean separation and lower feature norms;
Adam shows larger NC1 than SGD with a much lower effective rank.

Implication: Distance/covariance-based OOD scores can change because the feature
distribution they read has changed.
```

### Mechanism and Conclusion

```text
Claim: Detector reliability depends on the geometry it sees, not the optimizer
name directly.

Mechanism: Raw Mahalanobis uses class means and covariance-based distance; raw
kNN uses neighborhood distance. Both can change with feature norms, class
separation, covariance anisotropy, and effective rank.

Conclusion: Accuracy is necessary but not sufficient. Validation-selected
high-accuracy models can differ in calibration, feature-based OOD behavior, and
feature distribution geometry. This remains bounded post-hoc diagnostic evidence.
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
- `docs/research/wrn350_selected_3seed_metrics_notion_20260612.md`
- `data/manifests/wrn350_selected_3seed_poster_assets_20260612.md`
