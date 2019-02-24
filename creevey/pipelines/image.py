from creevey import Pipeline
from creevey.load_funcs.image import download_image
from creevey.write_funcs.image import write_image

download_image_pipeline = Pipeline(
    load_func=download_image, ops=[], write_func=write_image
)
