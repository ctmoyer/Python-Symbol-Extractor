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
import json
from pathlib import Path
from pprint import pprint

from argHandler import getArgs, getParsedOptions
# import customData
import helpers._utils as utils
# from symbolAnalyzer import Analyzer
from nodeProcessor import processTree
from helpers.astpp import dump

# https://www.tutorialspoint.com/python/os_walk.htm
# https://docs.python.org/3/library/getopt.html


def main():
    args = getParsedOptions()
    savedNodes = []
    
    with args['file'][0].open('r') as f: 
        codeText = f.read()

    tree = ast.parse(codeText)

    if(args['dump']):
        # dump(tree) outputs a string version of the tree structure
        print(dump(tree))

    savedNodes = processTree(args, tree)
    pprint(savedNodes)

    # JSON handling section
    jsonNodes = '['
    for node in savedNodes:
        jsonNodes += node.toJSON()
        jsonNodes += ','
    jsonNodes = jsonNodes[:-1] + ']'

    with open('jsonData.json', 'w') as outfile:
        outfile.write(jsonNodes)


if __name__ == '__main__':
    main()