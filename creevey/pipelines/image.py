from creevey import Pipeline
from creevey.load_funcs.image import load_image_from_url
from creevey.write_funcs.image import write_image

download_image_pipeline = Pipeline(
    load_func=load_image_from_url, ops=[], write_func=write_image
)
