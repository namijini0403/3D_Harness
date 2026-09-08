# 검증 기록

2026-09-09 · Windows · Python 3.11 · Pillow 12.2.0

| 범위 | 결과 |
|---|---|
| 사진 점검 자동 테스트 7개 | 통과: 2:1 후보/비율, 원본 해시 보존, EXIF 제거, 회전·손상·원시 형식, 미리보기 제한, 경로 중첩/누락, 기존 결과 보존, 빈 입력/잘못된 옵션 |
| 자동 설치 설정 테스트 5개 | 통과: 기존 모델/다른 서버/주석 보존, 경로 인코딩, 재실행, 충돌 거부, 백업·동시 변경 감지 |
| Windows 설치 전 점검 | PowerShell `-CheckOnly` 실행 통과. 프로그램 설치/설정 변경 없이 탐색 |
| Python 구문 검사 | scripts 4개 통과. Blender probe/설치 helper의 실제 bpy 실행을 뜻하지 않음 |
| config TOML / 예제 JSON | 파싱 통과 |
| MCP 도구 이름 | upstream 고정 커밋 및 PyPI 1.9.1 wheel 서버 소스에서 4개 함수와 bundled 애드온 확인 |
| 시작 지침 크기 | AGENTS.md 22줄. 실제 모델 토큰 수가 아님 |
| 원본 학교 사진·기존 프로젝트 분석 | 자료 미제공으로 미실행 |
| Blender MCP 실제 연결·probe 실행 | Blender/uvx 실행 환경을 확보하지 못해 미실행 |
| 투어 렌더·휴대폰·3DGS 학습 | 학교 입력과 대상 환경이 없어 미실행 |
| Astra 하네스 A/B 평가·절감률 | 미실행. [동일 조건 평가 절차](eval/README.md) 제공 |

재현 명령:

```powershell
python -m pip install -r requirements.txt
python -m unittest discover -s tests -v
python -m compileall -q scripts
```

사진 점검은 헤더 검사와 제한된 수의 디코딩 미리보기이며, 스티칭·선명도·사람 얼굴·개인정보·복원 가능성을 자동 판정하지 않는다. 공통 지침은 그 결과를 보고 실제 화면을 검사하도록 요구한다. 툴 스키마와 버전 확인은 통합 테스트를 대체하지 않는다.
