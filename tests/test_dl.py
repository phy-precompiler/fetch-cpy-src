# pylint: disable=missing-function-docstring
""" test `phy_cpydeps_update/_downloader.py` """
# imports
from pathlib import Path
from pprint import pprint

import pytest

# local imports
from phy_cpydeps_update._downloader import _get_github_repo, \
    _download_cpython_file, _download_cpython_dir


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
TMP_DIR = BASE_DIR / 'tmp'


def get_github_access_token() -> str:
    with (TEST_DIR / 'access_token').open(encoding='utf8') as _f:
        return _f.read()


@pytest.mark.skip()
def test_dl_file():
    access_token = get_github_access_token()
    repo = _get_github_repo(access_token=access_token)

    test_path_list = [
        'Parser/asdl_c.py'
    ]

    for test_path in test_path_list:
        _download_cpython_file(repo, test_path, '3.12', TMP_DIR)


def test_dl_dir():
    access_token = get_github_access_token()
    repo = _get_github_repo(access_token=access_token)

    test_path_list = [
        'Grammar'
    ]

    for test_path in test_path_list:
        _download_cpython_dir(repo, test_path, '3.12', TMP_DIR)
