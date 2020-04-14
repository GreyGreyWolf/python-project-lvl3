import bs4
from page_loader.created import create_name, create_dir
from page_loader.filter import get_content, write_content, filter_tag
from page_loader.cli import init_argparser


def start():
    parser = init_argparser()
    args = parser.parse_args()
    get_page(args.output, args.url)
    print('')
    print('Page loading is complete'.upper())
    print('')


def get_page(output, url):
    page_name = create_name(url)
    path_page, dir_files = create_dir(output, page_name)
    request = get_content(url)
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        filter_tag(tag, dir_files, url)
        html_page = soup.prettify('utf-8')
        write_content(html_page, path_page)
