"""Classes for downloading and processing datasets"""
import logging
import os
import sys
import tarfile
import threading
from typing import Type

import boto3
import botocore
from tqdm import tqdm


class _DatasetDirectoryInitializer:
    """
    Creates attributes pointing to subdirectories "raw", "interim", and
    "processed" of the provided `data_dir`. Intended to be used to
    initialize other dataset-related classes.
    """

    def __init__(self, data_dir: str):
        self.data_dir = data_dir
        self.raw_dir = os.path.join(self.data_dir, 'raw')
        self.interim_dir = os.path.join(self.data_dir, 'interim')
        self.processed_dir = os.path.join(self.data_dir, 'processed')


class BaseDownloader(_DatasetDirectoryInitializer):
    """
    Abstract base class for downloading datasets. Intended use is for
    classes inheriting from `BaseDataset` to delegate downloading to a
    class inheriting from `BaseDownloader` as part of its `get_raw` method,
    if the data is to be obtained by downloading.
    """

    def __init__(self, base_dir: str):
        super().__init__(base_dir)

    def download(self):
        raise NotImplementedError


class BaseExtractor:
    """
    Abstract base class for extracting dataset archive files. Intended
    use is for classes inheriting from `BaseDataset` to delegate extraction
    to a class inheriting from `BaseExtractor` as part of its `get_raw`
    method, if the data comes as some kind of archive file.
    """

    def __init__(self):
        raise NotImplementedError

    def extract(self):
        raise NotImplementedError


class BaseProcessor(_DatasetDirectoryInitializer):
    """
    Abstract base class for processing raw dataset files. Intended
    use is for classes inheriting from `BaseDataset` to delegate its
    `process` method to a class inheriting from `_Processor`, so that
    the processing steps for a specific dataset can be specified
    separately from steps for obtaining raw data that might be reusable
    across multiple datasets while still providing the convenience of
    working with one object per dataset.
    """

    def __init__(self, base_dir: str):
        super().__init__(base_dir)

    def process(self):
        raise NotImplementedError


class BaseDataset(_DatasetDirectoryInitializer):
    """
    Abstract base class for defining reproducible workflows for
    downloading and processing datasets.

    Constructor takes one parameter `base_dir` that points to a
    directory for storing the dataset. It then defines an attribute
    `raw_dir` that points to a subdirectory "raw" of base_dir and
    analogous attributes `interim_dir` and `processed_dir`.

    Intended use:

    - Method `get_raw` gets the raw data and puts it in `raw_dir`, for
    instance by downloading an archive file, expanding it, and then
    deleting it.
    - Method `process` gets the data ready for modeling and puts the
    result in `processed_dir`. If intermediate results are written to
    disk, they are written to `interim_dir`.
    - Method `build` runs `get_raw` and `process` in sequence, so that
    a user can have the entire dataset ready for modeling after a single
    method call.
    """

    def __init__(self, base_dir: str):
        super().__init__(base_dir)

    def get_raw(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def build(self):
        self.get_raw()
        self.process()


class S3Downloader(BaseDownloader):
    """
    Download a dataset that consists of a single file on S3.

    Attributes
    ----------
    s3_bucket
        Name of S3 bucket in which dataset file is stored.
    s3_key
        S3 key to dataset file.
    base_dir
        Local directory for storing dataset.
    """

    def __init__(self, s3_bucket: str, s3_key: str, base_dir: str) -> None:
        super().__init__(base_dir)
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key
        self.local_archive_path = os.path.join(
            self.raw_dir, os.path.basename(self.s3_key)
        )

    def download(self) -> None:
        """
        Download to "<base_dir>/raw/<s3_key>" the file in `s3_bucket`
        with key `s3_key`
        """
        logging.info(f'Downloading {self.s3_key} to {self.local_archive_path}')
        self._seen_so_far = 0

        if not os.path.isdir(self.raw_dir):
            os.makedirs(self.raw_dir)

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


class DownloadProgressPercentage:
    """Use as a callback to track download progress."""

    def __init__(self, client, bucket, key):
        self._key = key
        self._size = client.Bucket(bucket).Object(key).content_length
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):  # noqa: 170
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                f'\rProgress: {self._seen_so_far} / {self._size}  ({percentage:.2f}%)'
            )
            sys.stdout.flush()


class TarfileExtractor(BaseExtractor):
    """
    Extract members of a tarfile.

    Attributes
    ----------
    archive_path
        Path to archive to be extracted
    """

    def __init__(self, archive_path: str):
        self.local_archive_path = archive_path

    def extract(self) -> None:
        """Extract tarfile at `archive_path`"""
        with tarfile.open(self.local_archive_path) as archive:
            members = archive.getmembers()
            for item in tqdm(iterable=members, total=len(members)):
                archive.extract(
                    member=item, path=os.path.dirname(self.local_archive_path)
                )


class S3TarfileDataset(BaseDataset):
    """
    Download, extract, and delete a dataset stored as a tarfile on S3.

    Attributes
    ----------
    Processor
        Class that implements an `process` method, to which this
        class's `process` method is delegated.
    s3_bucket
        Name of S3 bucket in which dataset tarfile is stored.
    s3_key
        S3 key to dataset tarfile.
    base_dir
        Local directory for storing dataset.
    """

    def __init__(
        self,
        s3_bucket: str,
        s3_key: str,
        base_dir: str,
        Processor: Type['BaseProcessor'] = BaseProcessor,
    ):
        super().__init__(base_dir)
        self.base_dir = base_dir
        self.s3_bucket = s3_bucket
        self.s3_key = s3_key

        self.downloader = S3Downloader(
            s3_bucket=self.s3_bucket, s3_key=self.s3_key, base_dir=self.base_dir
        )
        self.extractor = TarfileExtractor(
            archive_path=self.downloader.local_archive_path
        )

        self.processor = Processor(base_dir=self.base_dir)
        self.process = self.processor.process

    def get_raw(self):
        """
        Download tarfile at `s3_key` in `s3_bucket` to '<base_dir>/raw',
        extract it, and delete the tarfile.
        """
        self.downloader.download()
        self.extractor.extract()
        os.remove(self.downloader.local_archive_path)
