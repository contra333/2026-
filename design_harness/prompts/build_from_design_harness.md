# Build From Design Harness Prompt

Use this prompt when asking Codex to produce a concrete design artifact.

```text
AGENTS.md와 design_harness/README.md를 먼저 읽고,
design_harness/tokens/wanted-inspired.json을 디자인 토큰으로 사용해줘.

목표:
- [HTML | PPTX | TeX | Figma handoff spec] 형식으로 통계학회 포스터/발표자료를 제작한다.

내용:
- docs/research/GPT제안_포스터초안.md를 기본 스토리라인으로 사용한다.
- 필요한 경우 docs/research/통계학회_포스터_실험계획.md와 docs/research/학습후_평가_집계_가이드.md를 참고한다.

디자인:
- `references/poster_layout/25_동계_통계학회_포스터_진군학.pptx`의 레이아웃을 따른다.
- 흰 배경, 검정 본문, 짙은 파란 섹션 바(`#2F5597`), 파란 포인트(`#0070C0`).
- 한글 폰트는 Pretendard 우선, 수식 폰트는 Cambria Math 우선.
- A0 포스터는 세로형 841mm x 1189mm, 1페이지, 2-column body.

검증:
- 텍스트 overflow와 섹션 겹침이 없는지 확인한다.
- 표 2개, 그림 2개 구조를 유지한다.
- 실행 가능한 생성 명령 또는 열 수 있는 산출물 경로를 알려준다.
```
