import textwrap
import warnings

from creevey.ops.image.stats import *
from creevey.ops.image.transforms import *


warnings.warn(
    textwrap.dedent(
        """
        creevey has been renamed "wildebeest." Please use the new name
        to get the latest version of this package.'
        """
    )
    .strip()
    .replace('\n', ' ')
)
