import os
import json
import re
import tempfile
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Any
from PIL import Image, ImageOps, ExifTags

ALBUMS_DIR = "Albums"
OUTPUT_FILE = "albums_metadata.json"

# EXIF Tag Mapping
# Using numeric constants or names where available in ExifTags.TAGS
# We'll rely on the tag names provided by PIL where possible, but mapping them to our schema
TAGS_TO_EXTRACT = {
    "DateTimeOriginal": "date_taken",
    "Model": "camera_model",
    "LensModel": "lens_model",
    "FocalLength": "focal_length",
    "ISOSpeedRatings": "iso",
    "FNumber": "aperture",
    "ExposureTime": "shutter_speed"
}

# Artist and Copyright EXIF tag IDs
ARTIST_TAG = 0x013B       # 315
COPYRIGHT_TAG = 0x8298    # 33432
GPS_IFD_TAG = 0x8825      # 34853 – pointer to GPS Info IFD
EXPECTED_ARTIST = "Chris Risner"
EXPECTED_COPYRIGHT = "Copyright 2026 Chris Risner"

def sanitize_exif_string(value):
    """
    Remove null bytes and control characters from EXIF strings.
    
    Args:
        value: EXIF value (any type)
    
    Returns:
        Cleaned string or original value if not string
    """
    if not isinstance(value, str):
        return value
    
    # Remove control characters (0x00-0x1f, 0x7f-0x9f)
    cleaned = re.sub(r'[\x00-\x08\x0b-\x0c\x0e-\x1f\x7f-\x9f]', '', value)
    cleaned = cleaned.strip()
    
    return cleaned if cleaned else None

def check_and_update_artist_copyright(image_path: Path) -> dict:
    """
    Check Artist and Copyright EXIF fields and update them if incorrect.
    Also strips any GPS/location data from the image EXIF.

    Saves the image in-place with corrected EXIF data, preserving JPEG
    quality via ``quality='keep'``.

    Args:
        image_path: Path to the image file

    Returns:
        Dict describing any fields that were changed, or empty dict
    """
    changes = {}
    try:
        img = Image.open(image_path)
        exif = img.getexif()

        current_artist = sanitize_exif_string(exif.get(ARTIST_TAG, "")) or ""
        current_copyright = sanitize_exif_string(exif.get(COPYRIGHT_TAG, "")) or ""

        artist_needs_update = current_artist != EXPECTED_ARTIST
        copyright_needs_update = current_copyright != EXPECTED_COPYRIGHT

        # Check for GPS data in both the top-level tag and the GPS IFD
        has_gps = GPS_IFD_TAG in exif or bool(exif.get_ifd(GPS_IFD_TAG))

        if not artist_needs_update and not copyright_needs_update and not has_gps:
            img.close()
            return {}

        if artist_needs_update:
            changes["artist"] = {
                "old": current_artist or "(not set)",
                "new": EXPECTED_ARTIST
            }
            exif[ARTIST_TAG] = EXPECTED_ARTIST

        if copyright_needs_update:
            changes["copyright"] = {
                "old": current_copyright or "(not set)",
                "new": EXPECTED_COPYRIGHT
            }
            exif[COPYRIGHT_TAG] = EXPECTED_COPYRIGHT

        if has_gps:
            # Remove the GPS IFD pointer from the top-level EXIF
            if GPS_IFD_TAG in exif:
                del exif[GPS_IFD_TAG]
            changes["gps"] = {"old": "present", "new": "removed"}

        # Fully load pixel data before saving back to the same path
        img.load()

        # Use the actual image format detected by Pillow rather than
        # relying on the file extension, which may not match.
        img_format = img.format or ""
        save_kwargs = {"exif": exif.tobytes()}

        if img_format.upper() == "JPEG":
            try:
                # Try lossless round-trip first
                save_kwargs["quality"] = "keep"
                save_kwargs["subsampling"] = "keep"
                _safe_save(img, image_path, save_kwargs)
            except Exception:
                # Fall back to high-quality save
                save_kwargs["quality"] = 98
                save_kwargs.pop("subsampling", None)
                _safe_save(img, image_path, save_kwargs)
        else:
            if img_format.upper() == "WEBP":
                save_kwargs["quality"] = 95
            _safe_save(img, image_path, save_kwargs)

        img.close()

        updated_fields = []
        if artist_needs_update:
            updated_fields.append("Artist")
        if copyright_needs_update:
            updated_fields.append("Copyright")
        if has_gps:
            updated_fields.append("GPS (removed)")
        print(f"  Updated {', '.join(updated_fields)} for {image_path.name}")

    except Exception as e:
        print(f"Error updating Artist/Copyright for {image_path}: {e}")

    return changes


