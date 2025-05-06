# pylint: disable=missing-function-docstring
""" test `phy_cpydeps_update/_downloader.py` """
# imports
from pathlib import Path
from pprint import pprint

import pytest

# local imports
from phy_cpydeps_update._downloader import _download_cpython_file, _download_cpython_dir


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
TMP_DIR = BASE_DIR / 'tmp'


@pytest.mark.skip()
def test_dl_file():
    test_path_list = [
        'Parser/asdl_c.py'
    ]

    for test_path in test_path_list:
        _download_cpython_file(test_path, '3.12', TMP_DIR)


def test_dl_dir():
    test_path_list = [
        'Tools/peg_generator'
    ]

    for test_path in test_path_list:
        _download_cpython_dir(test_path, '3.12', TMP_DIR)
