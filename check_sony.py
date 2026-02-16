#!/usr/bin/env python3
"""
Check EXIF data for Sony camera images in all albums.
Usage: python check_sony.py
"""

import os
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


def get_device_make(image_path):
    """Extract the device make from an image's EXIF data."""
    try:
        with Image.open(image_path) as img:
            exif = img.getexif()
            if not exif:
                return None
            for tag_id, value in exif.items():
                tag_name = TAGS.get(tag_id, tag_id)
                if tag_name == "Make":
                    return str(value).strip()
    except Exception:
        return None
    return None


def check_albums(albums_dir="Albums"):
    """Scan all albums and print images where the device make is Sony."""
    if not os.path.exists(albums_dir):
        print(f"Error: Directory '{albums_dir}' not found.")
        return

    root_path = Path(albums_dir)
    valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".tiff", ".tif"}
    total_images = 0
    sony_images = 0

    print("=" * 80)
    print("SONY DEVICE MAKE CHECK")
    print("=" * 80)

    for album_dir in sorted(root_path.iterdir()):
        if not album_dir.is_dir() or album_dir.name.startswith("."):
            continue

        album_matches = []

        for file in sorted(album_dir.iterdir()):
            if file.suffix.lower() not in valid_extensions:
                continue
            total_images += 1
            make = get_device_make(file)
            if make and make.lower().startswith("sony"):
                sony_images += 1
                album_matches.append((file.name, make))

        if album_matches:
            print(f"\n📁 ALBUM: {album_dir.name}")
            print("-" * 80)
            for filename, make in album_matches:
                print(f"  {filename}  (Make: {make})")

    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total images checked: {total_images}")
    print(f"Sony images found:    {sony_images}")
    print()


if __name__ == "__main__":
    check_albums()
