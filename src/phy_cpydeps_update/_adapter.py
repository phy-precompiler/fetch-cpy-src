""" Make adaption to downloaded files. 

The adaption should be as small as possible. Typically only absolute import 
statements should be adapted (to relative import and thus be importable).
"""
# imports
from pathlib import Path
import ast as builtin_ast
from typing import List



class AbsFromImportAdapter(builtin_ast.NodeVisitor):
    """ Change absolute import-from statements of given module name 
    to relative import. """

    # instance attributes
    match_mod: str
    _abs_importfrom_nodes: List[builtin_ast.ImportFrom]

    def __init__(self, match_mod_name: str):
        """ constructor """
        super().__init__()

        self.match_mod = match_mod_name
        self._abs_importfrom_nodes = []

    def visit_ImportFrom(self, node):
        """ override `visit_ImportFrom` method """
        node: builtin_ast.ImportFrom

        # DO NOT filter by `.startswith(match_mod)`, for the module name may be 
        # coincidentally other string prefixed with `match_mod`
        if node.level == 0 and node.module and node.module.split('.')[0] == self.match_mod:
            self._abs_importfrom_nodes.append(node)

        self.generic_visit(node)

    def adapt(self, src_file: Path, in_place: bool = True, dst_file: Path = None):
        """ Adapt source file.

        If `inplace=True`, the source file would be overwritten; or saved to another 
        path of `dst file`. 
        """
        assert src_file.suffix == '.py'

        # Parse code to ast node; the source file downloaded from cpython repository is 
        # guaranteed to be 'utf-8' encoding.
        with src_file.open('r', encoding='utf8') as _f:
            src_code = _f.read()
            ast_root = builtin_ast.parse(src_code, filename=str(src_file))
        
        # visit nodes and extract absolute imports with given name
        self.visit(ast_root)

        # iterate over concerned nodes
        code_lines = src_code.splitlines()

        for node in self._abs_importfrom_nodes:
            if node.module == self.match_mod:
                node.module = None
            else:
                node.module = '.'.join(node.module.split('.')[1:])
                print('*******************', node.module)

            node.level = 1

            # locate original source position
            start_line = node.lineno - 1
            end_line = getattr(node, 'end_lineno', node.lineno) - 1

            # adapted code for this node
            new_code = builtin_ast.unparse(node)

            # replace only the extracted nodes
            if start_line == end_line:  # single line
                # import node always occupy the entire line, no need to involving
                # the offset
                code_lines[start_line] = new_code

            else:  # multi line
                # try not to affect other lines by appending same-number empty lines
                ln_count = end_line + 1 - start_line
                code_lines[start_line: end_line + 1] = [new_code] + [''] * (ln_count - 1)

        # write adapted code
        if in_place:
            dst_file = src_file

        assert dst_file is not None
        with dst_file.open('w', encoding='utf8') as _f:
            _f.writelines([
                line + '\n' if not line.endswith('\n') else line 
                for line in code_lines
            ])
