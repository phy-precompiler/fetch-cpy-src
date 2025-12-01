""" cli app by `click` """
# imports
from importlib import resources
import shutil
from pathlib import Path

import typer
from rich.console import Console

# local imports
from fetch_cpy_src.manifest import Manifest


# CLI app
cli_app = typer.Typer()
console = Console()


def _copy_manifest_template(filename: str, target_dir: Path):
    """ copy manifest template file to target path """
    src = resources.files('fetch_cpy_src').joinpath('example-manifest.toml')
    target = target_dir / f'{filename}.toml'
    with resources.as_file(src) as src_path:
        shutil.copy(src_path, target)


@cli_app.command(name='new-manifest')
def cli_endpoint_new_manifest(
        filename: str = typer.Argument(
            ...,
            help='Name of the manifest file to create'
        ),
        dst: Path = typer.Option(
            Path.cwd().resolve(strict=True),
            '-d',
            '--dst',
            help='Destination directory where the new manifest file is created; if not given, the current directory is used'
        )
    ):
    """ Create a new manifest of cpython source files to be fetched. 
    
    FILENAME: name of the manifest file without extension.
    """
    # REMINDER: argument or option resolved by type `click.Path()` will be str, not pathlib.Path
    _copy_manifest_template(filename, Path(dst).resolve())


@cli_app.command(name='fetch')
def cli_endpoint_fetch(
        manifest: Path = typer.Option(
            None,
            '-m',
            '--manifest',
            help=(
                'Manifest file; if not given, the manifest of `phy` project is used'
            ),
        ),
        dst: Path = typer.Option(
            Path.cwd().resolve(strict=True),
            '-d',
            '--dst',
            help='Destination directory where fetched files will be saved; if not given, the current directory is used'
        ),
        access_token: str = typer.Option(
            None,
            '-a',
            '--access-token',
            envvar=Manifest.github_access_token_env_var,
            help='GitHub access token to avoid exceeding GitHub API rate limit'
        )
    ):
    """ Fetch files listed in manifest to destinition directory. """
    if not access_token:
        access_token = None  # type: ignore[assignment]

    with console.status('fetching ...', spinner='line'):
        if manifest is None:
            with resources.as_file(resources.files('fetch_cpy_src').joinpath('phy.toml')) as phy_manifest:
                fetched_files = Manifest.load(
                    phy_manifest, 
                    work_dir=Path(dst).resolve(),
                    github_access_token=access_token
                ).update()
        else:
            fetched_files = Manifest.load(
                Path(manifest).resolve(), 
                work_dir=Path(dst).resolve(),
                github_access_token=access_token
            ).update()
        
    for _path in fetched_files:
        print('Fetched file: ', _path)


def main():
    """ expose method entry to `pyproject.toml` script spec """
    cli_app()
