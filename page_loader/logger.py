import logging
import os
from page_loader import cli


class PageLoaderException(Exception):
    pass


parser = cli.init_argparser()
args = parser.parse_args()
level = args.log
level = cli.qualifier(level)
path = cli.checking_paths(args.output)


def get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    FORMATTER = logging.Formatter(
     '%(asctime)s - %(message)s')
    console_handler.setFormatter(FORMATTER)
    return console_handler


def get_file_handler(path, level):
    path_log = os.path.join(path, 'Log_Page_Loader.log')
    file_handler = logging.FileHandler(path_log)
    file_handler.setLevel(level)
    FORMATTER = logging.Formatter(
        '%(asctime)s  - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(FORMATTER)
    return file_handler


def get_logger(path, level):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(path, level))
    return logger


logger = get_logger(path, level)
