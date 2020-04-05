import pytest
import os
import tempfile
from page_loader import engine


url = 'https://greygreywolf.github.io/python-project-lvl3/'


def test_formatiopn_name():
    expected_name = 'greygreywolf-github-io-python-project-lvl3-.html'
    recieved_name = engine.formation_name(url)
    assert expected_name == recieved_name


def test_create_dir():
    with tempfile.TemporaryDirectory() as test_dir:
        file_name = engine.formation_name(url)
        dir_name = file_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        engine.get_page(test_dir, url)
        assert True == os.path.exists(resource_dir_name)


def test_create_file():
    with tempfile.TemporaryDirectory() as test_dir:
        file_name = engine.formation_name(url)
        dir_name = file_name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        full_created_path = os.path.join(resource_dir_name, file_name)
        engine.get_page(test_dir, url)
        assert True == os.path.isfile(full_created_path)
