import textwrap
import warnings

from creevey.ops.helpers.report import *

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
