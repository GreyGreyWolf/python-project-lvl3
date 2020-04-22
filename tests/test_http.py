import logging
import tempfile
import tempfile
import pytest
from page_loader import engine, filter, created
from page_loader.script import pageloader


def test_exception():
    test_dir = tempfile.TemporaryDirectory()
    name_dir = test_dir.name
    with pytest.raises(pageloader.PageLoaderException) as excinfo:
        engine.get_page(name_dir, 'hps://greygreywolf.github.io/python-project-lvl3/')
    with pytest.raises(pageloader.PageLoaderException) as excinfo:
        engine.get_page(name_dir, 'https://greygreywolf.giub.io/python-project-lvl3/')
    with pytest.raises(pageloader.PageLoaderException):
        engine.get_page('/', 'htps://greygreywolf.github.io/python-project-lvl3/')
    with pytest.raises(pageloader.PageLoaderException) as excinfo:
        engine.get_page(name_dir + '/bag', 'htps://greygreywolf.github.io/python-project-lvl3/')    