"""Runs in background Blender; never opens/saves a project or changes startup.blend."""
import json
from pathlib import Path
import sys
import bpy

mode = sys.argv[sys.argv.index('--') + 1]
if mode == 'inspect':
    print('HARNESS_SETUP=' + json.dumps({
        'addons': str(Path(bpy.utils.user_resource('SCRIPTS', create=True)) / 'addons'),
        'preferences': str(Path(bpy.utils.user_resource('CONFIG', create=True)) / 'userpref.blend'),
    }))
elif mode == 'enable':
    bpy.utils.refresh_script_paths()
    bpy.ops.preferences.addon_enable(module='blender_mcp')
    addon = bpy.context.preferences.addons.get('blender_mcp')
    if addon is None:
        raise RuntimeError('Blender MCP did not enable')
    addon.preferences.telemetry_consent = False
    if bpy.ops.wm.save_userpref() != {'FINISHED'}:
        raise RuntimeError('Could not save Blender preferences')
    print('HARNESS_SETUP=' + json.dumps({'enabled': True}))
else:
    raise ValueError('Unknown setup mode')
