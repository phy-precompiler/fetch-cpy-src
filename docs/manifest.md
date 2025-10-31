# Table of Contents

* [fetch\_cpy\_src.manifest](#fetch_cpy_src.manifest)
  * [ManifestItem](#fetch_cpy_src.manifest.ManifestItem)
    * [file\_adapters](#fetch_cpy_src.manifest.ManifestItem.file_adapters)
    * [dir\_adapters](#fetch_cpy_src.manifest.ManifestItem.dir_adapters)
  * [Manifest](#fetch_cpy_src.manifest.Manifest)
    * [tag](#fetch_cpy_src.manifest.Manifest.tag)
    * [work\_dir](#fetch_cpy_src.manifest.Manifest.work_dir)
    * [\_\_init\_\_](#fetch_cpy_src.manifest.Manifest.__init__)
    * [load](#fetch_cpy_src.manifest.Manifest.load)
    * [update](#fetch_cpy_src.manifest.Manifest.update)

<a id="fetch_cpy_src.manifest"></a>

# fetch\_cpy\_src.manifest

manifest to be downloaded & adapted

<a id="fetch_cpy_src.manifest.ManifestItem"></a>

## ManifestItem Objects

```python
@dataclass
class ManifestItem()
```

Item of the manifest.

Item of both type "file" & "dir" can have both `file_adapters` & `dir_adapters`.
For item of type "file", `dir_adapters` means those applied to the parent directory of
the file; for item of type "dir", `file_adapters` means those applied to the sub-file 
within the directory.

<a id="fetch_cpy_src.manifest.ManifestItem.file_adapters"></a>

#### file\_adapters

chain of adapters for file

<a id="fetch_cpy_src.manifest.ManifestItem.dir_adapters"></a>

#### dir\_adapters

chain of adapters for file

<a id="fetch_cpy_src.manifest.Manifest"></a>

## Manifest Objects

```python
class Manifest()
```

manifest of files & directories of cpython repo to be downloaded & adapted

<a id="fetch_cpy_src.manifest.Manifest.tag"></a>

#### tag

version in most cases

<a id="fetch_cpy_src.manifest.Manifest.work_dir"></a>

#### work\_dir

download & inplace-adaption directory

<a id="fetch_cpy_src.manifest.Manifest.__init__"></a>

#### \_\_init\_\_

```python
def __init__(tag: str,
             items: List[ManifestItem],
             work_dir: Path = None,
             github_access_token: str = None)
```

constructor

<a id="fetch_cpy_src.manifest.Manifest.load"></a>

#### load

```python
@classmethod
def load(cls,
         toml_file: Path,
         work_dir: Path = None,
         github_access_token: Optional[str] = None) -> 'Manifest'
```

create manifest from toml

<a id="fetch_cpy_src.manifest.Manifest.update"></a>

#### update

```python
def update() -> List[Path]
```

apply downloading & adaption, return proceeded files' path

