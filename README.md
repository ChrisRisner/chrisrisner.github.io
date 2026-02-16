# Portfolio Site

A static portfolio site generator that turns a directory of images into a responsive, single-page photo gallery.

## Features

*   **Static Generation**: Python script processes images and generates a lightweight static site.
*   **Responsive Design**: CSS Grid layout with a fixed sidebar on desktop and a hamburger menu on mobile.
*   **Lightbox**: Integrated PhotoSwipe 5.0 for full-screen image viewing with keyboard support.
*   **Content Management**: Simply add folders and images to the `Albums/` directory.

## Architecture

*   **Backend (Build)**: `src/build.py` uses Pillow to resize images, extract EXIF metadata, and generates `dist/db.json` and `dist/index.html` using Jinja2.
*   **Frontend**: Vanilla JavaScript (`src/static/app.js`) fetches the JSON data and renders the album grid client-side. Routing is handled via URL hash.

## Prerequisites

*   Python 3.11+

## Installation

1.  Clone the repository.
2.  Create a virtual environment:
    ```bash
    python3 -m venv .venv
    source .venv/bin/activate
    ```
3.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Content Management

1.  Create a folder in `Albums/` for each album (e.g., `Albums/Travel`).
2.  Add `.jpg`, `.png`, or `.webp` images to the folder.
3.  The folder name will become the album title.

## Usage

### Step 1: Scan Albums and Generate Metadata

First, scan your photo albums to extract EXIF data, compute dimensions, and pre-calculate sort order:

```bash
python src/scan_albums.py
```

This generates `albums_metadata.json` with:
- EXIF metadata (camera, lens, settings, date)
- Image dimensions (width, height, aspect ratio)
- Pre-computed sort order (portrait-pairing algorithm)
- Orientation classification (portrait/landscape)

### Step 2: Build Static Site

Next, build the static photo gallery site:

```bash
python src/build.py
```

This generates the `dist/` folder with:
- Optimized images (large and thumbnail sizes)
- HTML pages for each album
- Global database (db.json)
- Per-album metadata files (metadata.json)

### Step 3: Preview or Deploy

Serve the static site locally or deploy to hosting:

```bash
# Local preview
python -m http.server -d dist 8000

# Then visit http://localhost:8000
```

## Album Cover Configuration

You can manually select a cover photo for any album by editing `albums_metadata.json`:

```json
{
  "Portugal": {
    "album_title": "Portugal Trip 2026",
    "folder_name": "Portugal",
    "cover_filename": "_DSC1012.JPG",
    "photos": [...]
  }
}
```

Add the `cover_filename` field with the exact filename of the photo you want to use as the album cover. If not specified or if the file is not found, the first photo in the sorted order will be used.

## Output Structure

After running the build process, the `dist/` directory contains:

```
dist/
├── db.json                     # Global database (all albums)
├── index.html                  # Home page
├── 404.html                    # Error page
├── static/                     # CSS and JavaScript
├── media/                      # Optimized images
│   └── [album]/
│       ├── large_*.jpg         # Large images (1600x1200)
│       └── thumb_*.jpg         # Thumbnails (600x600)
└── [album]/
    ├── index.html              # Album page
    └── metadata.json           # Per-album metadata (smaller, album-specific)
```

### albums_metadata.json Schema

Each album contains:
- `album_title` - Display title
- `folder_name` - Source folder name
- `cover_filename` - (Optional) Manual cover image selection
- `photos[]` - Array of photo objects with:
  - `filename` - Original filename
  - `width`, `height` - Image dimensions
  - `aspect_ratio` - Computed ratio (width/height)
  - `orientation` - "portrait" or "landscape"
  - `sort_index` - Display order (0-based)
  - `metadata` - EXIF data (camera, lens, settings, etc.)

## Metadata Generation

To extract EXIF metadata (camera model, lens, exposure settings) from your images and generate a `albums_metadata.json` file:

```bash
python src/scan_albums.py
```

## Building the Site

To generate the site artifacts in the `dist/` directory:

```bash
python src/build.py
```

## Running Locally

To preview the site locally, you can serve the `dist` directory using Python's built-in HTTP server:

```bash
# Ensure you have built the site first
python src/build.py

# Serve the dist directory
cd dist
python -m http.server 8000
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## Deployment

The project is configured for automated deployment to GitHub Pages via GitHub Actions.
Any push to the `main` branch will trigger a build and deploy the content of `dist/` to the `gh-pages` environment.
