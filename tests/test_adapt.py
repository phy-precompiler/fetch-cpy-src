# pylint: disable=missing-function-docstring
""" test `phy_cpydeps_update/_adapter.py` """
# imports
from pathlib import Path
from pprint import pprint

import pytest

# local imports
from phy_cpydeps_update.adapter import ModAbsImportAdapter, \
    TopLevelScriptImportAdapter, AddDunderInitAdapter
from phy_cpydeps_update.manifest import Manifest


# constants
TEST_DIR = Path(__file__).resolve().parent
BASE_DIR = TEST_DIR.parent
SRC_DIR = BASE_DIR / 'src'
TMP_DIR = BASE_DIR / 'tmp'


@pytest.mark.skip()
def test_mod_adapt():
    adapter = ModAbsImportAdapter()
    src_file = TMP_DIR / 'Tools/peg_generator/pegen/python_generator.py'

    adapter.adapt(src_file, in_place=False, dst_file=TMP_DIR / 'python_generator_x.py')


@pytest.mark.skip()
def test_script_adapt():
    adapter = TopLevelScriptImportAdapter()
    src_file = TMP_DIR / 'Parser/asdl_c.py'

    adapter.adapt(src_file, in_place=False, dst_file=TMP_DIR / 'asdl_c.py')


@pytest.mark.skip()
def test_add_init_adapt():
    adapter = AddDunderInitAdapter()
    src_file = TMP_DIR / 'Parser/'

    adapter.adapt(src_file, in_place=True)


# @pytest.mark.skip()
def test_manifest():
    config_file = SRC_DIR / 'phy_cpydeps_update/cpy312.toml'
    manifest = Manifest.load(config_file, work_dir=TMP_DIR)

    manifest.update()
