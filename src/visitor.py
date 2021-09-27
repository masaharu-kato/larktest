"""
    Definition of Visitor class
"""

from dataclasses import dataclass
from typing import Any, Dict, List

PDFObj = Any
PDFDict = Dict[bytes, PDFObj]

class Visitor():
    def __default__(self, tree, env):
        raise

    def program(self, tree, env):
        return self.visit(tree.children[0].value, env)

    def comment(self, tree, env):
        return PDFComment(bytes(tree.children[0].value))

    def obj_int(self, tree, env):
        return int(tree.children[0].value)

    def obj_real(self, tree, env):
        return float(tree.children[0].value)
    
    def obj_str_ltr(self, tree, env):
        return str(tree.children[0].value)
    
    def obj_str_hex(self, tree, env):
        return str(tree.children[0].value) # TODO: Fix

    def obj_str(self, tree, env):
        return self.visit(tree.children[0], env)

    def obj_name(self, tree, env):
        return bytes(tree.children[0].value)

    def obj_array(self, tree, env):
        return [self.visit(c, env) for c in tree.children]

    def obj_dict(self, tree, env):
        cvals = [self.visit(c, env) for c in tree.children]
        return {k: v for k, v in zip(cvals[::2], cvals[1::2])}

    def obj_stream(self, tree, env):
        return PDFStream(tree.children[0].value, tree.children[2].value)

    def obj_null(self, tree, env):
        return None

    def obj_indir(self, tree, env):
        return PDFIndirObj(int(tree.children[0].value), int(tree.children[1].value), self.visit(tree.children[2], env))

    def obj_ref(self, tree, env):
        return PDFObjRef(int(tree.children[0].value), int(tree.children[1].value))

    def obj(self, tree, env):
        return self.visit(tree.children[0], env)

    def header(self, tree, env):
        return PDFHeader(tree.children[:])

    def xref_row(self, tree, env):
        return PDFXrefRow(int(tree.children[0].value), int(tree.children[1].value), str(tree.children[2].value))

    def xref_table(self, tree, env):
        return PDFXrefTable(int(tree.children[0].value), int(tree.children[1].value), [self.visit(c, env) for c in tree.children[2:]])

    def trailer(self, tree, env):
        return PDFTrailer(self.visit(tree.children[0], env), int(tree.children[1].value))

    def pdf_file(self, tree, env):
        cvals = [self.visit(c, env) for c in tree.children]
        return PDFFile(cvals[0], cvals[1:-2], cvals[-2], cvals[-1])
        # return PDFFile(None, [self.visit(c, env) for c in tree.children], None, None)

    def visit(self, tree, env):
        f = getattr(self, tree.data, self.__default__)
        return f(tree, env)


@dataclass
class PDFComment:
    content: bytes

@dataclass
class PDFHeader:
    comments: List[PDFComment]

@dataclass
class PDFStream:
    props  : PDFDict
    content: bytes

@dataclass
class PDFIndirObj:
    objno  : int
    genno  : int
    content: List[PDFObj]

@dataclass
class PDFObjRef:
    objno: int
    genno: int

@dataclass
class PDFXrefRow:
    objno: int
    genno: int
    kind : str

@dataclass
class PDFXrefTable:
    nlen: int
    ngen: int
    rows: List[PDFXrefRow]

@dataclass
class PDFTrailer:
    props    : PDFDict
    startxref: int

@dataclass
class PDFFile:
    header : PDFHeader
    objs   : List[PDFIndirObj]
    xrefs  : PDFXrefTable
    trailer: PDFTrailer
