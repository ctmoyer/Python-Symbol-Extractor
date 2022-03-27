from hashlib import sha1
import os

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

""" End Functions """