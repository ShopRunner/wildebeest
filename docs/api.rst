API
===

Generally, each module has a submodule which shares its name that defines generic components and an ``image`` submodule that defines components for working with images. Items in the former are imported into the module namespace, so that you can write e.g. from ``wildebeest.path_funcs import combine_outdir_dirname_extension`` rather than ``from wildebeest.path_funcs.path_funcs import combine_outdir_dirname_extension``.

pipelines
---------

pipelines
^^^^^^^^^

.. automodule:: wildebeest.pipelines.pipelines
   :special-members: __call__
   :members:

image
^^^^^

.. automodule:: wildebeest.pipelines.image
   :members:

load_funcs
----------

load_funcs
^^^^^^^^^^

.. automodule:: wildebeest.load_funcs.load_funcs
   :members:

image
^^^^^

.. automodule:: wildebeest.load_funcs.image
   :members:

ops
---

helpers
^^^^^^^

report
""""""

.. automodule:: wildebeest.ops.helpers.report
   :members:

image
^^^^^

stats
"""""

.. automodule:: wildebeest.ops.image.stats
   :members:

transforms
""""""""""

.. automodule:: wildebeest.ops.image.transforms
   :members:

path_funcs
----------

path_funcs
^^^^^^^^^^

.. automodule:: wildebeest.path_funcs.path_funcs
   :members:

write_funcs
-----------

image
^^^^^

.. automodule:: wildebeest.write_funcs.image
   :members:

util
----

util
^^^^

.. automodule:: wildebeest.util.util
   :members:

image
^^^^^

.. automodule:: wildebeest.util.image
   :members:

constants
---------

.. automodule:: wildebeest.constants
   :members:
