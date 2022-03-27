from ast import arguments, Assign, FunctionDef, Name, Attribute
# import ast
from hashlib import sha1
import os
from pyclbr import Function
from xml.dom.minidom import Attr

#example not implemented function 
def exampleFunc():
    raise NotImplementedError

""" Begin Functions """

def gatherFiles(folderPath='.'):    
    for root, dirs, files in os.walk(folderPath, topdown=False):
        for name in files:
            print(os.path.join(root, name))
        for name in dirs:
            print(os.path.join(root, name))

def getFileHexHash(filePath)->int:
    #type 
    hash = sha1()
    with open(filePath, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            hash.update(chunk)
    return hash.hexdigest()

def getNodeIdentifiers(node):
    idens = []
    if(isinstance(node, Assign)):
        for target in node.targets: 
            idens.append(getNodeIdentifiers(target))
    if(isinstance(node, FunctionDef)):
        idens.append(node.name)
    if(isinstance(node, Name)):
        idens.append(node.id)
    if(isinstance(node, Attribute)):
        idens.append(f'{getNodeIdentifiers(node.value)}.{node.attr}')
    return idens


def GatherArgs(node):
    # arguments node type doesn't support dynamic key access.
    # was forced to manually enumerate all types of fields.
    nodeArgs = {}
    for type in arguments._fields[0:]:
        nodeArgs[type] = []

    if(node.args.posonlyargs):
        for tmpArgs in node.args.posonlyargs:
            nodeArgs['posonlyargs'].append(tmpArgs.arg)

    if(node.args.args):
        for tmpArgs in node.args.args:
            nodeArgs['args'].append(tmpArgs.arg)

    if(node.args.vararg):
        for tmpArgs in node.args.vararg:
            nodeArgs['vararg'].append(tmpArgs.arg)

    if(node.args.kwonlyargs):
        for tmpArgs in node.args.kwonlyargs:
            nodeArgs['kwonlyargs'].append(tmpArgs.arg)

    if(node.args.kw_defaults):
        for tmpArgs in node.args.kw_defaults:
            nodeArgs['kw_defaults'].append(tmpArgs.value)

    if(node.args.kwarg):
        for tmpArgs in node.args.kwarg:
            nodeArgs['kwarg'].append(tmpArgs.arg)

    if(node.args.defaults):
        for tmpArgs in node.args.defaults:
            nodeArgs['defaults'].append(tmpArgs.value)

    return nodeArgs


""" End Functions """