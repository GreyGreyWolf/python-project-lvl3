import requests
import urllib
import sys
import os
import logging
from page_loader import engine, prepare


search_tags = {'link': 'href', 'img': 'src', 'script': 'src'}


def get_content(url):
    logger = logging.getLogger(__name__)
    try:
        response = requests.get(url)
    except (requests.exceptions.InvalidSchema,
            requests.exceptions.InvalidURL,
            requests.exceptions.MissingSchema) as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Request parameters error')
        raise engine.PageLoaderException() from e
    except requests.exceptions.ConnectionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error(
            'Invalid site address or connection error')
        raise engine.PageLoaderException() from e
    if response.status_code in [400, 403, 404, 410, 500, 503]:
        logger.error('The page does not respond')
        raise engine.PageLoaderException()
    response.encoding
    return response


def write_content(data, path):
    logger = logging.getLogger()
    try:
        with open(path, 'wb') as new_file:
            new_file.write(data)
    except FileNotFoundError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('The specified directory does not exist')
        raise engine.PageLoaderException() from e
    logger.info(f'Data is written to {path}!')


def get_tag(tag, dir_files, url):
    dict = {}
    logger = logging.getLogger()
    domain = urllib.parse.urlparse(url)
    flag = tag.name in search_tags.keys()
    attr = search_tags[tag.name]
    if flag is True and tag.has_attr(attr):
        internal_reference = urllib.parse.urlparse(tag[attr])
        path = urllib.parse.urlparse(tag[attr]).path
        extn = os.path.splitext(path)[1]
        if extn and not internal_reference.netloc:
            path_files = os.path.join(
                dir_files, prepare.get_valid_name(tag[attr]))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag[attr]))
            tag[attr] = tag[attr].replace(tag[attr], path_files)
            logger.info(
                'The link to the resource in the page has been replaced!')
            dict[local_url] = path_files
    return dict
