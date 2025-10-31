# Fetch selected part of cpython source repository.

This project is part of [`phy`](https://github.com/phy-precompiler).

## Install

```shell
pip install fetch-cpy-src
```


## List the files to be fetched 

Make a manifest toml file with scheme like the following example:

```toml
# git repo tag
tag = "3.12"


# Specify items of source to fetch.

# This is a demo item specification for fetch single file of source repo.
#
# There are two REQUIRED fields:
# `path`: path of the file to be fetched;
# `type`: set to "file" for fetching single file.
[[items]]
path = 'Parser/asdl_c.py'
type = 'file'

# The `xxx_adapters` are OPTIONAL fields. Adapters will make pre-defined modification
# to fetched source files. 
#
#  + `file_adapters` will apply modification to fetch file (if type = 'file') or 
#    any files within fetched directory (if type = 'dir').
#  + `dir_adapters` will apply modification to the directory of the fetched file 
#    (if type = 'file') or the fetched directory (if type = 'dir').
# 
# In this example, 
#  + `TopLevelScriptImportAdapter` will refactor the fetched python script file to 
#    importable submodules.
#  + `AddDunderInitAdapter` will put an empty `__init__.py` at fetched directory, 
#    and thus make it a package.
file_adapters = ['TopLevelScriptImportAdapter']
dir_adapters = ['AddDunderInitAdapter']


# This is a demo item specification for fetch sub-directory of source repo.
# `path`: path of the directory to be fetched;
# `type`: set to "dir" for fetching entire sub-directory.
[[items]]
path = 'Grammar/'
type = 'dir'


```

## Fetch files 

Supposing the manifest file is `demo.toml`, fetch the files within the manifest by 
this command: 

```shell
fetch-cpy-src fetch demo.toml
```

The full manual of the `fetch-cpy-src` command:

```shell
Usage: fetch-cpy-src [OPTIONS] COMMAND [ARGS]...

  group all sub commands

Options:
  --help  Show this message and exit.

Commands:
  fetch         Fetch files listed in manifest to destinition directory.
  new-manifest  Create a new manifest of cpython source files to be fetched.
```
