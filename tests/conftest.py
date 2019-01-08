import os
import sys


TEST_DIR = os.path.dirname(__file__)
SAMPLE_DATA_DIR = os.path.join(TEST_DIR, 'sample_data')

MADEYE_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/p__/images/7/73/Mad-Eye_Moody%27s_%22mad_eye%22.jpeg/revision/latest?path-prefix=protagonist'  # noqa: E501
)
STABLE_LOCAL_MADEYE_IMAGE_FILENAME = 'madeye.png'
STABLE_LOCAL_MADEYE_IMAGE_PATH = os.path.join(SAMPLE_DATA_DIR, STABLE_LOCAL_MADEYE_IMAGE_FILENAME)
TEMP_LOCAL_MADEYE_IMAGE_FILENAME_DEFAULT = 'latest?path-prefix=protagonist.png'
TEMP_LOCAL_MADEYE_IMAGE_PATH_DEFAULT = os.path.join(SAMPLE_DATA_DIR,
                                                    TEMP_LOCAL_MADEYE_IMAGE_FILENAME_DEFAULT
                                                    )
TEMP_LOCAL_MADEYE_IMAGE_FILENAME_CUSTOM = 'revision.png'
TEMP_LOCAL_MADEYE_IMAGE_PATH_CUSTOM = os.path.join(SAMPLE_DATA_DIR,
                                                   TEMP_LOCAL_MADEYE_IMAGE_FILENAME_CUSTOM
                                                   )


PHILOSOPHERS_STONE_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/smurfsfanon/images/3/32/Philosopher%27s_Stone.jpg'
)
STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME = 'philosophers_stone.png'
STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH = os.path.join(
    SAMPLE_DATA_DIR, STABLE_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME
)
TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME_DEFAULT = 'Philosopher%27s_Stone.png'
TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_DEFAULT = os.path.join(
    SAMPLE_DATA_DIR, TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME_DEFAULT
)
TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME_CUSTOM = '32.png'
TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_PATH_CUSTOM = os.path.join(
    SAMPLE_DATA_DIR, TEMP_LOCAL_PHILOSOPHERS_STONE_IMAGE_FILENAME_CUSTOM
)