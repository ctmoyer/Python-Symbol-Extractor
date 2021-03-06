import argparse
import pathlib


def getArgs() -> dict:
    parser = argparse.ArgumentParser(description="Analyze Python Files")
    parser.add_argument( '-f', '--file', nargs='+', type=pathlib.Path,
                        help="The file name of a Python file to analyze." )
    parser.add_argument( '--folder', type=pathlib.Path,
                        help="The path to a folder containing Python files to analyze." )
    parser.add_argument( '-r', '--recursive', nargs='?', type=int, const=0, default=-1, dest='recursionLevel',
                        help="Recursively searches all subfolders for Python files.\
                            A value of 0 gathers all files in the supplied folder.\
                            Positive integers represent how many layers deep the recursion should explore.\
                            -1 is the Default value when no value is supplied but thif flag is present.\
                            When a negative number is present, the recursion will explore all subfolders without limit." )
    parser.add_argument( '-d','--dump', nargs='?', type=bool, const=True, default=False, 
                        help='Print a human readable version of the AST found by configured visitor methods.')
    parser.add_argument( '--gitURL', nargs='?', type=str, default='https://github.com/ctmoyer/Python-Symbol-Extractor/', 
                        help='Get markdown links to github repo built automatically.')

    return vars(parser.parse_args())

def getParsedOptions() -> dict:
    argsDict = getArgs()
    optionsDict = {
        'file': None,
        'folder': None,
        'recursionLevel': None,
        'dump': None,
        'giturl': None
    }

    for option in argsDict:
        if option in ('file'):
            optionsDict[option] = argsDict['file']
        elif option in ('folder'):
            optionsDict[option] = argsDict[option]
        elif option in ('recursionLevel'):
            optionsDict[option] = argsDict[option]
        elif option in ('dump'):
            optionsDict[option] = argsDict[option]
        elif option in ('gitURL'):
            optionsDict[option] = argsDict[option]
        else:
            assert False, f'Unhandled Exception; Option: {option}'
    return optionsDict
