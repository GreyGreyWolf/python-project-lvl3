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


def create_name(url):
    url = url.split('?')[0]
    parsed_link = urllib.parse.urlparse(url) 
    if not parsed_link.netloc:
        for sym in url:
            if sym in " ?!/;:" :
                name = url.replace(sym, '-')
    else:
        if parsed_link.netloc.startswith('www'):
            parsed_link.netloc = parsed_link.netloc[4:]
        name = parsed_link.netloc + parsed_link.path
        for sym in name:
            if sym in " ?.!/;:":
                name = name.replace(sym, '-')
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


def write_content(url, path):
    if not url.startswith('http'):
        url =  ''.join(['https://', url])  
    request = requests.get(url)
    request.encoding
    with open(path, 'wb') as new_file:
        new_file.write(request.content)
    return request


def get_page(output, url):
    list_tags = []
    page_name = create_name(url)
    path_page, dir_files = create_dir(output, page_name)
    request = write_content(url, path_page)
    soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({ 'link': True, 'img': True, 'script': True}):
        if tag.name == 'link':
            parsed_link = urllib.parse.urlparse(tag['href'])
            path = urllib.parse.urlparse(tag['href']).path
            extn = os.path.splitext(path)[1]
            if extn and not parsed_link.netloc:
                list_tags.append(tag['href'])    
        elif (tag.name == 'img' or 'script') and tag.has_attr('src'):
            parsed_link = urllib.parse.urlparse(tag['src'])
            path = urllib.parse.urlparse(tag['src']).path
            extn = os.path.splitext(path)[1]
            if extn and not parsed_link.netloc:
                list_tags.append(tag['src']) 
        for elem in list_tags:
            path_files = os.path.join(dir_files, create_name(elem))
            domain = urllib.parse.urlparse(url)
            local_url = urllib.parse.urlunparse(domain._replace(path = elem))
            write_content(local_url, path_files)
  