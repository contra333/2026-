# WRN seed0 350eps grid-search 실험_0531

# 전체 실험 결과

[WRN_seed0_350eps_girdsearch_0531_notion_run_overview_ko.csv](https://app.notion.com/p/371a26cf6e72809ea7c1f70ba81791c9?pvs=21)

# 대표 모델 비교(ID-validation accuracy성능 기준)

## **1. Accuracy / Calibration 표**

| **비교축** | **후보** | **optimizer** | **LR** | **WD** | **checkpoint** | **best val acc** | **final val acc** | **ID test acc** | **ID test NLL** | **ECE** | **T-ECE** | **T** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | sgd | 0.1 | 0.0002 | epoch_0350 | 0.9612 | 0.9594 | 0.9546 | 0.2364 | 0.0331 | 0.0079 | 2.1146 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | adam | 0.001 | 0.0 | epoch_0350 | 0.9524 | 0.9518 | 0.9436 | 0.4667 | 0.0473 | 0.0071 | 4.3919 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | adam | 0.001 | 0.0001 | epoch_0350 | 0.9494 | 0.9476 | 0.9447 | 0.2844 | 0.0390 | 0.0060 | 2.4955 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | adamw | 0.005 | 0.0001 | epoch_0350 | 0.9528 | 0.9504 | 0.9468 | 0.5234 | 0.0451 | 0.0068 | 5.1008 |
- **1. Accuracy가 비슷한데 NLL이 높으면 생기는 문제**
    
    예를 들어 두 모델이 모두 95개를 맞춘다고 해도, 확률을 이렇게 줄 수 있습니다.
    
    `모델 A: 맞춘 정답에 0.90 확률, 틀린 샘플도 0.40 정도 confidence
    모델 B: 맞춘 정답에 0.60 확률, 틀린 샘플은 오답에 0.99 confidence`
    
    둘 다 accuracy는 비슷할 수 있습니다. 하지만 모델 B는 확률 예측이 나쁩니다. NLL은 이런 차이를 강하게 벌합니다.
    
    문제는 이런 곳에서 생깁니다.
    
    - **불확실성 판단이 나빠짐**: 모델이 틀릴 때도 자신감이 높으면 “이 예측은 위험하다”는 신호를 못 줍니다.
    - **threshold 기반 decision이 불안정**: confidence 0.9 이상만 자동 처리하고 나머지는 보류하는 시스템에서, 잘못된 샘플이 자동 처리될 수 있습니다.
    - **OOD / reject option과 충돌 가능**: ID classification은 맞추지만 confidence scale이 이상하면 logit 기반 OOD score가 왜곡될 수 있습니다.
    - **앙상블, downstream decision, risk-sensitive task에서 손해**: 확률을 비용 함수나 risk estimate로 쓰는 경우 NLL이 높은 모델은 decision value가 떨어집니다.
    - **calibration 해석이 어려워짐**: accuracy는 괜찮아 보여도, “이 모델의 90% confidence가 진짜 90% 맞는가?”라는 신뢰성은 떨어질 수 있습니다.
    
    현재 결과로 말하면, AdamW는 ID test acc=0.9468로 크게 나쁘지 않지만 NLL=0.5234로 높습니다. 즉 **맞고 틀림의 성능은 비슷한데, raw probability/logit quality는 SGD보다 훨씬 나쁘다**는 쪽으로 해석할 수 있습니다.
    
    **현재 실험에서의 결론**
    
    Raw model로 보면:
    
    `SGD가 가장 well-calibrated`
    
    근거:
    
    - 가장 낮은 raw ECE: SGD 0.0331
    - 가장 낮은 NLL: SGD 0.2364
    
    Temperature scaling을 적용한 calibrated predictor로 보면:
    
    `Adam wd>0가 T-ECE 기준 가장 well-calibrated`
    
    근거:
    
    - Adam wd>0 T-ECE 0.0060
    - AdamW T-ECE 0.0068
    - Adam wd0 T-ECE 0.0071
    - SGD T-ECE 0.0079
    
    하지만 표현은 조심해야 합니다.
    
    가장 안전한 문장:
    
    > SGD는 raw logits 기준에서 가장 좋은 NLL/ECE를 보여 가장 잘 calibrated된 원 모델이다. 반면 Adam/AdamW는 raw calibration은 나쁘지만, ID validation에서 fit한 scalar temperature를 적용하면 ECE가 SGD보다 낮아진다. 이는 Adam/AdamW의 calibration error가 상당 부분 logit scale mismatch에서 온다는 것을 시사한다.
    > 
    
    즉 “AdamW가 더 calibrated하다”라고 단순히 말하면 안 되고,
    
    `raw calibration: SGD 우세
    post-hoc temperature-scaled calibration: Adam/AdamW도 매우 잘 교정됨`
    
    으로 나눠 말하는 게 정확합니다.
    
- **2. Temperature T는 어떻게 찾고 어떻게 쓰나요?**
    
    모델은 class별 logit z를 냅니다. 보통은:
    
    `p = softmax(z)`
    
    로 확률을 만듭니다.
    
    Temperature scaling은 학습이 끝난 뒤, weight는 그대로 두고 logit만 이렇게 바꿉니다.
    
    `p_T = softmax(z / T)`
    
    여기서 T는 validation set에서 찾습니다. 이 repo에서는 ID validation logits/labels를 사용해서, validation NLL이 가장 낮아지도록 scalar T 하나를 최적화합니다.
    
    즉 과정은:
    
    `1. 학습 끝난 모델 고정
    2. ID validation set에 대해 logits 저장
    3. 여러 T 중 validation NLL이 낮아지는 T를 찾음
    4. test 때 logits / T를 softmax해서 calibrated probability로 사용`
    
    T의 의미는 이렇습니다.
    
    - T = 1: 원래 softmax 그대로
    - T > 1: logits를 줄임 → softmax가 덜 뾰족해짐 → confidence 낮아짐
    - T < 1: logits를 키움 → softmax가 더 뾰족해짐 → confidence 높아짐
    
    현재는 모두 T > 1입니다.
    
    `SGD:      T = 2.1146
    Adam wd0: T = 4.3919
    Adam wd+: T = 2.4955
    AdamW:    T = 5.1008`
    
    특히 AdamW와 Adam wd=0는 T가 큽니다. 이것은 **raw logits가 너무 크게 scale되어 confidence가 과하게 높았을 가능성**을 뜻합니다.
    
    **scalar logit scale 문제라는 말의 뜻**
    
    쉽게 말하면 이런 겁니다.
    
    모델의 class 순위는 꽤 괜찮습니다.
    
    `정답 class logit이 가장 큼`
    
    그래서 accuracy는 나쁘지 않습니다. 그런데 logit들의 크기 차이가 너무 큽니다.
    
    `[12, 1, -2, ...]  → softmax confidence 거의 0.999`
    
    실제로는 그 예측이 99.9%만큼 믿을 만하지 않은데, logit scale이 너무 커서 softmax confidence가 과하게 나옵니다.
    
    Temperature scaling은 이걸:
    
    `[12, 1, -2] / 5 = [2.4, 0.2, -0.4]`
    
    처럼 줄여서 confidence를 낮춥니다.
    
    그러면 class ranking은 거의 유지됩니다. argmax는 그대로라 accuracy는 거의 안 바뀝니다. 대신 확률의 “세기”만 더 현실적으로 바뀝니다.
    
    그래서 “calibration 문제가 scalar logit scale 문제일 수 있다”는 말은:
    
    > 모델이 어떤 class를 고를지는 크게 틀리지 않지만, 그 선택에 부여하는 confidence가 전체적으로 너무 세거나 약하다. 이 문제는 class별 복잡한 보정 없이 T 하나로 꽤 교정된다.
    > 
    
    라는 뜻입니다.
    
    반대로 calibration 문제가 복잡한 경우는 이런 겁니다.
    
    - class 1은 항상 overconfident
    - class 2는 항상 underconfident
    - 쉬운 샘플과 어려운 샘플의 confidence 왜곡이 다름
    - 특정 OOD-like texture에서만 confidence가 이상함
    
    이런 문제는 scalar T 하나로 잘 안 고쳐집니다. 그런데 현재 Adam/AdamW는 T-ECE가 크게 낮아졌으므로, 적어도 ID test calibration에 대해서는 **단순 logit scale 보정만으로도 많이 개선되는 형태**로 보입니다.
    
- **3. 정답확률 vs 모델의 출력하는 확률**
    
    직관적으로는 “정답 class에 높은 확률을 주면 좋은 것 아닌가?”가 맞아 보입니다. 그런데 **확률**로 출력한다는 순간, 그 숫자는 단순한 순위가 아니라 **맞을 가능성에 대한 약속**이 됩니다.
    
    예를 들어 모델이 어떤 이미지에 대해:
    
    `cat: 0.99
    dog: 0.01`
    
    라고 하면, 이건 단순히 “cat이 제일 그럴듯하다”가 아니라:
    
    > 나는 이 예측이 약 99% 정도 맞을 것이라고 본다
    > 
    
    라는 의미입니다.
    
    그런데 실제로 모델이 0.99 confidence로 예측한 샘플 100개를 모아봤더니 90개만 맞았다면, 이 모델은 **overconfident**입니다.
    
    `말한 confidence: 99%
    실제 accuracy: 90%`
    
    즉 overconfidence는 “정답 class에 높은 확률을 줬다” 자체가 문제가 아니라, **그 높은 확률만큼 실제로 맞지 않는다**는 뜻입니다.
    
    예를 들어 CIFAR-10에서 자동차 사진이 있고 정답이 car라고 합시다.
    
    모델 A:
    
    `car: 0.85
    truck: 0.10
    ship: 0.03
    ...`
    
    모델 B:
    
    `car: 0.999
    truck: 0.0005
    ship: 0.0002
    ...`
    
    둘 다 맞췄습니다. accuracy에는 둘 다 1점입니다.
    
    하지만 모델 B가 이런 식으로 모든 샘플에 0.999 confidence를 주고, 실제로는 94.7%만 맞는다면 문제가 생깁니다.
    
    왜냐하면 모델 B는 사실상 이렇게 말하고 있기 때문입니다.
    
    > 거의 절대 안 틀립니다.
    > 
    
    그런데 실제로는 5% 정도 틀립니다. 그러면 확률이 현실보다 과합니다.
    
    **정답 라벨이 하나인데도 왜 100% 확률을 주면 안 되나?**
    
    데이터셋에는 정답 라벨이 하나지만, 모델 입장에서는 입력 이미지 하나만 보고 추론합니다. 이미지에는 애매함이 있습니다.
    
    예를 들어:
    
    - 고양이와 개가 같이 있는 이미지
    - truck처럼 생긴 car
    - 흐릿한 airplane
    - 배경 때문에 헷갈리는 bird
    - label noise가 있는 샘플
    - train distribution과 조금 다른 test image
    
    정답 라벨은 하나로 정해져 있어도, 모델이 가진 정보만으로는 항상 100% 확신할 수 없습니다. 그래서 좋은 확률 모델은 쉬운 샘플에는 높은 confidence를 주고, 애매한 샘플에는 낮은 confidence를 줘야 합니다.
    
    **Overconfidence 예시**
    
    모델이 10,000개 CIFAR-10 test image에 대해 예측했다고 합시다.
    
    | **confidence 구간** | **샘플 수** | **실제 accuracy** | **좋은 calibration이라면** |
    | --- | --- | --- | --- |
    | 0.90 근처 | 1,000개 | 0.90 | 좋음 |
    | 0.90 근처 | 1,000개 | 0.75 | overconfident |
    | 0.60 근처 | 1,000개 | 0.80 | underconfident |
    
    즉 confidence 0.90이라고 말한 샘플들은 실제로도 대략 90% 맞아야 합니다. 이것이 calibration입니다.
    
    **NLL은 왜 overconfidence를 세게 벌하나?**
    
    NLL은 정답 class 확률 p_y에 대해:
    
    `NLL = -log(p_y)`
    
    입니다.
    
    정답에 높은 확률을 주면 NLL은 낮습니다.
    
    `정답 확률 0.9  → -log(0.9)  = 0.105
    정답 확률 0.5  → -log(0.5)  = 0.693`
    
    그런데 틀린 샘플에서 정답 class 확률을 아주 낮게 주면 큰 벌점을 받습니다.
    
    `정답 확률 0.1   → -log(0.1)   = 2.30
    정답 확률 0.01  → -log(0.01)  = 4.61
    정답 확률 0.001 → -log(0.001) = 6.91`
    
    즉 모델이 틀릴 때 “오답에 0.999”를 주면, 정답 class 확률은 거의 0이므로 NLL이 크게 튑니다.
    
    그래서 accuracy는 비슷해도, 틀린 샘플에서 너무 자신만만하게 틀리는 모델은 NLL이 나빠집니다.
    
    **현재 실험에 연결하면**
    
    AdamW best는:
    
    `ID test acc = 0.9468
    NLL = 0.5234
    ECE = 0.0451
    T = 5.1008`
    
    SGD best는:
    
    `ID test acc = 0.9546
    NLL = 0.2364
    ECE = 0.0331
    T = 2.1146`
    
    둘의 accuracy 차이는 크지 않지만, AdamW는 NLL이 훨씬 높고 T도 큽니다. 이는 AdamW가 raw logits에서 confidence를 너무 강하게 내는 경향이 있을 수 있음을 뜻합니다. 특히 틀리는 샘플에서 정답 확률을 너무 낮게 주거나, 전체 confidence scale이 과하게 커져 있을 가능성이 있습니다.
    
    짧게 말하면:
    
    > Classification에서 높은 확률은 좋지만, 그 확률은 실제 맞을 가능성과 맞아야 한다. 정답 class에 0.99를 자주 주는데 실제로는 0.95만 맞으면, 그 0.99는 과한 자신감이다.
    > 
    
    그래서 “정답 라벨이 하나니까 무조건 1에 가까운 확률을 주면 좋다”가 아니라,
    
    > 맞출 만한 샘플에는 높게, 헷갈릴 만한 샘플에는 낮게, 그리고 confidence 수준별 실제 정확도와 맞게
    > 
    
    주는 모델이 well-calibrated 모델입니다.
    

AdamW는 CIFAR-10 test accuracy만 보면 SGD와 큰 차이가 나지 않습니다. 즉, 어떤 class를 정답으로 고르는 능력 자체는 크게 무너지지 않았다.

하지만 NLL과 ECE는 SGD보다 나쁘다. 이것은 AdamW가 정답을 맞히느냐와 별개로, 자신이 낸 확률값의 신뢰도는 더 낮다는 뜻이다.

특히 틀린 샘플에서 오답 class에 너무 높은 확률을 주거나, 맞춘 샘플에서도 확률값이 실제 정답률과 잘 맞지 않았을 가능성이 있다.

또 AdamW의 fitted temperature 값이 크다. Temperature scaling은 학습이 끝난 뒤 logit을 T로 나누어서 confidence를 조정하는 방법이다. 

AdamW에서 큰 T가 필요했다는 것은, 원래 AdamW가 내는 logit 값의 크기가 너무 커서 softmax 확률이 지나치게 확신하는 방향으로 나왔다는 뜻으로 해석할 수 있다.

Temperature scaling을 적용한 뒤 T-ECE가 크게 낮아졌다는 점도 중요하다. 이는 AdamW의 calibration 문제가 class별로 복잡하게 꼬인 문제라기보다는, 

전체적으로 logit 크기가 너무 커서 confidence가 과하게 나온 문제였을 가능성을 보여준다. 즉, logit을 하나의 온도값으로 나누어 전체 confidence를 낮추자 calibration이 많이 좋아진 것이다.

AdamW는 정답을 고르는 성능은 SGD와 비슷하지만, 원래 출력하는 확률은 너무 자신만만한 방향으로 치우쳐 있었다. 그러나 이 문제는 temperature scaling이라는 간단한 후처리로 상당 부분 완화될 수 있었다.

## 2. OOD

**CIFAR100 - Logit**

| **비교축** | **후보** | **energy** | **maxlogit** | **msp** | **neg_entropy** |
| --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8476 | 0.8475 | 0.8721 | 0.8729 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.8973 | 0.8973 | 0.8432 | 0.8812 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.8997 | 0.8997 | 0.8814 | 0.8845 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.9038 | 0.9038 | 0.8432 | 0.8922 |

**CIFAR100 - Feature**

| **비교축** | **후보** | **mahalanobis** | **mahalanobis_l2** | **knn** | **knn_l2** | **gmm_tied** | **gmm_diag** | **gmm_shrinkage** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8613 | 0.8744 | 0.9043 | 0.9048 | 0.8613 | 0.9056 | 0.9069 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.6096 | 0.8728 | 0.8204 | 0.9016 | 0.6095 | 0.8631 | 0.8651 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.5680 | 0.7278 | 0.8556 | 0.8848 | 0.5678 | 0.8650 | 0.8008 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.4353 | 0.8524 | 0.6103 | 0.8943 | 0.4350 | 0.7903 | 0.8112 |

**CIFAR100 - NC/Hybrid**

| **비교축** | **후보** | **ncc_distance** | **nc_prototype_cosine** | **vim_id_score** |
| --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8884 | 0.8944 | 0.8845 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.8153 | 0.8863 | 0.8935 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.8497 | 0.8806 | 0.8655 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.7099 | 0.8806 | 0.8848 |

**TinyImageNet - Logit**

| **비교축** | **후보** | **energy** | **maxlogit** | **msp** | **neg_entropy** |
| --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8431 | 0.8429 | 0.8630 | 0.8641 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.8928 | 0.8928 | 0.8393 | 0.8749 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.9037 | 0.9035 | 0.8751 | 0.8795 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.8987 | 0.8987 | 0.8429 | 0.8865 |

**TinyImageNet - Feature**

| **비교축** | **후보** | **mahalanobis** | **mahalanobis_l2** | **knn** | **knn_l2** | **gmm_tied** | **gmm_diag** | **gmm_shrinkage** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8569 | 0.8649 | 0.9010 | 0.8983 | 0.8569 | 0.9034 | 0.9021 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.5654 | 0.8757 | 0.8039 | 0.8962 | 0.5653 | 0.8474 | 0.8458 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.5423 | 0.7379 | 0.8457 | 0.8863 | 0.5420 | 0.8520 | 0.7845 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.3983 | 0.8577 | 0.5914 | 0.8931 | 0.3979 | 0.7718 | 0.7837 |

**TinyImageNet - NC/Hybrid**

| **비교축** | **후보** | **ncc_distance** | **nc_prototype_cosine** | **vim_id_score** |
| --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8844 | 0.8864 | 0.8805 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.8102 | 0.8790 | 0.8846 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.8456 | 0.8820 | 0.8623 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.7194 | 0.8789 | 0.8763 |

**SVHN - Logit**

| **비교축** | **후보** | **energy** | **maxlogit** | **msp** | **neg_entropy** |
| --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.9344 | 0.9339 | 0.9316 | 0.9345 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.9258 | 0.9259 | 0.9038 | 0.9137 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.8288 | 0.8286 | 0.8520 | 0.8543 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.9283 | 0.9285 | 0.9012 | 0.9261 |

**SVHN - Feature**

| **비교축** | **후보** | **mahalanobis** | **mahalanobis_l2** | **knn** | **knn_l2** | **gmm_tied** | **gmm_diag** | **gmm_shrinkage** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.9729 | 0.9848 | 0.9681 | 0.9715 | 0.9729 | 0.9581 | 0.9804 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.9003 | 0.9924 | 0.9595 | 0.9898 | 0.9003 | 0.8877 | 0.9442 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.6604 | 0.8293 | 0.8626 | 0.8762 | 0.6601 | 0.7607 | 0.7510 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.7828 | 0.9821 | 0.8714 | 0.9843 | 0.7826 | 0.8828 | 0.9338 |

**SVHN - NC/Hybrid**

| **비교축** | **후보** | **ncc_distance** | **nc_prototype_cosine** | **vim_id_score** |
| --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.9541 | 0.9629 | 0.9849 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.9555 | 0.9887 | 0.9576 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.8759 | 0.9031 | 0.8439 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.8919 | 0.9864 | 0.9303 |

**MNIST - Logit**

| **비교축** | **후보** | **energy** | **maxlogit** | **msp** | **neg_entropy** |
| --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.9047 | 0.9036 | 0.8807 | 0.8825 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.9229 | 0.9231 | 0.9100 | 0.9210 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.9622 | 0.9615 | 0.9188 | 0.9226 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.9349 | 0.9356 | 0.9476 | 0.9538 |

**MNIST - Feature**

| **비교축** | **후보** | **mahalanobis** | **mahalanobis_l2** | **knn** | **knn_l2** | **gmm_tied** | **gmm_diag** | **gmm_shrinkage** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.9457 | 0.9728 | 0.9018 | 0.9185 | 0.9457 | 0.8518 | 0.9059 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.6301 | 0.9996 | 0.9082 | 0.9909 | 0.6300 | 0.7739 | 0.7749 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.4416 | 0.9641 | 0.9130 | 0.9143 | 0.4411 | 0.7081 | 0.5998 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.2712 | 0.9984 | 0.5423 | 0.9955 | 0.2708 | 0.6446 | 0.5905 |

**MNIST - NC/Hybrid**

| **비교축** | **후보** | **ncc_distance** | **nc_prototype_cosine** | **vim_id_score** |
| --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 0.8614 | 0.8960 | 0.9689 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.9675 | 0.9863 | 0.9394 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.9303 | 0.8901 | 0.8796 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 0.8896 | 0.9925 | 0.9072 |
- **raw calibration이 나쁜 편에 Overconfidence가 의심되는 상황에서도  logit OOD 지표에서는 꽤 좋은 성능을 보여주는 이유?**
    
    AdamW는 raw calibration이 나쁜 편인데도, 일부 logit OOD 지표에서는 꽤 좋은 성능을 보인다. 
    특히 CIFAR100에서 energy/maxlogit/neg_entropy가 좋고, MNIST에서는 msp/neg_entropy가 좋다. 이게 흥미로운 지점이다.
    
    **Logit OOD metric 정의**
    
    | **metric** | **정의** | **의미** |
    | --- | --- | --- |
    | msp | $\max_c softmax(z)_c$ | 가장 높은 softmax 확률. 높을수록 ID-like |
    | maxlogit | $\max_c z_c$ | 가장 큰 logit 값. 높을수록 ID-like |
    | energy_id_score | $T * log\sum exp(z / T), 여기서는 보통 T=1$ | logit 전체 크기를 보는 ID-like energy score. 높을수록 ID-like |
    | neg_entropy | $-H(softmax(z))$ | softmax entropy의 음수. 분포가 뾰족할수록 높음, 즉 높을수록 ID-like |
    
    **Overconfidence가 꼭 MSP/Energy OOD 성능을 망치지는 않는다**
    
    핵심은 calibration과 OOD detection이 다른 질문을 묻는다는 점이다.
    
    Calibration은 이렇게 묻는다.
    
    > ID test에서 모델이 0.95 confidence라고 말한 샘플들이 실제로도 약 95% 맞는가?
    > 
    
    OOD detection은 이렇게 묻는다.
    
    > ID sample의 score가 OOD sample의 score보다 전반적으로 더 높은가?
    > 
    
    즉 calibration은 **확률값의 절대적 신뢰도**를 보고, OOD AUROC는 **ID와 OOD score의 상대적 순위 분리**를 본다.
    
    예를 들어 AdamW가 ID sample에 대해 confidence를 너무 높게 낸다고 하자.
    
    `ID confidence: 0.99, 0.98, 0.97 ...
    실제 ID accuracy: 0.95 정도`
    
    이러면 calibration 관점에서는 overconfidence이다.
    
    그런데 OOD sample에 대해서는 confidence가 더 낮게 나온다면:
    
    `OOD confidence: 0.80, 0.75, 0.70 ...`
    
    OOD detection은 잘 될 수 있다. 왜냐하면 AUROC는 “0.99가 정말 99% 맞는가?”를 보지 않고, **ID score가 OOD score보다 높은가**를 보기 때문이다.
    
    반대로 OOD에도 confidence를 높게 주면 망한다.
    
    `ID confidence: 0.99
    OOD confidence: 0.98`
    
    이 경우는 calibration도 나쁘고 OOD 분리도 나쁠 수 있다.
    
    **현재 실험에서의 해석**
    
    AdamW는 ID calibration 관점에서 보면 좋지 않다.
    
    `AdamW ID test acc = 0.9468
    AdamW NLL = 0.5234
    AdamW ECE = 0.0451
    AdamW T = 5.1008`
    
    이건 raw logits가 과하게 커져서 softmax confidence가 너무 강하게 나왔을 가능성을 보여준다. 그런데 logit OOD에서는 다른 일이 일어날 수 있다. AdamW의 ID logits가 커졌더라도, OOD logits는 상대적으로 덜 커졌다면 energy나 maxlogit 기준으로 ID/OOD 분리가 좋아진다.
    
    특히 energy와 maxlogit은 확률 calibration 자체보다 **logit 크기와 logit magnitude separation**에 가깝다. 그래서 raw probability가 잘 calibrated되지 않았더라도, ID와 OOD 사이의 logit 크기 차이가 크면 OOD AUROC는 좋아질 수 있다. 또 energy와 maxlogit 값이 거의 비슷하게 움직이는 것도 자연스럽다. logit 하나가 지배적으로 크면:
    
    `logsumexp(z) ≈ max(z)`가 되기 때문이다. 현재 표에서도 energy와 maxlogit AUROC가 거의 같은 경우가 많다.
    
    **MSP는 조금 더 조심해서 봐야 한다**
    
    MSP는 softmax 확률이라 calibration과 더 가까워 보이지만, 이것도 ECE와 같은 것은 아니다.
    
    - ECE: ID에서 confidence와 실제 정답률이 맞는지
    - MSP OOD: ID의 max softmax가 OOD의 max softmax보다 높은지
    
    그래서 MSP도 overconfidence와 반드시 같은 방향으로 움직이지 않는다.
    
    AdamW가 ID에서 overconfident하더라도, OOD에서는 MSP가 충분히 낮으면 MSP OOD는 잘 된다.
    
    다만 현재 결과를 보면 AdamW의 MSP가 항상 좋은 것은 아니다.
    
    - CIFAR100: AdamW msp=0.8432, SGD 0.8721, Adam wd>0 0.8814
    - TinyImageNet: AdamW msp=0.8429, SGD 0.8630, Adam wd>0 0.8751
    - SVHN: AdamW msp=0.9012, SGD 0.9316
    - MNIST: AdamW msp=0.9476, 가장 좋음
    
    즉 AdamW의 MSP는 **MNIST에서는 좋지만 CIFAR100/Tiny/SVHN에서는 최고가 아니다.**
    
    반면 energy/maxlogit은 CIFAR100, TinyImageNet, MNIST에서 꽤 강하게 나온다.
    
    AdamW는 ID calibration 관점에서는 raw logits가 과하게 커져 overconfidence를 보인 정황이 있다. 그러나 logit-based OOD AUROC는 calibration 자체가 아니라 ID와 OOD 사이의 score ranking을 평가한다. 따라서 AdamW가 ID에서 overconfident하더라도 OOD sample의 logit score가 ID보다 충분히 낮으면 Energy나 MaxLogit OOD 성능은 좋게 나올 수 있다. 즉 uncalibrated confidence와 logit OOD separability는 연결되어 있지만 동일한 개념은 아니다.
    
    **다음에 확인하면 좋은 것**
    
    진짜 원인을 보려면 AUROC만으로는 부족하다. 다음 표나 그림이 있으면 좋다.
    
    - ID vs OOD energy_id_score histogram
    - ID vs OOD maxlogit histogram
    - ID vs OOD msp histogram
    - 각 detector별 ID score mean/quantile, OOD score mean/quantile
    - temperature scaling 전후 MSP OOD AUROC 변화
    
    특히 마지막이 중요하다. AdamW의 overconfidence가 단순 logit scale 문제라면, temperature scaling 후 MSP 분포가 어떻게 바뀌는지 보면 calibration과 OOD ranking의 관계를 더 명확히 볼 수 있다.
    

## 3. 기하지표

**Geometry scale / variance 표**

| **비교축** | **후보** | **within_var** | **inter_dist_l2** | **inter_dist_sq** | **anisotropy_lambda1_trace** | **effective_rank** | **condition_number_clipped** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 17.9139 | 14.3289 | 205.7676 | 0.1074 | 57.1476 | 9758.3727 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 27.2086 | 10.5331 | 111.3681 | 0.0809 | 54.6972 | 66658.1093 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 23.7590 | 13.4176 | 181.4323 | 0.1048 | 25.3559 | 4.9967e+07 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 9.8855 | 5.3713 | 29.2496 | 0.0860 | 70.0626 | 6.5344e+11 |

**Neural Collapse 표**

| **비교축** | **후보** | **nc0_width_norm** | **nc0_by_K** | **nc1** | **nc2_mean_cos** | **nc2_mean_etf** | **nc2_weight_etf** | **nc2_product_etf** | **nc3_cos_alignment** | **nc3_self_duality** | **nc3_self_duality_raw** | **nc4_agreement** |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 2.7041e-10 | 1.7306e-08 | 0.0682 | -0.1107 | 0.0020 | 0.0014 | 0.0015 | 0.9371 | 5.6619e-05 | 0.3624 | 0.9958 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 0.6924 | 44.3105 | 0.2279 | -0.1106 | 0.0029 | 0.0037 | 0.0029 | 0.8108 | 9.6968e-05 | 0.6206 | 0.9757 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 0.0132 | 0.8476 | 0.1874 | -0.1103 | 0.0044 | 0.0023 | 0.0032 | 0.9069 | 6.7779e-05 | 0.4338 | 0.9846 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 9.9058 | 633.9682 | 0.2713 | -0.1088 | 0.0052 | 0.0034 | 0.0034 | 0.6114 | 0.0001 | 0.8879 | 0.9634 |

**Feature norm diagnostic 표**

| **비교축** | **후보** | **feature norm train** | **cifar100 norm** | **tiny_imagenet norm** | **svhn norm** | **mnist norm** |
| --- | --- | --- | --- | --- | --- | --- |
| SGD best val | sgd_lr1e-1_wd2e-4 | 12.9345 | 12.8413 | 12.9489 | 12.3441 | 10.5349 |
| Adam wd=0 best val | adam_lr1e-3_wd0 | 12.8889 | 10.2114 | 9.9061 | 8.3884 | 6.0168 |
| Adam wd>0 best val | adam_lr1e-3_wd1e-4 | 14.5228 | 13.6773 | 13.3638 | 13.4653 | 7.9431 |
| AdamW best val | adamw_lr5e-3_wd1e-4 | 6.2890 | 4.5358 | 4.4196 | 4.5663 | 2.5574 |

## 3.1 기하지표와 Feature OOD 분석

### 핵심 수치 요약

**Feature OOD 평균 AUROC 요약**

| **비교축** | **raw Mahalanobis** | **Mahalanobis L2** | **raw kNN** | **kNN L2** | **GMM tied** | **GMM diag** | **GMM shrinkage** |
| --- | --- | --- | --- | --- | --- | --- | --- |
| SGD best val | 0.9092 | 0.9242 | 0.9188 | 0.9233 | 0.9092 | 0.9047 | 0.9238 |
| Adam wd=0 best val | 0.6764 | 0.9351 | 0.8730 | 0.9446 | 0.6763 | 0.8431 | 0.8575 |
| Adam wd>0 best val | 0.5531 | 0.8148 | 0.8692 | 0.8904 | 0.5527 | 0.7964 | 0.7340 |
| AdamW best val | 0.4719 | 0.9226 | 0.6538 | 0.9418 | 0.4716 | 0.7724 | 0.7798 |

**기하/feature norm 요약**

| **비교축** | **nc1** | **nc3_cos_alignment** | **inter_dist_l2** | **condition_number** | **train feature norm** | **MNIST norm** |
| --- | --- | --- | --- | --- | --- | --- |
| SGD best val | 0.0682 | 0.9371 | 14.3289 | 9.76e3 | 12.9345 | 10.5349 |
| Adam wd=0 best val | 0.2279 | 0.8108 | 10.5331 | 6.67e4 | 12.8889 | 6.0168 |
| Adam wd>0 best val | 0.1874 | 0.9069 | 13.4176 | 5.00e7 | 14.5228 | 7.9431 |
| AdamW best val | 0.2713 | 0.6114 | 5.3713 | 6.53e11 | 6.2890 | 2.5574 |

### 1. SGD는 raw feature detector가 이미 안정적이다

SGD best val은 `nc1=0.0682`로 가장 낮고, `nc3_cos_alignment=0.9371`, `nc4_agreement=0.9958`로 NC 관련 구조가 가장 안정적으로 보인다. 이와 함께 raw Mahalanobis, raw kNN, GMM tied, GMM shrinkage가 모두 약 `0.90` 이상이다.

또 SGD에서는 L2 normalization의 이득이 작다. Mahalanobis는 `0.9092 -> 0.9242`, kNN은 `0.9188 -> 0.9233` 정도만 상승한다. 즉 SGD feature에서는 raw feature norm과 covariance scale이 detector를 크게 방해하지 않는 것으로 보인다.

### 2. Adam/AdamW에서는 raw Mahalanobis와 GMM tied가 크게 약해진다

Adam wd=0, Adam wd>0, AdamW 모두에서 raw Mahalanobis와 GMM tied가 SGD보다 크게 낮다. 특히 AdamW best val은 raw Mahalanobis `0.4719`, GMM tied `0.4716`까지 떨어진다. GMM tied가 Mahalanobis와 거의 같은 방향으로 움직이는 이유는 두 방법 모두 class mean과 shared covariance 구조에 강하게 의존하기 때문이다.

이 결과는 Adam/AdamW feature가 raw Mahalanobis 계열의 가정과 잘 맞지 않는다는 신호로 볼 수 있다. 특히 AdamW는 `condition_number=6.53e11`로 covariance geometry가 매우 불안정하고, `inter_dist_l2=5.3713`으로 class mean 간 거리가 작으며, `nc3_cos_alignment=0.6114`로 classifier weight와 feature mean의 정렬도 약하다. 이 조합은 raw feature distance와 covariance inverse를 사용하는 detector에 불리하다.

### 3. 하지만 Feature OOD 자체가 실패했다고 말하면 안 된다

가장 중요한 점은 L2-normalized detector가 크게 회복된다는 것이다.

- AdamW Mahalanobis: `0.4719 -> 0.9226`
- AdamW kNN: `0.6538 -> 0.9418`
- Adam wd=0 Mahalanobis: `0.6764 -> 0.9351`
- Adam wd=0 kNN: `0.8730 -> 0.9446`

따라서 현재 결과는 “Adam/AdamW에서는 feature-based OOD가 안 된다”가 아니다. 더 정확히는 “Adam/AdamW에서는 raw feature norm과 covariance scale에 민감한 detector가 크게 손상되지만, feature L2 normalization을 적용하면 Mahalanobis와 kNN이 강하게 회복된다”이다.

### 4. Feature norm 차이가 detector 성능 변화와 강하게 연결된다

Feature norm 표를 보면 SGD는 train norm과 OOD norm이 비교적 가깝다. 예를 들어 SGD는 train norm `12.9345`, CIFAR100 norm `12.8413`, TinyImageNet norm `12.9489`, SVHN norm `12.3441`, MNIST norm `10.5349`이다.

반면 AdamW는 전체 feature norm scale이 작고, OOD norm이 train norm보다 훨씬 작다. AdamW는 train norm `6.2890`인데 MNIST norm은 `2.5574`, CIFAR100은 `4.5358`, TinyImageNet은 `4.4196`, SVHN은 `4.5663`이다.

이런 norm 차이는 raw Euclidean distance, raw Mahalanobis distance, raw density score에 직접 영향을 줄 수 있다. L2 normalization은 feature의 길이 정보를 제거하고 방향 정보를 중심으로 비교하게 만들기 때문에, AdamW에서 Mahalanobis와 kNN이 크게 회복되는 패턴은 feature norm/covariance-scale 효과가 주요 원인 후보임을 보여준다.

### 5. dataset별로 보면 MNIST에서 L2 회복이 가장 극단적이다

MNIST Feature 표에서 AdamW는 raw Mahalanobis `0.2712`, raw kNN `0.5423`으로 매우 낮다. 그러나 L2를 적용하면 Mahalanobis L2 `0.9984`, kNN L2 `0.9955`까지 회복된다. Adam wd=0도 MNIST에서 raw Mahalanobis `0.6301`에서 Mahalanobis L2 `0.9996`으로 오른다.

이 패턴은 MNIST가 CIFAR-10 feature space에서 norm 차이를 크게 유발하고, raw distance 기반 detector가 그 scale 차이를 잘못 읽을 수 있음을 시사한다. 다만 이 해석을 확정하려면 score histogram이나 ID/OOD feature norm distribution plot이 추가로 필요하다.

### 6. Neural Collapse 해석은 조심해야 한다

현재 결과는 Adam/AdamW에서 NC 관련 지표가 약해지는 방향과 raw feature OOD detector 저하가 함께 나타난다는 점을 보여준다. 예를 들어 AdamW는 `nc1`이 가장 높고, `nc3_cos_alignment`가 가장 낮으며, `inter_dist_l2`도 가장 작다. 동시에 raw Mahalanobis, raw kNN, GMM tied가 크게 낮다.

하지만 “NC가 덜 일어나서 feature OOD가 무너졌다”라고 단정하기에는 아직 이르다. L2 normalization만으로 Mahalanobis와 kNN이 크게 회복되기 때문이다. 그러므로 이번 결과는 NC 약화 하나로 설명하기보다는, optimizer가 만든 feature geometry 변화 중 feature norm, covariance scale, class mean separation, classifier-feature alignment가 detector별로 다르게 작용한다고 해석하는 것이 더 안전하다.

### 보고용 결론 문장

이번 WRN-28-10 seed0 grid-search에서는 SGD가 가장 NC-like한 feature geometry를 보이며 raw feature-based OOD detector도 안정적으로 동작했다. 반면 Adam/AdamW, 특히 AdamW에서는 `nc1` 증가, class mean 간 거리 감소, classifier-feature alignment 약화, covariance condition number 증가가 관찰되며 raw Mahalanobis, raw kNN, GMM tied 성능이 크게 저하되었다. 그러나 L2 feature normalization을 적용한 Mahalanobis와 kNN은 Adam/AdamW에서도 크게 회복되었다. 따라서 feature OOD 성능 저하는 단순히 “feature detector가 Adam/AdamW에서 실패한다”는 의미가 아니라, optimizer-induced feature geometry가 raw norm/covariance-sensitive detector의 가정과 충돌하고, detector-side normalization이 이를 상당 부분 완화한다는 의미로 해석하는 것이 적절하다.

### 주의할 claim

- 말해도 되는 것: Adam/AdamW에서 raw Mahalanobis와 GMM tied가 약해지고, L2-normalized Mahalanobis/kNN이 크게 회복된다.
- 말해도 되는 것: 이 회복은 feature norm 또는 covariance-scale 효과가 feature OOD 성능에 중요하다는 것을 시사한다.
- 조심해야 하는 것: “NC가 덜 일어나서 OOD가 무너졌다”라고 단정하는 표현.
- 조심해야 하는 것: 현재 `mahalanobis_l2`를 Mahalanobis++의 완전 재현이라고 부르는 표현. 여기서는 Mahalanobis++-motivated normalization control로 부르는 것이 안전하다.

### 다음 확인하면 좋은 것

- ID test와 각 OOD dataset의 Mahalanobis, Mahalanobis L2, kNN, kNN L2 score histogram
- ID/OOD feature norm distribution plot
- covariance eigenspectrum과 condition number 비교
- L2-normalized feature에서 geometry metric을 다시 계산한 표
- seed0/1/2 반복 실험에서 같은 패턴이 유지되는지 확인

**판정 먼저**

현재 결과는 논문 Optimizer choice matters for the emergence of Neural Collapse와 **큰 방향에서 정합적**입니다. 특히 다음 축이 잘 맞습니다.

- SGD: 가장 NC-like한 geometry.
- Adam with coupled WD: SGD보다는 약하지만 AdamW보다 NC에 가까움.
- Adam wd=0: coupled WD가 없어서 NC가 약함.
- AdamW: decoupled WD adaptive optimizer라 NC0/NC3가 크게 약해짐.
- 단, AdamW도 NC2나 NC4 일부는 좋아 보일 수 있음. 그래서 “NC가 전혀 없다”보다는 **partial NC / NC metric split**으로 쓰는 게 안전합니다.

확인한 파일은 geometry_scalars.csv, diagnostic_summary.csv, paper_pdf_pages.md, SOURCE_CARD.md, factory.py (line 29)입니다.

**대표 모델 기준**

| 비교축 | NC0 | NC1 | NC3 align | NC4 | inter dist | condition |
| --- | --- | --- | --- | --- | --- | --- |
| SGD best | 2.7e-10 | 0.0682 | 0.9371 | 0.9958 | 14.33 | 9.76e3 |
| Adam wd=0 | 0.6924 | 0.2279 | 0.8108 | 0.9757 | 10.53 | 6.67e4 |
| Adam wd>0 | 0.0132 | 0.1874 | 0.9069 | 0.9846 | 13.42 | 5.00e7 |
| AdamW best | 9.9058 | 0.2713 | 0.6114 | 0.9634 | 5.37 | 6.53e11 |

**옵티마이저별 해석**

SGD는 논문과 가장 잘 맞습니다. 논문은 SGD에서 weight decay가 NC0를 0으로 수축시키는 방향으로 작용한다고 설명합니다. 우리 실험에서도 SGD는 NC0≈0, 낮은 NC1, 높은 NC3 alignment, 높은 NC4를 보입니다. 즉 class 내부 분산이 상대적으로 작고, class mean과 classifier weight가 잘 정렬되어 있습니다.

Adam wd=0은 논문 관점에서 “NC가 잘 나오기 어려운 Adam”입니다. Adam 자체가 coupled WD를 쓸 때 NC에 가까워질 수 있다는 것이 논문의 주장인데, wd=0이면 그 구동력이 없습니다. 실제로 NC0=0.6924, NC1=0.2279, NC3=0.8108로 SGD보다 훨씬 덜 collapse되어 있습니다.

Adam wd>0은 흥미롭습니다. NC0=0.0132, NC3=0.9069로 Adam wd=0보다 크게 좋아집니다. 즉 coupled WD가 들어가면 Adam도 NC 방향으로 움직인다는 논문 주장과 맞습니다. 다만 NC1=0.1874, condition number 5.00e7이라 feature covariance는 여전히 SGD보다 불안정합니다. 그래서 “Adam도 NC가 된다”보다는 **coupled WD가 Adam의 NC0/NC3를 회복시키지만, feature covariance까지 SGD처럼 안정화되지는 않는다**가 더 정확합니다.

AdamW는 논문과 가장 직접적으로 맞는 결과입니다. 논문은 AdamW처럼 decoupled WD를 쓰는 adaptive optimizer에서 NC0/NC3가 크게 남고, true NC가 잘 발생하지 않는다고 주장합니다. 우리 결과도 NC0=9.9058, NC3 alignment=0.6114, inter_dist_l2=5.37, condition number 6.53e11로 같은 방향입니다.

**수학적 이유**

class logit이 z = W h(x)라고 합시다. cross-entropy의 마지막 layer gradient는 class 방향으로 합치면 대체로 0이 됩니다. 즉 row-sum s = W^T 1_K의 변화는 loss gradient 자체보다 weight decay 방식에 크게 좌우됩니다.

SGD나 coupled WD에서는 update에 ∇L + λW가 들어갑니다.

text

`W_{t+1} = W_t - η(∇L + λW_t)`

row-sum을 보면,

text

`s_{t+1} = W_{t+1}^T 1_K
        ≈ (1 - ηλ) s_t`

이므로 s_t가 지수적으로 0으로 줄어듭니다. 이게 NC0가 작아지는 핵심입니다. 논문도 SGD coupled/decoupled WD에서 NC0가 0으로 수렴한다고 정리합니다.

AdamW는 다릅니다. decoupled WD라서 대략

text

`W_{t+1} = (1 - ηλ) W_t - η D_t ∇L`

처럼 됩니다. 여기서 D_t는 Adam의 coordinate-wise adaptive preconditioner입니다. 원래 ∇L^T 1_K = 0에 가까워도, D_t ∇L은 class/coordinate마다 다르게 스케일되므로 row-sum 보존이 깨질 수 있습니다. decoupled WD는 W를 전체적으로 줄이기만 하고, λW를 adaptive gradient 안에 넣지 않으므로 NC0를 직접 0으로 몰아가는 효과가 약합니다.

그래서 AdamW에서는 W^T 1_K가 크게 남고, 이것이 NC3 self-duality 실패로 이어질 수 있습니다. 우리 결과의 AdamW NC0 높음과 NC3 alignment 낮음은 바로 이 구조와 맞습니다.

**중요한 주의점**

AdamW의 nc2_mean_cos=-0.1088은 CIFAR-10 simplex target -1/(K-1)=-1/9≈-0.1111에 꽤 가깝습니다. 또한 NC4=0.9634도 높습니다. 이것만 보면 AdamW도 collapse된 것처럼 보일 수 있습니다.

하지만 논문도 이 지점을 경고합니다. NC metric은 함께 움직이지 않을 수 있고, AdamW가 NC1/NC2 일부는 좋아 보여도 NC0/NC3가 실패하는 **partial Neural Collapse**가 가능하다고 설명합니다. 우리 결과도 딱 그 형태입니다. 따라서 AdamW에 대해 “NC가 없다”라고 단정하기보다:

> AdamW는 class-mean angular structure나 NCC agreement 일부는 유지하지만, NC0와 classifier-feature self-duality가 크게 약한 partial NC regime을 보인다.
> 

이 표현이 가장 안전합니다.

**보고용 결론**

이번 WRN-28-10 CIFAR-10 seed0 grid-search에서 optimizer별 geometry는 참고 논문의 핵심 주장과 정합적이다. SGD는 NC0, NC1, NC3, NC4가 모두 가장 안정적인 NC-like geometry를 보인다. Adam은 coupled weight decay가 있을 때 NC0와 NC3가 회복되지만, feature covariance condition은 여전히 불안정하다. AdamW는 decoupled weight decay adaptive optimizer의 특성상 NC0가 크게 남고 classifier-feature self-duality가 약하며, class mean separation도 작다. 이는 논문에서 제시한 “coupled weight decay가 adaptive optimizer에서 NC emergence의 핵심 축”이라는 주장과 일치한다.