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
    node: ast = field( repr=False, compare=False)
    parent: ast = field( repr=False, compare=False)
    fileName: str
    # Puts all following fields after fields without defaults.
    _: KW_ONLY
    parentName: str = field(init=False)
    name: str = field(init=False)
    nodeType: str = field(default='Generic')
    lineNum: int = field(init=False)
    id: UUID = field( default_factory=uuid4, init=False, repr=False )
    scope: str = field( init=False, repr=False )
    index: str = field( init=False, repr=False, compare=False )    
    
    def __post_init__(self):
        #TODO update .name assignments to be type sensitive
        self.name = utils.getNodeIdentifiers(self.node)
        self.parentName = utils.getNodeIdentifiers(self.parent)
        print(f'Parent Node: {self.parent}')
        self.lineNum = self.node.lineno
        # Scope and index serve different purposes
        # Scope is intended to provide information about the context 
        # Index is intended to provide a field to sort and query by
        if(self.parentName not in [None, '']):
            self.scope = f'{self.fileName}::{self.parentName}/{self.name}'
        else: self.scope = f'{self.fileName}::{self.name}'
        self.index = f'{self.fileName}::{self.parentName}/{self.name}'

@dataclass(order=True)
class FunctionDef_Symbol(Generic_Symbol):
    _: KW_ONLY
    args: list[str] = field( init=False )
    returns: list = field( init=False )

    def __post_init__(self):
        # self.name = self.node.name
        super().__post_init__()
        self.nodeType = 'FunctionDef'
        self.args = utils.GatherArgs(self.node)

                # Determine if return exists, and what type to expect, if available
        if(self.node.returns and self.node.returns != None):
            self.returns = self.node.returns.id
        else:
            # Check for return statement in body of function
            returnExists = False
            for child in self.node.body:
                if(isinstance(child, ast.Return)): returnExists = True
            self.returns = returnExists

@dataclass(order=True)
class Assign_Symbol(Generic_Symbol):
    _: KW_ONLY
    targets: list
    targetNames: list = field( init=False)

    def __post_init__(self):
        # self.name = self.node.name
        super().__post_init__()
        newTargets = []
        for target in self.targets:
            newTargets.append(target.id)
        self.targetNames = newTargets


""" AnnAssign is set for support in the Typing Release """
# @dataclass
# class AnnotatedAssign_Symbol(Generic_Symbol):
#     raise notImplementedError

""" AugAssign is outside the scope of initial Analysis"""
# @dataclass
# class AugmentedAssign_Symbol(Generic_Symbol):
#     raise notImplementedError
