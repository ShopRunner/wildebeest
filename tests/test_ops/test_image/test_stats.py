from collections import defaultdict

import numpy as np

from creevey.ops.image.transforms import resize
from creevey.ops.helpers import get_report_output_decorator, report_output
from creevey.ops.image.stats import calculate_dhash, calculate_mean_brightness
from tests.conftest import SAMPLE_DATA_DIR


class TestCalculateMeanBrightness:
    def test_calculate_mean_brightness_grayscale(self, sample_image_tall_grayscale):
        actual = calculate_mean_brightness(sample_image_tall_grayscale)
        assert isinstance(actual, float)


class TestReportMeanBrightness:  # integration tests for calculate_mean_brightness and reporting functions
    @get_report_output_decorator(key='mean_brightness')
    def decorator_report_mean_brightness(self, image):
        return calculate_mean_brightness(image)

    def test_record_mean_brightness_grayscale(self, sample_image_tall_grayscale):
        log_dict = defaultdict(dict)
        image_path = SAMPLE_DATA_DIR / 'creevey_rgb.jpg'
        self.decorator_report_mean_brightness(
            sample_image_tall_grayscale, inpath=image_path, log_dict=log_dict
        )
        assert isinstance(log_dict[image_path]['mean_brightness'], float)


#
#     def test_record_mean_brightness_all_black(self, sample_image_tall_grayscale):
#         log_dict = defaultdict(dict)
#         image_path = 'foo'
#         black_image = np.zeros(sample_image_tall_grayscale.shape, dtype='uint8')
#         record_mean_brightness(black_image, inpath=image_path, log_dict=log_dict)
#         assert log_dict[image_path]['mean_brightness'] == 0
#
#     def test_record_mean_brightness_rgb(self, sample_image_square_rgb):
#         log_dict = defaultdict(dict)
#         image_path = SAMPLE_DATA_DIR / 'creevey_rgb.jpg'
#         record_mean_brightness(
#             sample_image_square_rgb, inpath=image_path, log_dict=log_dict
#         )
#         assert isinstance(log_dict[image_path]['mean_brightness'], float)
#
#     def test_record_mean_brightness_rgba(self, sample_image_square_rgba):
#         log_dict = defaultdict(dict)
#         image_path = SAMPLE_DATA_DIR / 'creevey_rgba.png'
#         record_mean_brightness(
#             sample_image_square_rgba, inpath=image_path, log_dict=log_dict
#         )
#         assert isinstance(log_dict[image_path]['mean_brightness'], float)
#
#
# class TestRecordDHash:
#     def test_record_dhash_rgb_hashlen_rgb(self, sample_image_square_rgb):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_square_rgb, sqrt_hash_size=8, inpath='fake', log_dict=log_dict
#         )
#         assert len(f'{log_dict["fake"]["dhash"]:b}') in [63, 64]
#
#     def test_record_dhash_rgb_hashlen_rgba(self, sample_image_square_rgba):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_square_rgba, sqrt_hash_size=8, inpath='fake', log_dict=log_dict
#         )
#         assert len(f'{log_dict["fake"]["dhash"]:b}') in [63, 64]
#
#     def test_record_dhash_rgb_hashlen_gray(self, sample_image_tall_grayscale):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_tall_grayscale,
#             sqrt_hash_size=8,
#             inpath='fake',
#             log_dict=log_dict,
#         )
#         assert len(f'{log_dict["fake"]["dhash"]:b}') in [63, 64]
#
#     def test_record_dhash_hash_robust_to_resize_rgb(self, sample_image_square_rgb):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_square_rgb,
#             sqrt_hash_size=8,
#             inpath='original',
#             log_dict=log_dict,
#         )
#         report_dhash(
#             resize(sample_image_square_rgb, shape=(24, 24)),
#             sqrt_hash_size=8,
#             inpath='resized',
#             log_dict=log_dict,
#         )
#         bin(
#             int(log_dict["original"]["dhash"]) ^ int(log_dict["resized"]["dhash"])
#         ).count("1") < 10
#
#     def test_record_dhash_hash_robust_to_resize_rgba(self, sample_image_square_rgba):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_square_rgba,
#             sqrt_hash_size=8,
#             inpath='original',
#             log_dict=log_dict,
#         )
#         report_dhash(
#             resize(sample_image_square_rgba, shape=(24, 24)),
#             sqrt_hash_size=8,
#             inpath='resized',
#             log_dict=log_dict,
#         )
#         bin(
#             int(log_dict["original"]["dhash"]) ^ int(log_dict["resized"]["dhash"])
#         ).count("1") < 10
#
#     def test_record_dhash_hash_robust_to_resize_gray(self, sample_image_tall_grayscale):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_tall_grayscale,
#             sqrt_hash_size=8,
#             inpath='original',
#             log_dict=log_dict,
#         )
#         report_dhash(
#             resize(sample_image_tall_grayscale, shape=(24, 24)),
#             sqrt_hash_size=8,
#             inpath='resized',
#             log_dict=log_dict,
#         )
#         bin(
#             int(log_dict["original"]["dhash"]) ^ int(log_dict["resized"]["dhash"])
#         ).count("1") < 10
#
#     def test_record_dhash_hash_is_different_for_non_duplicates(
#         self, sample_image_square_rgb, sample_image_tall_grayscale
#     ):
#         log_dict = defaultdict(dict)
#         report_dhash(
#             sample_image_square_rgb, sqrt_hash_size=8, inpath='im1', log_dict=log_dict
#         )
#         report_dhash(
#             sample_image_tall_grayscale,
#             sqrt_hash_size=8,
#             inpath='im2',
#             log_dict=log_dict,
#         )
#         bin(int(log_dict["im1"]["dhash"]) ^ int(log_dict["im2"]["dhash"])).count(
#             "1"
#         ) > 10
