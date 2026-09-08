# Blender MCP · 작은 수정과 시각 검증

실제 MCP 도구 목록과 Blender 버전부터 확인한다. `get_scene_info`, `get_object_info`, `execute_blender_code`, `get_viewport_screenshot`이 기본 후보다. 조회 결과가 충분하면 추가 전수 조사를 생략한다. 상세 진단이 필요하면 `scripts/blender_probe.py`를 MCP 코드 실행으로 한 번 실행한다.

```python
exec(compile(open(r"C:\절대경로\3D_Harness\scripts\blender_probe.py", encoding="utf-8").read(), "blender_probe.py", "exec"))
```

위 경로는 **Blender가 실행되는 PC에서 읽을 수 있는 경로**여야 한다. 다른 PC/컨테이너라면 작은 스크립트 내용을 도구 인자로 전달한다. probe는 읽기 전용이며 파일을 저장하지 않는다.

변경 전 `work/checkpoints/`에 새 이름으로 .blend 사본을 저장한다. 기존 장면 전체 삭제 대신 전용 `Harness_` 컬렉션/이름을 사용한다. 객체 생성은 같은 이름 존재 여부를 확인해 갱신하고, 반복 실행 시 중복되지 않게 한다. 한 번에 작은 목적 하나(투영 수정/노드 연결/카메라 배치)를 완료한다. bpy data API를 우선하고 operator는 context를 확인한다.

사진 표시가 목적이면 Environment Texture의 Equirectangular 투영 또는 안쪽을 보는 UV 구를 사용한다. 전자는 배경이며 기하가 아니다. 구는 원점 카메라, UV seam·좌우 반전·안쪽 면·조명 영향을 검사한다. 사진 색을 보존하는 방출 재질을 검토하고 실제 색관리/뷰 변환을 확인한다. 구 밖으로 카메라를 움직여 복원처럼 연출하지 않는다.

메시 작업은 단위(m), 기준 길이의 출처, 출입구/바닥/벽을 먼저 확인하고 재질·장식을 나중에 한다. 수정 뒤 대표 뷰 1장과 필요한 반대 시점을 본다. 웹으로 내보내는 메시의 GLB는 변환된 재질·텍스처 경로·단위·축을 대상 뷰어에서 재확인한다. Gaussian PLY를 일반 메시 PLY처럼 다루지 않는다.

작업 완료는 `.blend` 저장 성공만으로 판단하지 않는다. 실제 사용자 시점에서 확인하고, 바뀐 객체·누락 텍스처 수·체크포인트·미리보기 경로만 요약한다. 장시간 렌더/학습은 MCP의 긴 동기 호출 대신 별도 로컬 작업으로 실행하고 상태 파일로 추적한다. 저장/복원/수정은 동시에 실행하지 않는다.

근거: [Blender MCP](https://github.com/ahujasid/blender-mcp), [Astra 건축 시각화 사례](https://developers.openai.com/blog/architectural-visualization-with-astra). 사례의 절차를 응용한 지침이며 학교 촬영 자료의 복원 성능 증거는 아니다.
