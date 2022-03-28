from ast import NodeVisitor, walk, iter_child_nodes, AST
from pathlib import Path

from symbolAnalyzer import Analyzer
import customData


def processTree(args, tree) -> list[dict]:
    workingDirectory: str = Path.cwd()
    fileName = args['file'][0].resolve()
    fileName = f'{fileName.relative_to(workingDirectory)}'
    savedNodes: list[AST] = []
    # Gather filtered nodes
    visitor: NodeVisitor = Analyzer(fileName)
    visitor.visit(tree)

    # Add name attribute to Module node
    tree.name = '__root__'
    # add reference to parent nodes for determining context
    for node in walk(tree):
        for child in iter_child_nodes(node):
            child.parent = node
    
    # Process found nodes
    for node in visitor.foundNodes:
        if(node.name == None): 
            del node
            continue

        savedNodes.append(customData.FunctionDef_Symbol(node, fileName))

    return savedNodes