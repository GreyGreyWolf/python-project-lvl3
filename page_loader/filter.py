import requests
import urllib
import sys
import os
from page_loader.created import create_name
from page_loader.logger import logger, PageLoaderException


def get_content(url):
    try:
        request = requests.get(url)
    except requests.exceptions.InvalidSchema as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Request parameters error')
        raise PageLoaderException() from e
    except requests.exceptions.ConnectionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error(
            'Invalid site address or connection error'
            )
        raise PageLoaderException() from e
    except requests.exceptions.Timeout as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Timed out waiting for a response')
        raise PageLoaderException() from e
    request.encoding
    return request


def write_content(data, path):
    with open(path, 'wb') as new_file:
        try:
            new_file.write(data)
        except MemoryError as e:
            logger.debug(sys.exc_info()[:2])
            logger.error('Not enough space to write the file')
            raise PageLoaderException() from e
    logger.info(f'Data is written to {path}!')


def filter_tag(tag, dir_files, url):
    domain = urllib.parse.urlparse(url)
    if tag.name == 'link' and tag.has_attr('href'):
        internal_reference = urllib.parse.urlparse(tag['href'])
        path = urllib.parse.urlparse(tag['href']).path
        extn = os.path.splitext(path)[1]
        if extn and not internal_reference.netloc:
            path_files = os.path.join(dir_files, create_name(tag['href']))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag['href']))
            request = get_content(local_url)
            write_content(request.content, path_files)
            tag['href'] = tag['href'].replace(tag['href'], path_files)
            logger.info(
                'The link to the resource in the page has been replaced!')
    elif (tag.name == 'img' or 'script') and tag.has_attr('src'):
        path = urllib.parse.urlparse(tag['src']).path
        extn = os.path.splitext(path)[1]
        internal_reference = urllib.parse.urlparse(tag['src'])
        if extn and not internal_reference.netloc:
            path_files = os.path.join(dir_files, create_name(tag['src']))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag['src']))
            request = get_content(local_url)
            write_content(request.content, path_files)
            tag['src'] = tag['src'].replace(tag['src'], path_files)
            logger.info(
                'The link to the resource in the page has been replaced!')
