# 연속 이동이 꼭 필요할 때

먼저 GPU/VRAM, OS, 촬영 경로, 서로 다른 위치에서 찍힌 겹치는 영상/사진을 확인한다. 한 지점의 360 사진을 여러 방향으로 잘라도 촬영 위치의 변화가 생기지는 않는다. 단안 깊이 추정으로 만든 공간은 추정임을 표시한다.

**작은 구간 → 카메라 정합 확인 → 학습 → 시청 검증** 순서다. 기존 설치가 있으면 유지한다. 새로 거대한 GPU 환경을 설치하기 전에 정합 가능한 입력과 목표를 확인한다. Blender MCP는 복원 엔진 자체가 아니다.

- 입력: 제조사 소프트웨어에서 스티칭한 equirectangular 이미지/영상. 흔들린 프레임·중복 정지 프레임을 줄이고 같은 물체가 다른 위치에서 관찰되는 구간을 고른다. 재촬영이면 정지된 공간, 충분한 빛, 느린 이동, 겹치는 경로를 우선한다. 벽만 보이는 구간·반사·사람 움직임은 실패 후보다.
- 처리: Nerfstudio는 equirectangular 입력을 지원한다. 설치된 `ns-process-data images --help`로 옵션을 확인한 뒤 아래 예제를 작은 샘플에 적용한다. 이미 perspective로 분할했다면 다시 equirectangular 처리하지 않는다.

```text
ns-process-data images --camera-type equirectangular --images-per-equirect 8 --data input/sample360 --output-dir work/reconstruction
ns-train splatfacto --data work/reconstruction
```

두 번째 명령은 **정합을 확인한 뒤에만** 실행한다. 등록 카메라 수/전체 수, 카메라 경로·희소점군 스크린샷, 분리된 방/뒤집힌 포즈를 기록한다. 낮은 정합률·틀린 포즈는 학습 횟수를 늘려 해결하지 않는다. 8→14 분할은 가능한 실험이며 추가 시점 촬영을 대체하지 않는다. 캡처 장비/촬영자는 지원되는 마스크나 crop으로 제외한다. 이미지에 검은색을 칠하는 것을 마스크로 간주하지 않는다.

- 출력: Gaussian은 SuperSplat 등 지원 뷰어에서 확인한다. 일반 PLY와 Gaussian 속성이 든 PLY는 다르다. Gaussian이 자동으로 충돌 가능한 벽/바닥이나 정밀 치수를 제공한다고 가정하지 않는다. 충돌 이동이 필요하면 별도 단순 메시가 필요하다.
- 품질: 학습에 넣지 않은 참조 사진/영상과 같은 시점으로 비교하고, 촬영 경로 안의 이동에서 구멍·떠다니는 점·과도한 흐림을 본다. 지원 대상 장치에서 로딩/회전/이동을 확인한 뒤 전체 범위로 확장한다.
- 실패: 입력 부족이면 좋은 파노라마 투어를 먼저 전달하고 추가 촬영 위치만 표시한다. 무한 학습/임의 구조 생성으로 성공을 꾸미지 않는다.

근거: [Nerfstudio 360 입력](https://docs.nerf.studio/quickstart/custom_dataset.html#data-equirectangular), [Splatfacto](https://docs.nerf.studio/nerfology/methods/splat.html), [COLMAP 촬영·정합](https://colmap.github.io/tutorial.html), [SuperSplat](https://github.com/playcanvas/supersplat). 명령은 공식 문서 기반 예제이며 이 PC에서 GPU 학습을 실행하지 않았다.
