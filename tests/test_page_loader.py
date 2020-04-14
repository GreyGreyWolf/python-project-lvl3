import pytest
import urllib
import bs4
import os
import tempfile
from page_loader.created import create_name, create_dir
from page_loader.filter import get_content, write_content, filter_tag
from page_loader.engine import get_page


url = 'https://greygreywolf.github.io/python-project-lvl3/'


def test_create_name_page():
    expected_name = 'greygreywolf-github-io-python-project-lvl3.html'
    recieved_name = create_name(url)
    assert expected_name == recieved_name


def test_create_name_dir_files():
    expected_name = 'greygreywolf-github-io-python-project-lvl3_files'
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = create_name(url)
        path_page, dir_file = create_dir(test_dir, page_name)
        recieved_name = os.path.basename(dir_file)
        assert expected_name == recieved_name


def test_create_name_files():
    expected_name = 'python-project-lvl3-assets-css-style.css'
    with tempfile.TemporaryDirectory() as test_dir:
        get_page(test_dir, url)
        page_name = create_name(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        path_page = os.path.join(resource_dir_name, page_name)
        dir_file = path_page[:-5] + '_files'
        received_name = os.listdir(dir_file)
        assert expected_name == received_name[0]


def test_create_dir():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = create_name(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        get_page(test_dir, url)
        assert True == os.path.exists(resource_dir_name)


def test_create_page():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = create_name(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        full_created_path = os.path.join(resource_dir_name, page_name)
        get_page(test_dir, url)
        assert True == os.path.isfile(full_created_path)


def test_download_file():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = create_name(url)
        path_page, dir_files = create_dir(test_dir, page_name)
        request = get_content(url)
        soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        domain = urllib.parse.urlparse(url)
        if tag.name == 'link' and tag.has_attr('href'):
            internal_reference = urllib.parse.urlparse(tag['href'])
            path = urllib.parse.urlparse(tag['href']).path
            extn = os.path.splitext(path)[1]
            if extn and not internal_reference.netloc:
                path_files = os.path.join(dir_files, create_name(tag['href']))
                get_page(test_dir, url)
                assert True == os.path.isfile(path_files)
     