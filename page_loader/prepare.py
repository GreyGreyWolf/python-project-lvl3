import os
from urllib.parse import urlparse
import re
import logging
import sys
from page_loader import engine


def normalize_name(name):
    name = re.sub(r'[^A-Za-z0-9]', '-', name)
    if name.startswith('-'):
        name = name[1:]
    elif name.endswith('-'):
        name = name[:-1]
    return name


def get_valid_name(url):
    parsed_link = urlparse(url)
    if not parsed_link.netloc:
        index = parsed_link.path.rfind('.')
        exten = parsed_link.path[index + 1:]
        main = parsed_link.path[: index]
        main = normalize_name(main)
        name = '{}.{}'.format(main, exten)
    else:
        if parsed_link.netloc.startswith('www'):
            parsed_link.netloc = parsed_link.netloc[4:]
        name = parsed_link.netloc + parsed_link.path
        name = normalize_name(name)
        name = '{}.{}'.format(name, 'html')
    return name


def get_dir_name(name):
    name_dir = name[:-5]
    return name_dir


def prepare_directory(output, page_name):
    '''
    This function creates the main directory where the page saved, and
     a directory for files, where files saved
    Returns the path to the main directory and
     to the directory with files
    '''
    logger = logging.getLogger()
    name_page_dir = get_dir_name(page_name)
    resource_dir_name = os.path.join(output, name_page_dir)
    try:
        os.makedirs(resource_dir_name)
    except FileExistsError as e:
        logger.debug(sys.exc_info())
        logger.error('The file already exists')
        raise engine.PageLoaderException() from e
    except FileNotFoundError as e:
        logger.debug(sys.exc_info())
        logger.error('The specified directory does not exist')
        raise engine.PageLoaderException() from e
    except PermissionError as e:
        logger.debug(sys.exc_info())
        logger.error('No rights to make changes.')
        raise engine.PageLoaderException() from e
    logger.info(
        f'The directory for page(html file) -{resource_dir_name} is created!')
    path_page = os.path.join(resource_dir_name, page_name)
    path_files = get_dir_name(path_page) + '_files'
    try:
        os.makedirs(path_files)
    except FileExistsError as e:
        logger.debug(sys.exc_info())
        logger.error('The file already exists')
        raise engine.PageLoaderException() from e
    logger.info(f'The directory for files -{path_files} is created!')
    return path_page, path_files
