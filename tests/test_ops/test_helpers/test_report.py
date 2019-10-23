from collections import defaultdict
from functools import partial

from creevey import CustomReportingPipeline
from creevey.load_funcs.image import load_image_from_url
from creevey.ops import get_report_output_decorator, report_output
from creevey.ops.image import calculate_mean_brightness
from creevey.path_funcs import join_outdir_filename_extension
from creevey.write_funcs.image import write_image

# @get_report_output_decorator(key='mean_brightness')
# def report_mean_brightness(image):
#     return calculate_mean_brightness(image)
#
#
# report_brightness_pipeline = CustomReportingPipeline(
#     load_func=load_image_from_url, ops=[report_mean_brightness], write_func=write_image
# )
#
# image_filenames = ['2RsJ8EQ', '2TqoToT', '2VocS58', '2scKPIp', '2TsO6Pc', '2SCv0q7']
# image_urls = [f'https://bit.ly/{filename}' for filename in image_filenames]
#
# keep_filename_png_in_cwd = partial(
#     join_outdir_filename_extension, outdir='.', extension='.png'
# )
# print(
#     report_brightness_pipeline.run(
#         inpaths=image_urls,
#         path_func=keep_filename_png_in_cwd,
#         n_jobs=1,
#         skip_existing=False,
#     )
# )


def test_report_output():
    log_dict = defaultdict(dict)
    result = report_output(
        func=lambda x: x + 1,
        func_input=1,
        key='plus1',
        inpath='fake',
        log_dict=log_dict,
    )
    assert result == 1
    assert log_dict['fake']['plus1'] == 2


def test_get_report_output_decorator():
    log_dict = defaultdict(dict)

    @get_report_output_decorator(key='plus1')
    def report_plus1(num):
        return num + 1

    result = report_plus1(1, inpath='fake', log_dict=log_dict)
    assert result == 1
    assert log_dict['fake']['plus1'] == 2
