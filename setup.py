import re
from setuptools import find_packages, setup

with open('CHANGELOG.md', 'r') as f:
    changelog = f.read()

__version__ = re.search(r'\[(\d+\.\d+\.\d+)\]', changelog).group(1)

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
]


setup(
    name='creevey',
    version=__version__,
    description='Bulk image processing',
    long_description=readme,
    packages=find_packages(exclude=('tests')),
    install_requires=regular_packages,
    extras_require={'dev': regular_packages + dev_packages},
    author='Greg Gandenberger',
    author_email='gsganden@gmail.com',
    url='https://github.com/ShopRunner/creevey',
    download_url=f'https://github.com/ShopRunner/creevey/tarball/{__version__}',
    long_description_content_type='text/markdown',
)
