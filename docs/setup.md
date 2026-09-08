# 최초 연결 · 선생님용

## Windows 자동 설치

Codex에 **“Blender MCP 자동 설치하고 연결 확인해줘”**라고 하면 됩니다. 에이전트는 아래 스크립트의 `-CheckOnly`로 먼저 점검한 뒤 설치를 실행합니다. 이미 정상 연결되면 설치를 생략합니다.

```powershell
powershell -NoProfile -File scripts/setup-blender.ps1 -CheckOnly
powershell -NoProfile -File scripts/setup-blender.ps1
```

자동 처리: Blender와 uv 탐색 → 없으면 winget으로 설치 → 격리된 Python과 Blender MCP 1.9.1 준비 → 선택한 Blender에 애드온 설치·활성화 → 텔레메트리 끄기 → Codex 설정 추가. Codex CLI 설치는 필요하지 않습니다. 기존 모델과 다른 MCP 설정은 유지하고 설정/Blender 환경설정은 변경 전에 백업합니다. 같은 설치의 재실행은 중복 등록하지 않습니다.

**설치 후에는 Blender를 열고 Codex 세션을 다시 시작하세요.** 1.9.1 애드온의 기본 자동 시작 기능을 사용합니다. 실제 장면 조회와 스크린샷까지 성공해야 연결 완료로 기록합니다. 예전 파일/설정에서 자동 시작이 꺼져 있거나 연결이 실패하면 아래 수동 연결을 사용합니다. 설치 완료를 연결 성공으로 표시하지 않습니다.

- Blender가 열려 있으면 저장하고 닫은 뒤 재실행합니다. 설치기가 강제 종료하지 않습니다.
- 다른 버전/설정이 있으면 보존하고 충돌을 알립니다. 에이전트가 해당 설정을 확인해 기존 연결을 우선 수리합니다.
- Blender가 여러 개면 자동 탐색된 버전을 점검하고 필요 시 `-BlenderPath 'C:\Program Files\Blender Foundation\Blender 4.5\blender.exe'`로 지정합니다.
- winget이 없거나 학교 PC의 설치 권한/실행 정책에 막히면 해당 항목만 수동 설치합니다. 보안 정책을 자동으로 해제하지 않습니다. OS 권한 창·앱 재시작은 자동으로 대신할 수 없을 수 있습니다.
- 이 스크립트는 Windows용입니다. macOS/Linux는 아래 공식 안내를 따릅니다.

개발 중에는 설치 없는 점검과 설정 보존 테스트를 수행했습니다. **실제 Blender가 없는 이 개발 PC에서 전체 설치·연결 성공을 검증하지는 못했습니다.**

## 수동 설치 / 기존 설정 연결

기존 Blender/Codex 설정이 있으면 먼저 그대로 연결해 확인합니다. 자동 업그레이드나 전체 설정 덮어쓰기는 하지 않습니다.

1. Blender를 설치해 열고, Codex에서 이 저장소 폴더와 GPT-6 Astra를 선택합니다. 모델 선택지에 없다면 계정에서의 제공 여부를 확인합니다. 모델을 임의로 바꾸지 않습니다.
2. `uvx --version`을 실행합니다. 없다면 [uv 공식 설치 안내](https://docs.astral.sh/uv/getting-started/installation/)로 설치하고 터미널/Codex를 다시 엽니다.
3. 새로 설치할 때만 터미널에서 실행합니다. 2026-09-09에 PyPI 배포를 확인한 **1.9.1**로 서버와 애드온을 맞췄습니다. 이 버전의 실제 Blender 통합 테스트는 이 저장소에서 수행하지 못했습니다.

```powershell
uvx blender-mcp==1.9.1 install-addon
codex mcp add blender --env DISABLE_TELEMETRY=true -- uvx blender-mcp==1.9.1
```

4. Blender → Edit → Preferences → Add-ons → `MCP for Blender` 활성화. 3D Viewport에서 `N` → MCP 패널 → `Start MCP Server`. 화면 이름은 설치 버전에 따라 다를 수 있습니다.
5. Codex를 새 세션으로 열고 `Blender 연결을 확인하고 현재 장면을 요약해줘`라고 합니다. 도구 목록 확인 → 장면 조회 → 스크린샷 순서로 확인합니다. 목록에 있다는 사실만으로 연결 성공은 아닙니다.
6. 정상 연결 후 [config 예제](../config/codex.example.toml)의 `enabled_tools`를 기존 설정의 Blender 항목에 합칩니다. **전체 config를 교체하지 마세요.** 이미 같은 서버가 있으면 중복 등록하지 않습니다. 현재 도구 이름이 다르면 실제 목록에 맞춥니다.

공식 [Codex MCP 안내](https://learn.chatgpt.com/docs/extend/mcp?surface=cli), [Blender MCP 설치 안내](https://github.com/ahujasid/blender-mcp)를 기준으로 작성했습니다. 이 저장소는 MCP를 포크하지 않고 연결하므로 유지보수할 코드와 의존성을 줄였습니다.

## 연결이 안 될 때

| 증상 | 먼저 확인할 것 |
|---|---|
| `uvx`를 못 찾음 | `Get-Command uvx`로 경로 확인, 앱 재시작, 필요 시 config의 command를 절대 경로로 지정 |
| 서버는 보이는데 장면 조회 실패 | Blender 실행·애드온 활성화·Start 상태, 127.0.0.1:9876, 중복 클라이언트 |
| 도구 목록이 비어 있음 | 허용 목록 이름과 설치된 도구 이름 비교, 서버/애드온 버전 |
| 타임아웃 | 장면 변화·실행 중 작업을 먼저 확인. 무작정 같은 생성 코드를 다시 실행하지 않음 |
| 학교 PC 설치 제한 | 사용 가능한 기존 도구로 사진 투어부터 진행, 필요한 설치 항목만 담당자에게 전달 |

학교 자료는 로컬에 둡니다. MCP 텔레메트리를 끄고 Poly Haven·Sketchfab·외부 생성 기능은 실제로 필요할 때만 켭니다. Blender 코드 실행 권한은 강하므로 작업 전 사본을 저장하고, MCP 포트를 외부에 노출하지 않습니다.

AGENTS.md는 프로젝트 지침입니다. 사용자 전역 지침이나 상위 폴더 지침과 충돌하면 Codex에 충돌 위치를 확인시킵니다. 일반 ChatGPT 대화에 파일 하나를 붙이는 것과 프로젝트 폴더를 여는 것은 다릅니다. [적용 범위](https://learn.chatgpt.com/docs/agent-configuration/agents-md).
