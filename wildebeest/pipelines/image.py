"""Image-processing pipelines"""
from typing import Any, Callable, Iterable, Optional, Union

from wildebeest import Pipeline
from wildebeest.load_funcs.image import load_image_from_url
from wildebeest.write_funcs.image import write_image


class DownloadImagePipeline(Pipeline):
    """
    Class for defining a pipeline that downloads images.

    Attributes
    ----------
    ops
        See `wildebeest.pipelines.Pipeline`.
    """

    def __init__(
        self,
        ops: Optional[
            Union[Callable[[Any], Any], Iterable[Callable[[Any], Any]]]
        ] = None,
    ):
        super().__init__(load_func=load_image_from_url, ops=ops, write_func=write_image)
