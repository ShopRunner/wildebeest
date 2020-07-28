# Wildebeest

![wildebeest stampede](https://live.staticflickr.com/2635/3947963283_e1528e22f3_b.jpg)

Wildebeest is a file processing framework. It is designed for IO-bound workflows that involve reading files into memory, doing some processing on their contents, and writing out the results. It makes running those workflows faster and more reliable by parallelizing them across files, optional skipping files that have already been processed, handling errors, and keeping organized records of what happened.

Wildebeest was developed for deep learning computer vision projects, so in addition to the general framework it also provides predefined components for image processing. However, it can be used for any project that involves processing data from many sources.

See [the docs](https://wildebeest.readthedocs.io/) for more details.
