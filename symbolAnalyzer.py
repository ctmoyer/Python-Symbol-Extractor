import ast
from pprint import pprint

import customData
# from customData import 

#https://docs.python.org/3/library/ast.html#abstract-grammar
#https://greentreesnakes.readthedocs.io/en/latest/nodes.html


def analyzeFile(filePath):
    with open(filePath, "r") as source:
        tree = ast.parse(source.read())

    analyzer = Analyzer()
    analyzer.visit(tree)
    analyzer.report()



class Analyzer(ast.NodeVisitor):
    foundNodes = []
    groupedNodes = {}

    def __init__(self, fileName):
        self.stats = {"import": [], "from": []}
        self.fileName = fileName

    def visit_FunctionDef(self, node):
        self.foundNodes.append(node)
        self.generic_visit(node)

    def visit_Import(self, node):
        for alias in node.names:
            self.stats["import"].append(alias.name)
        self.generic_visit(node)

    def visit_ImportFrom(self, node):
        for alias in node.names:
            self.stats["from"].append(alias.name)
        self.generic_visit(node)

    def report(self):
        pprint(self.stats)

# Each process function returns a dictionary of 
# consumable attributes appropriate to the needs of
# this project. 

# Tier 1 Triage level
def Process_FunctionDef(node):
    raise NotImplementedError

def Process_ClassDef(node):
    raise NotImplementedError

def Process_Call(node):
    raise NotImplementedError

def Process_Assign(node):
    raise NotImplementedError

# Tier 2
def Process_AsyncFunctionDef(node):
    return Process_FunctionDef(node)

def Process_TypedAssign(node):
    # covers ast.AnnAssign nodes
    raise NotImplementedError

def Process_Imports(node):
    raise NotImplementedError

def Process_ImportFrom(node):
    raise NotImplementedError

# Tier 3
def Process_AugAssign(node):
    # covers ast.AugAssign
    # Example: x += 2
    raise NotImplementedError


def Process_Alias(node):
    raise NotImplementedError
