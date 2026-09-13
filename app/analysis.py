import hashlib
from pathlib import Path
from PIL import Image
from PIL.ExifTags import TAGS


def compute_file_hash(filepath: Path) -> str:
    """SHA-256 hash of the file — useful later for evidence integrity checks."""
    sha256 = hashlib.sha256()
    with open(filepath, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            sha256.update(chunk)
    return sha256.hexdigest()


def extract_exif(img: Image.Image) -> dict:
    """Pull human-readable EXIF tags, if any exist."""
    exif_data = {}
    raw_exif = img.getexif()
    if raw_exif:
        for tag_id, value in raw_exif.items():
            tag_name = TAGS.get(tag_id, tag_id)
            exif_data[str(tag_name)] = str(value)
    return exif_data


def extract_metadata(filepath: Path) -> dict:
    """Main entry point: gathers everything we know about the image."""
    img = Image.open(filepath)

    exif = extract_exif(img)

    return {
        "width": img.width,
        "height": img.height,
        "format": img.format,
        "mode": img.mode,
        "file_size_kb": round(filepath.stat().st_size / 1024, 1),
        "sha256": compute_file_hash(filepath),
        "exif_found": len(exif) > 0,
        "exif_data": exif,
    }