#!/usr/bin/env python3
"""Scan all images in Albums and report any that contain GPS EXIF data."""

from __future__ import annotations

import sys
from pathlib import Path

from PIL import Image, ExifTags

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

ALBUMS_DIR = Path("Albums")
VALID_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

# EXIF IFD pointer for GPS data
GPS_IFD_TAG = 0x8825


def has_gps_data(image_path: Path) -> dict | None:
    """Return GPS EXIF dict if present, otherwise None."""
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if not exif:
                return None

            gps_ifd = exif.get_ifd(GPS_IFD_TAG)
            if gps_ifd:
                # Translate numeric tag IDs to human-readable names
                readable = {}
                for tag_id, value in gps_ifd.items():
                    tag_name = ExifTags.GPSTAGS.get(tag_id, f"Unknown({tag_id})")
                    readable[tag_name] = value
                return readable

    except Exception as e:
        print(f"  Error reading {image_path}: {e}", file=sys.stderr)

    return None


def main() -> int:
    """Main entry point for the script."""
    if not ALBUMS_DIR.exists():
        print(f"Directory {ALBUMS_DIR} not found.", file=sys.stderr)
        return EXIT_FAILURE

    found_count = 0

    for album_dir in sorted(ALBUMS_DIR.iterdir()):
        if not album_dir.is_dir() or album_dir.name.startswith("."):
            continue

        for image_path in sorted(album_dir.iterdir()):
            if image_path.suffix.lower() not in VALID_EXTENSIONS:
                continue

            gps = has_gps_data(image_path)
            if gps:
                found_count += 1
                print(f"{image_path}")
                for key, value in gps.items():
                    print(f"  {key}: {value}")
                print()

    if found_count == 0:
        print("No images with GPS data found.")
    else:
        print(f"Total: {found_count} image(s) with GPS data.")

    return EXIT_SUCCESS


if __name__ == "__main__":
    sys.exit(main())
