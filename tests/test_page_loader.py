import pytest
import os
import tempfile
from page_loader import engine

url = 'https://greygreywolf.github.io/python-project-lvl3/'
expected_file = './tests/fixtures/greygreywolf-github-io-python-project-lvl3-.html'


def read(file):
    with open(file, 'r', encoding="utf-8") as input_file:
        answer = input_file.read()
    return answer


def test_get_page1():
    with tempfile.TemporaryDirectory() as test_dir:
        name = engine.formation_name(url)
        dir_name = name[:-5]
        resource_dir_name = os.path.join(test_dir, dir_name)
        full_path = os.path.join(resource_dir_name, name)
        engine.get_page(test_dir, url) 
        assert read(full_path) == read(expected_file)


# def test_get_page():
#     with tempfile.TemporaryDirectory() as test_dir:
#         name = engine.formation_name(url)
#         dir_name = name[:-5]
#         resource_dir_name = os.path.join(test_dir, dir_name)
#         full_path = os.path.join(resource_dir_name, name)
#         engine.get_page(test_dir, url)
#         with open(full_path) as file1, open(expected_file) as file2:
#             for file1Line, file2Line in zip(file1, file2):
#                 assert file1Line == file2Line


def test_name_correct():
    expected_name = 'greygreywolf-github-io-python-project-lvl3-.html'
    recieved_name = engine.formation_name(url)
    assert expected_name == recieved_name
