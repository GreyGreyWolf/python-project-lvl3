import requests
import os
import urllib
import bs4
from page_loader.cli import init_argparser


def start():
    parser = init_argparser()
    args = parser.parse_args()
    get_page(args.output, args.url)
    print('\nPage loading is complete\n'.upper())


def create_name_page(url):
    unformatted_name = urllib.parse.urlparse(url)
    page_name = unformatted_name.netloc + unformatted_name.path
    if page_name.startswith('www'):
        page_name = page_name[4:]
    for sym in page_name:
        if sym in " ?.!/;:":
            page_name = page_name.replace(sym, '-')
    page_name = '{}.{}'.format(page_name, 'html')
    return page_name


def create_name_file(html_link):
    name_file = html_link
    if name_file.startswith('/'):
        name_file = html_link[1:]
    for sym in name_file:
        if sym in " ?!/;:":
            name_file = html_link.replace(sym, '-')
    return name_file
    

def create_dir_page(output, page_name):
    dir_name = page_name[:-5]
    resource_dir_name = os.path.join(output, dir_name)
    os.makedirs(resource_dir_name)
    full_path_page = os.path.join(resource_dir_name, page_name)
    return full_path_page


def create_dir_file(full_path_page):
    dir_files = full_path_page[:-5] + '_files'
    os.makedirs(dir_files)
    return dir_files


# def change_page(html_file, dir_files):
#     with open(html_file) as editable_file:
#         soup = bs4.BeautifulSoup(editable_file, 'xml')
#         for tag in soup.find_all(['link', 'script', 'img'])



def get_page(output, url):
    request = requests.get(url)
    request.encoding
    page_name = create_name_page(url)
    full_path_page = create_dir_page(output, page_name)
    dir_files = create_dir_file(full_path_page)
    with open(full_path_page, 'wb') as html_file:
        html_file.write(request.content)
    # change_page(full_path_page, dir_files)
