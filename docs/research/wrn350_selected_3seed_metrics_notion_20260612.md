# WRN-28-10 Selected 3-Seed Metric Summary for Notion

작성일: 2026-06-12 KST



이 문서는 `wrn350_selected_3seed_raw_eval_results_20260612`의 raw evaluation JSON을 기준으로, 선택된 5개 WRN-28-10/CIFAR-10 config의 metric을 3 seeds `mean +/- std`로 정리한 Notion import용 markdown이다.



핵심 원칙:



- 모든 `std`는 sample standard deviation, 즉 `ddof=1`이다.

- OOD metric은 `cifar100`, `tiny_imagenet`, `svhn`, `mnist`별로만 정리한다. 서로 다른 OOD dataset 간 평균은 이 문서의 OOD 표에 넣지 않는다.

- SGD와 AdamW는 선택 config가 각각 2개이므로 optimizer 안에서 LR/WD config별 행을 유지한다. config끼리 추가 평균내지 않는다.

- 모든 OOD score convention은 `higher score = more ID-like`, `ID label = 1`, `OOD label = 0`이다.

- `gmm_ddu_*`는 `DDU-style GMM feature density` 진단으로만 해석한다. 원 DDU 전체 reproduction이라고 쓰지 않는다.



## Source and Evidence Boundary

| Item | Value |
| --- | --- |
| Package | wrn350_selected_3seed_raw_eval_results_20260612 |
| Created at | 2026-06-12T21:02:59+09:00 |
| Model | WideResNet-28-10 dropout 0.3 |
| ID dataset | CIFAR-10 |
| OOD datasets | cifar100, tiny_imagenet, svhn, mnist |
| Seed0 source | /home/ghjin/2027ICLR/2027ICLR/results/WRN_seed0_350eps_girdsearch_0531.zip |
| Seed1/2 manifest | /home/ghjin/2027ICLR/2027ICLR/results/manifests/wrn350_selected_seed1_seed2_20260611_1142.json |



## Configs Included

| Optimizer | Config | LR | WD | Seeds | Checkpoint tags |
| --- | --- | --- | --- | --- | --- |
| SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0, 1, 2 | epoch_0350, final |
| SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0, 1, 2 | epoch_0350 |
| Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0, 1, 2 | epoch_0350 |
| AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0, 1, 2 | epoch_0350 |
| AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0, 1, 2 | epoch_0350 |



## Validation, ID Test, and Calibration

| Opt | Config | LR | WD | Best val epoch | Best val acc | Final val acc | ID test acc | ID test NLL | ECE | T-ECE | Temp. |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 336.3333 +/- 11.5902 | 0.9631 +/- 0.0039 | 0.9615 +/- 0.0040 | 0.9583 +/- 0.0016 | 0.2052 +/- 0.0113 | 0.0295 +/- 0.0011 | 0.0085 +/- 0.0018 | 1.8845 +/- 0.0575 |
| SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 314.0000 +/- 31.7962 | 0.9627 +/- 0.0015 | 0.9612 +/- 0.0019 | 0.9558 +/- 0.0014 | 0.2333 +/- 0.0027 | 0.0321 +/- 0.0014 | 0.0087 +/- 0.0011 | 2.0932 +/- 0.0581 |
| Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 296.0000 +/- 46.6798 | 0.9521 +/- 0.0032 | 0.9488 +/- 0.0036 | 0.9449 +/- 0.0010 | 0.2852 +/- 0.0112 | 0.0392 +/- 0.0006 | 0.0066 +/- 0.0009 | 2.4800 +/- 0.0545 |
| AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 243.3333 +/- 34.3560 | 0.9523 +/- 0.0009 | 0.9495 +/- 0.0008 | 0.9447 +/- 0.0024 | 0.5268 +/- 0.0048 | 0.0465 +/- 0.0020 | 0.0062 +/- 0.0015 | 5.0191 +/- 0.1098 |
| AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 280.0000 +/- 77.6724 | 0.9506 +/- 0.0022 | 0.9480 +/- 0.0025 | 0.9436 +/- 0.0002 | 0.5259 +/- 0.0157 | 0.0476 +/- 0.0005 | 0.0060 +/- 0.0007 | 5.1120 +/- 0.1150 |



## OOD Metrics by Dataset

아래 표들은 OOD dataset별로 분리되어 있다. `AUROC`, `FPR95`, `AUPR-IN` 각각은 같은 OOD dataset 안에서만 seed0/1/2 평균과 표준편차를 계산했다.

### OOD dataset: `cifar100`

