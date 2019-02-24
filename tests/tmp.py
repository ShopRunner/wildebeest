from functools import partial

from creevey import Pipeline
from creevey.load_funcs.image import download_image
from creevey.ops.image import resize
from creevey.write_funcs.image import write_image
from creevey.path_funcs import combine_outdir_dirname_extension


trim_bottom_100 = lambda image: image[:-100, :]
resize_224 = partial(resize, shape=(224, 224))

trim_resize_pipeline = Pipeline(
    load_func=download_image, ops=[trim_bottom_100, resize_224], write_func=write_image
)

image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]

keep_filename_png_in_cwd = partial(
    combine_outdir_dirname_extension, outdir='.', extension='.png'
)
trim_resize_pipeline.run(
    inpaths=image_urls,
    outpath_func=keep_filename_png_in_cwd,
    n_jobs=10,
    skip_existing=True,
)
