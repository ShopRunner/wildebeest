from creevey.ops import download
from creevey.pipelines import Pipeline

download_png_pipeline = Pipeline(load_func=download_bytes, write_func=write_png)
