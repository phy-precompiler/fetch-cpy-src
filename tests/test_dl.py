# pylint: disable=missing-function-docstring
""" test `phy_cpydeps_update/_downloader.py` """
# imports
from pathlib import Path
from pprint import pprint

import pytest

# local imports
from phy_cpydeps_update._downloader import _download_cpython_file


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
TMP_DIR = BASE_DIR / 'tmp'


def test_dl():
    test_path_list = [
        'Parser/asdl_c.py'
    ]

    for test_path in test_path_list:
        _download_cpython_file(test_path, '3.12', TMP_DIR)
