import tempfile
import pytest
from page_loader import getter
from page_loader import prepare
from page_loader.engine import PageLoaderException


def test_exceptions():
    with tempfile.TemporaryDirectory() as tmpdir:
        with pytest.raises(PageLoaderException):
            prepare.prepare_directory(
                '/python-poetry.org_files',
                 'python-poetry.org.html')
        with pytest.raises(PageLoaderException):
            request = getter.get_content('https://python-poetry.org')
            getter.get_file(request.content, '/aaa/vvv')
        with pytest.raises(PageLoaderException):
            getter.get_content('htps://python-poetry.org')
        with pytest.raises(PageLoaderException):
            getter.get_content('https:python-poetry.org')
        with pytest.raises(PageLoaderException):
            getter.get_content('https://httpbin.org/status/400')
        with pytest.raises(PageLoaderException):
            getter.get_content('https://httpbin.org/status/403')
        with pytest.raises(PageLoaderException):
            getter.get_content('https://httpbin.org/status/404')
        with pytest.raises(PageLoaderException):
            getter.get_content('https://httpbin.org/status/410')
        with pytest.raises(PageLoaderException):
            getter.get_content('https://httpbin.org/status/500')
        with pytest.raises(PageLoaderException):
            requests = getter.get_content('https://httpbin.org/status/503')
