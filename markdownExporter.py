import argparse
import json
import pathlib
from pprint import pprint


def getArgs() -> dict:
    parser = argparse.ArgumentParser(description="Analyze Python Files")
    parser.add_argument( '-f', '--file', nargs='+', type=pathlib.Path,
                        help="The file name of a Python file to analyze." )

    return vars(parser.parse_args())

def getParsedOptions() -> dict:
    argsDict = getArgs()
    optionsDict = {
        'file': None,
        'folder': None,
        'recursionLevel': None,
        'dump': None
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
        else:
            assert False, f'Unhandled Exception; Option: {option}'
    return optionsDict



def main():
    args = getParsedOptions()
    # print(args['file'])

    with args['file'][0].open('r') as importData:
        codeDict = json.load(importData)
    
    generateMarkdown(codeDict)

# TODO ENHANCEMENT
# Need to encode a line break such that Github will recognize it.
def generateMarkdown(codeDict, outputFolder, outputFile):
    outputString:str = ''
    for node in codeDict:
        nodeName = node['name']
        fileName = pathlib.Path(str(node['fileName']))
        fileName = fileName.as_posix()
        lineno = node['lineNum']
        url = f'https://github.com/ctmoyer/Python-Symbol-Extractor/blob/main/{fileName}#L{lineno}'
        # print(f'node.fileName: {fileName}')
        outputString += f'## {nodeName}\n\n'
        outputString += f'**Location:** [{fileName}]({url}){markdownTab(1)}|{markdownTab(1)}{lineno}\n'
        if node['args']['args'] not in [None, '', []]:
            strArgs = ', '.join(node['args']['args'])
            outputString += f'**Parameters:** {strArgs}{markdownTab(2)}|{markdownTab(2)}'
        else:
            outputString += f'**Parameters:** None{markdownTab(2)}|{markdownTab(2)}'
        returns = str(node['returns'])
        outputString += f'**Return:** {returns}\n'
        if node['parentName'] not in [None, '']:
            parentName = node['parentName']
            outputString += f'**Parent Context:** {parentName}\n'
        else:
            outputString += f'**Parent Context:** &nbsp;\_\_root\_\_\n'
        outputString += '\n'

    outputFile = pathlib.Path(outputFolder) / outputFile
    outputFile.parents[0].mkdir(parents=True, exist_ok=True)
    print(str(outputFile))

    with outputFile.open('w') as output:
        output.write(outputString)
    
        
def markdownTab(numTabs, *, tabSpace=4):
    return '&nbsp;'*numTabs * tabSpace

if __name__ == '__main__':
    main()