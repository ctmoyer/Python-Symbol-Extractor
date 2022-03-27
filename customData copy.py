import ast
from dataclasses import KW_ONLY, dataclass, field
from mimetypes import init
import helpers._utils as utils
from uuid import uuid4, UUID

# https://docs.python.org/3/library/dataclasses.html

@dataclass
class fileMeta:
    """ Used when gathering files with the --folder option """
    fileName: str
    filePath: str
    fileSize: int
    fileHash: int = field(init=False)

    def __post_init__(self):
        self.fileHash = utils.getFileHexHash(self.filePath)

@dataclass
class symbol:
    """Class for collecting info from ASY symbols and relating them to one another."""
    namespace: str
    label: str

@dataclass
class SymbolRelationship():
    id: UUID = field( default_factory=uuid4)


@dataclass(order=True)
class Generic_Symbol():
    srcNode: ast = field( repr=False)
    parent: ast = field( repr=False)
    fileName: str
    # Puts all following fields after fields without defaults.
    # _: KW_ONLY
    parentName: str = field(init=False)
    nodeName: str = field(init=False)
    index: str = field( init=False, repr=False )    
    id: UUID = field( default_factory=uuid4, init=False )
    nodeType: str = field(default='Generic')
    scope: str = field( init=False, repr=False )
    lineNum: int = field(init=False, repr=False)
    
    def __post_init__(self):
        #TODO update .nodeName assignments to be type sensitive
        self.nodeName = self.srcNode.name
        self.parentName = self.parent.name
        self.lineNum = self.srcNode.lineno
        if(self.parent.name != None):
            self.scope = f'{self.fileName}::{self.parent.name}/{self.nodeName}'
        else: self.scope = f'{self.fileName}::{self.nodeName}'
        self.index = f'{self.fileName}::{self.parentName}/{self.nodeName}'

@dataclass(order=True)
class FunctionDef_Symbol():
    srcNode: ast = field( repr=False)
    parent: ast = field( repr=False)
    fileName: str
    # Puts all following fields after fields without defaults.
    # _: KW_ONLY
    parentName: str = field(init=False)
    nodeName: str = field(init=False)
    index: str = field( init=False, repr=False )    
    id: UUID = field( default_factory=uuid4, init=False )
    nodeType: str = field(default='Generic')
    scope: str = field( init=False, repr=False )
    lineNum: int = field(init=False, repr=False)

    args: list[str] = field( init=False )
    returns: list = field( init=False )
    
    def __post_init__(self):
        #TODO update .nodeName assignments to be type sensitive
        self.nodeName = self.srcNode.name
        self.parentName = self.parent.name
        self.lineNum = self.srcNode.lineno
        if(self.parent.name != None):
            self.scope = f'{self.fileName}::{self.parent.name}/{self.nodeName}'
        else: self.scope = f'{self.fileName}::{self.nodeName}'
        self.index = f'{self.fileName}::{self.parentName}/{self.nodeName}'

        self.nodeType = 'FunctionDef'
        self.args = utils.GatherArgs(self.srcNode)

                # Determine if return exists, and what type to expect, if available
        if(self.srcNode.returns and self.srcNode.returns != None):
            self.returns = self.srcNode.returns.id
        else:
            # Check for return statement in body of function
            returnExists = False
            for child in self.srcNode.body:
                if(isinstance(child, ast.Return)): returnExists = True
            self.returns = returnExists



# @dataclass(order=True)
# class Assign_Symbol(Generic_Symbol):
#     targets: list
#     _: KW_ONLY
#     targetNames: list = field( init=False)

#     def __post_init__(self):
#         newTargets = []
#         for target in self.targets:
#             newTargets.append(target.id)
#         self.targetNames = newTargets

""" AnnAssign is set for support in the Typing Release """
# @dataclass
# class AnnotatedAssign_Symbol(Generic_Symbol):
#     raise notImplementedError

""" AugAssign is outside the scope of initial Analysis"""
# @dataclass
# class AugmentedAssign_Symbol(Generic_Symbol):
#     raise notImplementedError
