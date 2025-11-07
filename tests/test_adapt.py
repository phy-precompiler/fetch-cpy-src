""" test `fetch_cpy_src/adapter.py` """
# pylint: disable=missing-function-docstring

# imports; pylint: disable=unused-import
from pathlib import Path
from pprint import pprint

import pytest

# local imports
from fetch_cpy_src.adapter import ModAbsImportAdapter, TopLevelScriptImportAdapter, AddDunderInitAdapter
from fetch_cpy_src.manifest import Manifest
from tests._common import SRC_DIR, TMP_DIR


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


@pytest.mark.skip()
def test_manifest():
    config_file = SRC_DIR / 'fetch_cpy_src/cpy312.toml'
    manifest = Manifest.load(config_file, work_dir=TMP_DIR)

    manifest.update()
