# pylint: disable=missing-function-docstring,unused-import
""" test `fetch_cpy_src/cli.py` """
# imports
from click.testing import CliRunner
import pytest

# local imports
from fetch_cpy_src.cli import cli_app


# @pytest.mark.skip()
def test_new_manifest():
    cli_runner = CliRunner()
    result = cli_runner.invoke(cli_app, ['new-manifest', '--help'])
    
    print('\n', result.output)
    assert result.exit_code == 0
