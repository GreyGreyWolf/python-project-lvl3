import bs4
import logging
import os
from progress.bar import FillingSquaresBar
from page_loader.cli import init_argparser
from page_loader import prepare, getter


class PageLoaderException(Exception):
    pass


def start():
    parser = init_argparser()
    args = parser.parse_args()
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    FORMATTER = logging.Formatter('%(message)s')
    console_handler.setFormatter(FORMATTER)
    logger.addHandler(console_handler)
    path_log = os.path.join(args.output, 'Log_Page_Loader.log')
    file_handler = logging.FileHandler(path_log)
    file_handler.setLevel(args.log)
    FORMATTER = logging.Formatter(
        '%(asctime)s  - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(FORMATTER)
    logger.addHandler(file_handler)
    get_page(args.output, args.url)


def get_page(output, url):
    resources = {}
    logger = logging.getLogger()
    logger.info('Start program!')
    page_name = prepare.get_valid_name(url)
    path_page, dir_files = prepare.prepare_directory(output, page_name)
    logger.info('The directory creation process is complete')
    page = getter.get_content(url)
    soup = bs4.BeautifulSoup(page.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        resources.update(getter.get_tag(tag, dir_files, url))
    html_page = soup.prettify('utf-8')
    getter.write_content(html_page, path_page)
    for key, value in FillingSquaresBar(
         'Process download').iter(resources.items()):
        content = getter.get_content(key)
        getter.write_content(content.content, value)
    logger.info('The download page and the data is complete')
    logger.info('Process download is complete!')
    print('')
    print(f'The download is complete. Data is saved in {output}')
    print('')
