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
    new_name = unformatted_name.netloc + unformatted_name.path
    if new_name.startswith('www'):
        new_name = new_name[4:]
    new_name = new_name.replace('.', '-')
    new_name = new_name.replace('/', '-')
    new_name = '{}.{}'.format(new_name, 'html')
    return new_name


def create_dir(output, new_name):
    dir_name = new_name[:-5]
    resource_dir_name = os.path.join(output, dir_name)
    os.makedirs(resource_dir_name)
    full_path = os.path.join(resource_dir_name, new_name)
    return full_path


def get_page(output, url):
    request = requests.get(url)
    request.encoding
    new_name = formation_name(url)
    full_path = create_dir(output, new_name)
    with open(full_path, 'wb') as html_file:
        html_file.write(request.content)
