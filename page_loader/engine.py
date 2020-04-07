import requests
import os
import urllib
from bs4 import BeautifulSoup
from page_loader.cli import init_argparser


def start():
    parser = init_argparser()
    args = parser.parse_args()
    get_page(args.output, args.url)
    print('\nPage loading is complete'.upper())


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


def create_name_file(path):
    for sym in path:
        if sym in " ?!/;:":
            name_file = path.replace(sym, '-')
    return name_file
    

def create_dir_page(output, page_name):
    dir_name = page_name[:-5]
    resource_dir_name = os.path.join(output, dir_name)
    os.makedirs(resource_dir_name)
    full_path_page = os.path.join(resource_dir_name, page_name)
    return full_path_page


def create_dir_file(full_path_page):
    if full_path_page.endswith('/'):
        path_files = full_path_page[:-1] + '_files'
    else:
        path_files = full_path_page + '_files'
    os.makedirs(path_files)
    return path_files


# def change_page(full_path_page, path_files):
#     with open(full_path_page, 'r') as editable_file:
#         contetnts = editable_file.read()
#         soup = BeautifulSoup(contetnts, 'lxml')
#         tags = soup.findAll(['link','script', 'img'])
#         for tag in tags:
#             if tag.find('src'):
#                 full_path_files = os.path.join(path_files, create_name_file(?) )
#                 with open(path_files, 'w') as new_file:
#                     new_file.write()
#                 tag.replace_with(create_name_file(tag.text)


def get_page(output, url):
    request = requests.get(url)
    request.encoding
    file_name = create_name_page(url)
    full_path_page = create_dir_page(output, file_name)
    path_files = create_dir_file(full_path_page)
    with open(full_path_page, 'wb') as html_file:
        html_file.write(request.content)
    change_page(full_path_page, path_files)
