import requests
import os
import urllib
from page_loader.cli import init_argparser


def start():
    parser = init_argparser()
    args = parser.parse_args()
    get_page(args.output, args.url)
    print('\nPage loading is complete'.upper())


def formation_name(url):
    unformatted_name = urllib.parse.urlparse(url)
    file_name = unformatted_name.netloc + unformatted_name.path
    if file_name.startswith('www'):
        file_name = file_name[4:]
    for sym in file_name:
        if sym in " ?.!/;:":
            file_name = file_name.replace(sym,'-') 
    file_name = '{}.{}'.format(file_name, 'html')
    return file_name


def create_dir(output, file_name):
    dir_name = file_name[:-5]
    resource_dir_name = os.path.join(output, dir_name)
    os.makedirs(resource_dir_name)
    full_path = os.path.join(resource_dir_name, file_name)
    return full_path


def get_page(output, url):
    request = requests.get(url)
    request.encoding
    file_name = formation_name(url)
    full_path = create_dir(output, file_name)
    with open(full_path, 'wb') as html_file:
        html_file.write(request.content)
