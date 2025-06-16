""" manifest to be downloaded & adapted """
# imports
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, List

import tomli  # builtin `tomlib` is available until 3.11
from github import Repository

# local imports
from phy_cpydeps_update.downloader import _get_cpython_repo, _download_cpython_file, _download_cpython_dir
from phy_cpydeps_update import adapter


@dataclass
class ManifestItem:
    """ item of the manifest """
    path: str
    type: Literal['file', 'dir']
    adapters: List[adapter.Adapter]  # chain of adapters for file
    dir_adapters: List[adapter.Adapter]  # chain of adapters for file


def _inst_adapter(subcls_name: str) -> adapter.Adapter:
    """ instantiante a subclass of `Adapter` by its name """
    return getattr(adapter, subcls_name)()


class Manifest:
    """ manifest of files & directories of cpython repo to be downloaded & adapted """

    # instance attributes
    _cpy_repo: Repository

    tag: str  # version in most cases
    items: List[ManifestItem]
    work_dir: Path  # download & inplace-adaption directory 

    def __init__(
        self, 
        tag: str, 
        items: List[ManifestItem], 
        work_dir: Path = None, 
        github_access_token: str = None
    ):
        """ constructor """
        self.tag = tag
        self.items = items
        self.work_dir = (work_dir if work_dir else Path.cwd()).resolve()

        # read `github_access_token` from env
        self._cpy_repo = _get_cpython_repo(access_token=github_access_token)

    @classmethod
    def load(cls, toml_file: Path, work_dir: Path = None) -> 'Manifest':
        """ create manifest from toml """
        # read toml file
        toml_file = toml_file.resolve()
        with toml_file.open('rb') as _f:
            toml_dict = tomli.load(_f)

        items = []
        for _item_dict in toml_dict['items']:
            item = ManifestItem(
                path=_item_dict['path'],
                type=_item_dict['type'],
                adapters=[_inst_adapter(_adapter_name) for 
                          _adapter_name in _item_dict.get('adapters', list())],
                dir_adapters=[_inst_adapter(_adapter_name) for 
                              _adapter_name in _item_dict.get('dir_adapters', list())],
            )
            items.append(item)

        # read env for access token
        github_access_token = os.getenv('github_access_token', None)

        return cls(
            tag=toml_dict['tag'],
            items=items,
            work_dir=work_dir,
            github_access_token=github_access_token
        )


    def update(self) -> List[Path]:
        """ perform downloading & adaption, return proceeded files' path """
        updated_list: List[Path] = []

        # DO NOT merge downloading & adapting loop! For some adatption need work correctly when related 
        # downloading completed (like top-level-script adaption). Besides, the developer can test adaption
        # alone without downloadnig.

        # download
        for _item in self.items:
            # for file
            if _item.type == 'file':
                _download_cpython_file(self._cpy_repo, _item.path, self.tag, self.work_dir)

            elif _item.type == 'dir':
                _download_cpython_dir(self._cpy_repo, _item.path, self.tag, self.work_dir)

        # adaption
        for _item in self.items:

            # for file
            if _item.type == 'file':
                target_file = (self.work_dir / _item.path).resolve()
                target_dir = target_file.parent

                for _dir_adapter in _item.dir_adapters:
                    _dir_adapter.adapt(target_dir, in_place=True, dst=target_dir)

                for _adapter in _item.adapters:
                    print(f'Perform adapter {_adapter.__class__.__name__} to {target_file}')

                    _adapter.adapt(target_file, in_place=True, dst=target_file)
                    updated_list.append(target_file)

            # for directory
            elif _item.type == 'dir':
                target_dir = (self.work_dir / _item.path).resolve()
                
                for _dir_adapter in _item.dir_adapters:
                    _dir_adapter.adapt(target_dir, in_place=True, dst=target_dir)

                for _sub_dir, _folders, _files in os.walk(target_dir.resolve()):
                    _ = _folders
                    sub_dir = Path(_sub_dir)

                    for _file_name in _files:
                        target_file = sub_dir / _file_name

                        for _adapter in _item.adapters:
                            _adapter.adapt(target_file, in_place=True, dst=target_file)
                            updated_list.append(target_file)

        return updated_list
