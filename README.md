# Creevey

![](https://images.pottermore.com/bxd3o8b291gf/22qh5bCcA0g28OeKCwgwgE/70be84ace5da257fbd54d1ca0c06972c/ColinCreevey_WB_F2_ColinHoldingCamera_Still_080615_Land.jpg?w=320&h=320&fit=thumb&f=left&q=85)

Creevey helps you process large sets of files. It was designed to handle the non-deep learning parts of computer vision deep learning workflows, such as preparing an image dataset by taking a set of image URLs and for each URL, downloading the corresponding image, trimming off its bottom 100 pixels, resizing it to 224x224, and writing it to disk. However, it is general enough to support many workflows that involve processing many files by loading each one into memory, processing it, and writing it out. It provides a general framework for defining such workflows and executing them concurrently through either threading or multiprocessing. It also provides functions for common components of such workflows, such as file downloading and basic image processing.

## Creevey's Core `Pipeline` Abstraction

### Overview

 Creevey's core abstraction is the `Pipeline` class. A `Pipeline` object is initialized with a function `load_func` for loading data that is stored at a specified location into memory, a list (or other iterable) of functions `ops` to apply to that object in sequence after it is loaded into memory, a function `write_func` for writing out the final result of those transformations, and an optional string `parallel_strategy` indicating whether to prefer threads or processes for parallelization. (Threads are generally preferred for IO-bound workflows, while processes are preferred for CPU-bound workflows.)
 
 A `Pipeline` object's `run` method takes an iterable `inpaths` of input file paths, a function `outpath_func` for transforming each path in `inpaths` into a corresponding output path, the number `n_jobs` of threads or processes to run, and a Boolean `skip_existing` indicating whether to overwrite existing files or to skip processing input files that would result in overwriting existing files.
 
 ### Example
