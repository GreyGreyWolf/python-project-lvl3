import bs4
from progress.bar import FillingSquaresBar
from page_loader import cli
from page_loader import created
from page_loader import filter
from page_loader import logger


class PageLoaderException(Exception):
    pass


url, output, level = cli.init_argparser()
app_log = logger.get_logger(output, level)
bar = FillingSquaresBar('Process download', max=12)


def start():
    get_page(output, url)


def get_page(output, url):
    app_log.info('Start program!')
    page_name = created.create_name(url)
    bar.next()
    path_page, dir_files = created.create_dir(output, page_name)
    bar.next()
    app_log.info('The directory creation process is complete')
    bar.next()
    request = filter.get_content(url)
    bar.next()
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        filter.filter_tag(tag, dir_files, url)
        html_page = soup.prettify('utf-8')
        bar.next()
        filter.write_content(html_page, path_page)
        bar.next()
    app_log.info('The download page and the data is complete')
    app_log.info('Process download is complete!')
    bar.finish()
    print('')
    print(f'The download is complete. Data is saved in {output}')
    print('')
