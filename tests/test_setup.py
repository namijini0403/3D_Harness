from pathlib import Path
import tempfile
import tomllib
import unittest

from scripts.setup_blender import config_plan, save_config


class SetupTests(unittest.TestCase):
    def test_preserves_model_comments_and_other_servers(self):
        original = '# my settings\nmodel = "gpt-6-astra"\n[mcp_servers.other]\ncommand = "example"\n'
        result = config_plan(original, r'C:\도구 폴더\uvx.exe')
        self.assertTrue(result.startswith(original))
        parsed = tomllib.loads(result)
        self.assertEqual(parsed['model'], 'gpt-6-astra')
        self.assertEqual(parsed['mcp_servers']['other']['command'], 'example')
        self.assertEqual(parsed['mcp_servers']['blender']['command'], r'C:\도구 폴더\uvx.exe')

    def test_repeat_is_identical(self):
        once = config_plan('', 'uvx.exe')
        self.assertEqual(config_plan(once, 'uvx.exe'), once)

    def test_different_existing_config_is_preserved(self):
        with self.assertRaises(ValueError):
            config_plan('[mcp_servers.blender]\ncommand="custom"\n', 'uvx.exe')

    def test_malformed_and_sealed_tables_rejected(self):
        for original in ['invalid = [', 'mcp_servers = {}']:
            with self.assertRaises(ValueError):
                config_plan(original, 'uvx.exe')

    def test_backup_write_and_concurrent_change(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'config.toml'
            original = 'model="gpt-6-astra"\n'
            path.write_text(original, encoding='utf-8')
            updated = config_plan(original, 'uvx.exe')
            save_config(path, original, updated)
            self.assertEqual(path.read_text(encoding='utf-8'), updated)
            copies = list(path.parent.glob('*.bak'))
            self.assertEqual(len(copies), 1)
            self.assertEqual(copies[0].read_text(encoding='utf-8'), original)
            save_config(path, updated, updated)
            self.assertEqual(len(list(path.parent.glob('*.bak'))), 1)
            with self.assertRaises(ValueError):
                save_config(path, original, updated)


if __name__ == '__main__':
    unittest.main()
