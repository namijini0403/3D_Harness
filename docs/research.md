# 조사와 설계 판단

확인일: 2026-09-09. 공식 문서·GitHub 코드와 제작 사례를 조사했다. **아래의 하네스 선택은 이 프로젝트에 대한 설계 판단이며, 선생님 자료에서 측정한 성능 비교는 아니다.** 영상의 제목/채널 정보는 YouTube oEmbed와 검색/페이지로 확인했지만 전체 재생·자막 분석은 수행하지 못했다. 영상 속 구체적 명령을 검증한 것처럼 인용하지 않는다.

## 기술 근거 → 반영 사항

| 직접 확인한 자료 | 확인한 내용 | 하네스 판단 |
|---|---|---|
| [OpenAI Astra 가이드](https://developers.openai.com/api/docs/guides/latest-model) | 지침 파일의 영향, 주도적 작업과 프롬프팅 특성 | 충돌하는 긴 규칙을 줄이고 완료 조건 명시 |
| [AGENTS.md](https://learn.chatgpt.com/docs/agent-configuration/agents-md) | 디렉터리별 지침 적용 | 루트 지침 하나 + 필요한 안내만 읽기 |
| [Codex MCP](https://learn.chatgpt.com/docs/extend/mcp?surface=cli) | 서버 구성, 도구 허용 목록 | Blender 관련 도구 4개를 기본 후보로 제한 |
| [Astra 건축 제작 사례](https://developers.openai.com/blog/architectural-visualization-with-astra) | bpy 스크립트·미리보기 검사·엔진 전환 | 코드 저장과 시각 검증 반복을 채택. 촬영 복원 성공 사례와는 구별 |
| [Blender MCP 소스](https://github.com/ahujasid/blender-mcp/tree/5f8ddaf6e987c4aa0c3467fcc548838b28f64477) · [PyPI](https://pypi.org/project/blender-mcp/1.9.1/) | 서버/애드온, 코드 실행, 텔레메트리 제어, 1.9.1 배포 | 포크 없이 버전 지정 연결, 사본 저장, 로컬 사용 |
| [Marzipano](https://www.marzipano.net/) · [Tool](https://www.marzipano.net/tool/) | 브라우저 내 처리와 투어 export | 타일 기반 투어 및 시각 편집 경로 |
| [Pannellum 소스](https://github.com/mpetroff/pannellum) · [투어 예제](https://pannellum.org/documentation/examples/tour/) | 가벼운 뷰어, 장면 링크, 로컬 HTTP 사용 | 작은 샘플의 코드 기반 투어 경로 |
| [Nerfstudio 360 데이터](https://docs.nerf.studio/quickstart/custom_dataset.html) | 구면 입력의 perspective 샘플링과 crop | 360 입력을 일반 사진처럼 무조건 처리하지 않기 |
| [COLMAP 튜토리얼](https://colmap.github.io/tutorial.html) | 좋은 촬영·정합·재구성 흐름 | 학습 전 카메라 정합 검사 |
| [Splatfacto](https://docs.nerf.studio/nerfology/methods/splat.html) · [SuperSplat 소스](https://github.com/playcanvas/supersplat) | Gaussian 학습과 편집 도구 | 재구성과 최종 표시 분리; Blender 단독 만능 경로 배제 |

## 유튜브 제작 사례 · 시청용

| 영상 | 제작자 | 참고 범위 |
|---|---|---|
| [Create 3D with Claude AI with Blender MCP — Full 26-min Tutorial](https://www.youtube.com/watch?v=lCyQ717DuzQ) | DesignCode | Blender MCP 저장소가 연결한 튜토리얼. Claude 화면이므로 Codex 연결법은 공식 MCP 문서로 대체 |
| [Process 360 images with Marzipano for the TAGGIS platform](https://www.youtube.com/watch?v=MFho5HhrguQ) | Patrick Sävström | 360 투어 제작 사례. 영상 설명 확인 |
| [How to Use 360 Video for 3D Gaussian Splatting (and NeRFs!)](https://www.youtube.com/watch?v=LQNBTvgljAw) | Pixel Reconstruct | 360 영상 복원 사례의 존재·주제 확인. 실행 절차는 Nerfstudio 문서로 확인 |
| [Unleash the power of 360 cameras with AI-assisted 3D scanning. (Luma AI)](https://www.youtube.com/watch?v=kV0OAvlXShk) | Olli Huttunen | 360 촬영 활용 사례. 현재 서비스 기능/가격의 근거로 사용하지 않음 |

## 채택하지 않은 기본값

- Blender MCP 전체 포크: 이 작업에 필요한 것은 연결과 작업 규칙이므로 서버 유지보수 부담이 더 큼. 타사 코드는 복사하지 않았다.
- 모든 작업을 Blender로 처리: 단순 투어에 불필요한 모델링·렌더 비용이 생김.
- 무조건 3DGS: 다중 시점·정합·GPU·배포 제약을 통과해야 함.
- 매번 다중 에이전트/전체 문서 주입/최고 추론 단계: 효과를 측정하지 않은 상시 비용.
- 무조건 AI 업스케일/생성 보완: 기억 프로젝트에서 기록에 없는 디테일을 사실처럼 만들 위험.

촬영 자료가 도착하면 가장 먼저 이 판단을 실제 실패 화면과 비교한다. 라이선스는 기존 저장소의 MIT를 유지하며 외부 도구/자료는 각각의 라이선스를 따른다.
