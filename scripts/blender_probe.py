"""Run INSIDE Blender via MCP. Read-only; bounded JSON output."""
import json
from pathlib import Path
import bpy

scene = bpy.context.scene
missing = []
for image in bpy.data.images:
    if image.source == "FILE" and not image.packed_file and image.filepath:
        resolved = bpy.path.abspath(image.filepath, library=image.library)
        if not Path(resolved).is_file():
            missing.append(image.name)

print(json.dumps({
    "blender": bpy.app.version_string,
    "saved": bool(bpy.data.filepath),
    "scene": scene.name,
    "objects": len(scene.objects),
    "active_camera": scene.camera.name if scene.camera else None,
    "units": scene.unit_settings.system,
    "scale_length": scene.unit_settings.scale_length,
    "engine": scene.render.engine,
    "resolution": [scene.render.resolution_x, scene.render.resolution_y],
    "resolution_percent": scene.render.resolution_percentage,
    "missing_file_images_count": len(missing),
    "missing_file_images_sample": missing[:10],
    "limits": "Checks FILE images only; not UDIM, sequences, linked assets or visual quality."
}, ensure_ascii=True))