| Family | Detector | Opt | Config | LR | WD | AUROC | FPR95 | AUPR-IN | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logit | msp | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8766 +/- 0.0053 | 0.5579 +/- 0.0219 | 0.8584 +/- 0.0104 | 3 |
| logit | msp | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8727 +/- 0.0008 | 0.5795 +/- 0.0053 | 0.8600 +/- 0.0010 | 3 |
| logit | msp | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8817 +/- 0.0048 | 0.6329 +/- 0.0333 | 0.9075 +/- 0.0027 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8429 +/- 0.0005 | 0.6522 +/- 0.0087 | 0.9381 +/- 0.0020 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8442 +/- 0.0028 | 0.6558 +/- 0.0178 | 0.9390 +/- 0.0008 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8570 +/- 0.0051 | 0.4713 +/- 0.0149 | 0.8151 +/- 0.0108 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8482 +/- 0.0022 | 0.4894 +/- 0.0184 | 0.8066 +/- 0.0028 | 3 |
| logit | maxlogit | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8995 +/- 0.0033 | 0.4933 +/- 0.0136 | 0.9027 +/- 0.0038 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9020 +/- 0.0022 | 0.5475 +/- 0.0025 | 0.9142 +/- 0.0030 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9031 +/- 0.0018 | 0.5383 +/- 0.0064 | 0.9140 +/- 0.0028 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8572 +/- 0.0052 | 0.4684 +/- 0.0119 | 0.8152 +/- 0.0109 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8483 +/- 0.0022 | 0.4886 +/- 0.0179 | 0.8065 +/- 0.0028 | 3 |
| logit | energy_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8996 +/- 0.0032 | 0.4943 +/- 0.0120 | 0.9027 +/- 0.0037 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9020 +/- 0.0022 | 0.5485 +/- 0.0007 | 0.9142 +/- 0.0030 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9031 +/- 0.0018 | 0.5378 +/- 0.0037 | 0.9140 +/- 0.0028 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8775 +/- 0.0052 | 0.5505 +/- 0.0173 | 0.8555 +/- 0.0116 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8735 +/- 0.0008 | 0.5703 +/- 0.0050 | 0.8528 +/- 0.0002 | 3 |
| logit | neg_entropy | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8850 +/- 0.0045 | 0.6237 +/- 0.0331 | 0.8997 +/- 0.0032 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8898 +/- 0.0021 | 0.6512 +/- 0.0083 | 0.9101 +/- 0.0019 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8905 +/- 0.0008 | 0.6533 +/- 0.0170 | 0.9093 +/- 0.0024 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8700 +/- 0.0029 | 0.5716 +/- 0.0153 | 0.8718 +/- 0.0020 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8618 +/- 0.0027 | 0.6141 +/- 0.0066 | 0.8673 +/- 0.0014 | 3 |
| feature | mahalanobis | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.5779 +/- 0.0087 | 0.9420 +/- 0.0020 | 0.6088 +/- 0.0111 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.4402 +/- 0.0144 | 0.9610 +/- 0.0068 | 0.4597 +/- 0.0088 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.4388 +/- 0.0150 | 0.9598 +/- 0.0083 | 0.4613 +/- 0.0102 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8905 +/- 0.0011 | 0.4627 +/- 0.0118 | 0.8793 +/- 0.0023 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8750 +/- 0.0007 | 0.5283 +/- 0.0131 | 0.8661 +/- 0.0016 | 3 |
| feature | mahalanobis_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7230 +/- 0.0057 | 0.8208 +/- 0.0078 | 0.7255 +/- 0.0060 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8518 +/- 0.0021 | 0.5830 +/- 0.0141 | 0.8511 +/- 0.0016 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8535 +/- 0.0061 | 0.5888 +/- 0.0168 | 0.8525 +/- 0.0070 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9061 +/- 0.0010 | 0.4856 +/- 0.0081 | 0.9110 +/- 0.0010 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9040 +/- 0.0010 | 0.4869 +/- 0.0056 | 0.9107 +/- 0.0004 | 3 |
| feature | knn | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8542 +/- 0.0019 | 0.6686 +/- 0.0112 | 0.8631 +/- 0.0026 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.5875 +/- 0.0268 | 0.9385 +/- 0.0060 | 0.6061 +/- 0.0259 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.6053 +/- 0.0203 | 0.9358 +/- 0.0041 | 0.6304 +/- 0.0186 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9073 +/- 0.0010 | 0.4635 +/- 0.0104 | 0.9062 +/- 0.0017 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9050 +/- 0.0004 | 0.4772 +/- 0.0075 | 0.9054 +/- 0.0008 | 3 |
| feature | knn_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8810 +/- 0.0040 | 0.5703 +/- 0.0091 | 0.8886 +/- 0.0050 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8906 +/- 0.0033 | 0.5094 +/- 0.0088 | 0.8935 +/- 0.0049 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8907 +/- 0.0048 | 0.5032 +/- 0.0077 | 0.8923 +/- 0.0057 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8700 +/- 0.0029 | 0.5716 +/- 0.0153 | 0.8718 +/- 0.0020 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8618 +/- 0.0027 | 0.6141 +/- 0.0066 | 0.8673 +/- 0.0014 | 3 |
| feature | gmm_ddu_tied | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.5776 +/- 0.0087 | 0.9420 +/- 0.0019 | 0.6086 +/- 0.0111 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.4399 +/- 0.0144 | 0.9610 +/- 0.0068 | 0.4595 +/- 0.0088 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.4385 +/- 0.0150 | 0.9599 +/- 0.0082 | 0.4610 +/- 0.0102 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9085 +/- 0.0010 | 0.4997 +/- 0.0114 | 0.9153 +/- 0.0014 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9053 +/- 0.0023 | 0.5060 +/- 0.0188 | 0.9105 +/- 0.0009 | 3 |
| feature | gmm_ddu_diag | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8678 +/- 0.0027 | 0.6411 +/- 0.0084 | 0.8758 +/- 0.0040 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7900 +/- 0.0059 | 0.7657 +/- 0.0022 | 0.7924 +/- 0.0067 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.7954 +/- 0.0123 | 0.7733 +/- 0.0067 | 0.8019 +/- 0.0165 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9103 +/- 0.0010 | 0.4699 +/- 0.0164 | 0.9155 +/- 0.0010 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9066 +/- 0.0015 | 0.4908 +/- 0.0094 | 0.9123 +/- 0.0002 | 3 |
| feature | gmm_ddu_shrinkage | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8108 +/- 0.0087 | 0.7427 +/- 0.0107 | 0.8218 +/- 0.0092 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8112 +/- 0.0051 | 0.6926 +/- 0.0043 | 0.8052 +/- 0.0074 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8122 +/- 0.0073 | 0.7140 +/- 0.0106 | 0.8118 +/- 0.0091 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8911 +/- 0.0018 | 0.5405 +/- 0.0153 | 0.8930 +/- 0.0012 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8886 +/- 0.0015 | 0.5452 +/- 0.0094 | 0.8906 +/- 0.0010 | 3 |
| nc_hybrid | ncc_distance | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8473 +/- 0.0029 | 0.6745 +/- 0.0158 | 0.8531 +/- 0.0023 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.6895 +/- 0.0185 | 0.9561 +/- 0.0059 | 0.7195 +/- 0.0166 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.7082 +/- 0.0219 | 0.9516 +/- 0.0050 | 0.7407 +/- 0.0222 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8981 +/- 0.0015 | 0.5110 +/- 0.0147 | 0.8963 +/- 0.0023 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8948 +/- 0.0004 | 0.5126 +/- 0.0095 | 0.8925 +/- 0.0014 | 3 |
| nc_hybrid | nc_prototype_cosine | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8774 +/- 0.0045 | 0.5638 +/- 0.0144 | 0.8774 +/- 0.0048 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8772 +/- 0.0033 | 0.5622 +/- 0.0220 | 0.8828 +/- 0.0043 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8748 +/- 0.0087 | 0.5630 +/- 0.0155 | 0.8799 +/- 0.0081 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8902 +/- 0.0017 | 0.4475 +/- 0.0115 | 0.8725 +/- 0.0043 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8860 +/- 0.0012 | 0.4614 +/- 0.0092 | 0.8691 +/- 0.0021 | 3 |
| nc_hybrid | vim_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8696 +/- 0.0037 | 0.6191 +/- 0.0199 | 0.8795 +/- 0.0024 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8843 +/- 0.0009 | 1.0000 +/- 0 | 0.9298 +/- 0.0010 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8845 +/- 0.0029 | 1.0000 +/- 0 | 0.9281 +/- 0.0025 | 3 |

### OOD dataset: `tiny_imagenet`

