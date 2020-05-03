import bs4
import logging
from progress.bar import FillingSquaresBar
from page_loader.cli import init_argparser, qualifier
from page_loader import created, filter, logger


class PageLoaderException(Exception):
    pass


bar = FillingSquaresBar('Process download', max=12)


def start():
    parser = init_argparser()
    args = parser.parse_args()
    main_log = logger.get_logger(
        args.output, qualifier(args.log), 'main_logger')
    get_page(args.output, args.url)


def get_page(output, url):
    engine_log = logging.getLogger('main_logger.module_engine')
    engine_log.info('Start program!')
    page_name = created.create_name(url)
    bar.next()
    path_page, dir_files = created.create_dir(output, page_name)
    bar.next()
    engine_log.info('The directory creation process is complete')
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
    engine_log.info('The download page and the data is complete')
    engine_log.info('Process download is complete!')
    bar.finish()
    print('')
    print(f'The download is complete. Data is saved in {output}')
    print('')
