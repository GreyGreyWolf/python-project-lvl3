import logging
import os


def get_console_handler():
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    FORMATTER = logging.Formatter('%(message)s')
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


def get_logger(path, level, name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(get_console_handler())
    logger.addHandler(get_file_handler(path, level))
    return logger
