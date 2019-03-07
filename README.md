# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

**Creevey provides a simple framework for batch file processing pipelines that handles threading, piping, logging, and (optionally) skipping existing files for you.** It is designed for IO-bound batch workflows that involve reading files into memory, doing some processing on their contents, and writing out the results. **Creevey also provides predefined, extensible pipelines and reusable pipeline components, particularly for image processing.** 

## Example

For instance, the following code takes a list of image URLs and for each one downloads the file contents, trims off its bottom 100 pixels, resizes it to 224x224, and writes the result to disk, using ten threads for concurrency. Because `exceptions_to_catch=AttributeError` is being passed to the `run` call, this code will catch `AttributeError`s that arise during file processing, logging them as errors but continuing execution. (This error-handling functionality is useful for dealing with occasional corrupted input files.)

```python
from functools import partial

from creevey import Pipeline
from creevey.load_funcs.image import load_image_from_url
from creevey.ops.image import resize
from creevey.write_funcs.image import write_image
from creevey.path_funcs import join_outdir_filename_extension


trim_bottom_100 = lambda image: image[:-100, :]
resize_224 = partial(resize, shape=(224, 224))

trim_resize_pipeline = Pipeline(
    load_func=load_image_from_url, ops=[trim_bottom_100, resize_224], write_func=write_image
)

image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]

keep_filename_png_in_cwd = partial(
    join_outdir_filename_extension, outdir='.', extension='.png'
)
run_report = trim_resize_pipeline.run(
    inpaths=image_urls,
    path_func=keep_filename_png_in_cwd,
    n_jobs=10,
    skip_existing=True,
    exceptions_to_catch=AttributeError,
)
```

`trim_resize_pipeline.run(...)` returns a "run report:" a Pandas DataFrame with each input path as its index and columns indicating the corresponding output path ("outpath"), whether processing was skipped because a file already existed at the output path ("skipped_existing"), whether processing failed due to an exception in `exceptions_to_catch` ("exception_handled"), and a timestamp indicating when processing completed ("time_finished").

If `n_jobs` is greater than 1, then the order of the input files in the run report typically will not match the order in `inpaths`; a command like `run_report.loc[inpaths, :]` can be used to restore the original ordering if desired. 

## The `Pipeline` Class

Creevey's core abstraction is the `Pipeline` class.

### Creating a `Pipeline`

 A `Pipeline` constructor takes three arguments:
 
1. A function `load_func` that takes a string or Path object and returns some kind of data structure in memory. In this example, `download_image` takes an image URL and returns the contents of the corresponding image as a NumPy array.
1. A list `ops` of single-argument functions that can be piped together, with the first taking the return value of `load_func` as its input. Using a common data structure type for a single type of data is recommended so that it is easy to recombine `ops` functions; for instance, Creevey uses NumPy arrays for image data.
1. A function `write_image` that takes the output of the last function in `ops` and writes it out to a specified location. In this example, `write_image` takes a NumPy array image and writes it to disk.
 
### Running a `Pipeline`

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

You define and run a `CustomReportingPipeline` object in the same way that you define and run a basic `Pipeline` object, except that the elements of `ops` and `write_func` need to accept the input path as an additional keyword argument "inpath"; and `write_func`, `ops` and `write_func` need to accept a `defaultdict(dict)` object as another keyword argument "log_dict", which stores the run report information for a single file. You can then enrich your run reports in one of these functions by writing e.g. `log_dict[inpath]['mean_brightness'] = mean_brightness` inside one of the functions in the pipeline (assuming that you have calculated `mean_brightness`).

Creevey has some predefined pipeline component functions such as `record_mean_brightness` that are designed for use with `CustomReportingPipeline` objects. These functions all have names that start with "record." Other Creevey functions accept arbitrary keyword arguments so that they they work with `CustomReportingPipeline` objects, but they do not do any custom logging. You can add logging to them if desired by writing wrappers, or you can simply add another pipeline stage that does logging.

Files that would be written to an output location where there is an existing file are skipped entirely when `skip_existing=True`, so custom logs will not be written for those files.

## Limitations

Creevey provides concurrency through threading rather than multiprocessing, which is appropriate for **IO-bound rather than CPU-bound** workflows.

**Creevey does not force you to write threadsafe code.** It is intended to be used for workflows in which multiple files are all processed separately and written out to separate locations. This pattern is generally threadsafe, but it has are pitfalls. For instance, if your `write_func` checks whether an output directory exists and creates it if it does not, then it can happen that the process switches threads between checking whether the directory exists and attempting to create it, so that the attempt to create it raises an error. (One solution to this problem is to wrap the directory creation step in a `try/except` block, as in `creevey.write_funcs.image.write_image`.)

## Structure

Creevey contains the following modules. Generally, each one has a submodule which shares its name that defines generic components and an `image` submodule that defines components for working with images. Items in the former are imported into the module namespace, so that you can write e.g. `from creevey.path_funcs import combine_outdir_dirname_extension` rather than `from creevey.path_funcs.path_funcs import combine_outdir_dirname_extension`.


1. `pipelines` contains a `core` submodule that defines the `Pipeline` and `CustomReportingPipeline` classes in addition to submodules that define extensible instances of that class. The `Pipeline` class is also in the main `Creevey` namespace so that you can simply `from creevey import Pipeline`.
1. `load_funcs` provides functions such as `load_image_from_url` for reading files into memory.
1. `ops` provides functions such as `resize` for processing file contents after they have been loaded into memory.
1. `write_funcs` provides functions such as `write_image` for writing out the output of `ops`.
1. `path_funcs` provides functions such as `combine_outdir_dirname_extension` for deriving output paths from input paths.
1. `util` contains utility functions that complement Creevey's core functionality, such as a function to generate a list of paths to all image files recursively within a specified directory.

## Q&A

### Question

What if I want to download a file, write it to disk, do further processing on it, and then write it to disk again?

### Response

A Creevey pipeline starts with a `load_func` that loads an item into memory from a specified location (which can be e.g. a URL or a location on disk) and ends with a `write_func` that writes out an item to a specified location (which can be e.g. an S3 URI or a location on disk). If you want to write to disk twice as described, then you have two options: 

1. Run two pipelines in succession, where the first downloads and writes to disk, and the second loads back in from disk, does the additional processing, and then writes to disk again.
2. Create a `load_func` that writes to disk as a side effect.

Option 2 is more efficient in theory because it avoids reading from disk. However, it is likely that you will need to iterate on your image processing, whereas you will only have to download and write to disk once. As a result, Option 1 can be more efficient in practice.