| Family | Detector | Opt | Config | LR | WD | AUROC | FPR95 | AUPR-IN | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logit | msp | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8654 +/- 0.0018 | 0.5543 +/- 0.0177 | 0.8353 +/- 0.0036 | 3 |
| logit | msp | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8620 +/- 0.0011 | 0.5755 +/- 0.0075 | 0.8399 +/- 0.0027 | 3 |
| logit | msp | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8744 +/- 0.0054 | 0.6276 +/- 0.0341 | 0.9007 +/- 0.0036 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8408 +/- 0.0028 | 0.6393 +/- 0.0127 | 0.9385 +/- 0.0022 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8397 +/- 0.0021 | 0.6502 +/- 0.0169 | 0.9390 +/- 0.0011 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8524 +/- 0.0026 | 0.4493 +/- 0.0123 | 0.7988 +/- 0.0035 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8413 +/- 0.0035 | 0.4745 +/- 0.0171 | 0.7877 +/- 0.0049 | 3 |
| logit | maxlogit | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9010 +/- 0.0038 | 0.4527 +/- 0.0142 | 0.8985 +/- 0.0035 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8979 +/- 0.0015 | 0.5267 +/- 0.0082 | 0.9026 +/- 0.0026 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8989 +/- 0.0005 | 0.5184 +/- 0.0141 | 0.9033 +/- 0.0016 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8527 +/- 0.0026 | 0.4458 +/- 0.0080 | 0.7989 +/- 0.0035 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8415 +/- 0.0035 | 0.4727 +/- 0.0180 | 0.7878 +/- 0.0049 | 3 |
| logit | energy_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9012 +/- 0.0037 | 0.4524 +/- 0.0111 | 0.8986 +/- 0.0035 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8979 +/- 0.0015 | 0.5266 +/- 0.0083 | 0.9026 +/- 0.0026 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8989 +/- 0.0005 | 0.5177 +/- 0.0120 | 0.9033 +/- 0.0016 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8665 +/- 0.0018 | 0.5450 +/- 0.0139 | 0.8312 +/- 0.0038 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8630 +/- 0.0012 | 0.5668 +/- 0.0059 | 0.8292 +/- 0.0029 | 3 |
| logit | neg_entropy | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8785 +/- 0.0052 | 0.6169 +/- 0.0329 | 0.8858 +/- 0.0037 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8837 +/- 0.0025 | 0.6382 +/- 0.0138 | 0.8958 +/- 0.0018 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8837 +/- 0.0006 | 0.6476 +/- 0.0169 | 0.8954 +/- 0.0007 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8631 +/- 0.0016 | 0.5898 +/- 0.0182 | 0.8620 +/- 0.0019 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8590 +/- 0.0036 | 0.6278 +/- 0.0104 | 0.8614 +/- 0.0030 | 3 |
| feature | mahalanobis | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.5572 +/- 0.0143 | 0.9553 +/- 0.0068 | 0.5940 +/- 0.0131 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.3909 +/- 0.0185 | 0.9695 +/- 0.0056 | 0.4269 +/- 0.0102 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.3979 +/- 0.0035 | 0.9696 +/- 0.0072 | 0.4327 +/- 0.0048 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8818 +/- 0.0005 | 0.4587 +/- 0.0044 | 0.8637 +/- 0.0020 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8649 +/- 0.0015 | 0.5419 +/- 0.0143 | 0.8494 +/- 0.0007 | 3 |
| feature | mahalanobis_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7329 +/- 0.0044 | 0.8243 +/- 0.0162 | 0.7367 +/- 0.0067 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8610 +/- 0.0029 | 0.5628 +/- 0.0224 | 0.8593 +/- 0.0019 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8563 +/- 0.0052 | 0.5773 +/- 0.0215 | 0.8541 +/- 0.0057 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8997 +/- 0.0013 | 0.4813 +/- 0.0115 | 0.8993 +/- 0.0021 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9020 +/- 0.0018 | 0.4617 +/- 0.0068 | 0.9017 +/- 0.0020 | 3 |
| feature | knn | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8441 +/- 0.0055 | 0.6785 +/- 0.0225 | 0.8450 +/- 0.0067 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.5486 +/- 0.0447 | 0.9585 +/- 0.0096 | 0.5800 +/- 0.0407 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.5752 +/- 0.0215 | 0.9530 +/- 0.0061 | 0.6058 +/- 0.0239 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8997 +/- 0.0010 | 0.4589 +/- 0.0092 | 0.8943 +/- 0.0026 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8988 +/- 0.0008 | 0.4699 +/- 0.0066 | 0.8937 +/- 0.0009 | 3 |
| feature | knn_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8811 +/- 0.0053 | 0.5382 +/- 0.0111 | 0.8831 +/- 0.0055 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8899 +/- 0.0030 | 0.4929 +/- 0.0134 | 0.8902 +/- 0.0023 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8862 +/- 0.0031 | 0.4992 +/- 0.0044 | 0.8857 +/- 0.0045 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8631 +/- 0.0016 | 0.5898 +/- 0.0182 | 0.8620 +/- 0.0019 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8590 +/- 0.0036 | 0.6278 +/- 0.0104 | 0.8614 +/- 0.0030 | 3 |
| feature | gmm_ddu_tied | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.5569 +/- 0.0143 | 0.9554 +/- 0.0069 | 0.5938 +/- 0.0131 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.3906 +/- 0.0185 | 0.9695 +/- 0.0057 | 0.4267 +/- 0.0101 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.3975 +/- 0.0035 | 0.9697 +/- 0.0072 | 0.4324 +/- 0.0047 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9028 +/- 0.0008 | 0.4899 +/- 0.0146 | 0.9023 +/- 0.0045 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9039 +/- 0.0040 | 0.4826 +/- 0.0265 | 0.9005 +/- 0.0043 | 3 |
| feature | gmm_ddu_diag | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8565 +/- 0.0059 | 0.6575 +/- 0.0164 | 0.8551 +/- 0.0077 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7627 +/- 0.0097 | 0.8256 +/- 0.0119 | 0.7674 +/- 0.0107 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.7689 +/- 0.0168 | 0.8209 +/- 0.0123 | 0.7736 +/- 0.0207 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9033 +/- 0.0010 | 0.4745 +/- 0.0096 | 0.9031 +/- 0.0033 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9025 +/- 0.0021 | 0.4824 +/- 0.0150 | 0.9014 +/- 0.0017 | 3 |
| feature | gmm_ddu_shrinkage | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7970 +/- 0.0120 | 0.7746 +/- 0.0183 | 0.8069 +/- 0.0129 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7754 +/- 0.0089 | 0.7668 +/- 0.0143 | 0.7702 +/- 0.0095 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.7793 +/- 0.0154 | 0.7725 +/- 0.0179 | 0.7774 +/- 0.0188 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8829 +/- 0.0024 | 0.5425 +/- 0.0162 | 0.8776 +/- 0.0011 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8859 +/- 0.0029 | 0.5262 +/- 0.0133 | 0.8792 +/- 0.0027 | 3 |
| nc_hybrid | ncc_distance | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8416 +/- 0.0066 | 0.6672 +/- 0.0270 | 0.8373 +/- 0.0063 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.6916 +/- 0.0247 | 0.9637 +/- 0.0095 | 0.7158 +/- 0.0223 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.7066 +/- 0.0247 | 0.9594 +/- 0.0070 | 0.7313 +/- 0.0244 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8883 +/- 0.0003 | 0.5096 +/- 0.0110 | 0.8784 +/- 0.0009 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8873 +/- 0.0008 | 0.5064 +/- 0.0077 | 0.8770 +/- 0.0013 | 3 |
| nc_hybrid | nc_prototype_cosine | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8775 +/- 0.0061 | 0.5303 +/- 0.0197 | 0.8695 +/- 0.0065 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8753 +/- 0.0035 | 0.5487 +/- 0.0213 | 0.8753 +/- 0.0023 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8693 +/- 0.0061 | 0.5602 +/- 0.0119 | 0.8694 +/- 0.0054 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8832 +/- 0.0017 | 0.4385 +/- 0.0035 | 0.8578 +/- 0.0034 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8809 +/- 0.0003 | 0.4546 +/- 0.0096 | 0.8546 +/- 0.0016 | 3 |
| nc_hybrid | vim_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8654 +/- 0.0029 | 0.6257 +/- 0.0228 | 0.8731 +/- 0.0028 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8761 +/- 0.0015 | 1.0000 +/- 0 | 0.9157 +/- 0.0020 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8764 +/- 0.0033 | 1.0000 +/- 0 | 0.9157 +/- 0.0029 | 3 |

### OOD dataset: `svhn`