def _safe_save(img: Image.Image, target_path: Path, save_kwargs: dict):
    """
    Save an image to a temporary file first, then replace the original.

    This prevents a failed or partial write from corrupting the source file.

    Args:
        img: Pillow Image to save
        target_path: Final destination path
        save_kwargs: Keyword arguments forwarded to ``Image.save``
    """
    parent = target_path.parent
    fd, tmp_path = tempfile.mkstemp(
        suffix=target_path.suffix, dir=parent
    )
    os.close(fd)
    try:
        img.save(tmp_path, **save_kwargs)
        shutil.move(tmp_path, target_path)
    except Exception:
        # Clean up the temp file on failure
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
        raise


def get_exif_data(image_path):
    exif_data = {}
    try:
        with Image.open(image_path) as img:
            raw_exif = img.getexif()
            if not raw_exif:
                return {}

            # Search top-level EXIF tags
            for tag_id, value in raw_exif.items():
                tag_name = ExifTags.TAGS.get(tag_id)
                if tag_name in TAGS_TO_EXTRACT:
                    # Sanitize string values before formatting
                    sanitized_value = sanitize_exif_string(value)
                    if sanitized_value is not None:
                        key = TAGS_TO_EXTRACT[tag_name]
                        exif_data[key] = clean_value(key, sanitized_value)
            
            # Search EXIF IFD (contains detailed camera settings)
            exif_ifd = raw_exif.get_ifd(0x8769)
            if exif_ifd:
                for tag_id, value in exif_ifd.items():
                    tag_name = ExifTags.TAGS.get(tag_id)
                    if tag_name in TAGS_TO_EXTRACT:
                        # Sanitize string values before formatting
                        sanitized_value = sanitize_exif_string(value)
                        if sanitized_value is not None:
                            key = TAGS_TO_EXTRACT[tag_name]
                            exif_data[key] = clean_value(key, sanitized_value)
    except Exception as e:
        print(f"Error reading EXIF for {image_path}: {e}")
    
    return exif_data

def clean_value(key, value):
    """Format EXIF values into readable strings."""
    if key == "focal_length":
        # Tuple (numerator, denominator) or float
        if isinstance(value, tuple) and len(value) == 2:
             if value[1] != 0:
                 return f"{value[0]/value[1]} mm"
        try:
             return f"{float(value)} mm"
        except:
             pass
    
    if key == "aperture":
        if isinstance(value, tuple) and len(value) == 2:
            if value[1] != 0:
                return f"f/{value[0]/value[1]}"
        try:
             return f"f/{float(value)}"
        except:
             pass

    if key == "shutter_speed":
        # Often a tuple (1, 100) -> "1/100"
        if isinstance(value, tuple) and len(value) == 2:
            if value[0] == 1 and value[1] > 1:
                return f"1/{value[1]}s"
            if value[1] != 0:
                val = value[0] / value[1]
                if val < 1 and val > 0:
                     return f"1/{int(1/val)}s"
                return f"{val}s"
        try:
             val = float(value)
             if val < 1 and val > 0:
                 return f"1/{int(1/val)}s"
             return f"{val}s"
        except:
             pass

    if key == "iso":
        # Can be a tuple or int
        if isinstance(value, tuple):
             return value[0]
        return value

    return str(value)

