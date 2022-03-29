import ast
from dataclasses import KW_ONLY, dataclass, field
from pprint import pprint
import _utils as utils
from uuid import uuid4, UUID
import json

# https://docs.python.org/3/library/dataclasses.html

def findAllParents(node):
    # Assumes that tree that node is part of has already
    # added parent property pointing to parent node.
    # Also assumes that root Module node has name attr set to __root__ 
    nodeStack = []
    # visit parent
    if(type(node) in [ast.FunctionDef, ast.ClassDef]):
        # append dict entry to stack
        nodeStack.append({
            'name': node.name,
            'type':type(node).__name__,
            'lineno': node.lineno
        })
    # if no parent exists, return  
    if(hasattr(node, 'parent')):
        nodeStack.append(findAllParents(node.parent))
        return nodeStack        
    else: 
        nodeStack.append({
            'name': '__root__',
            'type': 'Module',
            'lineno': '0'
        })

        return nodeStack



@dataclass(order=True)
class Generic_Symbol():
    node: ast.AST = field( repr=False, compare=False)
    fileName: str
    # Puts all following fields after fields without defaults.
    _: KW_ONLY
    parent: ast.AST = field( repr=False, compare=False, init=False)
    parentName: str = field(init=False)
    # We need some way to reference the parent node
    # We can't use a generated UUID since that changes each runtime
    # So instead we make a composite index from as much scope information
    # as is available, and we call that Index.
    #  
    # parentIndex: str = field(init=False)
    
    name: str = field(init=False)
    nodeType: str = field(default='Generic')
    lineNum: int = field(init=False)
    id: UUID = field( default_factory=uuid4, init=False, repr=False )
    scope: str = field( init=False, repr=False )
    index: str = field( init=False, repr=False, compare=False )  
    context: dict = field (init=False, repr=True, compare=False)  
    
    def __post_init__(self):
        self.parent = self.node.parent
        #TODO update .name assignments to be type sensitive
        self.name = utils.getNodeIdentifiers(self.node)
        self.parentName = utils.getNodeIdentifiers(self.parent)
        # print(f'Parent Node: {self.parent}')
        self.lineNum = self.node.lineno
        # Scope and index serve different purposes
        # Scope is intended to provide information about the context 
        # Index is intended to provide a field to sort and query by
        if(self.parentName not in [None, '']):
            self.scope = f'{self.fileName}::{self.parentName}/{self.name}'
        else: self.scope = f'{self.fileName}::{self.name}'

        self.context = self.getContext()

        self.index = f'{self.fileName}::{self.parentName}/{self.name}'

    def toJSON(self):
        output = self.__dict__
        del output['node']
        del output['parent']
        output['id'] = str(output['id'])
        # print(output)
        return json.dumps(output, sort_keys=True)

    def getContext(self):
        # type: () -> dict
        # Recursively navigate up parent nodes, gathering identity
        # details as you go.

        #TODO implement
        workingCtx = findAllParents(self.node)
        return workingCtx


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
            # TODO ERROR
            # AttributeError: 'Subscript' object has no attribute 'id'
            # Seemingly caused by markdownGenerator trying to run with nodeProcessor.py 
            # as the target file.
            self.returns = self.node.returns.id
        else:
            # Check for return statement in body of function
            returnExists = False
            for child in self.node.body:
                if(isinstance(child, ast.Return)): returnExists = True
            self.returns = returnExists
    def toJSON(self):
        return super().toJSON()        


# TODO PHASE_1 
# Implement 
@dataclass(order=True)
class AsyncFunctionDef_Symbol(Generic_Symbol):
    pass


# TODO PHASE_1 
@dataclass(order=True)
class ClassDef_Symbol(Generic_Symbol):
    _: KW_ONLY
    funcs: list = field()



"""
PHASE_2 
"""
# TODO PHASE_2
# @dataclass(order=True)
# class Assign_Symbol(Generic_Symbol):
#     _: KW_ONLY
#     targets: list
#     targetNames: list = field( init=False)

#     def __post_init__(self):
#         # self.name = self.node.name
#         super().__post_init__()
#         newTargets = []
#         for target in self.targets:
#             newTargets.append(target.id)
#         self.targetNames = newTargets


"""
PHASE_3
"""
# TODO PHASE_3
""" AnnAssign is set for support in the Typing Release """
# @dataclass
# class AnnotatedAssign_Symbol(Generic_Symbol):
#     raise notImplementedError

# TODO PHASE_3
""" AugAssign is outside the scope of initial Analysis"""
# @dataclass
# class AugmentedAssign_Symbol(Generic_Symbol):
#     raise notImplementedError


"""
PHASE_4
"""
# TODO PHASE_4
@dataclass
class SymbolRelationship():
    id: UUID = field( default_factory=uuid4)
