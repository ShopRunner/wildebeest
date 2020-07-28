from collections import defaultdict

import numpy as np

from tests.conftest import SAMPLE_DATA_DIR
from wildebeest.ops.image.stats import (
    calculate_dhash,
    calculate_mean_brightness,
    report_dhash,
    report_mean_brightness,
)
from wildebeest.ops.image.transforms import resize


class TestCalculateMeanBrightness:
    def test_calculate_mean_brightness_known_val(self):
        assert calculate_mean_brightness(np.array([[0, 0, 0], [1, 1, 1]])) == 0.5

    def test_calculate_mean_brightness_gray(self, sample_image_tall_grayscale):
        assert isinstance(calculate_mean_brightness(sample_image_tall_grayscale), float)

    def test_calculate_mean_brightness_rgb(self, sample_image_square_rgb):
        assert isinstance(calculate_mean_brightness(sample_image_square_rgb), float)

    def test_calculate_mean_brightness_rgba(self, sample_image_square_rgba):
        assert isinstance(calculate_mean_brightness(sample_image_square_rgba), float)


class TestReportMeanBrightness:
    def test_report_mean_brightness(self, sample_image_square_rgb):
        log_dict = defaultdict(dict)
        image_path = SAMPLE_DATA_DIR / 'wildebeest_rgb.jpg'
        result = report_mean_brightness(
            sample_image_square_rgb, log_dict=log_dict, inpath=image_path
        )
        assert log_dict[image_path]['mean_brightness'] == calculate_mean_brightness(
            sample_image_square_rgb
        )
        assert (result == sample_image_square_rgb).all()


class TestCalculateDHash:
    def test_calculate_dhash_rgb_hashlen_rgb(self, sample_image_square_rgb):
        hash = calculate_dhash(sample_image_square_rgb, sqrt_hash_size=8)
        assert _hashlen(hash) in [63, 64]

    def test_calculate_dhash_rgb_hashlen_rgba(self, sample_image_square_rgba):
        hash = calculate_dhash(sample_image_square_rgba, sqrt_hash_size=8)
        assert _hashlen(hash) in [63, 64]

    def test_calculate_dhash_rgb_hashlen_gray(self, sample_image_tall_grayscale):
        hash = calculate_dhash(sample_image_tall_grayscale, sqrt_hash_size=8)
        assert _hashlen(hash) in [63, 64]

    def test_record_dhash_hash_robust_to_resize_rgb(self, sample_image_square_rgb):
        hash = calculate_dhash(sample_image_square_rgb, sqrt_hash_size=8)
        resized_hash = calculate_dhash(
            resize(sample_image_square_rgb, shape=(24, 24)), sqrt_hash_size=8
        )
        assert _hamming_dist(hash, resized_hash) < 10

    def test_record_dhash_hash_robust_to_resize_rgba(self, sample_image_square_rgba):
        hash = calculate_dhash(sample_image_square_rgba, sqrt_hash_size=8)
        resized_hash = calculate_dhash(
            resize(sample_image_square_rgba, shape=(24, 24)), sqrt_hash_size=8
        )
        assert _hamming_dist(hash, resized_hash) < 10

    def test_record_dhash_hash_robust_to_resize_gray(self, sample_image_tall_grayscale):
        hash = calculate_dhash(sample_image_tall_grayscale, sqrt_hash_size=8)
        resized_hash = calculate_dhash(
            resize(sample_image_tall_grayscale, shape=(24, 24)), sqrt_hash_size=8
        )
        assert _hamming_dist(hash, resized_hash) < 10

    def test_record_dhash_hash_is_different_for_non_duplicates(
        self, sample_image_square_rgb, sample_image_tall_grayscale
    ):
        hash1 = calculate_dhash(sample_image_square_rgb, sqrt_hash_size=8)
        hash2 = calculate_dhash(sample_image_tall_grayscale, sqrt_hash_size=8)
        assert _hamming_dist(hash1, hash2) > 10


def _hamming_dist(hash1, hash2):
    return bin(hash1 ^ hash2).count("1")


def _hashlen(hash):
    return len(f'{hash:b}')


class TestReportDHash:
    def test_report_dhash(self, sample_image_square_rgb):
        log_dict = defaultdict(dict)
        image_path = SAMPLE_DATA_DIR / 'wildebeest_rgb.jpg'
        result = report_dhash(
            sample_image_square_rgb, inpath=image_path, log_dict=log_dict
        )
        assert log_dict[image_path]['dhash'] == calculate_dhash(sample_image_square_rgb)
        assert (result == sample_image_square_rgb).all()