class ChangeTracker:
    """Track all changes during album scanning for reporting."""
    
    def __init__(self):
        self.start_time = datetime.now()
        self.changes_by_album = {}
        self.albums_added = []
        self.albums_removed = []
    
    def log_photo_added(self, album: str, filename: str, sort_index: int):
        self._ensure_album(album)
        self.changes_by_album[album]["photos_added"].append({
            "filename": filename,
            "sort_index": sort_index,
            "reason": "new photo in folder"
        })
    
    def log_photo_removed(self, album: str, filename: str, sort_index: int):
        self._ensure_album(album)
        self.changes_by_album[album]["photos_removed"].append({
            "filename": filename,
            "previous_sort_index": sort_index,
            "reason": "no longer in folder"
        })
    
    def log_photo_updated(self, album: str, filename: str, changes: Dict):
        self._ensure_album(album)
        self.changes_by_album[album]["photos_updated"].append({
            "filename": filename,
            "changes": changes
        })
    
    def log_album_added(self, album: str):
        self.albums_added.append(album)
    
    def log_album_removed(self, album: str):
        self.albums_removed.append(album)
    
    def _ensure_album(self, album: str):
        if album not in self.changes_by_album:
            self.changes_by_album[album] = {
                "photos_added": [],
                "photos_removed": [],
                "photos_updated": []
            }
    
    def generate_report(self) -> Dict[str, Any]:
        """Generate complete change log report."""
        duration = (datetime.now() - self.start_time).total_seconds()
        
        # Calculate summary
        total_added = sum(len(a["photos_added"]) for a in self.changes_by_album.values())
        total_removed = sum(len(a["photos_removed"]) for a in self.changes_by_album.values())
        total_updated = sum(len(a["photos_updated"]) for a in self.changes_by_album.values())
        
        return {
            "timestamp": self.start_time.isoformat(),
            "scan_duration_seconds": round(duration, 2),
            "summary": {
                "albums_added": len(self.albums_added),
                "albums_removed": len(self.albums_removed),
                "photos_added": total_added,
                "photos_removed": total_removed,
                "photos_updated": total_updated
            },
            "albums_added": self.albums_added,
            "albums_removed": self.albums_removed,
            "changes": [
                {
                    "album": album,
                    **details
                }
                for album, details in self.changes_by_album.items()
                if details["photos_added"] or details["photos_removed"] or details["photos_updated"]
            ]
        }
    
    def save_to_file(self, directory: str = "AlbumChanges"):
        """Save change log to timestamped JSON file."""
        os.makedirs(directory, exist_ok=True)
        
        timestamp = self.start_time.strftime("%Y%m%d_%H%M%S")
        filename = f"album_changes_{timestamp}.json"
        filepath = os.path.join(directory, filename)
        
        report = self.generate_report()
        
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"Change log saved to {filepath}")
        return filepath

def load_existing_metadata(filepath: str) -> Dict[str, Any]:
    """Load and validate existing metadata file."""
    if not os.path.exists(filepath):
        print(f"No existing metadata at {filepath}, creating fresh scan.")
        return {}
    
    try:
        with open(filepath, 'r') as f:
            return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error loading existing metadata: {e}")
        print("Proceeding with fresh scan.")
        return {}

def merge_photo_metadata(
    old_photos: List[Dict],
    new_scanned_photos: List[Dict],
    changes: ChangeTracker,
    album_name: str
) -> List[Dict]:
    """
    Merge old and new photo metadata, preserving sort_index and photo_name.
    
    Args:
        old_photos: Photos from existing albums_metadata.json
        new_scanned_photos: Photos scanned from filesystem
        changes: ChangeTracker instance for logging
        album_name: Name of album being processed
    
    Returns:
        Merged list of photos with preserved and updated fields
    """
    # Build lookup by filename
    old_by_filename = {p['filename']: p for p in old_photos}
    new_by_filename = {p['filename']: p for p in new_scanned_photos}
    
    # Track filenames
    old_filenames = set(old_by_filename.keys())
    new_filenames = set(new_by_filename.keys())
    
    # Identify changes
    kept_filenames = old_filenames & new_filenames
    removed_filenames = old_filenames - new_filenames
    added_filenames = new_filenames - old_filenames
    
    # Build result list
    merged_photos = []
    
    # 1. Process existing photos (preserve sort_index and photo_name)
    for filename in sorted(kept_filenames):
        old_photo = old_by_filename[filename]
        new_photo = new_by_filename[filename]
        
        # Create merged photo, preserving critical fields
        merged = {
            "filename": filename,
            "photo_name": old_photo.get("photo_name", filename),  # Preserve custom name
            "width": new_photo["width"],                           # Update from filesystem
            "height": new_photo["height"],
            "aspect_ratio": new_photo["aspect_ratio"],
            "orientation": new_photo["orientation"],
            "metadata": new_photo["metadata"],                     # Update EXIF
            "sort_index": old_photo["sort_index"]                  # Preserve order
        }
        
        # Track if metadata changed
        if old_photo.get("metadata") != new_photo["metadata"]:
            changes.log_photo_updated(album_name, filename, {
                "metadata": {
                    "old": old_photo.get("metadata", {}),
                    "new": new_photo["metadata"]
                }
            })
        
        merged_photos.append(merged)
    
    # 2. Process new photos (append to end)
    if merged_photos:
        max_sort_index = max(p["sort_index"] for p in merged_photos)
    else:
        max_sort_index = -1
    
    for i, filename in enumerate(sorted(added_filenames)):
        new_photo = new_by_filename[filename]
        new_sort_index = max_sort_index + i + 1
        
        new_photo["photo_name"] = filename  # Default photo_name
        new_photo["sort_index"] = new_sort_index
        
        merged_photos.append(new_photo)
        changes.log_photo_added(album_name, filename, new_sort_index)
    
    # 3. Log removed photos
    for filename in removed_filenames:
        old_photo = old_by_filename[filename]
        changes.log_photo_removed(
            album_name,
            filename,
            old_photo.get("sort_index")
        )
    
    # Sort by sort_index before returning
    merged_photos.sort(key=lambda p: p["sort_index"])
    
    return merged_photos

