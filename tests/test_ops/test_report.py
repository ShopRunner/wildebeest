from collections import defaultdict

from creevey.ops.helpers.report import get_report_output_decorator, report_output


def test_report_output():
    log_dict = defaultdict(dict)
    result = report_output(
        func=lambda x: x + 1,
        func_input=1,
        key='plus1',
        inpath='fake',
        log_dict=log_dict,
    )
    assert result == 2
    assert log_dict['fake']['plus1'] == result


def test_get_report_output_decorator():
    log_dict = defaultdict(dict)

    @get_report_output_decorator(key='plus1', log_dict=log_dict)
    def plus1(num):
        return num + 1

    result = plus1(1, inpath='fake')
    assert result == 2
    assert log_dict['fake']['plus1'] == result
