.. wildebeest documentation master file, created by
   sphinx-quickstart on Wed Feb 13 13:07:01 2019.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Wildebeest
==========

.. image:: images/wildebeest_stampede.jpg

Wildebeest is a file processing framework. It is designed for IO-bound workflows that involve reading files into memory, processing their contents, and writing out the results. It makes running those workflows faster and more reliable by parallelizing across files, handling errors, making it easy to skip files that have already been processed, and keeping organized records of what was done.

Wildebeest was developed for deep learning computer vision projects, so in addition to the general framework it also provides predefined components for image processing. However, it can be used for any project that involves processing data from many sources.

Wildebeest was known as Creevey until version 3.0.0.

.. toctree::
   
   quickstart.rst
   api.rst
   limitations.rst
   contrib.rst
   conduct.rst


Indices and tables
==================

* :ref:`modindex`
