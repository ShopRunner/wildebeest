from functools import partial

from creevey.util import find_files_with_extensions

IMAGE_EXTENSIONS = ["jpeg", "jpg", "png", "bmp", "gif"]


find_image_files = partial(find_files_with_extensions, extensions=IMAGE_EXTENSIONS)
