# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

Creevey is an image processing library that focuses on the non-deep learning parts of deep learning workflows, such as downloading and resizing images in bulk.

## Downloading

Given an iterable of image URLs, Creevey provides a function to download those images to a specified output directory with parallelization. For instance:

```python
from creevey import download_images_as_png

download_dir = 'example'
image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]
download_images_as_png(urls=image_urls,
                       outdir=download_dir,
                       n_jobs=3
                       )
```

This function tries to be smart about handling errors by retrying or skipping the downloads that raise them as appropriate. Run `help(download_images_as_png)` for additional information, including options for specifying output paths, logging, and skipping files that have already been downloaded.

This function is capable of generating a lot of requests in a short amount of time, so use it with care to avoid overwhelming anyone's servers.

## Resizing

Given an iterable of image paths, Creevey provides a function to resize those images to a specified shape and write the result to a specified output directory with parallelization. For instance, if you ran the code snippet above to download three images to an 'example' directory, then you could run this snippet to write copies resized to 100x100 pixels to an 'example_resized' directory:

```python
import os

from creevey import resize_multiple_files

resized_dir = 'example_resized'
image_paths = [os.path.join(download_dir, filename) for filename in os.listdir(download_dir)]
resize_multiple_files(paths=image_paths, shape=(100, 100), outdir=resized_dir, n_jobs=3)
```

## Creating Imagenet-Style Symlinks

Deep learning frameworks sometimes expect trainining/validation splits and class labels to be encoded in the directory structure following this format:

```
train
+-- label1
    +-- image1
    +-- image2
+-- label2
    +-- image3
    +-- image4
valid
+-- label1
    +-- image5
    +-- image6
+-- label2
    +-- image7
    +-- image8
```

Given a Pandas DataFrame containing image paths and labels, Creevey provides a function to create symlinks to those images that are organized in this format. It allows the user to specify the name of a column to group by, so that rows with the same value in that column are either all in "train" or all in "test." This feature could be used, for instance, when working with medical images that include multiple images for some patients to perform the training/validation split at the patient level rather than the image level. For instance:

```python
import pandas as pd

from creevey import create_imagenet_style_symlinks

df = pd.DataFrame({'image_path': [os.path.join(resized_dir, fn) for fn in image_filenames],
                   'tag': ['colin'] * 3 + ['dennis'] * 3,
                   'group': [1, 1, 2, 3, 4, 5]
                  })
create_imagenet_style_symlinks(df=df,
                               label_colname='tag',
                               path_colname='image_path',
                               valid_size=2,
                               outdir='example_symlinks',
                               groupby_colname='group',
                               )
```

## Specifying Data Processing Workflows

The `dataset` module provides classes for specifying data processing workflows. It assumes that each dataset corresponds to a single "base directory" with subdirectories "raw" for storing data as received from some source without any transformations, "processed" for storing derived products from the contents of "raw" for modeling purposes, and "interim" for any intermediate results produced from the contents of "raw" but not needed for modeling purposes. Dataset classes inherit from an abstract class `_Dataset` and specify a method `get_raw` and a method `process`. They then have a method `build` that runs `get_raw` and `process` in sequence so that users can obtain both raw and processed data that is ready for modeling with a single method call.

For instance, the class `S3TarfileDataset` is for a dataset the raw data is contained in a single tarfile on S3. It is instantiated with a base directory `Path` object, an S3 bucket name and an S3 key. Its `get_raw` method downloads the corresponding tarfile to the "raw" subdirectory of the base directory, extracts its contents, and deletes the tarfile. Processing steps are dataset-specific, so its `process` method raises a `NotImplementedError` until specified by a user (e.g. by subclassing).  

This module is uses composition to make it easy to mix and match methods based on dataset type. For instance, `S3TarfileDataset` delegates downloading to an `S3Downloader` object and archive extraction to a `TarfileExtractor` object.
