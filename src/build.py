#!/usr/bin/env python3
"""
Portfolio Site Builder
Generates static site from content in Albums/ directory.
"""

import os
import sys
import json
import shutil
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timezone

from PIL import Image, ExifTags, ImageOps
from jinja2 import Environment, FileSystemLoader

# Configuration
ALBUMS_DIR = Path("Albums")
DIST_DIR = Path("dist")
MEDIA_DIR = DIST_DIR / "media"
TEMPLATE_DIR = Path("src/templates")
STATIC_DIR = Path("src/static")

# Base URL configuration
BASE_URL = os.getenv("SITE_BASE_URL", "")

LARGE_SIZE = (1600, 1200)
THUMB_SIZE = (600, 600)

def setup_directories():
    """Ensure output directories exist."""
    print("Setting up directories...")
    MEDIA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Copy static assets if they exist
    if STATIC_DIR.exists():
        dist_static = DIST_DIR / "static"
        if dist_static.exists():
            shutil.rmtree(dist_static)
        shutil.copytree(STATIC_DIR, dist_static)

def get_exif_data(img: Image.Image) -> Dict[str, str]:
    """Extract and format specific EXIF data."""
    meta = {}
    exif = img.getexif()
    if not exif:
        return meta
        
    for key, val in exif.items():
        if key in ExifTags.TAGS:
            tag = ExifTags.TAGS[key]
            if tag == "DateTime" or tag == "DateTimeOriginal":
                meta["date_taken"] = str(val)
            elif tag == "ExposureTime":
                # Convert fraction if needed, simplistically for now
                meta["shutter"] = str(val)
            elif tag == "FNumber":
                meta["aperture"] = f"f/{float(val):.1f}"
            elif tag == "ISOSpeedRatings":
                meta["iso"] = str(val)
    return meta

def process_image(img_path: Path, album_slug: str) -> Optional[Dict[str, Any]]:
    """Process a single image."""
    try:
        filename = img_path.name
        slug_dir = MEDIA_DIR / album_slug
        slug_dir.mkdir(exist_ok=True)
        
        large_filename = f"large_{filename}"
        thumb_filename = f"thumb_{filename}"
        
        large_path = slug_dir / large_filename
        thumb_path = slug_dir / thumb_filename
        
        with Image.open(img_path) as img:
            # Handle orientation if needed (Exif transpose)
            img = ImageOps.exif_transpose(img)
            
            # Extract Meta
            meta = get_exif_data(img)
            
            # Save Large
            img_large = img.copy()
            img_large.thumbnail(LARGE_SIZE)
            img_large.save(large_path, quality=85)
            
            # Save Thumb
            img_thumb = img.copy()
            img_thumb.thumbnail(THUMB_SIZE)
            img_thumb.save(thumb_path, quality=80)
            
            width, height = img_large.size
            
            return {
                "src": f"/media/{album_slug}/{large_filename}",
                "w": width,
                "h": height,
                "meta": meta,
                "thumb": f"/media/{album_slug}/{thumb_filename}"
            }
    except Exception as e:
        print(f"Error processing {img_path}: {e}")
        return None

