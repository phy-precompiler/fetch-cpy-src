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
# to fetched source files. To use proper adapters, refer to the docstring of 
# submodule `fetch_cpy_src.adapter`. 
file_adapters = ['TopLevelScriptImportAdapter']
dir_adapters = ['AddDunderInitAdapter']


# This is a demo item specification for fetch sub-directory of source repo.
# `path`: path of the directory to be fetched;
# `type`: set to "dir" for fetching entire sub-directory;
[[items]]
path = 'Grammar/'
type = 'dir'
```

## Use `cli` to fetch files

```shell
Usage: fetch-cpy-src [OPTIONS] COMMAND [ARGS]...

  group all sub commands

Options:
  --help  Show this message and exit.

Commands:
  fetch         Fetch files listed in manifest to destinition directory.
  new-manifest  Create a new manifest of cpython source files to be fetched.
```
