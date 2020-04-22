import pytest
import urllib
import bs4
import os
import tempfile
from page_loader import engine, filter, created


url = 'https://greygreywolf.github.io/python-project-lvl3/'


def test_create_name():
    expected_page = 'greygreywolf-github-io-python-project-lvl3.html'
    expected_file = 'python-project-lvl3-assets-css-style.css'
    with tempfile.TemporaryDirectory() as test_dir:
        engine.get_page(test_dir, url)
        recieved_page = created.create_name(url)
        dir_name = recieved_page[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        path_page = os.path.join(resource_dir_name, recieved_page)
        dir_file = path_page[:-5] + '_files'
        received_file = os.listdir(dir_file)
        assert expected_file == received_file[0]
        assert expected_page == recieved_page


def test_create_dir():
    expected_dir_file = 'greygreywolf-github-io-python-project-lvl3_files'
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = created.create_name(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        dir_file = resource_dir_name + '_files'
        received_dir_file = os.path.basename(dir_file)
        engine.get_page(test_dir, url)
        assert True == os.path.exists(resource_dir_name)
        assert expected_dir_file == received_dir_file    


def test_download_page():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = created.create_name(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        full_created_path = os.path.join(resource_dir_name, page_name)
        engine.get_page(test_dir, url)
        assert True == os.path.isfile(full_created_path)


def test_download_file():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = created.create_name(url)
        path_page, dir_files = created.create_dir(test_dir, page_name)
        request = filter.get_content(url)
        soup = bs4.BeautifulSoup(request.text, 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        domain = urllib.parse.urlparse(url)
        if tag.name == 'link' and tag.has_attr('href'):
            internal_reference = urllib.parse.urlparse(tag['href'])
            path = urllib.parse.urlparse(tag['href']).path
            extn = os.path.splitext(path)[1]
            if extn and not internal_reference.netloc:
                path_files = os.path.join(dir_files, created.create_name(tag['href']))
                engine.get_page(test_dir, url)
                assert True == os.path.isfile(path_files)
