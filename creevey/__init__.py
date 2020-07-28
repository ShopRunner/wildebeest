import textwrap
import warnings

from creevey._version import __version__
from creevey.pipelines import *

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
