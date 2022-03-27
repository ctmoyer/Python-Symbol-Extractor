import ast
from pprint import pprint
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
    functions = {}
    foundNodes = []

    def __init__(self):
        self.stats = {"import": [], "from": []}

    def visit_FunctionDef(self, node):
        # print(node.name)
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

def Process_FunctionDef(node):
    raise NotImplementedError

def Process_AsyncFunctionDef(node):
    return Process_FunctionDef(node)

def Process_ClassDef(node):
    raise NotImplementedError

def Process_Assign(node):
    raise NotImplementedError

def Process_TypedAssign(node):
    # covers ast.AnnAssign nodes
    raise NotImplementedError

def Process_AugAssign(node):
    # covers ast.AugAssign
    # Example: x += 2
    raise NotImplementedError

def Process_Imports(node):
    raise NotImplementedError

def Process_ImportFrom(node):
    raise NotImplementedError

def Process_Alias(node):
    raise NotImplementedError

# TODO Remove this func. Left for reference.
class FuncLister(ast.NodeVisitor):
    foundNodes = []
    def visit_FunctionDef(self, node):
        # print(node.name)
        self.foundNodes.append(node)
        self.generic_visit(node)
