# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

Creevey helps you process large sets of files. It is designed to handle the non-deep learning parts of computer vision deep learning workflows, such as preparing an image dataset by taking a set of image URLs and for each URL, downloading the corresponding image, trimming off its bottom 100 pixels, resizing it to 224x224, and writing it to disk. However, it is general enough to support many workflows that involve processing many files by loading each one into memory, processing it, and writing it out. It provides a general framework for defining such workflows and executing them in multiple threads. It also provides functions for common components of such workflows, such as file downloading and basic image processing.

Because Creevey provides concurrency for threads rather than processes, it is more appropriate for IO-bound workflows than for CPU-bound workflows. 

## Creevey's Basic `Pipeline` Abstraction

### Overview

 Creevey's core abstraction is the `Pipeline` class. A `Pipeline` object is initialized with a function `load_func` for loading data that is stored at a specified location into memory, an iterable of functions `ops` to apply to that object in sequence after it is loaded into memory, and a function `write_func` for writing out the final result of those transformations.
 
 A `Pipeline` object's `run` method takes an iterable `inpaths` of input paths, a function `outpath_func` for transforming each path in `inpaths` into a corresponding output path, the number `n_jobs` of threads to run, and a Boolean `skip_existing` indicating whether to overwrite existing files or to skip processing input files that would result in overwriting existing files.
 
 ### Example

Let's define the pipeline described above, which downloads images, trims off the bottom 100 pixels, resizes to 224x224, and writes to disk. We will then apply it pipeline to images with URLs in the `image_url` column of the CSV "my_images.csv", writing each file to the local directory "raw/images", preserving its filename.

```python
from functools import partial

import pandas as pd

from creevey.load_funcs import download_bytes
from creevey.ops import load_image_from_bytes, resize
from creevey.path_funcs import replace_directory 
from creevey.pipelines import Pipeline
from creevey.write_funcs import write_png


trim_bottom_100 = lambda image: image[:-100, :]
resize_224 = partial(resize, width=224, height=224)

my_pipeline = Pipeline(
    load_func=download_bytes,
    ops=[load_image_from_bytes, trim_bottom_100, resize_224],
    write_func=write_png,
)

my_df = pd.read_csv('my_images.csv')
urls = my_df.loc[:, 'image_url']
outpath_func = partial(replace_directory, outdir='raw/images')

my_pipeline.run(inpaths=urls, outpath_func=outpath_func, n_jobs=10)
```

## Recording File Properties

You might want to record some information about what happened as you processed the files. For instance, you might want records of the mapping from each input path to the corresponding output path. You may also want to record some metadata about the files that you can extract from there contents while you have them in memory for other processing.

For instance, in one project I work with tens of thousands of images from motion-activated cameras. Those cameras switch between a standard RGB mode during the day and an infrared mode at night. It is helpful to know which images were taken in which mode, for instance to experiment with training separate models for the two modes. It is easy to see which mode an image was taken in once it is loaded into memory as a NumPy array, but opening tens of thousands of images for this purpose is expensive. It would be better to record this information as a side effect while performing processing steps like those above.


