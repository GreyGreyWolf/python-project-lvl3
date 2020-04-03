import argparse
from pathlib import Path


default_path = Path().absolute()
Text = '{} or {}'.format(
            'Specify the path to save the page (Example: /var/tmp)',
            'use by default (current directory)')


def init_argparser():
    parser = argparse.ArgumentParser(
        prog='download', description='Page Loader')
    parser.add_argument('url', type=str, help='enter a link')
    parser.add_argument(
        '-o', '--output',
        default=default_path,
        help=Text
    )
    return parser
