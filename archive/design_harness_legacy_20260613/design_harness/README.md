# Design Harness

이 폴더는 Claude Design의 "디자인 시스템 업로드 후 생성" 방식을 Codex CLI에서
재현하기 위한 하네스입니다. Codex CLI에는 Claude Design처럼 `.fig`를 업로드하고
`Publish`하는 전용 화면이 없으므로, 디자인 시스템을 Codex가 읽을 수 있는 규칙과
토큰으로 바꿔 두는 방식이 가장 안정적입니다.

## 현재 구조

- `../AGENTS.md`: Codex가 이 작업공간에서 자동으로 읽는 디자인 작업 규칙.
- `fonts/pretendard/`: 프로젝트 로컬 Pretendard 폰트, 라이선스, 출처 기록.
- `tokens/wanted-inspired.json`: Wanted Design System 기반의 시작 토큰.
- `prompts/stat_poster_prd.md`: 포스터 기획 문서 생성/정리 프롬프트.
- `prompts/build_from_design_harness.md`: HTML, TeX, PPTX 제작 요청 프롬프트.
- `templates/stat_poster_a0.html`: 841mm × 1189mm A0 세로 포스터 HTML 시작 템플릿.
- `templates/wanted_poster_macros.tex`: 작년 PPTX 레이아웃과 한글 Pretendard,
  수식 Cambria Math 우선 토큰을 옮긴 TeX 매크로.
- `../poster/poster.tex`: TeX/PDF 최종 포스터 작업용 A0 세로 템플릿.

## 디자인 기준

현재 주 디자인 기준은 `../references/poster_layout/25_동계_통계학회_포스터_진군학.pptx`입니다. 이 파일은
PowerPoint 내부 크기상 A1 세로형에 가깝지만, 현재 학회 규정은 **841mm ×
1189mm A0 세로형 1페이지**이므로 하네스는 A0 세로형으로 스케일업했습니다.

반영한 레이아웃 규칙:

- 상단 큰 제목/저자 영역.
- 짙은 파란색 섹션 바.
- 본문 2열 구성.
- 흰 배경과 검정 본문.
- 하단 얇은 파란 라인과 acknowledgment/footer 영역.
- 한글 폰트는 Pretendard 우선, 수식 폰트는 Cambria Math 우선.

## Figma 파일을 쓰는 방법

현재 `../references/design_system/Wanted Design System (Community).fig`는 zip archive이고, 내부에는
`canvas.fig`, `thumbnail.png`, `meta.json`, `images/`가 들어 있습니다. `canvas.fig`는
Figma 자체 바이너리라서 Codex가 디자인 시스템 전체를 안정적으로 직접 해석하기에는
적합하지 않습니다.

권장 경로는 세 가지입니다.

1. 빠른 경로: Figma에서 `.fig`를 열고 색상, 타이포, 간격, 주요 컴포넌트를 JSON,
   CSS variables, 또는 스크린샷으로 export한 뒤 `tokens/`와 `templates/`를 갱신합니다.
2. 좋은 경로: Codex에 Figma MCP를 연결해 Figma 파일을 직접 조회하게 합니다.
   Codex 공식 매뉴얼 기준으로 MCP는 CLI와 IDE extension에서 지원되고, Figma MCP도
   연결 대상입니다.
3. 임시 경로: 현재처럼 `.fig`의 썸네일과 메타데이터만 참고해 Wanted 스타일에 맞는
   starter token을 만들고, 결과물을 보면서 보정합니다.

## Figma MCP 설정 예시

Figma 계정과 토큰이 준비되어 있으면 `~/.codex/config.toml` 또는 신뢰한 프로젝트의
`.codex/config.toml`에 MCP 서버를 등록할 수 있습니다.

```toml
[mcp_servers.figma]
url = "https://mcp.figma.com/mcp"
bearer_token_env_var = "FIGMA_OAUTH_TOKEN"
```

설정 후 새 Codex 세션을 시작하고 `/mcp`로 서버가 활성화되었는지 확인합니다. 그 다음
Figma 파일 URL이나 node URL을 주고 "이 파일의 color/text variables를 추출해
`design_harness/tokens/`에 반영해줘"라고 요청하면 됩니다.

## 추천 제작 순서

1. 연구 내용을 PRD로 고정합니다.
2. 최종 인쇄본은 `../poster/poster.tex`를 XeLaTeX로 컴파일해 PDF로 만듭니다.
3. 빠른 레이아웃 검토가 필요하면 HTML 템플릿을 보조로 사용합니다.
4. 발표나 공동편집이 필요할 때만 PPTX로 변환합니다.
5. Figma에서 정확한 토큰을 export하면 token 파일과 `templates/wanted_poster_macros.tex`를 함께 갱신하고 템플릿 구조는 유지합니다.

## TeX 포스터 컴파일

한글과 수식 폰트 처리를 위해 최종본은 XeLaTeX를 권장합니다. 로컬 TeX 환경에는
`texlive-xetex`, `texlive-lang-korean`, Cambria Math가 있으면 가장 안정적입니다.
Pretendard는 `fonts/pretendard/static/`의 프로젝트 로컬 OTF를 우선 사용합니다.

```bash
cd ../poster
xelatex poster.tex
```

현재처럼 XeLaTeX나 `kotex`가 없는 최소 TeX 환경에서는 구조 검증용으로만
`pdflatex` fallback을 사용할 수 있습니다. 이 경우 한글과 폰트 정확도는 최종 검증으로
보면 안 됩니다.

```bash
cd ../poster
pdflatex poster.tex
```

참고문헌을 붙이면 `biber` 또는 `bibtex`를 추가하고, 최종 PDF 안정화를 위해
XeLaTeX를 한 번 더 실행합니다.

## Codex 요청 예시

```text
이 저장소의 AGENTS.md와 design_harness를 기준으로,
docs/research/GPT제안_포스터초안.md의 내용을 841mm × 1189mm A0 세로 HTML 포스터로 만들어줘.
표 2개, 그림 자리 2개만 쓰고 작년 PPTX 기반 Wanted-inspired token을 적용해.
```

```text
Figma MCP로 Wanted Design System 파일의 색상/타이포 토큰을 읽어서
design_harness/tokens/wanted-inspired.json을 exact token으로 보정해줘.
```

```text
AGENTS.md와 design_harness를 기준으로 poster/poster.tex를 완성해줘.
docs/research/GPT제안_포스터초안.md를 스토리라인으로 쓰고,
최종 실험 CSV가 없으면 표와 그림은 placeholder를 유지해.
규격은 반드시 841mm x 1189mm A0 세로형 1페이지로 맞춰.
```

```text
현재 HTML 포스터를 발표용 16:9 PPTX 8장으로 변환해줘.
각 장은 핵심 주장, 실험, 결과표, geometry figure, takeaway 순서로 구성해.
```
