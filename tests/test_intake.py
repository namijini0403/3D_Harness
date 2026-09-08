import hashlib
import json
from pathlib import Path
import tempfile
import unittest

from PIL import Image
from scripts.inspect_panos import inspect


class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.source = self.root / "input"
        self.source.mkdir()
        self.out = self.root / "work"

    def make_image(self, name, size, orientation=1):
        path = self.source / name
        exif = Image.Exif()
        exif[274] = orientation
        Image.new("RGB", size, "navy").save(path, exif=exif)
        return path

    def test_candidates_and_originals_unchanged(self):
        image = self.make_image("학교.jpg", (800, 400))
        before = hashlib.sha256(image.read_bytes()).hexdigest()
        self.make_image("flat.jpg", (640, 360))
        report = inspect(self.source, self.out)
        self.assertEqual(report["counts"], {"check_projection": 1, "candidate_2to1": 1})
        self.assertEqual(before, hashlib.sha256(image.read_bytes()).hexdigest())
        self.assertEqual(len(json.loads((self.out / "report.json").read_text(encoding="utf-8"))["files"]), 2)
        for row in report["files"]:
            with Image.open(self.out / row["preview"]) as preview:
                self.assertFalse(preview.getexif())
                self.assertLessEqual(preview.width, 1024)

    def test_rotation_corrupt_and_raw(self):
        self.make_image("rotate.jpg", (800, 400), 6)
        (self.source / "broken.jpg").write_bytes(b"not a jpeg")
        (self.source / "camera.insv").write_bytes(b"raw placeholder")
        report = inspect(self.source, self.out)
        self.assertEqual(report["counts"], {
            "unreadable": 1, "needs_conversion_or_unsupported": 1, "check_orientation": 1})

    def test_preview_budget(self):
        for n in range(4):
            self.make_image(f"{n}.png", (200, 100))
        result = inspect(self.source, self.out, previews=1)
        self.assertEqual(result["previews"], 1)
        self.assertEqual(len(result["files"]), 4)

    def test_missing_and_overlapping_paths(self):
        for source, target in [(self.root / "missing", self.out),
                               (self.source, self.source),
                               (self.source, self.source / "out"),
                               (self.source, self.root)]:
            with self.assertRaises(ValueError):
                inspect(source, target)

    def test_existing_report_is_not_overwritten(self):
        inspect(self.source, self.out)
        with self.assertRaises(FileExistsError):
            inspect(self.source, self.out)

    def test_empty_input(self):
        result = inspect(self.source, self.out)
        self.assertEqual(result["counts"], {})
        self.assertEqual(result["previews"], 0)

    def test_invalid_preview_budget(self):
        with self.assertRaises(ValueError):
            inspect(self.source, self.out, previews=-1)


if __name__ == "__main__":
    unittest.main()
