"""TK"""
import argparse
import logging
import psutil
import time


def main():
    """TK

    Args: TK

    Returns: TK
    """
    pass


def _parse_args() -> dict:
    """Parse command-line arguments, and log them with level INFO.

    Also provides file docstring as description for --help/-h.

    Returns:
        Command-line argument names and values as keys and values of a
            Python dictionary
    """
    parser = argparse.ArgumentParser(description=__doc__)
    # parser.add_argument('--foo', '-f', type=str, help='Named argument', required=False)
    # parser.add_argument('bar',
    #                     nargs='*',
    #                     help='Variable-length positional argument',
    #                     )
    # parser.add_argument('--baz', action='store_true', help='Flag argument')
    args = vars(parser.parse_args())
    logging.info(f'Arguments passed at command line: {args}')
    return args


def _log_memory() -> None:
    memory = psutil.virtual_memory()
    logging.info(f'Memory total:  {_convert_to_gb(memory.total)} GB')
    logging.info(f'Memory used:  {_convert_to_gb(memory.used)} GB')
    logging.info(f'Memory available:  {_convert_to_gb(memory.available)} GB')


def _convert_to_gb(num_bytes: float) -> float:
    return round(num_bytes / (2 ** 30), 2)


if __name__ == '__main__':
    start_time = time.time()
    logging.basicConfig(format='%(levelname)s %(asctime)s %(message)s')
    logging.getLogger().setLevel(logging.INFO)
    args_dict = _parse_args()
    _log_memory()

    main(**args_dict)

    _log_memory()
    end_time = time.time()
    logging.info(f'Completed in {round(end_time - start_time, 2)} seconds')
