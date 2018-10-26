import json
import os
import pickle
from pprint import pprint

winningRuns, losingRuns, cards, relics = None, None, None, None
cwd = os.path.dirname(__file__)

#Load all the variables from 
def loadVars():
    varFileNames = ['cards.json', 'relics.json']
    varFilePaths = [None, None]
    varList = [None, None]

    for file in range(len(varFileNames)):
        varFilePaths[file] = os.path.join(cwd, '..', 'Data', varFileNames[file])
        varList[file] = json.load(open(varFilePaths[file]))

    #Set Variables to global scope and write cards and relics
    global cards, relics, winningRuns, losingRuns
    cards = varList[0]
    relics = varList[1]


    #Try to load up the wins and loses, if unable to then parse them from dump file
    winsPath = os.path.join(cwd, '..', 'Data', 'wins.pkl')
    losePath = os.path.join(cwd, '..', 'Data', 'loses.pkl')

    try:
        winningRuns = pickle.load(open(winsPath, 'r+'))
        losingRuns = pickle.load(open(losePath, 'r+'))
    except IOError:
        print("No run files found, loading from bulk data")
        loadFromFile(winsPath, losePath)
    
#Parses the wins and loses from the dump file
def loadFromFile(winsPath, losePath):
    runsPath = os.path.join(cwd, '..', 'Data', 'data_2018-10-24_0-5000.json')
                                 
    runs = json.load(open(runsPath))

    global winningRuns, losingRuns
    winningRuns = []
    losingRuns = []

    #If floors reached = 50 then died to final boss, 51 means victory
    for run in runs:
        floor = run['event']['floor_reached']
        if floor == 50:
            losingRuns.append(run)
        elif floor == 51:
            winningRuns.append(run)

    pickle.dump(winningRuns, open(winsPath, 'w'))
    pickle.dump(losingRuns, open(losePath, 'w'))
    
    
        

if __name__=='__main__':
    loadVars()
