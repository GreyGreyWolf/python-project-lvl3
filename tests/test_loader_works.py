import pytest
import urllib
import bs4
import os
import re
import tempfile
import logging
from page_loader import getter, prepare, engine, cli


current_doc = ['<link class="main-stylesheet" href="/css/global.min.css" rel="stylesheet" type="text/css" />',
                '<link class="main-stylesheet" href="/css/icons.min.css" rel="stylesheet" type="text/css" />',
                 '<link class="main-stylesheet" href="/css/fonts.css" rel="stylesheet" type="text/css" />',
                  '<link class="main-stylesheet" href="/css/main.css" rel="stylesheet" type="text/css" />']


def test_normalize_name():
    current_names = ['https://greygreywolf.github.io/python-project-lvl3/',
                      'https://python-poetry.org',
                       '/name/name']
    expected_names = ['https---greygreywolf-github-io-python-project-lvl3',
                       'https---python-poetry-org',
                        'name-name']
    for elem in current_names:
        received_name = prepare.normalize_name(elem)
        status = received_name  in expected_names
        assert status == True


def test_get_valid_name():
    current_names = ['https://greygreywolf.io/python-project-lvl3/',
                      'www.python-poetry.org',
                       '/python-project-lvl3/assets/css/style.css?v=82b94381e']
    expected_names = ['greygreywolf-io-python-project-lvl3.html',
                       'www-python-poetry.org',
                        'python-project-lvl3-assets-css-style.css']
    for elem in current_names:
        received_name = prepare.get_valid_name(elem)
        status = received_name in expected_names
        assert status == True


def test_prepare_directory():
    expected_name_page_directory = 'test'
    expected_name_files_directory = 'test_files'
    with tempfile.TemporaryDirectory() as test_dir:
        path_page, files_directory = prepare.prepare_directory(test_dir, 'test.html')
        page_directory = os.path.dirname(path_page)
        name_page_directory = os.path.basename(page_directory)
        name_files_directory = os.path.basename(files_directory)
        status_page_directory = os.path.exists(page_directory)
        status_path_files = os.path.exists(files_directory)
        assert status_page_directory == True
        assert status_path_files == True
        assert name_page_directory == expected_name_page_directory
        assert name_files_directory == expected_name_files_directory


def test_get_tag():
    expected_number_resources = len(current_doc)
    receivde_resources = {}
    soup = bs4.BeautifulSoup(''.join(current_doc), 'lxml')
    for tag in soup.find_all({'link': True, 'img': True, 'script': True}):
        receivde_resources.update(getter.get_tag(tag, './test_dir', 'https://mypage.org'))
    print(receivde_resources)
    assert len(receivde_resources)  == expected_number_resources


def test_replace_url():
    received_resources = {}
    expected_doc = ['<link class="main-stylesheet" href="./test_dir/css-global-min.css" rel="stylesheet" type="text/css" />',
            '<link class="main-stylesheet" href="./test_dir/css-icons-min.css" rel="stylesheet" type="text/css" />',
             '<link class="main-stylesheet" href="./test_dir/css-fonts.css" rel="stylesheet" type="text/css" />',
              '<link class="main-stylesheet" href="./test_dir/css-main.css" rel="stylesheet" type="text/css" />']
    expected_soup = bs4.BeautifulSoup(''.join(expected_doc), 'lxml')
    expected_page = expected_soup.prettify()
    received_soup = bs4.BeautifulSoup(''.join(current_doc), 'lxml')
    for tag in received_soup.find_all({'link': True, 'img': True, 'script': True}):
        received_resources.update(getter.get_tag(tag, './test_dir/', 'https://mypage.org'))
    received_page = received_soup.prettify()
    assert received_page == expected_page


def test_init_argparser():
    assert cli.qualifier('debug') == logging.DEBUG
    assert cli.qualifier('info') == logging.INFO
    assert cli.qualifier('error') == logging.ERROR
    assert cli.qualifier('warning') == logging.WARNING
    assert cli.qualifier('critical') == logging.CRITICAL
