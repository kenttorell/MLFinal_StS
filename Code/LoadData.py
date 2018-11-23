import json
import os
import pickle
import numpy as np
from pprint import pprint

winningRuns, losingRuns, cards, relics, X, Y = None, None, None, None, None, None
cwd = os.path.dirname(__file__)
pathToData = os.path.join(cwd, '..', 'Data')

    
#Parses the wins and loses from the dump file
def loadFromFile(winsPath, losePath):
    #runsPath = os.path.join(pathToData, 'data_2018-10-24_0-5000.json')

    runs = []

    for f in os.listdir(os.path.join(pathToData, 'runs')):
        runsPath = os.path.join(pathToData, 'runs', f, f)
        runs += json.load(open(runsPath))
        print("Reading: ", f, "Cumulative size: ", len(runs))
        if len(runs) > 100000:
            break

    #runs = json.load(open(runsPath))
       

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
    
#Load all the variables from 
def loadVars():
    varFileNames = ['cards.json', 'relics.json']
    varFilePaths = [None, None]
    varList = [None, None]

    for file in range(len(varFileNames)):
        varFilePaths[file] = os.path.join(pathToData, varFileNames[file])
        varList[file] = json.load(open(varFilePaths[file]))

    #Set Variables to global scope and write cards and relics
    global cards, relics, winningRuns, losingRuns
    cards = varList[0]
    relics = varList[1]


    #Try to load up the wins and loses, if unable to then parse them from dump file
    winsPath = os.path.join(pathToData, 'wins.pkl')
    losePath = os.path.join(pathToData, 'loses.pkl')

    try:
        #pickle.load(open("break")) #This is for debugging
        winningRuns = pickle.load(open(winsPath, 'r+'))
        losingRuns = pickle.load(open(losePath, 'r+'))
        print("Run data files found and loaded")
    except IOError:
        print("No run files found, loading from bulk data")
        loadFromFile(winsPath, losePath)

def loadArrays():
    global X, Y
    xPath = os.path.join(pathToData, 'X.npy')
    yPath = os.path.join(pathToData, 'Y.npy')
    try:
        #np.load("break") #For debugging
        # np.load("Break")
        X = np.load(xPath)
        Y = np.load(yPath)
        print("Loaded Arrays from file")
    except IOError:
        print("No array files found, parsing from data files")
        loadVars()
        index = list(cards.keys())
        numCards = len(index)
        runs = winningRuns + losingRuns
        X = np.zeros((len(runs), numCards*2))
        Y = np.concatenate((np.ones(len(winningRuns)), np.zeros(len(losingRuns))))
        np.save(yPath, Y)
        rowCount = 0
        for run in runs:
            #print ('row: ', rowCount)
            for card in run[u'event'][u'master_deck']:
                cardName = str(card)
                #print ('index: ', str(index[collumnCount]))
                #print ('card: ', str(card))
                for i in range(len(index)):
                    indexCardName = str(index[i])
                    upgradedIndexCardName = str(indexCardName + '+1')
                    if cardName == indexCardName:
                        #print cardName, i
                        X[rowCount][i] += 1
                    elif cardName == upgradedIndexCardName:
                         X[rowCount][i+numCards] += 1
            rowCount += 1
        np.save(xPath, X)
                    
        
def main():
    loadArrays()

if __name__=='__main__':
    loadArrays()
