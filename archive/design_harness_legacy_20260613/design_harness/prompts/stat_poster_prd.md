# Statistics Poster PRD Prompt

Use this prompt when converting research notes into a poster-ready design brief.

```text
이 저장소의 AGENTS.md와 design_harness/tokens/wanted-inspired.json을 기준으로
통계학회 포스터 PRD를 작성해줘.

입력 문서:
- docs/research/GPT제안_포스터초안.md
- docs/research/통계학회_포스터_실험계획.md
- docs/research/학습후_평가_집계_가이드.md
- docs/research/추가실험_승인_컨텍스트.md

출력:
1. 한 문장 핵심 주장
2. 포스터 독자와 읽는 상황
3. 841mm × 1189mm A0 세로 레이아웃 섹션 구성
4. 표 2개와 그림 2개의 정확한 목적
5. 필요한 데이터 파일 목록과 컬럼 스키마
6. 디자인 톤과 금지사항
7. HTML, PPTX, TeX 각각의 제작 전략

제약:
- 본문 포스터에는 표 2개, 그림 2개를 넘기지 말 것.
- 정확도만 강조하지 말고 calibration, OOD, feature geometry 연결을 중심 메시지로 둘 것.
- DDU는 "DDU-style GMM feature-density score"로 표기할 것.
```
