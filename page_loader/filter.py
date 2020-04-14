import requests
import urllib
import os
from page_loader.created import create_name


def get_content(url):
    if not url.startswith('http'):
        url = ''.join(['https://', url])
    request = requests.get(url)
    request.encoding
    return request


def write_content(data, path):
    with open(path, 'wb') as new_file:
        new_file.write(data)


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
