import logging
import tempfile
import pytest
from page_loader import engine, filter, created, logger


def test_exception():
    test_dir = tempfile.TemporaryDirectory()
    name_dir = test_dir.name
    with pytest.raises(logger.PageLoaderException) as excinfo:
        engine.get_page(name_dir, 'htps://greygreywolf.github.io/python-project-lvl3')
    with pytest.raises(logger.PageLoaderException) as excinfo:
        engine.get_page(name_dir, 'https://greygreywolf.giub.io/python-project-lvl3')
    with pytest.raises(logger.PageLoaderException) as excinfo:
        engine.get_page(name_dir + '/bag', 'https://greygreywolf.github.io/python-project-lvl3')
