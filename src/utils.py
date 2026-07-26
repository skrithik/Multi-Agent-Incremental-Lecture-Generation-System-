import os
import re
from typing import List


def natural_sort_key(s: str):
    """Sort 'slide2.png' before 'slide10.png' instead of alphabetically."""
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", s)]


def get_sorted_image_paths(images_dir: str) -> List[str]:
    valid_ext = {".png", ".jpg", ".jpeg", ".webp"}
    if not os.path.isdir(images_dir):
        raise FileNotFoundError(f"Images directory not found: {images_dir}")
    files = [f for f in os.listdir(images_dir) if os.path.splitext(f)[1].lower() in valid_ext]
    files.sort(key=natural_sort_key)
    return [os.path.join(images_dir, f) for f in files]


def build_image_content_blocks(image_paths: List[str]):
    """Build chat-template content blocks for a list of local image files."""
    return [{"type": "image", "url": p} for p in image_paths]