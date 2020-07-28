from collections import defaultdict

from wildebeest.ops import get_report_output_decorator, report_output


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
