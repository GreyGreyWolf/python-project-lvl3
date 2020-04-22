import bs4
import requests
import sys
from page_loader.script.pageloader import PageLoaderException, logger
from progress.bar import FillingSquaresBar
from page_loader.created import create_name, create_dir
from page_loader import filter


bar = FillingSquaresBar('Process download', max=30)


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
        request = filter.get_content(url)
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
        filter.filter_tag(tag, dir_files, url)
        bar.next()
        logger.info('Tag-file uploaded!')
        html_page = soup.prettify('utf-8')
        bar.next()
    try:
        filter.write_content(html_page, path_page)
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
