# Module: Python Symbol Extractor (PyTractor)
# Author: Chris Moyer
#
# PyTractor analyzes python text source files and aggregates
# specified symbols and maps relationships in file, and between
# files.
# This produces a data blob suitable for visualizing how various
# symbols are used across a project.

# import travellerHandlers from './travellerHandlers.py
import ast
from pathlib import Path
from pprint import pprint

from argHandler import getArgs, getParsedOptions
import customData
import helpers._utils as utils
from symbolAnalyzer import FuncLister
from helpers.astpp import dump

# https://www.tutorialspoint.com/python/os_walk.htm
# https://docs.python.org/3/library/getopt.html


def main():

    workingDirectory = Path.cwd()
    #Get cmdline args
    args = getParsedOptions()
    nodeBuilder = {} # contains all generated data from found nodes

    #Verify that we can open the provided file
    with args['file'][0].open('r') as f: 
        codeText = f.read()

    tree = ast.parse(codeText)
    nodes = FuncLister()
    nodes.visit(tree)
    # Add name attribute to Module node
    tree.name = '__root__'

    # add reference to parent nodes for determining context
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            child.parent = node
    
    # dump(tree) outputs a string version of the tree structure
    # print(dump(tree))
    
    print(nodes.foundNodes)
    for node in nodes.foundNodes:
        if(node.name == None): 
            del node
            continue

        fileName = args['file'][0].resolve()
        fileName = f'{fileName.relative_to(workingDirectory)}'
        # test = customData.FunctionDef_Symbol(node, node.parent, fileName)
        # print(test.name)
        # Index represents parentCtx + Func label
        if(node.parent.name == '__root__'): 
            print(f'\nID: {fileName}::{node.name}')
            print(f'Name: {node.name}')
        else: 
            print(f'\nID: {fileName}::{node.parent.name}/{node.name}')
            print(f'Name: {node.parent.name}/{node.name}')


        print(f'File Path: {fileName}')
        print('Line Number: {node.lineno}')
        print('Type: FunctionDefiniton')
        nodeArgs = utils.GatherArgs(node)        
        print(f'args: {nodeArgs}')

        # Determine if return exists, and what type to expect, if available
        if(node.returns and node.returns != None):
            print(f'Return: {node.returns.id}')
        else:
            # Check for return statement in body of function
            returnExists = False
            for child in node.body:
                if(isinstance(child, ast.Return)): returnExists = True
            print(f'Return: {returnExists}')



if __name__ == '__main__':
    main()