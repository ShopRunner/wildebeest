# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

Creevey helps you process files. It is designed for **IO-bound** batch workflows that involve **reading files** into memory, **doing some processing** on their contents, and **writing out the results**. It provides a general abstraction for defining such workflows and running them across multiple threads. It also provides some predefined, extensible workflows and some reusable workflow components, particularly for image processing. 

## Example

For instance, this code takes a list of image URLs and for each one downloads the file contents, trims off its bottom 100 pixels, resizes it to 224x224, and writes the result to disk, using ten threads for concurrency.

```python
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

keep_filename_png_in_cwd = partial(combine_outdir_dirname_extension, outdir='.', extension='.png')
trim_resize_pipeline.run(inpaths=image_urls, outpath_func=keep_filename_png_in_cwd, n_jobs=10, skip_existing=True)
```

## The `Pipeline` Class

Creevey's core abstraction is the `Pipeline` class. 

### Creating a `Pipeline`

Here is the code that defines the `Pipeline` object in the snippet above:
 
```python
trim_resize_pipeline = Pipeline(
    load_func=download_image, ops=[trim_bottom_100, resize_224], write_func=write_image
)
```

 A `Pipeline` object has three attributes:
 
1. A function `load_func` that takes a string or Path object and returns some kind of data structure in memory. In this example, `download_image` takes an image URL and returns the contents of the corresponding image as a NumPy array.
- A list `ops` of single-argument functions that can be piped together, with the first taking the return value of `load_func` as its input. This example follows common practice for image data by using functions each of which takes a NumPy array and returns a NumPy array.
- A function `write_image` that takes the output of the last function in `ops` and writes it out to a specified location. In this example, `write_image` takes a NumPy array and writes it to disk.
 
### Running a `Pipeline`

Here is the code that runs the pipeline in the snippet above:

```python
trim_resize_pipeline.run(inpaths=image_urls, outpath_func=keep_filename_png_in_cwd, n_jobs=10, skip_existing=True)
```

A `Pipeline` object's `run` method takes four arguments:
 
1. An iterable `inpaths` of input paths (a list of image URLs in this example).
- A function `outpath_func` for transforming each path in `inpaths` into a corresponding output path. In this example, `keep_filename_png_in_cwd` uses the filename from the URL but gives it a PNG extension and places it in the current working directory.
- The number `n_jobs` of threads to run (10 in this example).
- A Boolean `skip_existing` indicating whether to overwrite existing files or to skip processing input files that would result in overwriting existing files.

## Benefits

For workflows that involve reading files into memory, processing their contents, and writing out the results, **Creevey handles piping the files through a series of functions with concurrency and (if desired) skipping over input files that would be written to locations that already exist**, while allowing the user full control over what those functions do.

## Limitations

- Creevey provides concurrency through threading rather than multiprocessing, which is appropriate for IO-bound rather than CPU-bound workflows.
- Creevey does not force you to write threadsafe code. It is intended to be used for workflows in which multiple files are all processed separately and written out to separate locations, which is a generally threadsafe pattern, but there are pitfalls. For instance, if your `write_func` checks whether an output directory exists and creates it if it does not, then it can happen that the process switches threads between checking whether the directory exists and attempting to create it, so that the attempt to create it raises an error. (One solution to this problem is to wrap the directory creation step in a `try/except` block, as in `creevey.write_funs.image.write_image`.) Note that [logging from multiple threads requires no special effort](https://docs.python.org/3/howto/logging-cookbook.html), so you can include logging in your pipeline functions.

## Structure

Creevey has five modules. Generally, each one has a submodule which shares its name that defines generic components and an `image` submodule that defines components for working with images. Items in the former are imported into the module namespace, so that you can write e.g. `from creevey.path_funcs import combine_outdir_dirname_extension` rather than `from creevey.path_funcs.path_funcs import combine_outdir_dirname_extension`.

1. `pipelines` contains a `core` submodule that defines the `Pipeline` class in addition to submodules that define extensible instances of that class.
- `load_funcs` provides functions such as `download_image` for reading files into memory.
- `ops` provides functions such as `resize` for processing file contents after they have been loaded into memory.
- `write_funcs` provides functions such as `write_image` for writing out the output of `ops`.
- `path_funcs` provides functions such as `combine_outdir_dirname_extension` for deriving output paths from input paths.
