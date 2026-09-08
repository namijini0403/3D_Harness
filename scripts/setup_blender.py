"""Called by setup-blender.ps1 with an isolated blender-mcp dependency."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import uuid

TOOLS = ["get_scene_info", "get_object_info", "execute_blender_code", "get_viewport_screenshot"]


def config_plan(original, uvx):
    parsed = tomllib.loads(original)
    expected = {"command": str(uvx), "args": ["blender-mcp==1.9.1"],
                "enabled_tools": TOOLS, "startup_timeout_sec": 60, "tool_timeout_sec": 120,
                "env": {"DISABLE_TELEMETRY": "true", "BLENDER_HOST": "127.0.0.1", "BLENDER_PORT": "9876"}}
    existing = parsed.get("mcp_servers", {}).get("blender")
    if existing is not None:
        if existing == expected:
            return original
        raise ValueError("Existing blender MCP config preserved. Inspect it before changing versions or paths.")
    block = '\n\n[mcp_servers.blender]\n'
    for key, value in expected.items():
        if key != "env":
            block += f'{key} = {json.dumps(value, ensure_ascii=False)}\n'
    block += '\n[mcp_servers.blender.env]\n'
    block += ''.join(f'{k} = {json.dumps(v)}\n' for k, v in expected["env"].items())
    result = original + block
    tomllib.loads(result)  # Reject sealed inline tables and malformed input before writes.
    return result


def backup(path):
    if path.is_file():
        saved = path.with_name(path.name + '.harness-' + uuid.uuid4().hex[:12] + '.bak')
        shutil.copy2(path, saved)
        return saved


def save_config(path, original, updated):
    path = Path(path)
    current = path.read_text(encoding='utf-8-sig') if path.exists() else ''
    if current != original:
        raise ValueError('Config changed during setup; no config was overwritten. Rerun setup.')
    if updated == original:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    backup(path)
    with tempfile.NamedTemporaryFile(mode='w', encoding='utf-8', dir=path.parent, delete=False) as temp:
        temp.write(updated)
        temporary = Path(temp.name)
    try:
        os.replace(temporary, path)
    finally:
        temporary.unlink(missing_ok=True)


def blender_step(executable, mode):
    helper = Path(__file__).with_name('setup_blender_addon.py')
    result = subprocess.run([str(executable), '--background', '--python-exit-code', '1',
                             '--python', str(helper), '--', mode],
                            capture_output=True, encoding='utf-8', errors='replace', timeout=120)
    if result.returncode:
        raise RuntimeError('Blender setup failed: ' + result.stderr[-1500:] + result.stdout[-1500:])
    for line in result.stdout.splitlines():
        if line.startswith('HARNESS_SETUP='):
            return json.loads(line.split('=', 1)[1])
    raise RuntimeError('Blender did not return setup confirmation')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--blender', required=True, type=Path)
    parser.add_argument('--uvx', required=True, type=Path)
    parser.add_argument('--config', type=Path, default=Path(os.environ.get('CODEX_HOME', Path.home() / '.codex')) / 'config.toml')
    args = parser.parse_args()
    original = args.config.read_text(encoding='utf-8-sig') if args.config.exists() else ''
    updated = config_plan(original, args.uvx)
    info = blender_step(args.blender, 'inspect')
    # Use the exact selected Blender's directory, including on a first launch.
    from blender_mcp.addon_manager import get_bundled_addon_path, find_existing_addon_installs
    source = get_bundled_addon_path()
    directory = Path(info['addons'])
    target = directory / 'blender_mcp.py'
    existing = find_existing_addon_installs([directory]) if directory.exists() else []
    if any(p != target for p in existing):
        raise ValueError('Existing differently named Blender MCP addon preserved; inspect it first.')
    if target.exists() and target.read_bytes() != source.read_bytes():
        raise ValueError('Existing different addon preserved; inspect its version before upgrading.')
    directory.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        shutil.copy2(source, target)
    pref_backup = backup(Path(info['preferences']))
    enabled = blender_step(args.blender, 'enable')
    save_config(args.config, original, updated)
    print(json.dumps({'installed': True, 'addon': str(target), 'enabled': enabled['enabled'],
                      'config': str(args.config), 'preferences_backup': str(pref_backup) if pref_backup else None,
                      'connection': 'unverified: open Blender and restart Codex, then query scene and screenshot'}, ensure_ascii=True))


if __name__ == '__main__':
    main()
