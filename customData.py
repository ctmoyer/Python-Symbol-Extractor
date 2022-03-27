import ast
from dataclasses import KW_ONLY, dataclass, field
from mimetypes import init
import helpers._utils as _utils
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
        self.fileHash = _utils.getFileHexHash(self.filePath)

@dataclass
class symbol:
    """Class for collecting info from ASY symbols and relating them to one another."""
    namespace: str
    label: str

@dataclass
class SymbolRelationship():
    id: UUID = field( default_factory=uuid4)


@dataclass
class Generic_Symbol():
    node: ast # type:ast
    parent: ast
    lineNum: int
    fileName: str
    # Puts all following fields after fields without defaults.
    _: KW_ONLY
    nodeType: str = field(default='Generic')
    scope: str = field( init=False )
    id: UUID = field( default_factory=uuid4, init=False )    
    
    def __post_init__(self):
        self.scope = f'{self.parent.name}/{self.name}'

@dataclass
class FunctionDef_Symbol(Generic_Symbol):
    name: str
    args: list[str]

    def __post_init__(self):
        self.nodeType = 'FunctionDef'

@dataclass
class Assign_Symbol(Generic_Symbol):
    targets: list
    _: KW_ONLY
    targetNames: list = field( init=False)

    def __post_init__(self):
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
