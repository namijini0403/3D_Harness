# 360 사진 → 지점 이동 투어

기존 뷰어가 있으면 수리한다. 새 작업은 소수 사진의 코드 작업에 Pannellum, 많은 고해상도 사진의 타일 기반 제작에 Marzipano를 우선 검토한다. 한 프로젝트에 둘을 중복 도입하지 않는다.

1. `python scripts/inspect_panos.py input --out work/intake` 실행(재실행은 새 출력 폴더). 요약 JSON과 샘플 미리보기 1장부터 본다. JPG/PNG 등으로 스티칭된 **단안 전체 구면 2:1**인지 확인한다. `.insv`, dual-fisheye, 16:9 재구도, stereo, partial pano는 별도 변환/설정이 필요하다. 비율만 보고 단정하지 않는다. 제조사 프로그램의 스티칭 내보내기를 우선 사용하며 원본을 늘여서 2:1로 만들지 않는다.
2. 서로 연결되는 2–3개 지점을 골라 ID·파일·시작 방향·연결 지점을 기록한다. 보이지 않는 출입구/연결은 추측 확정하지 않는다. `examples/tour.json`은 기록 형식의 예시이며 뷰어가 직접 읽는 형식은 아니다.
3. 선택한 뷰어의 공식 투어 예제를 바탕으로 **실행 가능한 뷰어**를 만든다. Pannellum은 `scenes`, `hotSpots`, `sceneId`; Marzipano는 export의 `data.js` 구조를 유지한다. Pannellum 각도는 도, Marzipano yaw/pitch는 라디안이다. 좌표를 그대로 복사하지 않는다. 시작 방향과 이동 후 시선은 화면을 보고 보정한다.
4. 먼저 파생본 4096×2048로 검사한다(권장 시작값, 품질 보장값 아님). 글자 판독이 부족하면 해당 장면 해상도/타일을 조정한다. 8192×4096 RGBA 디코딩만 약 128 MiB이며 JPEG 파일 크기와 다르다. 여러 원본을 한 번에 preload하지 않는다. 고해상도는 뷰어의 multires 타일 기능을 쓴다.
5. 결과 폴더만 HTTP로 제공한다. 예: `python -m http.server 8000 --bind 127.0.0.1 --directory output/tour`. `file://`로만 검사하거나 input 폴더 전체를 서버로 열지 않는다. 오프라인 요구가 있으면 JS/CSS/이미지를 로컬에 포함하고 외부 요청 없이 시험한다. 재배포 라이선스를 동봉한다.

완료: 첫 장면 로딩 → 상하좌우 회전 → 모든 의도된 링크 이동 → 복귀/장면 목록 → 새로고침을 실제 브라우저에서 확인. 좌우 반전·이음새·수평선·핫스폿 목적지·오류 화면을 확인한다. 대상 PC에서 확인하고, 휴대폰이 목표면 실제 휴대폰 검증 또는 미검증 표시. 학교 이름·얼굴·게시판은 공유 전에 검토한다. 결과 폴더·실행 명령·확인 화면·미검증 항목을 전달한다.

검은 화면은 이미지 요청 실패/상대 경로/콘솔/WebGL 한도부터, 늘어짐은 투영부터, 이동 시 뒤돌아봄은 노드 방향부터 검사한다. 이 경로에는 Blender 렌더링이나 3DGS 학습이 필수 사항이 아니다.

근거: [Pannellum 투어](https://pannellum.org/documentation/examples/tour/), [Pannellum 배포](https://github.com/mpetroff/pannellum), [Marzipano Tool](https://www.marzipano.net/tool/).
