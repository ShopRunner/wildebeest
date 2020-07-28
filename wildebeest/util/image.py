"""Miscellaneous utilities for images"""
from functools import partial
import mimetypes

from wildebeest.util import find_files_with_extensions

find_image_files = partial(
    find_files_with_extensions,
    extensions=[k for k, v in mimetypes.types_map.items() if v.startswith("image/")],
)
"""Find all image files in a directory"""
