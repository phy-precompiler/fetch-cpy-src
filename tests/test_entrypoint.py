""" test this package can be found by meta package """
# pylint: disable=missing-function-docstring

# imports; pylint: disable=unused-import
import importlib.metadata
import pytest


@pytest.mark.skip()
def test_print_entrypoint_group():
    for ep in importlib.metadata.entry_points(group='phy_sub_commands'):
        print(f'name={ep.name}, value={ep.value}, module={ep.module}')
