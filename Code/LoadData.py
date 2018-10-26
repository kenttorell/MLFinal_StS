import json
import os
from pprint import pprint

def loadFromFile():

    cwd = os.path.dirname(__file__)
    dataPath = os.path.join(cwd, '..', 'Data', 'data_2018-10-24_0-5000.json')

    print(cwd)
    print(dataPath)
    
    with open(dataPath) as f:
        data = json.load(f)
        
    pprint(data[0])

if __name__=='__main__':
    loadFromFile()
