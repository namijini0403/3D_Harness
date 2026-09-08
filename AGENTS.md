# School spatial-memory harness

Deliver a usable, faithful spatial experience with minimal user effort. Reply in Korean.
Read `STATE.md` if present, then only the relevant `recipes/` file. Do not preload research or all recipes.

## Route before building
- Existing project: inspect and repair the smallest failing part; preserve its stack.
- Stitched 360 photos + click-to-move: `recipes/tour.md` (default for this project).
- Continuous positional movement: `recipes/reconstruction.md`; panoramas alone are not geometry.
- Editable geometry, materials, camera or Blender diagnosis: `recipes/blender.md`.
- Missing connection: `docs/setup.md`. Missing media: finish setup, then ask for one sample and its intended movement.

## Work contract
1. Inspect available files, one representative image and current output. State the likely failure and chosen route briefly. Infer routine details; ask only for missing facts that change the result.
2. Get one room / 2–3 nodes working before scaling. Preserve capture truth; label estimated dimensions and invented geometry. Never describe a panorama sphere or generated mesh as measured reconstruction.
3. Use local scripts for repeatable processing; MCP for Blender state and targeted execution. Discover actual tool names. Serialize Blender mutations; batch related edits in one bounded script. Save a new checkpoint first. Scope edits to owned objects; make reruns safe.
4. Return counts, errors and artifact paths, not full scene dumps. Inspect one preview per meaningful change, more only for unresolved defects. On the same failure twice, change the hypothesis or route; do not repeat blindly. After a timeout inspect state before rerunning.
5. Verify the user's experience: image orientation, readable detail, links/movement and target-device loading. Test affected behavior, then stop when acceptance passes. If a check cannot run, record it as unverified, never passed.
6. Keep originals untouched. Work in `work/`, deliver in `output/`. Keep school media and derived previews out of Git; do not upload them or enable external generation services without authorization. This does not block local work.
7. Update `STATE.md` in at most 15 lines: goal, route, inputs, versions, artifacts, evidence, failure, next action. Final: result path, checks, remaining limitation. Avoid re-exploration, unsolicited features and subagents by default.

Optimize total successful-task cost, not merely answer length. Keep the selected Astra model; start with the user's reasoning setting. Increase effort only for a diagnosed hard problem. No claimed savings without measured runs.
