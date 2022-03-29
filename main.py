# Module: Python Symbol Extractor (PyTractor)
# Author: Chris Moyer
#
# PyTractor analyzes python text source files and aggregates
# specified symbols and maps relationships in file, and between
# files.
# This produces a data blob suitable for visualizing how various
# symbols are used across a project.

# import travellerHandlers from './travellerHandlers.py

"""
Thank you to:
    Alex Leone (acleone ~AT~ gmail.com) for writing the dump function 
    to make understanding the returned AST object easier!
    You can find the source for dump @: 
    http://alexleone.blogspot.co.uk/2010/01/python-ast-pretty-printer.html

"""
from ast import NodeVisitor, walk, iter_child_nodes, AST, parse
import json
from pathlib import Path
from pprint import pprint


from argHandler import getParsedOptions
import customData
import _utils as utils
from symbolAnalyzer import Analyzer
# from nodeProcessor import processTree
from astpp import dump
import markdownExporter

# https://www.tutorialspoint.com/python/os_walk.htm
# https://docs.python.org/3/library/getopt.html


def main():
    args = getParsedOptions()
    
    if args['file'] != None:
        with args['file'].open('r') as file:
            codeText = file.read()
    

    tree = parse(codeText)

    if(args['dump']):
        # dump(tree) outputs a string version of the tree structure
        print(dump(tree))

    savedNodes = processTree(args, tree)

    jsonNodes = getJSONObj(savedNodes)

    outputFilePath = Path('exports/jsonData.json')

    code = exportJSON(jsonNodes, outputFilePath)

    outputFileName = ".".join(str(args['file'].as_posix()).split('/'))[:-3] + '.md'
    markdownExporter.generateMarkdown(code, 'docs', outputFileName)

def processTree(args, tree) -> list[dict]:
    workingDirectory: str = Path.cwd()
    fileName = args['file'].resolve()
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

def getJSONObj(savedNodes) -> dict:

    jsonNodes = '['
    for node in savedNodes:
        jsonNodes += node.toJSON()
        jsonNodes += ','
    jsonNodes = jsonNodes[:-1] + ']'
    return jsonNodes

def exportJSON(jsonNodes, outputFilePath:Path):
    with outputFilePath.open('w', encoding='utf-8') as outfile:
        outfile.write(jsonNodes)

    with outputFilePath.open(encoding='utf-8') as infile:
        code = json.load(infile)
    
    return code


if __name__ == '__main__':
     main()