def get_image_dimensions(image_path: Path) -> tuple[int, int]:
    """Extract image dimensions with EXIF orientation applied."""
    try:
        with Image.open(image_path) as img:
            img = ImageOps.exif_transpose(img)
            return img.size  # (width, height)
    except Exception as e:
        print(f"Error reading dimensions for {image_path}: {e}")
        return (0, 0)

def classify_orientation(width: int, height: int) -> tuple[float, str]:
    """Calculate aspect ratio and classify orientation."""
    aspect_ratio = width / height if height > 0 else 1.0
    orientation = "portrait" if aspect_ratio < 0.85 else "landscape"
    return aspect_ratio, orientation

def optimize_photo_order(photos: list) -> list:
    """Reorder photos to pair portraits for better grid layout."""
    portraits = []
    landscapes = []
    
    for p in photos:
        w, h = p.get('width', 1), p.get('height', 1)
        ratio = w / h if h else 1.0
        
        if ratio < 0.85:
            portraits.append(p)
        else:
            landscapes.append(p)
    
    ordered = []
    for i in range(0, len(portraits), 2):
        if i + 1 < len(portraits):
            ordered.extend([portraits[i], portraits[i+1]])
        else:
            ordered.append(portraits[i])
    
    ordered.extend(landscapes)
    return ordered

def scan_albums():
    """Enhanced album scanning with incremental updates and change tracking."""
    # Load existing metadata
    old_metadata = load_existing_metadata(OUTPUT_FILE)
    
    # Initialize change tracker
    changes = ChangeTracker()
    
    # Prepare new metadata structure
    albums_data = {}
    
    if not os.path.exists(ALBUMS_DIR):
        print(f"Directory {ALBUMS_DIR} not found.")
        return

    root_path = Path(ALBUMS_DIR)
    scanned_album_names = set()
    
    # Scan albums
    for album_dir in [d for d in root_path.iterdir() if d.is_dir()]:
        album_name = album_dir.name
        
        # Skip hidden folders
        if album_name.startswith('.'):
            continue
        
        scanned_album_names.add(album_name)
        print(f"Scanning album: {album_name}")
        
        # Get old album data if exists
        old_album = old_metadata.get(album_name, {})
        old_photos = old_album.get("photos", [])
        
        # Track new album
        if album_name not in old_metadata:
            changes.log_album_added(album_name)
        
        # Phase 1: Scan filesystem for new photos
        new_scanned_photos = []
        valid_extensions = {'.jpg', '.jpeg', '.png', '.webp'}
        
        for file in album_dir.iterdir():
            if file.suffix.lower() in valid_extensions:
                # Check and update Artist/Copyright EXIF fields
                ac_changes = check_and_update_artist_copyright(file)
                if ac_changes:
                    changes.log_photo_updated(album_name, file.name, ac_changes)

                # Get EXIF metadata
                metadata = get_exif_data(file)
                
                # Get image dimensions
                width, height = get_image_dimensions(file)
                
                # Calculate aspect ratio and orientation
                aspect_ratio, orientation = classify_orientation(width, height)
                
                new_scanned_photos.append({
                    "filename": file.name,
                    "width": width,
                    "height": height,
                    "aspect_ratio": round(aspect_ratio, 3),
                    "orientation": orientation,
                    "metadata": metadata
                })
        
        # Phase 2: Merge with old metadata (preserves sort_index and photo_name)
        merged_photos = merge_photo_metadata(
            old_photos,
            new_scanned_photos,
            changes,
            album_name
        )
        
        # Build album entry
        albums_data[album_name] = {
            "album_title": old_album.get("album_title", album_name),
            "subtitle": old_album.get("subtitle", ""),
            "summary": old_album.get("summary", ""),
            "folder_name": album_name,
            "photos": merged_photos
        }
    
    # Track removed albums
    old_album_names = set(old_metadata.keys())
    removed_albums = old_album_names - scanned_album_names
    for album in removed_albums:
        changes.log_album_removed(album)

    # Write output
    with open(OUTPUT_FILE, 'w') as f:
        json.dump(albums_data, f, indent=2)
    
    print(f"Metadata generated in {OUTPUT_FILE}")
    
    # Save change log
    changes.save_to_file()

if __name__ == "__main__":
    scan_albums()
