import argparse
import logging
from pathlib import Path


default_path = Path().absolute()
text_download = '{} or {}'.format(
            'Specify the path to save the page (Example: /var/tmp)',
            'use by default (current directory)')
text_logger = 'specify the logging level:{}'.format(
     '"debuf", "info", "warning", "error", "critical"')
text_raise = '"debug", "info", "warning", "error", "critical"'


def qualifier(param):
    if param == 'debug':
        return logging.DEBUG
    elif param == 'info':
        return logging.INFO
    elif param == 'warning':
        return logging.WARNING
    elif param == 'error':
        return logging.ERROR
    elif param == 'critical':
        return logging.CRITICAL
    raise argparse.ArgumentTypeError(
        'Unknown parametr: "{}". Use one of this: {}'.format(
            param, text_raise))


def init_argparser():
    parser = argparse.ArgumentParser(
        prog='download', description='Page Loader')
    parser.add_argument('url', type=str, help='enter a link')
    parser.add_argument(
        '-o', '--output',
        default=default_path,
        help=text_download)
    parser.add_argument(
        '-l', '--log',
        default='info',
        # choices=[
        #     'debug', 'info',
        #     'warning', 'error', 'critical'],
        help=text_logger)
    return parser
