import bs4
import requests
import sys
from page_loader.script import pageloader
from progress.bar import FillingSquaresBar
from page_loader import created 
from page_loader import filter


bar = FillingSquaresBar('Process download', max=30)


def get_page(output, url):
    pageloader.logger.info('Start program!')
    page_name = created.create_name(url)
    bar.next()
    try:
        path_page, dir_files = created.create_dir(output, page_name)
        bar.next()
    except PermissionError as e:
        pageloader.logger.debug(sys.exc_info()[:2])
        pageloader.logger.error('No rights to make changes.')
        raise pageloader.PageLoaderException() from e
    pageloader.logger.info('Dirrectory created!')
    try:
        request = filter.get_content(url)
        bar.next()
    except requests.exceptions.InvalidSchema as e:
        pageloader.logger.debug(sys.exc_info()[:2])
        pageloader.logger.error('Request parameters error')
        raise pageloader.PageLoaderException() from e
    except requests.exceptions.ConnectionError as e:
        pageloader.logger.debug(sys.exc_info()[:2])
        pageloader.logger.error(
            'Invalid site address or connection error'
            )
        raise pageloader.PageLoaderException() from e
    except requests.exceptions.Timeout as e:
        pageloader.logger.debug(sys.exc_info()[:2])
        pageloader.logger.error('Timed out waiting for a response')
        raise pageloader.PageLoaderException() from e
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        filter.filter_tag(tag, dir_files, url)
        bar.next()
        pageloader.logger.info('Tag-file uploaded!')
        html_page = soup.prettify('utf-8')
        bar.next()
    try:
        filter.write_content(html_page, path_page)
        bar.next()
    except FileNotFoundError as e:
        pageloader.logger.debug(sys.exc_info()[:2])
        pageloader.ogger.error('The specified directory does not exist')
        raise pageloader.PageLoaderException() from e
    except MemoryError as e:
        pageloader.logger.debug(sys.exc_info()[:2])
        pageloader.logger.error('Not enough space to write the file')
        raise pageloader.PageLoaderException() from e
    pageloader.logger.info('HTML changed and saved')
    pageloader.logger.info('Download is complete!')
    bar.finish()
