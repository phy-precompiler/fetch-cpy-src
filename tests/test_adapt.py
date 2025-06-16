# pylint: disable=missing-function-docstring
""" test `phy_cpydeps_update/_adapter.py` """
# imports
from pathlib import Path
from pprint import pprint

import pytest

# local imports
from phy_cpydeps_update.adapter import AbsoluteImportFromAdapter


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
TMP_DIR = BASE_DIR / 'tmp'


@pytest.mark.skip()
def test_adapt():
    adaptor = AbsoluteImportFromAdapter('pegen')
    src_file = TMP_DIR / 'Tools/peg_generator/pegen/python_generator.py'

    adaptor.adapt(src_file, in_place=False, dst=TMP_DIR / 'python_generator_x.py')
