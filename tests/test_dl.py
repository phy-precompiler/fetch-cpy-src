# pylint: disable=missing-function-docstring,unused-import
""" test `fetch_cpy_src/downloader.py` """
# imports
import pytest

# local imports
from fetch_cpy_src.downloader import _get_cpython_repo, \
    _download_cpython_file, _download_cpython_dir
from tests._common import TEST_DIR, TMP_DIR


def get_github_access_token() -> str:
    with (TEST_DIR / 'access_token').open(encoding='utf8') as _f:
        return _f.read()


@pytest.mark.skip()
def test_dl_file():
    access_token = get_github_access_token()
    repo = _get_cpython_repo(access_token=access_token)

    test_path_list = [
        'Parser/asdl_c.py',
        'Parser/asdl.py',
        'Parser/Python.asdl',
    ]

    for test_path in test_path_list:
        _download_cpython_file(repo, test_path, '3.12', TMP_DIR)


@pytest.mark.skip()
def test_dl_dir():
    access_token = get_github_access_token()
    repo = _get_cpython_repo(access_token=access_token)

    test_path_list = [
        'Grammar/',
        'Tools/peg_generator/pegen/',
    ]

    for test_path in test_path_list:
        _download_cpython_dir(repo, test_path, '3.12', TMP_DIR)
