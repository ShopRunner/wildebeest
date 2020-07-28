
Limitations
-----------

Wildebeest provides concurrency through threading rather than multiprocessing, which is appropriate for **IO-bound rather than CPU-bound** workflows.

**Wildebeest does not force you to write threadsafe code.** It is intended to be used for workflows in which multiple files are all processed separately and written out to separate locations. This pattern is generally threadsafe, but it has some pitfalls. For instance, if your ``write_func`` checks whether an output directory exists and creates it if it does not, then it can happen that the process switches threads between checking whether the directory exists and attempting to create it, so that the attempt to create it raises an error. (One solution to this problem is to wrap the directory creation step in a ``try/except`` block, as in ``wildebeest.write_funcs.image.write_image``.)
