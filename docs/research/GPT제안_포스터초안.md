# 한국 통계학회 포스터초안

> Production update, 2026-06-11 KST: 현재 `poster/poster.tex` 초안은 표 2개와
> 그림 3개 구조다. Figure 1은 reliability failure 개념도이고, 기존 empirical
> reliability scatter는 Figure 2, raw-to-L2 recovery는 Figure 3으로 이동했다.
> 고정 제목은 `Optimizer-Induced Feature Geometry Shapes Post-Hoc OOD Detection Reliability`,
> Key Question은 `비슷한 Accuracy라도 optimizer가 만든 feature geometry가 모델의 신뢰성에 어떤 영향을 미치는가?`이다.

## 1. 포스터 주제

**Test accuracy alone is not enough : optimizer-induced feature geometry can change calibration and post-hoc OOD detection reliability.**

높은 classification accuracy를 보여도 penultimate feature space의 분포 구조는 optimizer와 regularization에 따라 달라질 수 있다”는 문제의식과, feature-based OOD detector가 class mean, covariance, feature norm, inter-class separation에 의존한다는 연구 공백이 있습니다.

---

## 2. 실험

### Stage 1. Main experiment :

가장 먼저 이것만 완성하면 됩니다.

| 항목 | 설정 |
| --- | --- |
| ID dataset | CIFAR-10 |
| Architecture | WideResNet-28-10 또는 ResNet-18 |
| Optimizer | SGD, Adam, AdamW |
| Seeds | 최소 3개 |
| Epoch | 350 epochs 권장. 시간이 부족하면 200 epochs + final checkpoint |
| Weight decay | 모두 `5e-4`로 시작 |
| Batch size | 128 |
| LR schedule | 기존 프로젝트 표준 schedule 유지 |
| OOD datasets | CIFAR-100, Tiny-ImageNet, SVHN, MNIST |
| Main detectors | MSP, Energy, Mahalanobis, Mahalanobis-L2, kNN, DDU-style GMM |
| Main geometry | NC0, NC1, NC2 mean cosine, NC3, WithinVar, InterDist, feature norm stats, covariance eigenspectrum |

이 실험의 목적은 단순합니다.

1. SGD, Adam, AdamW의 test accuracy가 비슷한지 확인한다.
2. ECE/NLL/T-ECE가 optimizer별로 달라지는지 본다.
3. Mahalanobis, kNN, DDU-style GMM 같은 feature-based OOD detector가 optimizer별로 다르게 반응하는지 본다.
4. 그 차이가 WithinVar, covariance spectrum, feature norm dispersion, NC metric과 함께 움직이는지 본다.

현재 metric 문서상으로도 Classification/Calibration은 Accuracy, NLL, ECE, temperature-scaled ECE, OOD는 AUROC/AUPR-IN/FPR95, detector는 MSP/Energy 및 Mahalanobis/L2-Mahalanobis/kNN/DDU, geometry는 NC0~NC3, within-class variance, inter-class distance, feature norm, covariance eigenspectrum 등을 쓰는 방향으로 정리되어 있습니다.

---

## 3. 포스터에 넣을 표와 그림

A0 포스터가 과해지는 것을 막기 위해 empirical result만 보면 표 2개와 empirical 그림 2개로
압축한다. 다만 현재 production draft에서는 reliability 개념 설명을 위해 Figure 1
개념도를 추가하여, 전체 figure 번호는 다음처럼 사용한다.

- Figure 1: Reliability Failure concept diagram.
- Figure 2: Accuracy-Matched Reliability Split.
- Figure 3: Raw-to-L2 Recovery Suggests Norm/Scale Sensitivity.

### 표 1. Accuracy / Calibration / OOD 요약표

행은 optimizer, 열은 대표 지표만 둡니다.

| Optimizer | Acc ↑ | NLL ↓ | ECE ↓ | T-ECE ↓ | MSP AUROC ↑ | Energy AUROC ↑ | Maha AUROC ↑ | Maha-L2 AUROC ↑ | kNN AUROC ↑ | GMM AUROC ↑ |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |

일단 실험결과에서 모든 dataset의 결과를 다 측정한 후에 결과를 분석하고 여기서 **near-OOD 평균**과 **farOOD 평균에서 유의미한 결과가 있으면 near-OOD 평균**과 **far-OOD 평균**으로 나누자.

| Optimizer | Acc | ECE | Near-OOD Maha | Near-OOD Maha-L2 | Near-OOD kNN | Near-OOD GMM | Far-OOD Avg |
| --- | --- | --- | --- | --- | --- | --- | --- |

포스터 메시지는 near-OOD에서 더 잘 드러날 가능성이 큽니다. 이전 NeurIPS 맥락에서도 near-OOD는 feature manifold와 class boundary에 가까워 covariance, within-class dispersion, centroid separation 변화에 더 민감하다고 정리되어 있습니다.

### 표 2. Geometry 요약표

| Optimizer | NC0 ↓ | NC1 ↓ | WithinVar ↓ | InterDist ↑ | Norm Std | Top eigenvalue / trace | Effective rank |
| --- | --- | --- | --- | --- | --- | --- | --- |

여기서 너무 많은 NC metric을 넣지 마세요. 포스터에서는 **NC1, WithinVar, InterDist, covariance spectrum**만으로도 충분합니다. NC0/NC3는 Adam vs AdamW 차이를 강조할 때 보조로 넣으면 됩니다.

첨부 문서에서도 optimizer가 representation geometry를 바꾸지만 기존 논문은 이것이 OOD 성능, calibration, uncertainty score 분포에 미치는 영향을 직접 평가하지 않았다는 gap을 핵심 질문으로 잡고 있습니다.

---

## 4. 그림 구성

### Figure 1. “Reliability failure: miscalibration and OOD acceptance”

개념도

- 왼쪽: confidence와 empirical accuracy가 어긋나는 miscalibration.
- 오른쪽: OOD sample이 high ID-like score를 받아 정상 입력처럼 처리되는 OOD acceptance.
- 핵심 메시지: **Miscalibration은 confidence threshold decision을 흔들고, OOD acceptance는 지원하지 않는 입력을 downstream decision으로 넘긴다.**

### Figure 2. “같은 accuracy, 다른 OOD reliability”

막대그래프 또는 점그래프

- x축 : optimizer
- y축 : Acc, ECE, Mahalanobis AUROC, DDU-style GMM AUROC
- 핵심 메시지 : **accuracy는 비슷한데 feature-based OOD는 다르다**

### Figure 3. “왜 달라지는가: feature geometry”

두 그림 중 하나만 선택하세요.

1. **PCA/UMAP feature visualization**
    - SGD vs AdamW feature 분포 비교
    - 너무 예쁘게 그리기보다 class compactness 차이가 보이면 충분합니다.
2. **Covariance eigenspectrum plot**
    - optimizer별 class-conditional covariance eigenvalue 평균
    - Mahalanobis/DDU-style detector가 covariance에 민감하다는 메시지와 바로 연결됩니다.

기존 NeurIPS 결과에서도 vanilla SAM은 within-class dispersion과 covariance scale을 키우고, 이 변화가 Mahalanobis/DDU degradation의 원인으로 해석되었습니다.  이 논리를 이번 포스터에서는 SAM이 아니라 **SGD/Adam/AdamW optimizer choice**로 확장하면 됩니다.

---

## 5. 실험

### 1순위: 반드시 해야 함

```
CIFAR-10 / WRN-28-10 또는 ResNet-18
SGD, Adam, AdamW
3 seeds
Accuracy, NLL, ECE, T-ECE
MSP, Energy
Mahalanobis, Mahalanobis-L2, kNN, DDU-style GMM
NC1, WithinVar, InterDist, feature norm stats, covariance eigenspectrum
```

이것만으로 포스터 메시지는 성립합니다.

### 2순위: 시간이 있으면 추가

```
AdamW -> Adam interpolation
```

이 실험은 “decoupled vs coupled weight decay가 geometry를 바꾼다”는 주장을 더 강하게 만듭니다. 기존 문헌에서도 AdamW에서 Adam으로 coupled weight decay 비율을 늘리면 NC0, NC2, NC3가 개선되지만 validation accuracy는 크게 변하지 않는다고 정리되어 있습니다.

### 3순위: 포스터에는 넣지 말고 appendix/추가자료

```
ViM
NECO
NC residual subspace
ViT
CIFAR-100 ID
SN-on/off full ablation
```

이들은 ICLR 2027 본 논문에는 중요하지만, 통계학회 포스터에는 너무 많습니다.

---

## 6. detector 선택에서 주의할 점

DDU는 포스터에서 **“DDU-style GMM feature-density score”**라고 쓰는 것이 안전합니다. 원래 DDU는 residual connection과 spectral normalization을 포함한 training recipe 위에 Gaussian density를 붙이는 방법이라서, spectral normalization 없이 Gaussian log-density만 계산하면 “original DDU reproduction”이라고 부르면 위험합니다. 문서에서도 SN 없이 쓰는 경우에는 “DDU-style Gaussian feature-density scores”라고 부르라고 정리되어 있습니다.

따라서 포스터 표기:

```
DDU-style GMM
```

또는

```
GMM feature density inspired by DDU
```

가 좋습니다.

---

## 7. 통계 분석은 간단하게

통계학회 포스터이므로 단순 평균표만 있으면 약할 수 있습니다. 하지만 너무 복잡한 검정도 필요 없습니다. 다음 3개면 충분합니다.

### A. mean ± std

각 optimizer별로 3 seeds 결과를 보고합니다.

```
mean ± std over 3 seeds
```

### B. paired Δ 분석

같은 seed끼리 비교합니다.

```
ΔMetric = Metric(AdamW, seed s) - Metric(SGD, seed s)
```

예를 들어:

| Metric | Δ Adam − SGD | Δ AdamW − SGD |
| --- | --- | --- |
| Accuracy | +0.1 ± 0.2 | +0.0 ± 0.2 |
| ECE | -0.5 ± 0.1 | -0.3 ± 0.2 |
| Maha AUROC | -3.2 ± 0.8 | -5.6 ± 1.1 |
| WithinVar | +0.4 ± 0.1 | +0.8 ± 0.2 |

이렇게 하면 “정확도 차이가 작아도 geometry/OOD 차이는 크다”를 설득하기 쉽습니다.

### C. Spearman correlation

포스터에는 한 줄만 쓰면 됩니다.

```
Across trained checkpoints, feature dispersion and covariance-spectrum metrics are correlated with feature-based OOD AUROC.
```

첨부 문서에서도 Spearman 분석은 각 checkpoint를 관측치로 두고 geometry metric과 OOD metric의 순위 상관을 계산하는 방식으로 정리되어 있습니다.

---

## 8. 실제 학습 실행 계획

### Run group A: main optimizer comparison

```
# CIFAR-10 / WRN or ResNet-18 / seed 0,1,2
SGD:lr=0.1,momentum=0.9,wd=5e-4
Adam:  lr 후보 1e-3, 3e-4
AdamW: lr 후보 1e-3, 3e-4,wd=5e-4
```

Adam/AdamW는 SGD와 같은 lr을 쓰면 안 될 가능성이 큽니다. 먼저 seed0으로 lr 후보를 작게 grid search해서 **test accuracy가 SGD와 비슷한 matched setting**을 고르세요.

추천 순서:

1. `seed0`으로 optimizer별 lr 후보 실행
2. test accuracy가 비슷한 config 선택
3. 선택된 config로 `seed0,1,2` full run
4. final checkpoint에서 post-hoc evaluation
5. geometry metric 저장
6. 표와 그림 생성

### Run group B: detector evaluation

각 trained checkpoint마다 동일하게 평가합니다.

```
ID test: CIFAR-10 test
Near-OOD: CIFAR-100, Tiny-ImageNet
Far-OOD: SVHN, MNIST
```

모든 score 방향은 현재 프로젝트 convention처럼:

```
higher = more ID-like
ID label = 1
OOD label = 0
```

로 통일하세요. 기존 metric 문서도 이 convention을 명시합니다.

### Run group C: geometry extraction

각 checkpoint마다 ID train 또는 ID train+val feature에서 다음을 저장합니다.

```
features_train.npy
features_test.npy
logits_test.npy
labels_train.npy
labels_test.npy
class_means.npy
covariance_eigenspectrum.npy
metrics_geometry.json
metrics_calibration.json
metrics_ood.json
```
