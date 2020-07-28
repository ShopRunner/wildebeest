from pathlib import Path
from setuptools import find_packages, setup

version_file_path = Path(__file__).parent / 'wildebeest' / '_version.py'

with open(version_file_path, 'r') as version_file:
    exec(version_file.read())

with open('README.md') as r:
    readme = r.read()

regular_packages = [
    'boto3',
    'joblib',
    'opencv-contrib-python',
    'pandas',
    'pillow',
    'requests',
    'retrying',
    'scikit-learn',
    'tqdm',
]
dev_packages = [
    'black',
    'flake8',
    'flake8-docstrings',
    'flake8-import-order',
    'matplotlib',
    'pytest',
    'pytest-cov',
    'responses',
]


setup(
    name='wildebeest',
    version=__version__,
    description='Bulk image processing',
    long_description=readme,
    packages=find_packages(exclude=('tests')),
    install_requires=regular_packages,
    extras_require={'dev': regular_packages + dev_packages},
    author='Greg Gandenberger',
    author_email='gsganden@gmail.com',
    url='https://github.com/ShopRunner/wildebeest',
    download_url=f'https://github.com/ShopRunner/wildebeest/tarball/{__version__}',
    long_description_content_type='text/markdown',
)
