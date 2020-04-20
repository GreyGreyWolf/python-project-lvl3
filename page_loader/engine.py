import bs4
import requests
import sys
import logging
import os
from progress.bar import FillingSquaresBar
from page_loader.created import create_name, create_dir
from page_loader.filter import get_content, write_content, filter_tag
from page_loader.cli import init_argparser, qualifier


class PageLoaderException(Exception):
    pass


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


bar = FillingSquaresBar('Process download', max=30)

def start():
    parser = init_argparser()
    args = parser.parse_args()
    path = args.output
    path_log = os.path.join(path, 'Log_Page_Loader.log')
    url = args.url
    level = args.log
    logslevel = qualifier(level)
    file_handler = logging.FileHandler(path_log)
    file_handler.setLevel(logslevel)
    formatter = logging.Formatter(
        '%(asctime)s  - %(name)s - %(levelname)s - %(message)s'
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console = logging.StreamHandler()
    console.setLevel(logging.ERROR)
    formatter_console = logging.Formatter(
        '%(asctime)s - %(message)s')
    console.setFormatter(formatter_console)
    logger.addHandler(console)
    try:
        get_page(path, url)
    except PageLoaderException:
        sys.exit(1)
    else:
        sys.exit(0)



def get_page(output, url):
    logger.info('Start program!')
    page_name = create_name(url)
    bar.next()
    try:
        path_page, dir_files = create_dir(output, page_name)
        bar.next()
    except PermissionError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('No rights to make changes.')
        raise PageLoaderException() from e
    logger.info('Dirrectory created!')
    try:
        request = get_content(url)
        bar.next()
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
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        filter_tag(tag, dir_files, url)
        bar.next()
        logger.info('Tag-file uploaded!')
        html_page = soup.prettify('utf-8')
        bar.next()
    try:
        write_content(html_page, path_page)
        bar.next()
    except FileNotFoundError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('The specified directory does not exist')
        raise PageLoaderException() from e
    except MemoryError as e:
        logger.debug(sys.exc_info()[:2])
        logger.error('Not enough space to write the file')
        raise PageLoaderException() from e
    logger.info('HTML changed and saved')
    logger.info('Download is complete!')
    bar.finish()
