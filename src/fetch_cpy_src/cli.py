""" cli app by `click` """
# imports
from importlib import resources
import shutil
from pathlib import Path
import click

# local imports
from fetch_cpy_src.manifest import Manifest


@click.group()
def cli_app():
    """ group all sub commands """
    pass


def _copy_manifest_template(filename: str, target_dir: Path):
    """ copy manifest template file to target path """
    src = resources.files('fetch_cpy_src').joinpath('example-manifest.toml')
    target = target_dir / f'{filename}.toml'
    with resources.as_file(src) as src_path:
        shutil.copy(src_path, target)


@cli_app.command(name='new-manifest')
@click.argument(
    'filename', 
    type=click.STRING, 
    help='name of the manifest file without extension'
)
@click.option(
    '-d', 
    '--dst', 
    type=click.Path, 
    default=Path.cwd().resolve(strict=True), 
    help='destinition directory that the new manifest file created in'
)
def cli_endpoint_new_manifest(filename: str, dst: Path):
    """ Create a new manifest of cpython source files to be fetched, at current path. """
    _copy_manifest_template(filename, dst)


@cli_app.command(name='fetch')
@click.option(
    '-m', 
    '--manifest', 
    type=click.Path, 
    default=resources.as_file(resources.files('fetch_cpy_src').joinpath('phy.toml')),
    help='manifest file'
)
@click.option(
    '-d', 
    '--dst', 
    type=click.Path, 
    default=Path.cwd().resolve(strict=True), 
    help='destinition directory that fetched files to be saved in'
)
def cli_endpoint_fetch(manifest: Path, dst: Path):
    """ Create a new manifest of cpython source files to be fetched, at current path. """
    fetched_files = Manifest.load(manifest, work_dir=dst).update()
    for _path in fetched_files:
        print('Fetched file: ', _path)
