import os
import urllib
import sys
from page_loader import engine


def normalize_name(name):
    for sym in name:
        if sym in " ?.!/;:":
            name = name.replace(sym, '-')
            if name.startswith('-'):
                name = name[1:]
            elif name.endswith('-'):
                name = name[:-1]
    return name


def create_name(url):
    url = url.split('?')[0]
    parsed_link = urllib.parse.urlparse(url)
    if not parsed_link.netloc:
        name = url
        name = normalize_name(name)
        index = name.rfind('-')
        exten = name[index + 1:]
        main = name[: index]
        if main.endswith('-'):
            main = main[:-1]
        name = '{}.{}'.format(main, exten)
        engine.app_log.info('The name of the file generated!')
    else:
        if parsed_link.netloc.startswith('www'):
            parsed_link.netloc = parsed_link.netloc[4:]
        name = parsed_link.netloc + parsed_link.path
        name = normalize_name(name)
        name = '{}.{}'.format(name, 'html')
        engine.app_log.info('The name of the page generated!')
    return name


def create_dir(output, page_name):
    dir_name = page_name[:-5]
    resource_dir_name = os.path.join(output, dir_name)
    try:
        os.makedirs(resource_dir_name)
    except FileExistsError as e:
        engine.app_log.debug(sys.exc_info()[:2])
        engine.app_log.error('The file already exists')
        raise engine.PageLoaderException() from e
    except FileNotFoundError as e:
        engine.app_log.debug(sys.exc_info()[:2])
        engine.app_log.error('The specified directory does not exist')
        raise engine.PageLoaderException() from e
    except PermissionError as e:
        engine.app_log.debug(sys.exc_info()[:2])
        engine.app_log.error('No rights to make changes.')
        raise engine.PageLoaderException() from e
    engine.app_log.info('The directory page is created!')
    path_page = os.path.join(resource_dir_name, page_name)
    path_files = path_page[:-5] + '_files'
    os.makedirs(path_files)
    engine.app_log.info('The file page is created!')
    return path_page, path_files
