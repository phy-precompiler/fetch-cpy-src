""" Make adaption to downloaded files. 

The adaption should be as small as possible. Typically only absolute import 
statements should be adapted (to relative import and thus be importable). 

Although PEP-8 recommends that developer should use absolute imports as possible as 
one can, but the `_cpython` module of `phy` is purely internal used sub-module, which 
is much more sutible for relative imports.
"""
# imports
from pathlib import Path
import ast as builtin_ast
from abc import ABC, abstractmethod
from typing import List, Optional, Union


class Adapter(ABC):
    """ base class of adapter """

    @abstractmethod
    def adapt(self, src: Path, in_place: bool = True, dst: Path = None) -> Optional[Path]:
        """ protocol abstract method """
        raise NotImplementedError


class ModAbsImportAdapter(Adapter, builtin_ast.NodeVisitor):
    """ The module that copied to `phy` project should to adapted to relative imports, which 
    ensure this module can be imported by `phy` components correctly. 
    
    Only flat structured module (non-nested one) is supported.
    """

    # instance attributes
    match_mod_name: str
    _abs_from_import_nodes: List[builtin_ast.ImportFrom]

    def __init__(self):
        """ constructor """
        super().__init__()

        self.match_mod_name = None
        self._abs_from_import_nodes = []

    def visit_ImportFrom(self, node: builtin_ast.ImportFrom):
        """ visit `ImportFrom` ast node """
        # find import statements like:
        #    + from <match_mod> import xxx
        #    + from <match_mod>.yyy import xxx
        # 
        # DO NOT filter by `.startswith(match_mod)`, for the module name may be 
        # coincidentally other string prefixed with `match_mod`
        if node.level == 0 and node.module and node.module.split('.')[0] == self.match_mod_name:
            self._abs_from_import_nodes.append(node)

        self.generic_visit(node)

    def adapt(self, src: Path, in_place: bool = True, dst: Path = None) -> Optional[Path]:
        """ Adapt source file.

        If `inplace=True`, the source file would be overwritten; or saved to another 
        path of `dst file`. 
        """
        assert src.suffix == '.py'

        # get match module names
        self.match_mod_name = src.parent.stem

        # clean
        self._abs_from_import_nodes = []

        # Parse code to ast node; the source file downloaded from cpython repository is 
        # guaranteed to be 'utf-8' encoding.
        with src.open('r', encoding='utf8') as _f:
            src_code = _f.read()
            ast_root = builtin_ast.parse(src_code, filename=str(src))
        
        # visit nodes and extract absolute imports with given name
        self.visit(ast_root)

        # iterate over concerned nodes
        code_lines = src_code.splitlines()
        trans_node: builtin_ast.ImportFrom = None

        for node in self._abs_from_import_nodes:
            # transfer "from <match_mod> import xxx" to "from . import xxx"
            if node.module == self.match_mod_name:
                node.module = None

            # transfer "from <match_mod>.yyy import xxx" to "from .yyy import xxx"
            else:
                node.module = '.'.join(node.module.split('.')[1:])
                print('Visted `ImportForm` ast which is of module: ', node.module)

            node.level = 1
            trans_node = node

            # locate original source position
            start_line = node.lineno - 1
            end_line = getattr(node, 'end_lineno', node.lineno) - 1

            # adapted code for this node
            new_code = builtin_ast.unparse(trans_node)

            # replace only the extracted nodes
            if start_line == end_line:  # single line
                # import node always occupy the entire line, no need to involving
                # the offset
                code_lines[start_line] = new_code

            else:  # multi line
                # try not to affect other lines by appending empty lines of the same number
                ln_count = end_line + 1 - start_line
                code_lines[start_line: end_line + 1] = [new_code] + [''] * (ln_count - 1)

        # write adapted code
        if in_place:
            dst = src

        assert dst is not None
        with dst.open('w', encoding='utf8') as _f:
            _f.writelines([
                line + '\n' if not line.endswith('\n') else line 
                for line in code_lines
            ])

        return dst


