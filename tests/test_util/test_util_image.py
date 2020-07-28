from tests.conftest import TEMP_DATA_DIR
from wildebeest.util.image import find_image_files


def test_find_images(generate_file_tree):  # noqa: F811
    image_paths = find_image_files(search_dir=TEMP_DATA_DIR)
    assert all(path.exists() for path in image_paths)
    assert len(image_paths) == 3
