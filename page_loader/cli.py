import argparse
import logging
import os


text_download = '{} or {}'.format(
    'Specify the path to save the page (Example: /var/tmp)',
    'use by default (current directory)')
text_logger = 'Specify the logging level:{}'.format(
    '"debuf", "info", "warning", "error", "critical" or use by default (INFO)')
text_paths = (
    '''The specified path does not exist or no rights to make changes''')
default_path = os.getcwd()


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


def checking_paths(path):
    acces = os.access(path, os.W_OK)
    existence_path = os.path.isdir(path)
    if existence_path and acces:
        return path
    else:
        raise argparse.ArgumentTypeError(text_paths)


def init_argparser():
    parser = argparse.ArgumentParser(
        prog='download', description='Page Loader')
    parser.add_argument('-u', '--url', type=str, dest='url',
                        help='enter a link')
    parser.add_argument(
        '-o', '--output',
        type=checking_paths,
        default=default_path,
        help=text_download)
    parser.add_argument(
        '-l', '--log',
        default='info',
        choices=['debug', 'info', 'warning', 'error', 'critical'],
        help=text_logger)
    return parser
