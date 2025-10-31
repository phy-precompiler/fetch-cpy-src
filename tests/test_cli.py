# pylint: disable=missing-function-docstring,unused-import
""" test `fetch_cpy_src/cli.py` """
# imports
from click.testing import CliRunner
import pytest

# local imports
from fetch_cpy_src.cli import cli_app, _copy_manifest_template
from tests._common import TMP_DIR


@pytest.mark.skip()
def test_copy_manifest_template():
    _copy_manifest_template('demo', TMP_DIR)


@pytest.mark.skip()
def test_new_manifest():
    cli_runner = CliRunner()
    result = cli_runner.invoke(cli_app, ['new-manifest', 'demo'])
    
    print('\n', result.output)
    assert result.exit_code == 0
