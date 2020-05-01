import logging
import tempfile
import pytest
from page_loader.filter import write_content, get_content
from page_loader.created import create_dir
from page_loader.engine import PageLoaderException


def test_exceptions():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(PageLoaderException) as excinfo:
            create_dir(
                '/greygreywolf-github-io-python-project-lvl3_files',
                 'greygreywolf-github-io-python-project-lvl3.html')
        with pytest.raises(PageLoaderException) as excinfo:
            request = get_content('https://greygreywolf.github.io/python-project-lvl3/')
            write_content(request.content, '/aaa/vvv')
        with pytest.raises(PageLoaderException) as excinfo:
            get_content('htps://greygreywolf.github.io/python-project-lvl3/')
        with pytest.raises(PageLoaderException) as excinfo:
            get_content('https:greygreywolf.github.io/python-project-lvl3/')
        with pytest.raises(PageLoaderException) as excinfo:
            get_content('https://greygreywolf.gio/python-project-lvl3/')
        with pytest.raises(PageLoaderException) as excinfo:
            requests = get_content('https://httpgreygreywolf.github.io/python-project-lvl3/')