| Family | Detector | Opt | Config | LR | WD | AUROC | FPR95 | AUPR-IN | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logit | msp | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9335 +/- 0.0257 | 0.3975 +/- 0.1297 | 0.8776 +/- 0.0588 | 3 |
| logit | msp | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9230 +/- 0.0093 | 0.4764 +/- 0.0470 | 0.8637 +/- 0.0197 | 3 |
| logit | msp | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8518 +/- 0.0079 | 0.7175 +/- 0.0696 | 0.7960 +/- 0.0128 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8860 +/- 0.0371 | 0.5911 +/- 0.1274 | 0.9083 +/- 0.0163 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8617 +/- 0.0452 | 0.6579 +/- 0.0827 | 0.9024 +/- 0.0150 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9353 +/- 0.0433 | 0.2577 +/- 0.1361 | 0.8457 +/- 0.1111 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9220 +/- 0.0106 | 0.3249 +/- 0.0257 | 0.8164 +/- 0.0282 | 3 |
| logit | maxlogit | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8659 +/- 0.0336 | 0.5765 +/- 0.1124 | 0.7555 +/- 0.0431 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9151 +/- 0.0216 | 0.6360 +/- 0.1589 | 0.8952 +/- 0.0169 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8812 +/- 0.0277 | 0.7878 +/- 0.0988 | 0.8589 +/- 0.0267 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9358 +/- 0.0435 | 0.2523 +/- 0.1372 | 0.8461 +/- 0.1115 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9224 +/- 0.0106 | 0.3202 +/- 0.0291 | 0.8168 +/- 0.0282 | 3 |
| logit | energy_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8663 +/- 0.0336 | 0.5756 +/- 0.1156 | 0.7557 +/- 0.0431 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9149 +/- 0.0215 | 0.6409 +/- 0.1579 | 0.8952 +/- 0.0168 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8809 +/- 0.0281 | 0.7899 +/- 0.1010 | 0.8588 +/- 0.0269 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9360 +/- 0.0268 | 0.3846 +/- 0.1301 | 0.8775 +/- 0.0610 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9250 +/- 0.0099 | 0.4629 +/- 0.0466 | 0.8620 +/- 0.0206 | 3 |
| logit | neg_entropy | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8557 +/- 0.0086 | 0.7107 +/- 0.0731 | 0.7718 +/- 0.0331 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9160 +/- 0.0227 | 0.5894 +/- 0.1290 | 0.8911 +/- 0.0207 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9029 +/- 0.0232 | 0.6554 +/- 0.0842 | 0.8728 +/- 0.0334 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9823 +/- 0.0027 | 0.0979 +/- 0.0171 | 0.9605 +/- 0.0052 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9703 +/- 0.0132 | 0.1578 +/- 0.0632 | 0.9348 +/- 0.0267 | 3 |
| feature | mahalanobis | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.6399 +/- 0.0471 | 0.8668 +/- 0.0529 | 0.4623 +/- 0.0236 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7101 +/- 0.0913 | 0.8075 +/- 0.1294 | 0.4809 +/- 0.0964 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8202 +/- 0.0556 | 0.5427 +/- 0.1642 | 0.6044 +/- 0.1015 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9879 +/- 0.0016 | 0.0683 +/- 0.0091 | 0.9733 +/- 0.0020 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9818 +/- 0.0031 | 0.1028 +/- 0.0205 | 0.9624 +/- 0.0036 | 3 |
| feature | mahalanobis_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8508 +/- 0.0262 | 0.5780 +/- 0.0524 | 0.7281 +/- 0.0439 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9772 +/- 0.0134 | 0.1197 +/- 0.0772 | 0.9530 +/- 0.0265 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9858 +/- 0.0063 | 0.0756 +/- 0.0337 | 0.9698 +/- 0.0129 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9599 +/- 0.0075 | 0.2537 +/- 0.0588 | 0.9352 +/- 0.0119 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9608 +/- 0.0134 | 0.2531 +/- 0.0944 | 0.9370 +/- 0.0176 | 3 |
| feature | knn | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8303 +/- 0.0377 | 0.8167 +/- 0.1063 | 0.7608 +/- 0.0456 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7837 +/- 0.0995 | 0.7836 +/- 0.1875 | 0.6642 +/- 0.1108 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8747 +/- 0.0350 | 0.5608 +/- 0.2101 | 0.7831 +/- 0.0351 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9663 +/- 0.0133 | 0.2130 +/- 0.0916 | 0.9423 +/- 0.0201 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9657 +/- 0.0068 | 0.2368 +/- 0.0498 | 0.9453 +/- 0.0086 | 3 |
| feature | knn_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8698 +/- 0.0198 | 0.7093 +/- 0.0964 | 0.8195 +/- 0.0142 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9793 +/- 0.0095 | 0.1228 +/- 0.0669 | 0.9598 +/- 0.0153 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9835 +/- 0.0098 | 0.0934 +/- 0.0668 | 0.9700 +/- 0.0146 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9823 +/- 0.0027 | 0.0979 +/- 0.0171 | 0.9605 +/- 0.0052 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9703 +/- 0.0132 | 0.1578 +/- 0.0632 | 0.9348 +/- 0.0267 | 3 |
| feature | gmm_ddu_tied | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.6396 +/- 0.0470 | 0.8669 +/- 0.0528 | 0.4620 +/- 0.0236 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7099 +/- 0.0913 | 0.8076 +/- 0.1293 | 0.4805 +/- 0.0963 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8201 +/- 0.0556 | 0.5428 +/- 0.1642 | 0.6040 +/- 0.1015 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9561 +/- 0.0063 | 0.3115 +/- 0.0566 | 0.9395 +/- 0.0053 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9550 +/- 0.0171 | 0.3126 +/- 0.1363 | 0.9314 +/- 0.0202 | 3 |
| feature | gmm_ddu_diag | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7527 +/- 0.0345 | 0.9404 +/- 0.0380 | 0.6891 +/- 0.0324 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.7824 +/- 0.1088 | 0.7462 +/- 0.1797 | 0.6741 +/- 0.1173 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8607 +/- 0.0288 | 0.6009 +/- 0.0568 | 0.7631 +/- 0.0693 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9817 +/- 0.0018 | 0.1076 +/- 0.0124 | 0.9659 +/- 0.0024 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9756 +/- 0.0111 | 0.1481 +/- 0.0707 | 0.9534 +/- 0.0175 | 3 |
| feature | gmm_ddu_shrinkage | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7384 +/- 0.0574 | 0.8711 +/- 0.0891 | 0.6252 +/- 0.0397 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8530 +/- 0.0846 | 0.5348 +/- 0.2626 | 0.7143 +/- 0.1244 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8966 +/- 0.0270 | 0.4241 +/- 0.0687 | 0.7762 +/- 0.0749 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9481 +/- 0.0041 | 0.3443 +/- 0.0587 | 0.9205 +/- 0.0032 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9478 +/- 0.0152 | 0.3535 +/- 0.1113 | 0.9180 +/- 0.0195 | 3 |
| nc_hybrid | ncc_distance | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8272 +/- 0.0487 | 0.7740 +/- 0.1143 | 0.7383 +/- 0.0661 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8478 +/- 0.0560 | 0.8203 +/- 0.1650 | 0.7896 +/- 0.0593 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9003 +/- 0.0318 | 0.6335 +/- 0.2425 | 0.8594 +/- 0.0283 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9597 +/- 0.0093 | 0.2808 +/- 0.0960 | 0.9353 +/- 0.0073 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9568 +/- 0.0080 | 0.3011 +/- 0.0577 | 0.9320 +/- 0.0103 | 3 |
| nc_hybrid | nc_prototype_cosine | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8729 +/- 0.0286 | 0.6579 +/- 0.0899 | 0.8062 +/- 0.0399 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9821 +/- 0.0068 | 0.1063 +/- 0.0469 | 0.9639 +/- 0.0101 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9839 +/- 0.0117 | 0.0957 +/- 0.0792 | 0.9692 +/- 0.0185 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9878 +/- 0.0009 | 0.0634 +/- 0.0033 | 0.9713 +/- 0.0019 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9824 +/- 0.0030 | 0.0930 +/- 0.0163 | 0.9609 +/- 0.0032 | 3 |
| nc_hybrid | vim_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8751 +/- 0.0396 | 0.6927 +/- 0.1809 | 0.8310 +/- 0.0443 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9229 +/- 0.0074 | 1.0000 +/- 0 | 0.9650 +/- 0.0222 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9274 +/- 0.0050 | 1.0000 +/- 0 | 0.9754 +/- 0.0064 | 3 |

### OOD dataset: `mnist`

