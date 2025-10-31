# Table of Contents

* [fetch\_cpy\_src.adapter](#fetch_cpy_src.adapter)
  * [FileAdapter](#fetch_cpy_src.adapter.FileAdapter)
    * [adapt](#fetch_cpy_src.adapter.FileAdapter.adapt)
  * [DirAdapter](#fetch_cpy_src.adapter.DirAdapter)
    * [adapt](#fetch_cpy_src.adapter.DirAdapter.adapt)
  * [ModAbsImportAdapter](#fetch_cpy_src.adapter.ModAbsImportAdapter)
    * [\_\_init\_\_](#fetch_cpy_src.adapter.ModAbsImportAdapter.__init__)
    * [visit\_ImportFrom](#fetch_cpy_src.adapter.ModAbsImportAdapter.visit_ImportFrom)
    * [adapt](#fetch_cpy_src.adapter.ModAbsImportAdapter.adapt)
  * [TopLevelScriptImportAdapter](#fetch_cpy_src.adapter.TopLevelScriptImportAdapter)
    * [\_\_init\_\_](#fetch_cpy_src.adapter.TopLevelScriptImportAdapter.__init__)
    * [visit\_Import](#fetch_cpy_src.adapter.TopLevelScriptImportAdapter.visit_Import)
    * [visit\_ImportFrom](#fetch_cpy_src.adapter.TopLevelScriptImportAdapter.visit_ImportFrom)
    * [adapt](#fetch_cpy_src.adapter.TopLevelScriptImportAdapter.adapt)
  * [AddDunderInitAdapter](#fetch_cpy_src.adapter.AddDunderInitAdapter)

<a id="fetch_cpy_src.adapter"></a>

# fetch\_cpy\_src.adapter

Make adaption to downloaded files.

The adaption should be as small as possible. Typically only absolute import 
statements should be adapted (to relative import and thus be importable). 

Although PEP-8 recommends that developer should use absolute imports as possible as 
one can, but the `_cpython` module of `phy` is purely internal used sub-module, which 
is much more sutible for relative imports.

<a id="fetch_cpy_src.adapter.FileAdapter"></a>

## FileAdapter Objects

```python
class FileAdapter(ABC)
```

base class of file adapter

<a id="fetch_cpy_src.adapter.FileAdapter.adapt"></a>

#### adapt

```python
@abstractmethod
def adapt(src_file: Path,
          in_place: bool = True,
          dst_file: Path = None) -> Optional[Path]
```

apply adaption to file

<a id="fetch_cpy_src.adapter.DirAdapter"></a>

## DirAdapter Objects

```python
class DirAdapter(ABC)
```

base class of directory adapter

<a id="fetch_cpy_src.adapter.DirAdapter.adapt"></a>

#### adapt

```python
@abstractmethod
def adapt(src_dir: Path,
          in_place: bool = True,
          dst_dir: Path = None) -> Optional[Path]
```

apply adaption to directory

<a id="fetch_cpy_src.adapter.ModAbsImportAdapter"></a>

## ModAbsImportAdapter Objects

```python
class ModAbsImportAdapter(FileAdapter, builtin_ast.NodeVisitor)
```

The module that copied to `phy` project should to adapted to relative imports, which
ensure this module can be imported by `phy` components correctly. 

Only flat structured module (non-nested one) is supported.

<a id="fetch_cpy_src.adapter.ModAbsImportAdapter.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

constructor

<a id="fetch_cpy_src.adapter.ModAbsImportAdapter.visit_ImportFrom"></a>

#### visit\_ImportFrom

```python
def visit_ImportFrom(node: builtin_ast.ImportFrom)
```

visit `ImportFrom` ast node

<a id="fetch_cpy_src.adapter.ModAbsImportAdapter.adapt"></a>

#### adapt

```python
def adapt(src_file: Path,
          in_place: bool = True,
          dst_file: Path = None) -> Optional[Path]
```

Adapt source file.

If `inplace=True`, the source file would be overwritten; or saved to another 
path of `dst file`.

<a id="fetch_cpy_src.adapter.TopLevelScriptImportAdapter"></a>

## TopLevelScriptImportAdapter Objects

```python
class TopLevelScriptImportAdapter(FileAdapter, builtin_ast.NodeVisitor)
```

Some ".py" file does not belong to module, and it imports same level file module or package
via absolute import. 

To adapt such script to be usable in `phy` project, firstly make the script folder a module by
adding `__init__.py` file, and then change the absolute import statements to relative ones. 

BE CAREFUL!!! This adapter should be applied after all sibling scripts downloaded, in order to 
get all importable symbols.

<a id="fetch_cpy_src.adapter.TopLevelScriptImportAdapter.__init__"></a>

#### \_\_init\_\_

```python
def __init__()
```

constructor

<a id="fetch_cpy_src.adapter.TopLevelScriptImportAdapter.visit_Import"></a>

#### visit\_Import

```python
def visit_Import(node: builtin_ast.Import)
```

visit `Import` ast node

<a id="fetch_cpy_src.adapter.TopLevelScriptImportAdapter.visit_ImportFrom"></a>

#### visit\_ImportFrom

```python
def visit_ImportFrom(node: builtin_ast.ImportFrom)
```

visit `ImportFrom` ast node

<a id="fetch_cpy_src.adapter.TopLevelScriptImportAdapter.adapt"></a>

#### adapt

```python
def adapt(src_file: Path,
          in_place: bool = True,
          dst_file: Path = None) -> Optional[Path]
```

Adapt source file.

If `inplace=True`, the source file would be overwritten; or saved to another 
path of `dst file`.

<a id="fetch_cpy_src.adapter.AddDunderInitAdapter"></a>

## AddDunderInitAdapter Objects

```python
class AddDunderInitAdapter(DirAdapter)
```

add an empty "__init__.py" to directory to make it a package

