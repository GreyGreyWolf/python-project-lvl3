import requests
import os
import urllib
import bs4
from page_loader.cli import init_argparser


def start():
    parser = init_argparser()
    args = parser.parse_args()
    get_page(args.output, args.url)
    print('')
    print('Page loading is complete'.upper())
    print('')


def normalize_name(name):
    for sym in name:
        if sym in " ?.!/;:":
            name = name.replace(sym, '-')
            if name.startswith('-'):
                name = name[1:]
            elif name.endswith('-'):
                name = name[:-1]
    return name


def create_name(url):
    url = url.split('?')[0]
    parsed_link = urllib.parse.urlparse(url)
    if not parsed_link.netloc:
        name = url
        name = normalize_name(name)
        index = name.rfind('-')
        exten = name[index + 1:]
        main = name[: index]
        if main.endswith('-'):
            main = main[:-1]
        name = '{}.{}'.format(main, exten)
    else:
        if parsed_link.netloc.startswith('www'):
            parsed_link.netloc = parsed_link.netloc[4:]
        name = parsed_link.netloc + parsed_link.path
        name = normalize_name(name)
        name = '{}.{}'.format(name, 'html')
    return name


def create_dir(output, page_name):
    dir_name = page_name[:-5]
    resource_dir_name = os.path.join(output, dir_name)
    os.makedirs(resource_dir_name)
    path_page = os.path.join(resource_dir_name, page_name)
    path_files = path_page[:-5] + '_files'
    os.makedirs(path_files)
    return path_page, path_files


def get_content(url):
    if not url.startswith('http'):
        url = ''.join(['https://', url])
    request = requests.get(url)
    request.encoding
    return request


def filter_tag(tag, dir_files, url):
    domain = urllib.parse.urlparse(url)
    if tag.name == 'link' and tag.has_attr('href'):
        internal_reference = urllib.parse.urlparse(tag['href'])
        path = urllib.parse.urlparse(tag['href']).path
        extn = os.path.splitext(path)[1]
        if extn and not internal_reference.netloc:
            path_files = os.path.join(dir_files, create_name(tag['href']))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag['href']))
            request = get_content(local_url)
            write_content(request.content, path_files)
            tag['href'] = tag['href'].replace(tag['href'], path_files)
    elif (tag.name == 'img' or 'script') and tag.has_attr('src'):
        path = urllib.parse.urlparse(tag['src']).path
        extn = os.path.splitext(path)[1]
        internal_reference = urllib.parse.urlparse(tag['src'])
        if extn and not internal_reference.netloc:
            path_files = os.path.join(dir_files, create_name(tag['src']))
            local_url = urllib.parse.urlunparse(
                domain._replace(path=tag['src']))
            request = get_content(local_url)
            write_content(request.content, path_files)
            tag['src'] = tag['src'].replace(tag['src'], path_files)


def write_content(data, path):
    with open(path, 'wb') as new_file:
        new_file.write(data)


def get_page(output, url):
    page_name = create_name(url)
    path_page, dir_files = create_dir(output, page_name)
    request = get_content(url)
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        filter_tag(tag, dir_files, url)
        html_page = soup.prettify('utf-8')
        write_content(html_page, path_page)