| Family | Detector | Opt | Config | LR | WD | AUROC | FPR95 | AUPR-IN | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| logit | msp | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9176 +/- 0.0388 | 0.5311 +/- 0.1238 | 0.9318 +/- 0.0414 | 3 |
| logit | msp | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9134 +/- 0.0340 | 0.5516 +/- 0.1304 | 0.9288 +/- 0.0340 | 3 |
| logit | msp | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9354 +/- 0.0169 | 0.4684 +/- 0.1032 | 0.9521 +/- 0.0128 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9383 +/- 0.0081 | 0.4395 +/- 0.0674 | 0.9620 +/- 0.0042 | 3 |
| logit | msp | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9365 +/- 0.0077 | 0.4352 +/- 0.0435 | 0.9626 +/- 0.0029 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9410 +/- 0.0440 | 0.2792 +/- 0.1685 | 0.9431 +/- 0.0489 | 3 |
| logit | maxlogit | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9420 +/- 0.0374 | 0.2713 +/- 0.1685 | 0.9447 +/- 0.0399 | 3 |
| logit | maxlogit | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9728 +/- 0.0109 | 0.1615 +/- 0.0864 | 0.9789 +/- 0.0085 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9289 +/- 0.0110 | 0.6285 +/- 0.1043 | 0.9537 +/- 0.0069 | 3 |
| logit | maxlogit | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9207 +/- 0.0054 | 0.6738 +/- 0.0804 | 0.9473 +/- 0.0048 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9422 +/- 0.0441 | 0.2702 +/- 0.1646 | 0.9438 +/- 0.0491 | 3 |
| logit | energy_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9432 +/- 0.0374 | 0.2634 +/- 0.1659 | 0.9453 +/- 0.0400 | 3 |
| logit | energy_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9733 +/- 0.0107 | 0.1576 +/- 0.0873 | 0.9793 +/- 0.0084 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9282 +/- 0.0110 | 0.6411 +/- 0.1047 | 0.9535 +/- 0.0069 | 3 |
| logit | energy_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9199 +/- 0.0054 | 0.6830 +/- 0.0795 | 0.9470 +/- 0.0047 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9203 +/- 0.0396 | 0.5148 +/- 0.1268 | 0.9328 +/- 0.0421 | 3 |
| logit | neg_entropy | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9159 +/- 0.0349 | 0.5349 +/- 0.1385 | 0.9296 +/- 0.0349 | 3 |
| logit | neg_entropy | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9399 +/- 0.0175 | 0.4415 +/- 0.1070 | 0.9541 +/- 0.0131 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9461 +/- 0.0067 | 0.4351 +/- 0.0670 | 0.9616 +/- 0.0045 | 3 |
| logit | neg_entropy | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9463 +/- 0.0045 | 0.4286 +/- 0.0441 | 0.9612 +/- 0.0036 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9648 +/- 0.0225 | 0.2208 +/- 0.1716 | 0.9721 +/- 0.0177 | 3 |
| feature | mahalanobis | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9550 +/- 0.0243 | 0.3021 +/- 0.1967 | 0.9656 +/- 0.0181 | 3 |
| feature | mahalanobis | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.6305 +/- 0.1952 | 0.9624 +/- 0.0408 | 0.7127 +/- 0.1613 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.3728 +/- 0.1321 | 0.9879 +/- 0.0157 | 0.4431 +/- 0.0998 | 3 |
| feature | mahalanobis | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.4007 +/- 0.0231 | 0.9751 +/- 0.0298 | 0.4369 +/- 0.0158 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9804 +/- 0.0190 | 0.1204 +/- 0.1254 | 0.9829 +/- 0.0163 | 3 |
| feature | mahalanobis_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9828 +/- 0.0125 | 0.1085 +/- 0.0866 | 0.9852 +/- 0.0106 | 3 |
| feature | mahalanobis_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9826 +/- 0.0179 | 0.0981 +/- 0.1063 | 0.9851 +/- 0.0154 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9988 +/- 0.0004 | 0.0002 +/- 0.0004 | 0.9991 +/- 0.0003 | 3 |
| feature | mahalanobis_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9991 +/- 0.0005 | 0.0001 +/- 0.0002 | 0.9993 +/- 0.0004 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9150 +/- 0.0199 | 0.6049 +/- 0.0923 | 0.9375 +/- 0.0163 | 3 |
| feature | knn | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9087 +/- 0.0253 | 0.6187 +/- 0.1500 | 0.9338 +/- 0.0183 | 3 |
| feature | knn | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9318 +/- 0.0331 | 0.4487 +/- 0.2479 | 0.9481 +/- 0.0240 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.5645 +/- 0.0724 | 0.9928 +/- 0.0114 | 0.6852 +/- 0.0543 | 3 |
| feature | knn | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.6493 +/- 0.0456 | 0.9812 +/- 0.0280 | 0.7493 +/- 0.0324 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9441 +/- 0.0263 | 0.3971 +/- 0.1479 | 0.9572 +/- 0.0203 | 3 |
| feature | knn_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9378 +/- 0.0284 | 0.4290 +/- 0.1886 | 0.9528 +/- 0.0206 | 3 |
| feature | knn_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9522 +/- 0.0329 | 0.2815 +/- 0.1811 | 0.9599 +/- 0.0261 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9969 +/- 0.0015 | 0.0079 +/- 0.0064 | 0.9973 +/- 0.0013 | 3 |
| feature | knn_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9982 +/- 0.0005 | 0.0025 +/- 0.0014 | 0.9985 +/- 0.0005 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9648 +/- 0.0225 | 0.2209 +/- 0.1717 | 0.9721 +/- 0.0177 | 3 |
| feature | gmm_ddu_tied | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9550 +/- 0.0243 | 0.3020 +/- 0.1967 | 0.9656 +/- 0.0181 | 3 |
| feature | gmm_ddu_tied | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.6301 +/- 0.1954 | 0.9625 +/- 0.0407 | 0.7125 +/- 0.1614 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.3723 +/- 0.1322 | 0.9879 +/- 0.0156 | 0.4428 +/- 0.0998 | 3 |
| feature | gmm_ddu_tied | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.4004 +/- 0.0232 | 0.9751 +/- 0.0298 | 0.4366 +/- 0.0157 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8818 +/- 0.0103 | 0.8513 +/- 0.0907 | 0.9190 +/- 0.0074 | 3 |
| feature | gmm_ddu_diag | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8569 +/- 0.0150 | 0.9341 +/- 0.0105 | 0.9011 +/- 0.0131 | 3 |
| feature | gmm_ddu_diag | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7738 +/- 0.0570 | 0.9839 +/- 0.0265 | 0.8452 +/- 0.0493 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.6785 +/- 0.0362 | 0.9889 +/- 0.0074 | 0.7573 +/- 0.0274 | 3 |
| feature | gmm_ddu_diag | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.6768 +/- 0.0102 | 0.9953 +/- 0.0032 | 0.7583 +/- 0.0254 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9331 +/- 0.0180 | 0.5010 +/- 0.1385 | 0.9511 +/- 0.0137 | 3 |
| feature | gmm_ddu_shrinkage | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9169 +/- 0.0204 | 0.6356 +/- 0.1464 | 0.9414 +/- 0.0143 | 3 |
| feature | gmm_ddu_shrinkage | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.7364 +/- 0.1184 | 0.9487 +/- 0.0479 | 0.8060 +/- 0.0893 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.6623 +/- 0.0944 | 0.9368 +/- 0.0357 | 0.7043 +/- 0.0929 | 3 |
| feature | gmm_ddu_shrinkage | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.6677 +/- 0.0340 | 0.9488 +/- 0.0285 | 0.7032 +/- 0.0331 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.8942 +/- 0.0293 | 0.6772 +/- 0.0947 | 0.9209 +/- 0.0250 | 3 |
| nc_hybrid | ncc_distance | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.8776 +/- 0.0406 | 0.7079 +/- 0.1459 | 0.9053 +/- 0.0340 | 3 |
| nc_hybrid | ncc_distance | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9413 +/- 0.0334 | 0.3643 +/- 0.2267 | 0.9538 +/- 0.0254 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8846 +/- 0.0048 | 0.9057 +/- 0.0240 | 0.9241 +/- 0.0043 | 3 |
| nc_hybrid | ncc_distance | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9119 +/- 0.0145 | 0.8413 +/- 0.0901 | 0.9446 +/- 0.0103 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9298 +/- 0.0295 | 0.4836 +/- 0.1384 | 0.9458 +/- 0.0237 | 3 |
| nc_hybrid | nc_prototype_cosine | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9189 +/- 0.0345 | 0.4964 +/- 0.1757 | 0.9353 +/- 0.0275 | 3 |
| nc_hybrid | nc_prototype_cosine | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9304 +/- 0.0349 | 0.3912 +/- 0.1584 | 0.9403 +/- 0.0296 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9950 +/- 0.0023 | 0.0170 +/- 0.0116 | 0.9957 +/- 0.0020 | 3 |
| nc_hybrid | nc_prototype_cosine | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9973 +/- 0.0004 | 0.0064 +/- 0.0019 | 0.9976 +/- 0.0003 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9713 +/- 0.0221 | 0.1635 +/- 0.1392 | 0.9760 +/- 0.0194 | 3 |
| nc_hybrid | vim_id_score | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9774 +/- 0.0131 | 0.1373 +/- 0.0977 | 0.9818 +/- 0.0104 | 3 |
| nc_hybrid | vim_id_score | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9242 +/- 0.0396 | 0.5128 +/- 0.2507 | 0.9457 +/- 0.0279 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9160 +/- 0.0105 | 1.0000 +/- 0 | 0.9758 +/- 0.0172 | 3 |
| nc_hybrid | vim_id_score | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9132 +/- 0.0006 | 1.0000 +/- 0 | 0.9700 +/- 0.0042 | 3 |



## NCC Classifier Accuracy

이 값은 OOD AUROC가 아니라 ID test에서 nearest-class-center classifier label accuracy를 측정한 hybrid diagnostic이다.

| Opt | Config | LR | WD | NCC ID-test accuracy | n |
| --- | --- | --- | --- | --- | --- |
| SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9583 +/- 0.0017 | 3 |
| SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9556 +/- 0.0007 | 3 |
| Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9444 +/- 0.0008 | 3 |
| AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9308 +/- 0.0031 | 3 |
| AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9326 +/- 0.0020 | 3 |



## Geometry Scalars on `id_train`

아래 scalar들은 `metrics_geometry.json`의 `id_train` 아래에 있는 numeric metric을 모두 집계한 것이다. `covariance_eigenspectrum`은 길이 640의 vector라서 표에는 펼치지 않고, metric dictionary에 별도로 적었다.

