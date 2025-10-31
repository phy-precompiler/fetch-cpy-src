""" cli app by `click` """
# imports
from importlib import resources
import shutil
from pathlib import Path
import click

# constants



@click.group()
def cli_app():
    """ group all sub commands """
    pass


def _copy_manifest_template(filename: str, target_dir: Path):
    """ copy manifest template file to target path """
    src = resources.files('fetch_cpy_src').joinpath('example-manifest.toml')
    print('>>>>>>>>>>>>', src)
    target = target_dir / f'{filename}.toml'
    with resources.as_file(src) as src_path:
        shutil.copy(src_path, target)


@cli_app.command(name='new-manifest')
@click.argument('filename')
def cli_endpoint_new_manifest(filename: str):
    """ Create a new manifest of cpython source files to be fetched, at current path. """
    target_dir = Path.cwd().resolve(strict=True)
    _copy_manifest_template(filename, target_dir)
