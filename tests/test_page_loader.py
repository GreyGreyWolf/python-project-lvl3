import pytest
import os
import tempfile
from page_loader import engine


url = 'https://greygreywolf.github.io/python-project-lvl3/'


def test_create_name_page():
    expected_name = 'greygreywolf-github-io-python-project-lvl3-.html'
    recieved_name = engine.create_name_page(url)
    assert expected_name == recieved_name


def test_create_dir_page():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = engine.create_name_page(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        engine.get_page(test_dir, url)
        assert True == os.path.exists(resource_dir_name)


def test_create_page():
    with tempfile.TemporaryDirectory() as test_dir:
        page_name = engine.create_name_page(url)
        dir_name = page_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        full_created_path = os.path.join(resource_dir_name, page_name)
        engine.get_page(test_dir, url)
        assert True == os.path.isfile(full_created_path)