| Metric | Opt | Config | LR | WD | Value | n |
| --- | --- | --- | --- | --- | --- | --- |
| nc0_width_norm | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 4.105e-11 +/- 3.948e-12 | 3 |
| nc0_width_norm | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 2.669e-10 +/- 3.583e-12 | 3 |
| nc0_width_norm | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.0133 +/- 0.0004 | 3 |
| nc0_width_norm | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 9.5424 +/- 0.4908 | 3 |
| nc0_width_norm | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 8.5851 +/- 0.0294 | 3 |
| nc0_by_K | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 2.627e-09 +/- 2.527e-10 | 3 |
| nc0_by_K | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 1.708e-08 +/- 2.293e-10 | 3 |
| nc0_by_K | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.8505 +/- 0.0263 | 3 |
| nc0_by_K | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 610.7122 +/- 31.4112 | 3 |
| nc0_by_K | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 549.4487 +/- 1.8833 | 3 |
| nc1 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.0512 +/- 0.0025 | 3 |
| nc1 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.0665 +/- 0.0017 | 3 |
| nc1 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.1896 +/- 0.0025 | 3 |
| nc1 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.2765 +/- 0.0059 | 3 |
| nc1 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.2690 +/- 0.0081 | 3 |
| nc2_mean_cos | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | -0.1107 +/- 8.668e-05 | 3 |
| nc2_mean_cos | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | -0.1108 +/- 2.616e-05 | 3 |
| nc2_mean_cos | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | -0.1102 +/- 0.0002 | 3 |
| nc2_mean_cos | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | -0.1084 +/- 0.0004 | 3 |
| nc2_mean_cos | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | -0.1080 +/- 0.0008 | 3 |
| nc2_mean_etf | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.0022 +/- 0.0001 | 3 |
| nc2_mean_etf | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.0020 +/- 9.024e-05 | 3 |
| nc2_mean_etf | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.0046 +/- 0.0003 | 3 |
| nc2_mean_etf | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.0052 +/- 0.0001 | 3 |
| nc2_mean_etf | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.0056 +/- 0.0002 | 3 |
| nc2_weight_etf | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.0012 +/- 5.414e-05 | 3 |
| nc2_weight_etf | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.0014 +/- 4.844e-05 | 3 |
| nc2_weight_etf | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.0022 +/- 0.0001 | 3 |
| nc2_weight_etf | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.0032 +/- 0.0002 | 3 |
| nc2_weight_etf | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.0033 +/- 0.0001 | 3 |
| nc2_product_etf | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.0014 +/- 6.403e-05 | 3 |
| nc2_product_etf | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.0015 +/- 2.067e-05 | 3 |
| nc2_product_etf | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.0032 +/- 5.11e-05 | 3 |
| nc2_product_etf | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.0034 +/- 5.698e-05 | 3 |
| nc2_product_etf | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.0033 +/- 0.0001 | 3 |
| nc3_cos_alignment | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9502 +/- 0.0028 | 3 |
| nc3_cos_alignment | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9380 +/- 0.0010 | 3 |
| nc3_cos_alignment | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9052 +/- 0.0023 | 3 |
| nc3_cos_alignment | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.6130 +/- 0.0049 | 3 |
| nc3_cos_alignment | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.6146 +/- 0.0054 | 3 |
| nc3_self_duality | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 5.058e-05 +/- 1.573e-06 | 3 |
| nc3_self_duality | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 5.624e-05 +/- 3.714e-07 | 3 |
| nc3_self_duality | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 6.858e-05 +/- 1.236e-06 | 3 |
| nc3_self_duality | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.0001 +/- 7.78e-07 | 3 |
| nc3_self_duality | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.0001 +/- 9.529e-07 | 3 |
| nc3_self_duality_raw | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.3237 +/- 0.0101 | 3 |
| nc3_self_duality_raw | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.3599 +/- 0.0024 | 3 |
| nc3_self_duality_raw | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.4389 +/- 0.0079 | 3 |
| nc3_self_duality_raw | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.8867 +/- 0.0050 | 3 |
| nc3_self_duality_raw | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.8867 +/- 0.0061 | 3 |
| nc4_agreement | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.9949 +/- 0.0005 | 3 |
| nc4_agreement | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.9956 +/- 0.0005 | 3 |
| nc4_agreement | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.9859 +/- 0.0016 | 3 |
| nc4_agreement | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.9607 +/- 0.0037 | 3 |
| nc4_agreement | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.9634 +/- 0.0037 | 3 |
| within_var | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 18.6117 +/- 0.9928 | 3 |
| within_var | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 17.5224 +/- 0.3436 | 3 |
| within_var | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 23.8613 +/- 0.3400 | 3 |
| within_var | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 10.0839 +/- 0.2785 | 3 |
| within_var | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 10.6185 +/- 0.5137 | 3 |
| inter_dist_l2 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 16.6181 +/- 0.1942 | 3 |
| inter_dist_l2 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 14.2840 +/- 0.1660 | 3 |
| inter_dist_l2 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 13.3375 +/- 0.0818 | 3 |
| inter_dist_l2 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 5.2276 +/- 0.1271 | 3 |
| inter_dist_l2 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 5.4714 +/- 0.0699 | 3 |
| inter_dist_sq | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 276.8530 +/- 6.5231 | 3 |
| inter_dist_sq | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 204.4963 +/- 4.7445 | 3 |
| inter_dist_sq | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 179.4177 +/- 2.2469 | 3 |
| inter_dist_sq | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 27.7497 +/- 1.3250 | 3 |
| inter_dist_sq | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 30.4546 +/- 0.7348 | 3 |
| anisotropy_lambda1_trace | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 0.0911 +/- 0.0062 | 3 |
| anisotropy_lambda1_trace | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 0.1093 +/- 0.0019 | 3 |
| anisotropy_lambda1_trace | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 0.1085 +/- 0.0032 | 3 |
| anisotropy_lambda1_trace | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 0.0779 +/- 0.0076 | 3 |
| anisotropy_lambda1_trace | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 0.0821 +/- 0.0041 | 3 |
| effective_rank | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 59.5493 +/- 1.7959 | 3 |
| effective_rank | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 57.9202 +/- 1.0871 | 3 |
| effective_rank | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 25.5516 +/- 0.3920 | 3 |
| effective_rank | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 76.9248 +/- 6.0659 | 3 |
| effective_rank | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 74.1540 +/- 3.5984 | 3 |
| condition_number_clipped | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 4.131e+04 +/- 2.098e+04 | 3 |
| condition_number_clipped | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 9748 +/- 586.5205 | 3 |
| condition_number_clipped | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 2.369e+10 +/- 4.081e+10 | 3 |
| condition_number_clipped | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 4.428e+11 +/- 2.169e+11 | 3 |
| condition_number_clipped | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 4.054e+11 +/- 3.329e+10 | 3 |



## Feature Norm Statistics by Split

Feature norm 통계는 ID split과 각 OOD split을 분리해서 정리한다.

