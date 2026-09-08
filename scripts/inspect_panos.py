"""Local intake only. A 2:1 aspect ratio is a candidate, not proof of projection."""
import argparse
from collections import Counter
import json
from pathlib import Path
import warnings

from PIL import Image

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"}


def inspect(source, destination, previews=6):
    source, destination = Path(source).resolve(), Path(destination).resolve()
    if not source.is_dir():
        raise ValueError("Input directory does not exist")
    if destination == source or source in destination.parents or destination in source.parents:
        raise ValueError("Input and output directories must not overlap")
    if not 0 <= previews <= 24:
        raise ValueError("Preview count must be between 0 and 24")
    # A fresh directory avoids accidentally overwriting an earlier diagnosis.
    destination.mkdir(parents=True, exist_ok=False)
    rows, made = [], 0
    with warnings.catch_warnings():
        warnings.simplefilter("error", Image.DecompressionBombWarning)
        for path in sorted(source.rglob("*")):
            if not path.is_file():
                continue
            row = {"file": path.relative_to(source).as_posix()}
            if path.is_symlink() or not path.resolve().is_relative_to(source):
                row["status"] = "skipped_link"
            elif path.suffix.lower() not in SUPPORTED:
                row["status"] = "needs_conversion_or_unsupported"
            else:
                try:
                    with Image.open(path) as im:
                        width, height = im.size
                        orientation = im.getexif().get(274, 1)
                        row.update(width=width, height=height,
                                   disk_mib=round(path.stat().st_size / 2**20, 2),
                                   rgba_mib=round(width * height * 4 / 2**20, 2),
                                   exif_orientation=orientation)
                        row["status"] = ("candidate_2to1" if width == height * 2
                                         else "check_projection")
                        if orientation != 1:
                            row["status"] = "check_orientation"
                        im.verify()
                    if made < previews:
                        with Image.open(path) as im:
                            im.thumbnail((1024, 512))
                            # A new RGB image intentionally drops EXIF/GPS metadata.
                            preview = Image.new("RGB", im.size)
                            preview.paste(im.convert("RGB"))
                            name = f"preview-{made + 1:02d}.jpg"
                            preview.save(destination / name, quality=85)
                        row["preview"] = name
                        made += 1
                except (OSError, ValueError, SyntaxError,
                        Image.DecompressionBombWarning, Image.DecompressionBombError) as exc:
                    row["status"] = "unreadable"
                    row["error"] = type(exc).__name__
            rows.append(row)
    report = {"files": rows, "counts": dict(Counter(r["status"] for r in rows)),
              "previews": made,
              "limits": "Header checks for all supported images; decoded previews only. "
                        "No projection, sharpness, privacy or reconstruction certification."}
    (destination / "report.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--previews", type=int, default=6)
    args = parser.parse_args()
    try:
        result = inspect(args.input, args.out, args.previews)
    except (OSError, ValueError) as exc:
        parser.exit(2, f"{exc}\n")
    print(json.dumps({"counts": result["counts"], "previews": result["previews"],
                      "report": str(args.out / "report.json")}, ensure_ascii=True))


if __name__ == "__main__":
    main()