def optimize_photo_order(photos: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Reorder photos to pair portraits together for better grid layout.
    """
    portraits = []
    landscapes = []
    
    for p in photos:
        w, h = p.get('w', 1), p.get('h', 1)
        ratio = w / h if h else 1.0
        
        if ratio < 0.85: # Clear portrait
            portraits.append(p)
        else:
            landscapes.append(p)
            
    # Create final list pairs
    ordered = []
    
    # Add pairs of portraits
    for i in range(0, len(portraits), 2):
        if i + 1 < len(portraits):
            ordered.extend([portraits[i], portraits[i+1]])
        else:
            ordered.append(portraits[i]) # Orphan portrait
            
    # Add landscapes
    ordered.extend(landscapes)
    
    return ordered

def select_cover_photo(photos: List[Dict[str, Any]], album_meta: dict) -> Dict[str, Any]:
    """Select album cover photo with fallback."""
    cover_filename = album_meta.get("cover_filename")
    
    if cover_filename:
        for photo in photos:
            if photo.get("src", "").endswith(cover_filename):
                print(f"  Using specified cover: {cover_filename}")
                return photo
        print(f"  Warning: Cover '{cover_filename}' not found, using first image")
    
    return photos[0]

def apply_metadata_sort_order(photos: List[Dict[str, Any]], album_meta: dict) -> List[Dict[str, Any]]:
    """Apply pre-computed sort order from metadata."""
    sort_map = {}
    for photo_meta in album_meta.get("photos", []):
        filename = photo_meta.get("filename")
        sort_index = photo_meta.get("sort_index")
        if filename is not None and sort_index is not None:
            sort_map[filename] = sort_index
    
    if not sort_map:
        return optimize_photo_order(photos)
    
    def get_sort_key(photo):
        src = photo.get("src", "")
        filename = Path(src).name.replace("large_", "")
        return sort_map.get(filename, 999)
    
    return sorted(photos, key=get_sort_key)

def extract_filename(src_url: str) -> str:
    """Extract original filename from processed URL."""
    filename = Path(src_url).name
    # Remove 'large_' prefix
    return filename.replace("large_", "")

def format_display_meta(meta: dict) -> dict:
    """Format metadata for display."""
    formatted = {}
    
    if "camera_model" in meta or "Model" in meta:
        formatted["camera"] = meta.get("camera_model") or meta.get("Model")
    
    # Combine lens_model if available
    if "lens_model" in meta:
        formatted["lens"] = meta["lens_model"]
    
    # Combine settings into single string
    settings_parts = []
    if "aperture" in meta:
        settings_parts.append(meta["aperture"])
    if "shutter_speed" in meta:
        settings_parts.append(meta["shutter_speed"])
    if "iso" in meta:
        settings_parts.append(f"ISO {meta['iso']}")
    
    if settings_parts:
        formatted["settings"] = ", ".join(settings_parts)
    
    # Extract date
    if "date_taken" in meta:
        # Parse "2026:01:04 11:09:45" to "2026-01-04"
        date_str = meta["date_taken"]
        formatted["date"] = date_str.split()[0].replace(":", "-")
    
    return formatted

def calculate_album_stats(photos: list) -> dict:
    """Calculate album statistics."""
    portrait_count = sum(1 for p in photos if (p["w"] / p["h"]) < 0.85)
    landscape_count = len(photos) - portrait_count
    
    # Extract unique cameras
    cameras = set()
    dates = []
    for photo in photos:
        meta = photo.get("meta", {})
        if "camera" in meta:
            cameras.add(meta["camera"])
    
    return {
        "total_photos": len(photos),
        "portrait_count": portrait_count,
        "landscape_count": landscape_count,
        "cameras": sorted(list(cameras)),
        "date_range": {
            "earliest": min(dates) if dates else None,
            "latest": max(dates) if dates else None
        }
    }

def find_album_navigation(current_slug: str, all_albums: list) -> Optional[dict]:
    """Find previous and next albums for navigation."""
    slugs = [a["slug"] for a in all_albums]
    try:
        current_idx = slugs.index(current_slug)
        return {
            "prev_album": slugs[current_idx - 1] if current_idx > 0 else None,
            "next_album": slugs[current_idx + 1] if current_idx < len(slugs) - 1 else None
        }
    except ValueError:
        return None

def generate_sitemap(base_url: str, albums_data: list, build_time: datetime) -> str:
    """
    Generate XML sitemap for all pages.
    
    Args:
        base_url: Site base URL (e.g., 'https://chrisrisner.com')
        albums_data: List of album dictionaries with slug and photos
        build_time: Current build timestamp
        
    Returns:
        Complete XML sitemap as string
    """
    from xml.etree import ElementTree as ET
    
    # Create root element
    urlset = ET.Element('urlset', xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')
    
    # Add home page
    url = ET.SubElement(urlset, 'url')
    ET.SubElement(url, 'loc').text = f'{base_url}/'
    ET.SubElement(url, 'lastmod').text = build_time.strftime('%Y-%m-%d')
    ET.SubElement(url, 'changefreq').text = 'weekly'
    ET.SubElement(url, 'priority').text = '1.0'
    
    # Add album pages
    for album in albums_data:
        url = ET.SubElement(urlset, 'url')
        ET.SubElement(url, 'loc').text = f'{base_url}/{album["slug"]}/'
        
        # Extract last modified from most recent photo date
        if album.get('photos'):
            photo_dates = []
            for photo in album['photos']:
                if photo.get('meta', {}).get('date_taken'):
                    try:
                        # Parse "2026:01:08 20:16:24" format
                        date_str = photo['meta']['date_taken'].split()[0]
                        photo_dates.append(date_str.replace(':', '-'))
                    except (IndexError, ValueError):
                        pass
            
            if photo_dates:
                ET.SubElement(url, 'lastmod').text = max(photo_dates)
        
        ET.SubElement(url, 'changefreq').text = 'monthly'
        ET.SubElement(url, 'priority').text = '0.8'
    
    # Add about page
    url = ET.SubElement(urlset, 'url')
    ET.SubElement(url, 'loc').text = f'{base_url}/about/'
    ET.SubElement(url, 'lastmod').text = build_time.strftime('%Y-%m-%d')
    ET.SubElement(url, 'changefreq').text = 'yearly'
    ET.SubElement(url, 'priority').text = '0.6'
    
    # Generate XML string with declaration
    tree = ET.ElementTree(urlset)
    ET.indent(tree, space='  ')  # Pretty print with 2-space indent
    
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(urlset, encoding='unicode')

def generate_robots_txt(base_url: str) -> str:
    """
    Generate robots.txt content.
    
    Args:
        base_url: Site base URL for sitemap reference
        
    Returns:
        robots.txt content as string
    """
    return f"""# robots.txt for {base_url}
# Allow all crawlers to access all content

User-agent: *
Allow: /

# Sitemap location
Sitemap: {base_url}/sitemap.xml
"""

def generate_album_metadata(
    album: dict,
    all_albums: list,
    builder_version: str = "1.0.0"
) -> dict:
    """
    Generate per-album metadata structure.
    
    Args:
        album: Album dict with slug, title, photos
        all_albums: List of all albums (for navigation)
        builder_version: Build script version
    
    Returns:
        Complete metadata dict ready for JSON serialization
    """
    photos = album["photos"]
    
    # Calculate statistics
    stats = calculate_album_stats(photos)
    
    # Find navigation
    navigation = find_album_navigation(album["slug"], all_albums)
    
    # Build complete metadata
    metadata = {
        "slug": album["slug"],
        "title": album["title"],
        "folder": album.get("folder", album["title"]),
        "photos": [
            {
                "filename": extract_filename(p["src"]),
                "src": p["src"],
                "thumb": p["thumb"],
                "w": p["w"],
                "h": p["h"],
                "aspect_ratio": round(p["w"] / p["h"], 3) if p["h"] > 0 else 1.0,
                "orientation": "portrait" if (p["w"] / p["h"]) < 0.85 else "landscape",
                "sort_index": idx,
                "meta": format_display_meta(p.get("meta", {}))
            }
            for idx, p in enumerate(photos)
        ],
        "stats": stats,
        "navigation": navigation,
        "generated": {
            "timestamp": datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z'),
            "builder_version": builder_version
        }
    }
    
    return metadata

def main() -> int:
    """Main build entry point."""
    print("Starting build process...")
    setup_directories()
    
    # Load albums metadata
    albums_metadata = {}
    metadata_file = Path("albums_metadata.json")
    if metadata_file.exists():
        print("Loading albums_metadata.json...")
        with open(metadata_file) as f:
            albums_metadata = json.load(f)
    
    albums_data = []

    if not ALBUMS_DIR.exists():
        print(f"Error: {ALBUMS_DIR} not found.")
        return 1

    for album_path in sorted(ALBUMS_DIR.iterdir()):
        if not album_path.is_dir() or album_path.name.startswith('.'):
            continue
            
        album_slug = album_path.name.lower().replace(" ", "-")
        print(f"Processing Album: {album_path.name}")
        
        photos = []
        valid_extensions = {".jpg", ".jpeg", ".png", ".webp", ".JPG", ".JPEG"}
        
        for img_path in sorted(album_path.iterdir()):
            if img_path.suffix in valid_extensions:
                photo_data = process_image(img_path, album_slug)
                if photo_data:
                    photos.append(photo_data)
        
        # Get album metadata if available
        album_meta = albums_metadata.get(album_path.name, {})
        
        # Apply metadata-driven sort order or fallback to runtime algorithm
        photos = apply_metadata_sort_order(photos, album_meta)
        
        if photos:
            # Select cover photo (manual or first)
            cover_photo = select_cover_photo(photos, album_meta)
            
            albums_data.append({
                "slug": album_slug,
                "title": album_path.name,
                "subtitle": album_meta.get("subtitle", ""),
                "summary": album_meta.get("summary", ""),
                "cover": cover_photo["thumb"],
                "photos": photos
            })
    
    db = {"albums": albums_data}
    
    # Save DB
    with open(DIST_DIR / "db.json", "w") as f:
        json.dump(db, f, indent=2)
    print(f"Database generated with {len(albums_data)} albums.")
        
    # Generate HTML
    if (TEMPLATE_DIR / "index.html").exists():
        env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
        template = env.get_template("index.html")
        
        # 1. Generate Home Page
        print("Generating Home Page...")
        home_html = template.render(db=db, current_album=None, base_url=BASE_URL)
        with open(DIST_DIR / "index.html", "w") as f:
            f.write(home_html)
            
        # 2. Generate Album Pages
        print("Generating Album Pages...")
        for album in albums_data:
            slug = album["slug"]
            album_dir = DIST_DIR / slug
            album_dir.mkdir(exist_ok=True, parents=True)
            
            album_html = template.render(db=db, current_album=album, base_url=BASE_URL)
            with open(album_dir / "index.html", "w") as f:
                f.write(album_html)
            
            # Generate per-album metadata.json
            album_metadata = generate_album_metadata(album, albums_data, builder_version="1.0.0")
            with open(album_dir / "metadata.json", "w") as f:
                json.dump(album_metadata, f, indent=2)
                
        print(f"Generated home and {len(albums_data)} album pages.")

        # 3. Generate 404 Page
        print("Generating 404 Page...")
        if (TEMPLATE_DIR / "404.html").exists():
            template_404 = env.get_template("404.html")
            html_404 = template_404.render(db=db, base_url=BASE_URL)
            with open(DIST_DIR / "404.html", "w") as f:
                f.write(html_404)
        else:
            print("Warning: 404.html template not found.")


        # 4. Generate About Page
        if (TEMPLATE_DIR / "about.html").exists():
            print("Generating About Page...")
            template_about = env.get_template("about.html")
            about_html = template_about.render(db=db, base_url=BASE_URL)
            about_dir = DIST_DIR / "about"
            about_dir.mkdir(exist_ok=True, parents=True)
            with open(about_dir / "index.html", "w") as f:
                f.write(about_html)
        else:
            print("Warning: about.html template not found.")

        # 5. Generate Sitemap
        print("Generating sitemap.xml...")
        base_url = BASE_URL or "https://chrisrisner.com"
        build_time = datetime.now(timezone.utc)
        sitemap_content = generate_sitemap(base_url, albums_data, build_time)
        
        with open(DIST_DIR / "sitemap.xml", "w", encoding="utf-8") as f:
            f.write(sitemap_content)
        
        print(f"Sitemap generated with {len(albums_data) + 2} URLs")
        
        # 6. Generate robots.txt
        print("Generating robots.txt...")
        robots_content = generate_robots_txt(base_url)
        
        with open(DIST_DIR / "robots.txt", "w", encoding="utf-8") as f:
            f.write(robots_content)
        
        print("robots.txt generated")

    else:
        print("Warning: index.html template not found.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