| Split | Opt | Config | LR | WD | Dim | N | Norm mean | Norm std | Min | Q25 | Median | Q75 | Max | n |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| id_train | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 45000 +/- 0 | 14.2310 +/- 0.1504 | 1.7899 +/- 0.0636 | 7.3227 +/- 0.4691 | 12.9784 +/- 0.1581 | 14.0997 +/- 0.1441 | 15.3445 +/- 0.1590 | 23.5354 +/- 0.4811 | 3 |
| id_train | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 45000 +/- 0 | 12.8847 +/- 0.1298 | 1.7440 +/- 0.0087 | 6.4950 +/- 0.2448 | 11.6491 +/- 0.1399 | 12.7288 +/- 0.1349 | 13.9784 +/- 0.1190 | 22.5280 +/- 0.9680 | 3 |
| id_train | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 45000 +/- 0 | 14.3868 +/- 0.1221 | 2.0349 +/- 0.0741 | 6.2526 +/- 0.3197 | 12.9672 +/- 0.1616 | 14.2484 +/- 0.1508 | 15.6500 +/- 0.1117 | 26.4832 +/- 0.6775 | 3 |
| id_train | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 45000 +/- 0 | 6.2149 +/- 0.0863 | 1.3226 +/- 0.0360 | 2.3176 +/- 0.2606 | 5.2562 +/- 0.0603 | 6.0410 +/- 0.0761 | 7.0028 +/- 0.1105 | 14.1011 +/- 1.1746 | 3 |
| id_train | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 45000 +/- 0 | 6.5007 +/- 0.0706 | 1.3803 +/- 0.0298 | 2.3300 +/- 0.0970 | 5.5059 +/- 0.0606 | 6.3112 +/- 0.0763 | 7.3143 +/- 0.0895 | 15.1247 +/- 0.6922 | 3 |
| id_val | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 5000 +/- 0 | 14.0498 +/- 0.1331 | 1.7234 +/- 0.0383 | 8.3765 +/- 0.6432 | 12.8602 +/- 0.1149 | 13.9394 +/- 0.1497 | 15.1115 +/- 0.1480 | 22.2884 +/- 1.0420 | 3 |
| id_val | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 5000 +/- 0 | 12.7526 +/- 0.1198 | 1.6684 +/- 0.0108 | 7.3964 +/- 0.7568 | 11.5748 +/- 0.1320 | 12.6403 +/- 0.1226 | 13.8083 +/- 0.1305 | 21.3591 +/- 1.1127 | 3 |
| id_val | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 5000 +/- 0 | 14.3556 +/- 0.1134 | 2.0244 +/- 0.0679 | 7.2298 +/- 0.9361 | 12.9659 +/- 0.1209 | 14.2183 +/- 0.1499 | 15.5940 +/- 0.1037 | 24.6236 +/- 0.4587 | 3 |
| id_val | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 5000 +/- 0 | 6.0778 +/- 0.0526 | 1.4205 +/- 0.0334 | 2.2891 +/- 0.4036 | 5.0417 +/- 0.0313 | 5.9041 +/- 0.0429 | 6.9470 +/- 0.0819 | 12.5089 +/- 0.5730 | 3 |
| id_val | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 5000 +/- 0 | 6.3365 +/- 0.0679 | 1.4767 +/- 0.0350 | 2.3273 +/- 0.2525 | 5.2638 +/- 0.0576 | 6.1528 +/- 0.0876 | 7.2438 +/- 0.0834 | 13.5382 +/- 0.6493 | 3 |
| id_test | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 14.0806 +/- 0.1368 | 1.7279 +/- 0.0611 | 8.6195 +/- 0.2392 | 12.8966 +/- 0.1364 | 13.9679 +/- 0.1304 | 15.1566 +/- 0.1618 | 22.4431 +/- 0.7237 | 3 |
| id_test | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 10000 +/- 0 | 12.7696 +/- 0.1380 | 1.6812 +/- 0.0090 | 7.0096 +/- 0.1925 | 11.5944 +/- 0.1420 | 12.6421 +/- 0.1505 | 13.8133 +/- 0.1439 | 20.4849 +/- 0.7156 | 3 |
| id_test | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 14.3801 +/- 0.1168 | 2.0236 +/- 0.0707 | 6.2940 +/- 1.3349 | 12.9768 +/- 0.1339 | 14.2439 +/- 0.1363 | 15.6261 +/- 0.0968 | 26.2949 +/- 1.6881 | 3 |
| id_test | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 6.0686 +/- 0.0751 | 1.4226 +/- 0.0425 | 2.0679 +/- 0.1065 | 5.0181 +/- 0.0486 | 5.8920 +/- 0.0590 | 6.9285 +/- 0.0903 | 13.0663 +/- 0.4681 | 3 |
| id_test | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 6.3422 +/- 0.0806 | 1.4821 +/- 0.0358 | 2.0965 +/- 0.3040 | 5.2624 +/- 0.0597 | 6.1493 +/- 0.0747 | 7.2408 +/- 0.1153 | 13.3160 +/- 0.3254 | 3 |
| ood_test_cifar100 | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 13.5613 +/- 0.1399 | 1.7257 +/- 0.0430 | 7.6863 +/- 0.8011 | 12.3753 +/- 0.1253 | 13.4568 +/- 0.1309 | 14.6414 +/- 0.1454 | 21.8118 +/- 0.7686 | 3 |
| ood_test_cifar100 | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 10000 +/- 0 | 12.8140 +/- 0.1774 | 1.6374 +/- 0.0215 | 6.3551 +/- 0.3677 | 11.6905 +/- 0.1827 | 12.7460 +/- 0.1697 | 13.8654 +/- 0.1882 | 20.7326 +/- 0.3020 | 3 |
| ood_test_cifar100 | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 13.6929 +/- 0.0585 | 1.9545 +/- 0.0627 | 4.3126 +/- 0.3272 | 12.4800 +/- 0.0525 | 13.7355 +/- 0.0263 | 14.9785 +/- 0.0200 | 22.0489 +/- 0.3835 | 3 |
| ood_test_cifar100 | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 4.5202 +/- 0.0649 | 0.8471 +/- 0.0131 | 1.8143 +/- 0.2048 | 3.9518 +/- 0.0582 | 4.4446 +/- 0.0647 | 5.0065 +/- 0.0710 | 10.5164 +/- 0.4023 | 3 |
| ood_test_cifar100 | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 4.7015 +/- 0.0686 | 0.8993 +/- 0.0147 | 1.6676 +/- 0.2665 | 4.1011 +/- 0.0740 | 4.6187 +/- 0.0653 | 5.2036 +/- 0.0654 | 10.7793 +/- 0.1918 | 3 |
| ood_test_tiny_imagenet | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 13.5058 +/- 0.1468 | 1.7331 +/- 0.0200 | 6.4804 +/- 0.6301 | 12.3388 +/- 0.1344 | 13.3869 +/- 0.1310 | 14.5708 +/- 0.1668 | 21.9141 +/- 0.5707 | 3 |
| ood_test_tiny_imagenet | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 10000 +/- 0 | 12.9390 +/- 0.2386 | 1.6432 +/- 0.0353 | 6.6731 +/- 0.7474 | 11.8147 +/- 0.2045 | 12.8774 +/- 0.2312 | 13.9849 +/- 0.2720 | 20.3726 +/- 0.5381 | 3 |
| ood_test_tiny_imagenet | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 13.4173 +/- 0.1494 | 1.9222 +/- 0.0420 | 3.5036 +/- 0.8788 | 12.1896 +/- 0.1703 | 13.4401 +/- 0.1232 | 14.6619 +/- 0.0960 | 22.4141 +/- 0.9987 | 3 |
| ood_test_tiny_imagenet | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 4.3505 +/- 0.1119 | 0.8846 +/- 0.0216 | 1.4191 +/- 0.0385 | 3.7608 +/- 0.1047 | 4.2611 +/- 0.1109 | 4.8274 +/- 0.1200 | 10.4171 +/- 0.7837 | 3 |
| ood_test_tiny_imagenet | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 4.5771 +/- 0.0501 | 0.9343 +/- 0.0240 | 1.5616 +/- 0.3816 | 3.9638 +/- 0.0523 | 4.4757 +/- 0.0538 | 5.0724 +/- 0.0536 | 11.3791 +/- 0.5160 | 3 |
| ood_test_svhn | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 26032 +/- 0 | 12.6644 +/- 1.0912 | 1.5983 +/- 0.2624 | 6.1388 +/- 1.0590 | 11.6466 +/- 0.8696 | 12.5718 +/- 0.9900 | 13.6363 +/- 1.2290 | 20.8126 +/- 2.0947 | 3 |
| ood_test_svhn | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 26032 +/- 0 | 12.5262 +/- 0.7920 | 1.5654 +/- 0.1443 | 5.7916 +/- 1.2754 | 11.4915 +/- 0.8793 | 12.4595 +/- 0.8411 | 13.5205 +/- 0.7353 | 19.2206 +/- 0.8513 | 3 |
| ood_test_svhn | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 26032 +/- 0 | 12.6341 +/- 0.7512 | 2.3699 +/- 0.4971 | 3.9226 +/- 1.3591 | 11.0474 +/- 0.8419 | 12.6789 +/- 0.7610 | 14.2511 +/- 0.7663 | 23.4206 +/- 2.2099 | 3 |
| ood_test_svhn | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 26032 +/- 0 | 4.1567 +/- 0.3585 | 0.7618 +/- 0.0987 | 1.5090 +/- 0.2278 | 3.6607 +/- 0.3006 | 4.1356 +/- 0.3585 | 4.6377 +/- 0.4274 | 7.9528 +/- 0.5458 | 3 |
| ood_test_svhn | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 26032 +/- 0 | 4.9006 +/- 0.3241 | 0.9535 +/- 0.1988 | 1.6461 +/- 0.1020 | 4.2335 +/- 0.1583 | 4.8383 +/- 0.2705 | 5.5165 +/- 0.4388 | 9.8666 +/- 1.2007 | 3 |
| ood_test_mnist | SGD | sgd_lr1e-1_wd5e-4_anchor | 0.1 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 10.7151 +/- 0.8828 | 1.3387 +/- 0.1428 | 5.5449 +/- 0.7926 | 9.8117 +/- 0.8715 | 10.7045 +/- 0.8749 | 11.6110 +/- 0.9006 | 15.2814 +/- 0.7915 | 3 |
| ood_test_mnist | SGD | sgd_lr1e-1_wd2e-4 | 0.1 | 2e-4 | 640 +/- 0 | 10000 +/- 0 | 9.8967 +/- 0.6022 | 1.1557 +/- 0.1081 | 5.8927 +/- 0.3166 | 9.0918 +/- 0.4948 | 9.8874 +/- 0.5684 | 10.6698 +/- 0.6846 | 13.8917 +/- 0.7696 | 3 |
| ood_test_mnist | Adam | adam_lr1e-3_wd1e-4 | 1e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 7.5769 +/- 1.5730 | 1.5333 +/- 0.0234 | 2.0325 +/- 0.2502 | 6.5737 +/- 1.6715 | 7.6393 +/- 1.6981 | 8.6376 +/- 1.6062 | 12.4159 +/- 0.8046 | 3 |
| ood_test_mnist | AdamW | adamw_lr5e-3_wd1e-4 | 5e-3 | 1e-4 | 640 +/- 0 | 10000 +/- 0 | 2.7200 +/- 0.3204 | 0.5530 +/- 0.0305 | 1.1675 +/- 0.0829 | 2.3286 +/- 0.3114 | 2.6569 +/- 0.3278 | 3.0404 +/- 0.3287 | 5.3923 +/- 0.7608 | 3 |
| ood_test_mnist | AdamW | adamw_lr5e-3_wd5e-4_anchor | 5e-3 | 5e-4 | 640 +/- 0 | 10000 +/- 0 | 2.8786 +/- 0.3240 | 0.5775 +/- 0.0905 | 1.1167 +/- 0.4265 | 2.4931 +/- 0.2768 | 2.8430 +/- 0.3084 | 3.2070 +/- 0.3506 | 5.8188 +/- 0.7416 | 3 |



