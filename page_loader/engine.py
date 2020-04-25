import bs4
from progress.bar import FillingSquaresBar
from page_loader.created import create_name, create_dir
from page_loader import filter, cli
from page_loader.logger import logger


bar = FillingSquaresBar('Process download', max=30)


def start():
    parser = cli.init_argparser()
    args = parser.parse_args()
    path = args.output
    url = args.url
    get_page(path, url)


def get_page(output, url):
    logger.info('Start program!')
    page_name = create_name(url)
    bar.next()
    path_page, dir_files = create_dir(output, page_name)
    bar.next()
    logger.info('The directory creation process is complete')
    request = filter.get_content(url)
    bar.next()
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        filter.filter_tag(tag, dir_files, url)
        bar.next()
        html_page = soup.prettify('utf-8')
        bar.next()
        filter.write_content(html_page, path_page)
        bar.next()
    logger.info('The download page and the data is complete')
    logger.info('Process download is complete!')
    bar.finish()
    print('')
    print(f'The download is complete. Data is saved in {output}')
    print('')
