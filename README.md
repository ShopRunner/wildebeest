# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

**Creevey provides a simple framework for batch file processing pipelines that handles threading, piping, logging, and (optionally) skipping existing files for you.** It is designed for IO-bound batch workflows that involve reading files into memory, doing some processing on their contents, and writing out the results. **Creevey also provides predefined, extensible pipelines and reusable pipeline components, particularly for image processing.** 

## Example

For instance, this code takes a list of image URLs and for each one downloads the file contents, trims off its bottom 100 pixels, resizes it to 224x224, and writes the result to disk, using ten threads for concurrency. Because `exceptions_to_catch=AttributeError` is being passed to the `run` call, it will catch `AttributeError`s that arise during file processing, logging them as errors but continuing execution. (This functionality is useful for handling corrupted input files.)

```python
from functools import partial

from creevey import Pipeline
from creevey.load_funcs.image import download_image
from creevey.ops.image import resize
from creevey.write_funcs.image import write_image
from creevey.path_funcs import join_outdir_filename_extension


trim_bottom_100 = lambda image: image[:-100, :]
resize_224 = partial(resize, shape=(224, 224))

trim_resize_pipeline = Pipeline(
    load_func=download_image, ops=[trim_bottom_100, resize_224], write_func=write_image
)

image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]

keep_filename_png_in_cwd = partial(
    join_outdir_filename_extension, outdir='.', extension='.png'
)
run_record = trim_resize_pipeline.run(
    inpaths=image_urls,
    path_func=keep_filename_png_in_cwd,
    n_jobs=10,
    skip_existing=True,
    exceptions_to_catch=AttributeError,
)
```

`trim_resize_pipeline.run(...)` returns a "run report:" a Pandas DataFrame with each input path as its index and columns indicating the corresponding output path ("outpath"), whether processing was skipped because a file already existed at the output path ("skipped_existing"), whether processing failed due to an exception in `exceptions_to_catch` ("exception_handled"), and a timestamp indicating when processing complete ("time_finished"). 

## The `Pipeline` Class

Creevey's core abstraction is the `Pipeline` class. 

### Creating a `Pipeline`

Here is the code that defines the `Pipeline` object in the snippet above:
 
```python
trim_resize_pipeline = Pipeline(
    load_func=download_image, ops=[trim_bottom_100, resize_224], write_func=write_image
)
```

 The `Pipeline` constructor takes three arguments:
 
1. A function `load_func` that takes a string or Path object and returns some kind of data structure in memory. In this example, `download_image` takes an image URL and returns the contents of the corresponding image as a NumPy array.
1. A list `ops` of single-argument functions that can be piped together, with the first taking the return value of `load_func` as its input. This example follows common practice for image data by using functions each of which takes a NumPy array and returns a NumPy array.
1. A function `write_image` that takes the output of the last function in `ops` and writes it out to a specified location. In this example, `write_image` takes a NumPy array and writes it to disk.
 
### Running a `Pipeline`

Here is the code that runs the pipeline in the snippet above:

```python
run_record = trim_resize_pipeline.run(
    inpaths=image_urls,
    path_func=keep_filename_png_in_cwd,
    n_jobs=10,
    skip_existing=True,
    exceptions_to_catch=AttributeError,
)
```

A `Pipeline` object's `run` method takes the following arguments:
 
1. An iterable `inpaths` of input paths (a list of image URLs in this example).
1. A function `outpath_func` for transforming each path in `inpaths` into a corresponding output path. In this example, `keep_filename_png_in_cwd` uses the filename from the URL but gives it a PNG extension and places it in the current working directory.
1. The number `n_jobs` of threads to run (10 in this example).
1. A Boolean `skip_existing` indicating whether to overwrite existing files or to skip processing input files that would result in overwriting existing files.
1. An exception type or tuple of exceptions types `exceptions_to_catch` (optional) to catch and log without raising.

### Extending an Existing Pipeline

We can simplify our sample code snippet by using an existing pipeline for downloading and writing images and simply adding our `ops`.

```python
from creevey.pipelines.image import download_image_pipeline

trim_resize_pipeline = download_image_pipeline
trim_resize_pipeline.ops = [trim_bottom_100, resize_224]
```

More generally, it is easy to modify an existing `Pipeline` object simply by modifying the relevant attributes.

## The `CustomReportingPipeline` Class

The `Pipeline` class's `run` method returns a "run report" with basic information about what happened during the run. The `CustomReportingPipeline` allows you to add additional information to these reports by adding to them within your `load_func`, `ops`, and `write_func`. For instance, when processing a set of image files you might wish to record each image's mean brightness while you already have it open so that you can later experiment with removing washed-out images from your dataset.

You define and run a `CustomReportingPipeline` object in the same way that you define and run a basic `Pipeline` object, except that the elements of `ops` and `write_func` need to accept the input path as an additional positional argument; and `write_func`, `ops` and `write_func` need to accept a `defaultdict(dict)` object as another additional positional argument. Creevey uses the name `log_dict` for that `defaultdict(dict)` object, which stores the run report information for a single file. You can then enrich your run reports in one of these functions by writing e.g. `log_dict[inpath]['mean_brightness'] = mean_brightness` (assuming that you have calculated `mean_brightness`).

## Limitations

Creevey provides concurrency through threading rather than multiprocessing, which is appropriate for **IO-bound rather than CPU-bound** workflows.

**Creevey does not force you to write threadsafe code.** It is intended to be used for workflows in which multiple files are all processed separately and written out to separate locations, which is a generally threadsafe pattern, but there are pitfalls. For instance, if your `write_func` checks whether an output directory exists and creates it if it does not, then it can happen that the process switches threads between checking whether the directory exists and attempting to create it, so that the attempt to create it raises an error. (One solution to this problem is to wrap the directory creation step in a `try/except` block, as in `creevey.write_funs.image.write_image`.)

## Structure

Creevey contains the following modules. Generally, each one has a submodule which shares its name that defines generic components and an `image` submodule that defines components for working with images. Items in the former are imported into the module namespace, so that you can write e.g. `from creevey.path_funcs import combine_outdir_dirname_extension` rather than `from creevey.path_funcs.path_funcs import combine_outdir_dirname_extension`.

1. `pipelines` contains a `core` submodule that defines the `Pipeline` class in addition to submodules that define extensible instances of that class. The `Pipeline` class is also in the main `Creevey` namespace so that you can simply `from creevey import Pipeline`.
1. `load_funcs` provides functions such as `download_image` for reading files into memory.
1. `ops` provides functions such as `resize` for processing file contents after they have been loaded into memory.
1. `write_funcs` provides functions such as `write_image` for writing out the output of `ops`.
1. `path_funcs` provides functions such as `combine_outdir_dirname_extension` for deriving output paths from input paths.
1. `util` contains utility functions that complement Creevey's core functionality, such as a function to generate a list of paths to all image files recursively within a specified directory.
