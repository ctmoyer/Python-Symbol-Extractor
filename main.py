# Module: Python Symbol Extractor (PyTractor)
# Author: Chris Moyer
# 
# PyTractor analyzes python text source files and aggregates
# specified symbols and maps relationships in file, and between
# files.
# This produces a data blob suitable for visualizing how various 
# symbols are used across a project.

# import travellerHandlers from './travellerHandlers.py 
import argparse
import pathlib
from pprint import pprint
import sys

# https://www.tutorialspoint.com/python/os_walk.htm
# https://docs.python.org/3/library/getopt.html


def main():

    parser = argparse.ArgumentParser(description="Analyze Python Files")
    parser.add_argument( '-f', '--file', nargs='+',
                        help="the file name of a Python file to analyze." )
    parser.add_argument( '--folder', type=pathlib.Path,
                        help="the path to a folder containing Python files to analyze." )
    parser.add_argument( '-r', '--recursive', nargs='?', type=bool, const=True, default=False, 
                        help="recursively searches all subfolders for Python files." )

    args = vars(parser.parse_args())
    pprint(args)

    file = None
    folder = None
    recursive = None
    for option in args:
        if option in ('file'):
            file = args[option][0]
            print(file)
        elif option in ('folder'):
            folder = args[option]
            print(folder)
        elif option in ('recursive'):
            recursive = args[option]
            print(recursive)
        else:
            assert False, f'Unhandled Exception; Option: {option}'

if __name__ == '__main__':
    # Any code placed here will execute when this file is called from 
    # stdin, an interpreter, or a script. 
    # When this is imported as Module, however, the __name__ attribute
    # will read the file's name instead of __main__, meaning this 
    # code will not execute on module import.
    main()