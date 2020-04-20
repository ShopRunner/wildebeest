API
===

Generally, each module has a submodule which shares its name that defines generic components and an `image` submodule that defines components for working with images. Items in the former are imported into the module namespace, so that you can write e.g. from `creevey.path_funcs import combine_outdir_dirname_extension` rather than `from creevey.path_funcs.path_funcs import combine_outdir_dirname_extension`.

pipelines
---------

pipelines
^^^^^^^^^

.. automodule:: creevey.pipelines.pipelines
   :special-members: __call__
   :members:

image
^^^^^

.. automodule:: creevey.pipelines.image
   :members:

load_funcs
----------

load_funcs
^^^^^^^^^^

.. automodule:: creevey.load_funcs.load_funcs
   :members:

image
^^^^^

.. automodule:: creevey.load_funcs.image
   :members:

ops
---

helpers
^^^^^^^

report
""""""

.. automodule:: creevey.ops.helpers.report
   :members:

image
^^^^^

stats
"""""

.. automodule:: creevey.ops.image.stats
   :members:

transforms
""""""""""

.. automodule:: creevey.ops.image.transforms
   :members:

path_funcs
----------

path_funcs
^^^^^^^^^^

.. automodule:: creevey.path_funcs.path_funcs
   :members:

write_funcs
-----------

image
^^^^^

.. automodule:: creevey.write_funcs.image
   :members:

util
----

util
^^^^

.. automodule:: creevey.util.util
   :members:

image
^^^^^

.. automodule:: creevey.util.image
   :members:

constants
---------

.. automodule:: creevey.constants
   :members:
