0611 23:28분기준 poster.pdf강화방안(통계학회 포스터)
핵심은 “Adam/AdamW가 다르다”를 직관 문장으로만 말하지 말고, weight decay가 adaptive update 안에 들어가느냐/밖에 있느냐가 NC/feature geometry 동역학을 바꾼다는 점입니다. 단, 이 논문은 optimizer → Neural Collapse / representation geometry 근거로 쓰고, Mahalanobis/kNN/OOD 성능 저하의 직접 증명으로 쓰면 안 됩니다. 이 source boundary는 프로젝트 source에도 명시되어 있습니다.

현재 poster.tex의 Optimizer 섹션은 업데이트 식과 직관은 있지만, 왜 그 update rule 차이가 geometry 차이로 이어지는지가 한 단계 비어 있습니다. Optimizer choice matters... 논문에서 포스터에 가져올 만한 연결고리는 아래입니다.

첫째, 이 논문은 NC를 마지막층 feature와 classifier weight가 만드는 기하구조로 보고, optimizer choice가 NC emergence에 중요한 역할을 한다고 말합니다. 특히 NC0를 NC의 필요조건으로 두고, decoupled weight decay를 쓰는 adaptive optimizer에서 NC가 나타나기 어렵다는 이론 근거를 제시합니다.

둘째, 핵심 수학적 장치는 last-layer weight row-sum입니다. Cross-entropy에서 마지막층 loss gradient의 row-sum은 0이 되므로, NC0 동역학은 loss gradient보다 weight decay와 optimizer update 방식에 의해 크게 좌우됩니다. 논문은 SGD/L2에서 W
t+1
	

=(1−ηλ)W
t
	

−ηV
t+1
	

이고, α
t
	

=
K
1
	

∥W
t
⊤
	

1∥
2
2
	

가 지수적으로 0으로 감소한다고 설명합니다.

셋째, Adam/AdamW에서 중요한 점은 L2 regularization과 decoupled weight decay가 더 이상 같은 것이 아니라는 점입니다. 논문은 이 equivalence가 vanilla SGD에서는 성립하지만 Adam/AdamW 같은 adaptive optimizer나 momentum이 있을 때는 성립하지 않는다고 지적합니다. 즉, Adam은 λw
t
	

가 adaptive scaling 안으로 들어가고, AdamW는 adaptive gradient step 뒤에 별도 shrinkage를 적용합니다.

넷째, 논문에서 포스터용으로 가장 좋은 evidence는 AdamW-to-Adam interpolation입니다. total weight decay를 고정하고 coupled component만 늘리면 NC0, NC2, NC3가 부드럽게 개선되지만 validation accuracy는 크게 변하지 않습니다. 이건 “accuracy가 비슷해도 geometry는 달라질 수 있다”는 우리 포스터 메시지와 매우 잘 맞습니다.

# 추천 본문 ver1
## Optimizers: Update Rules and Geometry Intuition

Optimizer는 loss를 줄이는 절차이지만, 동시에 feature geometry를 형성하는 implicit bias를 만든다. 핵심 차이는 gradient scaling과 weight decay가 결합되는 방식이다.

Let (g_t=\nabla_w L(w_t)).

[
\text{SGD/L2:}\quad
w_{t+1}=(1-\eta\lambda)w_t-\eta g_t
]

[
\text{Adam/L2:}\quad
\tilde g_t=g_t+\lambda w_t,\quad
w_{t+1}=w_t-\eta\frac{\hat m_t(\tilde g)}{\sqrt{\hat v_t(\tilde g)}+\epsilon}
]

[
\text{AdamW:}\quad
w_{t+1}=(1-\eta\lambda)w_t-\eta\frac{\hat m_t(g)}{\sqrt{\hat v_t(g)}+\epsilon}
]

SGD/L2에서는 weight decay가 모든 방향에 비교적 직접적인 shrinkage로 작용한다. Adam/L2에서는 (\lambda w_t)가 gradient에 더해진 뒤 first/second moment를 통해 좌표별로 adaptive scaling된다. AdamW에서는 gradient moment는 (g_t)만으로 계산하고, weight decay는 update 밖에서 별도 shrinkage로 적용된다.

이 차이는 단순한 학습 속도 차이가 아니다. Neural Collapse 관점에서 optimizer와 weight-decay coupling은 class feature compactness, class-mean geometry, classifier-feature alignment 같은 representation geometry를 다르게 만들 수 있다. 따라서 비슷한 ID accuracy에 도달하더라도, optimizer/LR/WD가 만든 penultimate feature geometry는 post-hoc feature detector가 보는 score landscape를 바꿀 수 있다.

# 추천 본문 ver2
## Mini Mechanism Box: Weight-Decay Coupling Changes NC Geometry

For the last-layer weight (W_t), define the NC0 row-sum metric

[
\alpha_t=\frac{1}{K}|W_t^\top \mathbf{1}_K|_2^2.
]

Cross-entropy has a zero row-sum gradient:

[
(\nabla_W L_{\mathrm{CE}})^\top \mathbf{1}_K=0.
]

Thus the evolution of (\alpha_t) is driven mainly by optimizer and weight decay dynamics. Under SGD/L2,

[
W_{t+1}=(1-\eta\lambda)W_t-\eta V_{t+1}
\quad\Rightarrow\quad
\alpha_{t+1}\approx (1-\eta\lambda)^2\alpha_t.
]

So weight decay contracts the classifier row-sum toward the NC0 condition. In adaptive optimizers, however, putting (\lambda W_t) inside the adaptive update or applying it outside as decoupled shrinkage changes the geometry trajectory. This gives a mathematical reason why Adam and AdamW can reach similar accuracy while inducing different feature/classifier geometry.

포스터 본문에 들어갈 분량을 생각하면, 저는 첫 번째 본문 + Mini Mechanism Box의 첫 두 줄만 추천합니다. 즉 실제 A0에는 아래 정도로 압축하는 게 좋습니다.

Key mechanism: For cross-entropy last-layer weights, the loss-gradient row sum is zero. Therefore the NC0 row-sum geometry is driven by optimizer/weight-decay dynamics. In SGD/L2, weight decay contracts NC0 toward zero; in Adam vs AdamW, the same λW term is either inside or outside adaptive scaling, changing the geometry trajectory.

여기서 조심할 표현은 세 가지입니다.

AdamW causes Mahalanobis collapse는 쓰지 않는 게 좋습니다. 대신 **“AdamW-style decoupled weight decay can induce a different NC/feature-geometry trajectory”**라고 쓰세요.

Neural Collapse weakening alone causes OOD failure도 피해야 합니다. 대신 **“NC/geometry differences provide a plausible mechanism; OOD link is evaluated by our post-hoc diagnostics”**가 안전합니다.

AdamW is bad도 피해야 합니다. 논문 자체도 AdamW-to-Adam interpolation에서 validation accuracy는 크게 변하지 않지만 NC metrics가 달라진다고 말하므로, 포스터 메시지는 **“accuracy and geometry can decouple”**입니다.

검증한 것은 업로드된 poster.tex의 현재 Optimizer 섹션, poster_section_text.md, 그리고 paper.pdf / paper_pdf_pages.md의 NC0, weight-decay coupling, AdamW-to-Adam interpolation 부분입니다. 검증하지 못한 것은 이 새 문장이 실제 포스터 레이아웃에서 얼마나 들어가는지와, 현재 너의 WRN 실험에서 NC0까지 안정적으로 표에 넣을 수 있는지입니다.