class TopLevelScriptImportAdapter(Adapter, builtin_ast.NodeVisitor):
    """ Some ".py" file does not belong to module, and it imports same level file module or package 
    via absolute import. 
    
    To adapt such script to be usable in `phy` project, firstly make the script folder a module by
    adding `__init__.py` file, and then change the absolute import statements to relative ones. """

    # instance attributes
    _importable_names: List[str]
    _abs_import_nodes: List[Union[builtin_ast.Import, builtin_ast.ImportFrom]]

    def __init__(self):
        """ constructor """
        super().__init__()

        self._importable_names = []
        self._abs_import_nodes = []

    def visit_Import(self, node: builtin_ast.Import):
        """ visit `Import` ast node """
        # find import statements like
        #    + import <importable_name>
        #    + import <importable_name>.xxx, <importable_name>.yyy
        # 
        # Some rare cases (like "import <importable_name>.xxx, zzz", which is surely of bad practice) 
        # are ignored.
        first_imported_name_head = node.names[0].name.split('.')[0]

        if first_imported_name_head in self._importable_names:
            if all(_alias.name.split('.')[0] == first_imported_name_head for _alias in node.names):
                self._abs_import_nodes.append(node)

        self.generic_visit(node)

    def visit_ImportFrom(self, node: builtin_ast.ImportFrom):
        """ visit `ImportFrom` ast node """
        # find import statements like:
        #    + from <importable_name> import xxx
        #    + from <importable_name>.yyy import xxx

        if node.level == 0 and node.module and node.module.split('.')[0] in self._importable_names:
            self._abs_import_nodes.append(node)

        self.generic_visit(node)

    def adapt(self, src: Path, in_place: bool = True, dst: Path = None) -> Optional[Path]:
        """ Adapt source file.

        If `inplace=True`, the source file would be overwritten; or saved to another 
        path of `dst file`. 
        """
        assert src.suffix == '.py'

        # get importable names; skip checking whether folder is a package.
        script_dir = src.parent.resolve()

        # clean
        self._importable_names = []
        self._abs_import_nodes = []

        for _path in script_dir.iterdir():
            self._importable_names.append(_path.stem)

        # Parse code to ast node; the source file downloaded from cpython repository is 
        # guaranteed to be 'utf-8' encoding.
        with src.open('r', encoding='utf8') as _f:
            src_code = _f.read()
            ast_root = builtin_ast.parse(src_code, filename=str(src))
        
        # visit nodes and extract absolute imports with given name
        self.visit(ast_root)

        # iterate over concerned nodes
        code_lines = src_code.splitlines()
        trans_node: builtin_ast.ImportFrom = None

        for node in self._abs_import_nodes:

            # from ... import ...
            if isinstance(node, builtin_ast.ImportFrom):

                # transfer "from <importable_name> import xxx" to 
                # "from .<importable_name> import xxx";
                # transfer "from <importable_name>.yyy import xxx" to
                # "from .<importable_name>.yyy import xxx"
                node.module = '.' + node.module

                node.level = 1
                trans_node = node

            # import ...
            elif isinstance(node, builtin_ast.Import):

                # transfer "import <importable_name>" to "from . import <importable_name>"
                first_imported_name = node.names[0].name
                if len(node.names) == 1 and '.' not in first_imported_name:
                    trans_node = builtin_ast.ImportFrom(
                        module=None,
                        names=[builtin_ast.alias(first_imported_name)],
                        level=1
                    )

                # transfer "import <importable_name>.xxx, <match_moimportable_named>.yyy" to 
                # "from .<importable_name> import xxx, yyy"
                else:
                    first_imported_name_head = node.names[0].name.split('.')[0]

                    trans_node = builtin_ast.ImportFrom(
                        module=first_imported_name_head,
                        names=[builtin_ast.alias(
                            name='.'.join(_alias.name.split('.')[1:])
                        ) for _alias in node.names],
                        level=1
                    )
            else:
                raise TypeError  # never throws

            # locate original source position
            start_line = node.lineno - 1
            end_line = getattr(node, 'end_lineno', node.lineno) - 1

            # adapted code for this node
            new_code = builtin_ast.unparse(trans_node)

            # replace only the extracted nodes
            if start_line == end_line:  # single line
                # import node always occupy the entire line, no need to involving
                # the offset
                code_lines[start_line] = new_code

            else:  # multi line
                # try not to affect other lines by appending empty lines of the same number
                ln_count = end_line + 1 - start_line
                code_lines[start_line: end_line + 1] = [new_code] + [''] * (ln_count - 1)

        # write adapted code
        if in_place:
            dst = src

        assert dst is not None
        with dst.open('w', encoding='utf8') as _f:
            _f.writelines([
                line + '\n' if not line.endswith('\n') else line 
                for line in code_lines
            ])

        return dst


class AddDunderInitAdapter(Adapter):
    """ add an empty "__init__.py" to directory to make it a package """

    def adapt(self, src: Path, in_place: bool = True, dst: Path = None) -> Optional[Path]:
        # validate
        assert src.is_dir()
        
        # write adapted code
        if in_place:
            dst = src

        dst.mkdir(parents=True, exist_ok=True)
        dst_file = (dst / '__init__.py').resolve()
        dst_file.touch(exist_ok=True)
