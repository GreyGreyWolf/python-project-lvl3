import requests
import urllib
import sys
import os
import logging
from page_loader import engine, created


def get_content(url):
    filter_get_log = logging.getLogger('main_logger.module_filter_func_get')
    try:
        request = requests.get(url)
    except (requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
            requests.exceptions.MissingSchema) as e:
        filter_get_log.debug(sys.exc_info()[:2])
        filter_get_log.error('Request parameters error')
        raise engine.PageLoaderException() from e
    except requests.exceptions.ConnectionError as e:
        filter_get_log.debug(sys.exc_info()[:2])
        filter_get_log.error(
            'Invalid site address or connection error'
            )
        raise engine.PageLoaderException() from e
    if request.status_code in [400, 403, 404, 410, 500, 503]:
        filter_get_log.error('The page does not respond')
        raise engine.PageLoaderException()
    request.encoding
    return request


def write_content(data, path):
    filter_write_log = logging.getLogger(
        'main_logger.module_filter_func_write')
    try:
        with open(path, 'wb') as new_file:
            new_file.write(data)
    except FileNotFoundError as e:
        filter_write_log.debug(sys.exc_info()[:2])
        filter_write_log.error('The specified directory does not exist')
        raise engine.PageLoaderException() from e
    except MemoryError as e:
        filter_write_log.debug(sys.exc_info()[:2])
        filter_write_log.error('Not enough space to write the file')
        raise engine.PageLoaderException() from e
    filter_write_log.info(f'Data is written to {path}!')


def filter_tag(tag, dir_files, url):
    filter_tag_log = logging.getLogger('main_logger.module_filter_func_filter')
    domain = urllib.parse.urlparse(url)
    if tag.name == 'link' and tag.has_attr('href'):
        internal_reference = urllib.parse.urlparse(tag['href'])
        path = urllib.parse.urlparse(tag['href']).path
        extn = os.path.splitext(path)[1]
        if extn and not internal_reference.netloc:
            path_files = os.path.join(
                dir_files, created.create_name(tag['href']))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag['href']))
            request = get_content(local_url)
            write_content(request.content, path_files)
            tag['href'] = tag['href'].replace(tag['href'], path_files)
            filter_tag_log.info(
                'The link to the resource in the page has been replaced!')
    elif (tag.name == 'img' or 'script') and tag.has_attr('src'):
        path = urllib.parse.urlparse(tag['src']).path
        extn = os.path.splitext(path)[1]
        internal_reference = urllib.parse.urlparse(tag['src'])
        if extn and not internal_reference.netloc:
            path_files = os.path.join(
                dir_files, created.create_name(tag['src']))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag['src']))
            request = get_content(local_url)
            write_content(request.content, path_files)
            tag['src'] = tag['src'].replace(tag['src'], path_files)
            filter_tag_log.info(
                'The link to the resource in the page has been replaced!')