## Metric Dictionary

### Classification, Validation, and Calibration Metrics

| Metric | Meaning | Direction |
| --- | --- | --- |
| best_val_epoch | Validation accuracy가 가장 높았던 epoch. | descriptive |
| best_val_acc | ID validation split에서 관측된 최고 accuracy. | higher better |
| final_val_acc | 최종 checkpoint 기준 ID validation accuracy. | higher better |
| id_test_acc | ID test split에서의 classification accuracy. | higher better |
| id_test_nll | ID test split negative log-likelihood. | lower better |
| ece_15bin | 15-bin Expected Calibration Error. | lower better |
| temperature_scaled_ece_15bin | ID validation에서 fit한 temperature를 적용한 뒤의 15-bin ECE. | lower better |
| temperature | Temperature scaling에서 학습된 scalar temperature. | diagnostic |
| ncc_accuracy_id_test | ID train class mean으로 만든 nearest-class-center classifier의 ID test accuracy. | higher better |

### OOD Aggregate Metrics

| Metric | Meaning | Direction |
| --- | --- | --- |
| AUROC | ID score가 OOD score보다 높게 rank될 확률. ID label=1, OOD label=0. | higher better |
| FPR95 | ID recall을 95%로 맞추는 threshold에서 OOD가 ID로 통과하는 비율. | lower better |
| AUPR-IN | ID를 positive class로 둔 precision-recall curve 아래 면적. | higher better |

### OOD Detectors

| Detector | Family | Score | Note |
| --- | --- | --- | --- |
| msp | logit | maximum softmax probability. | higher means more ID-like |
| maxlogit | logit | maximum logit. | higher means more ID-like |
| energy_id_score | logit | T logsumexp(z / T), project ID-like sign. | not negative energy in storage |
| neg_entropy | logit | negative predictive entropy. | higher means lower entropy and more ID-like |
| mahalanobis | feature | negative tied-covariance class Mahalanobis distance. | fit on ID train features |
| mahalanobis_l2 | feature | Mahalanobis after detector-side L2 feature normalization. | Mahalanobis++-motivated control, not full reproduction |
| knn | feature | negative k-th nearest-neighbor distance, k=50. | fit on ID train features |
| knn_l2 | feature | kNN after detector-side L2 feature normalization. | feature-scale control |
| gmm_ddu_tied | feature | DDU-style GMM log density with tied covariance. | not full DDU reproduction |
| gmm_ddu_diag | feature | DDU-style GMM log density with classwise diagonal covariance. | not full DDU reproduction |
| gmm_ddu_shrinkage | feature | DDU-style GMM log density with classwise shrinkage covariance. | alpha selected on ID val likelihood |
| ncc_distance | nc_hybrid | negative distance to nearest ID train class mean. | prototype distance diagnostic |
| nc_prototype_cosine | nc_hybrid | maximum cosine between L2 feature and L2 class mean. | prototype angular diagnostic |
| vim_id_score | nc_hybrid | ViM-derived ID-like score after project transform. | diagnostic only |

### Geometry Metrics

| Metric | Meaning | Direction |
| --- | --- | --- |
| nc0_width_norm | global mean / class-mean centering 관련 NC0 width statistic. | diagnostic |
| nc0_by_K | NC0 statistic scaled by number of classes. | diagnostic |
| nc1 | within-class variability relative to class separation. | lower often means more collapsed class geometry |
| nc2_mean_cos | class mean cosine structure statistic. | diagnostic |
| nc2_mean_etf | class means의 ETF deviation. | lower means closer to ETF |
| nc2_weight_etf | classifier weights의 ETF deviation. | lower means closer to ETF |
| nc2_product_etf | class mean / weight product geometry ETF deviation. | diagnostic |
| nc3_cos_alignment | classifier weight와 class mean direction의 cosine alignment. | higher means stronger alignment |
| nc3_self_duality | normalized self-duality distance. | lower means closer self-duality |
| nc3_self_duality_raw | raw Frobenius self-duality distance before paper normalization. | lower means closer self-duality |
| nc4_agreement | classifier prediction and nearest-class-center prediction agreement. | higher means stronger agreement |
| within_var | ID train within-class feature variance. | diagnostic |
| inter_dist_l2 | off-diagonal class mean pair L2 distance. | higher means larger class-mean separation |
| inter_dist_sq | squared class mean pair distance. | higher means larger class-mean separation |
| anisotropy_lambda1_trace | largest covariance eigenvalue divided by covariance trace. | higher means more anisotropic covariance |
| effective_rank | entropy-based effective rank of within-class covariance spectrum. | higher means covariance energy is spread over more directions |
| condition_number_clipped | clipped covariance condition-number diagnostic. | higher means more ill-conditioned covariance |
| covariance_eigenspectrum | 640-dimensional sorted within-class covariance eigenvalue vector. | vector diagnostic; not expanded in table |

### Feature Statistics

| Metric | Meaning | Direction |
| --- | --- | --- |
| feature_dim | feature dimensionality. | metadata |
| num_samples | samples in the split used for feature statistics. | metadata |
| feature_norm_mean | mean L2 norm of penultimate features. | diagnostic |
| feature_norm_std | standard deviation of feature L2 norm. | diagnostic |
| feature_norm_min/q25/median/q75/max | feature L2 norm quantiles. | diagnostic |



## 수식 정의

수식은 Notion 가져오기에서 깨지지 않도록 표 안에 넣지 않고, 각각 독립된 block equation으로 둔다.

Accuracy:

$$
\mathrm{Accuracy}=\frac{1}{n}\sum_{i=1}^{n}\mathbf{1}(\hat{y}_i=y_i)
$$

Negative log-likelihood:

$$
\mathrm{NLL}=-\frac{1}{n}\sum_{i=1}^{n}\log p_i(y_i)
$$

ECE with bins:

$$
\mathrm{ECE}=\sum_{b=1}^{B}\frac{|B_b|}{n}\left|\mathrm{acc}(B_b)-\mathrm{conf}(B_b)\right|
$$

AUROC under the project convention, where higher score is more ID-like:

$$
\mathrm{AUROC}=P(s(x_{\mathrm{ID}})>s(x_{\mathrm{OOD}}))
$$

Mahalanobis ID-like score:

$$
s(x)=-\min_k (h(x)-\mu_k)^T\Sigma^{-1}(h(x)-\mu_k)
$$

kNN ID-like score:

$$
s(x)=-d_k(h(x),\mathcal{H}_{\mathrm{ID\ train}})
$$

Feature norm:

$$
\|h(x)\|_2=\sqrt{\sum_j h_j(x)^2}
$$

Sample standard deviation used in all `mean +/- std` cells:

$$
s=\sqrt{\frac{1}{m-1}\sum_{r=1}^{m}(x_r-\bar{x})^2}
$$



## Notes for Later Analysis



- Poster용 `near` 또는 `far` 평균이 필요하면 별도 분석 단계에서 명시적으로 만들 수 있다. 다만 이 Notion import 문서의 OOD 표는 사용자의 요청에 맞춰 dataset별 값만 둔다.

- `train_metrics.jsonl`과 `val_metrics.jsonl`에는 epoch-wise logs가 보존되어 있다. 이 문서에서는 `training_summary.json`의 best/final validation summary만 3-seed 표로 집계했다.

- `sgd_lr1e-1_wd5e-4_anchor`의 seed0은 package convention상 `final` checkpoint이며, 나머지 seed/config는 `epoch_0350` 평가다.
