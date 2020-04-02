
Structure
---------

Creevey contains the following modules. Generally, each one has a submodule which shares its name that defines generic components and an ``image`` submodule that defines components for working with images. Items in the former are imported into the module namespace, so that you can write e.g. ``from creevey.path_funcs import combine_outdir_dirname_extension`` rather than ``from creevey.path_funcs.path_funcs import combine_outdir_dirname_extension``.


#. ``pipelines`` contains a ``core`` submodule that defines the ``Pipeline`` and ``CustomReportingPipeline`` classes in addition to submodules that define extensible instances of that class. The ``Pipeline`` class is also in the main ``Creevey`` namespace so that you can simply ``from creevey import Pipeline``.
#. ``load_funcs`` provides functions such as ``load_image_from_url`` for reading files into memory.
#. ``ops`` provides functions such as ``resize`` for processing file contents after they have been loaded into memory.
#. ``write_funcs`` provides functions such as ``write_image`` for writing out the output of ``ops``.
#. ``path_funcs`` provides functions such as ``combine_outdir_dirname_extension`` for deriving output paths from input paths.
#. ``util`` contains utility functions that complement Creevey's core functionality, such as a function to generate a list of paths to all image files recursively within a specified directory.
