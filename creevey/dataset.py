"""
Classes for downloading and processing datasets in reproducible ways.
"""
import logging
import os
from pathlib import Path
import sys
import tarfile
import threading
from tqdm import tqdm
from typing import Type

import boto3
import botocore


class S3TarfileDataset(_Dataset):
    """
    Retrieve and process a dataset stored as a tarfile on S3.

    Attributes
    ----------
    Processor
        Class that implements an `process` method, to which this
        class's `process` method is to be delegated.
    s3_bucket
        Name of S3 bucket in which dataset tarfile is stored.
    s3_key
        S3 key to dataset tarfile.
    base_dir
        Local directory for storing dataset.
    """

    def __init__(
        self, Processor: Type['_Processor'], s3_bucket: str, s3_key: str, base_dir: Path
    ):
        super().__init__(base_dir)
        self.base_dir = base_dir
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

        self.downloader = S3Downloader(
            s3_bucket=self.s3_bucket, s3_key=self.s3_key, local_dir=self.base_dir
        )
        self.extractor = Tarf sileExtractor(
            archive_path=self.downloader.local_archive_path
        )

        self.processor = Processor(data_dir=self.base_dir)
        self.process = self.processor.process

        def get_raw(self):
            self.downloader.download()
            self.extractor.extract()
            os.remove(self.download.local_archive_path)


class _Dataset(_DatasetInitializer):
    """
    Abstract base class for defining reproducible workflows for
    downloading and processing datasets.

    Constructor takes one parameter `base_dir` that points to a
    directory for storing the dataset. It then defines an attribute
    `raw_dir` that points to a subdirectory "raw" of base_dir and
    analogous attributes `interim_dir` and `processed_dir`.

    Intended use:

    - Method `get_raw` gets the raw data and puts it in `raw_dir`, for
    instance by downloading an archive file, expanding it, and deleting
    it.
    - Method `process` gets the data ready for modeling and puts the
    result in `processed_dir`. If intermediate results are written to
    disk, they are written to `interim_dir`.
    - Method `build` runs `get_raw` and `process` in sequence, so that
    a user can have the entire dataset ready for modeling after a single
    method call.
    """

    def __init__(self, base_dir: Path):
        super().__init__(base_dir)

    def get_raw(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def build(self):
        self.get_raw()
        self.process()


class _DatasetInitializer:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir
        self.raw_data_dir = self.data_dir / 'raw'
        self.interim_data_dir = self.raw_data_dir.parent / 'interim'
        self.processed_data_dir = self.raw_data_dir.parent / 'processed'


class S3Downloader(_Downloader):
    """
    Download a dataset from S3.

    Attributes
    ----------
    s3_bucket
        Name of S3 bucket in which dataset tarfile is stored.
    s3_key
        S3 key to dataset tarfile.
    base_dir
        Local directory for storing dataset.
    """
    def __init__(self, s3_bucket: str, s3_key: str, base_dir: Path) -> None:
        super().__init__(base_dir)
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.local_archive_path = self.raw_dir/ os.path.basename(self.s3_key)

    def download(self):
        logging.info(f'Downloading {self.s3_key} to {self.local_archive_path}')
        self._seen_so_far = 0

        if not self.local_dir.is_dir():
            os.makedirs(self.local_dir)

        s3_client = boto3.resource('s3')
        progress = DownloadProgressPercentage(s3_client, self.s3_bucket, self.s3_key)
        try:
            s3_client.Bucket(self.s3_bucket).download_file(
                Key=self.s3_key,
                Filename=str(self.local_archive_path),
                Callback=progress,
            )
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == '404':
                print('The object does not exist.')
            else:
                raise


class _Downloader(_DatasetInitializer):
    def __init__(self, base_dir: Path):
        super().__init__(base_dir)

    def download(self):
        raise NotImplementedError


class DownloadProgressPercentage:
    """
    Use as a callback to track download progress
    """
    def __init__(self, client, bucket, key):
        self._key = key
        self._size = client.Bucket(bucket).Object(key).content_length
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                f'\rProgress: {self._seen_so_far} / {self._size}  ({percentage:.2f}%)'
            )
            sys.stdout.flush()


class TarfileExtractor(_Extractor):
    """
    Extract members of a tarfile.

    Attributes
    ----------
    archive_path
        Path to archive to be extracted
    """
    def __init__(self, archive_path: Path):
        self.archive_path = archive_path

    def extract(self):
        with tarfile.open(self.archive_path) as archive:
            members = archive.getmembers()
            for item in tqdm(iterable=members, total=len(members)):
                archive.extract(member=item, path=self.local_archive_path.parent)


class _Extractor:
    def __init__(self):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError


class _Processor(DatasetInitializer):
    def __init__(self, base_dir: Path):
        super().__init__(base_dir)

    def process(self):
        raise NotImplementedError
