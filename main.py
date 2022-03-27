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
import ast
from pathlib import Path
from pprint import pprint

from argHandler import getArgs, getParsedOptions
import customData
import helpers._utils as utils
from symbolAnalyzer import Analyzer, FuncLister
from helpers.astpp import dump

# https://www.tutorialspoint.com/python/os_walk.htm
# https://docs.python.org/3/library/getopt.html


def main():

    workingDirectory = Path.cwd()
    #Get cmdline args
    args = getParsedOptions()

    with args['file'][0].open('r') as f: 
        codeText = f.read()

    tree = ast.parse(codeText)

    #TODO replace FuncLister with Analyzer
    nodes = FuncLister()
    nodes = Analyzer()
    nodes.visit(tree)
    # Add name attribute to Module node
    tree.name = '__root__'

    # add reference to parent nodes for determining context
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    
    if(args['dump']):
        # dump(tree) outputs a string version of the tree structure
        print(dump(tree))
    
    # Question: Process nodes here, or in Analyzers at visit-time?
    for node in nodes.foundNodes:
        if(node.name == None): 
            del node
            continue

        fileName = args['file'][0].resolve()
        fileName = f'{fileName.relative_to(workingDirectory)}'
        test = customData.FunctionDef_Symbol(node, node.parent, fileName)
        pprint('\n')
        pprint(test)



if __name__ == '__main__':
    main()