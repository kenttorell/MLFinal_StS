from xgboost import XGBClassifier
import LoadData
import numpy as np
import math
import random

def prepareData(X, Y, seed=None):
    np.random.seed(seed)
    numPredictors = X.shape[1]
    numRuns = X.shape[0]
    trainingIdxs = np.random.choice(numRuns, numRuns, replace=False)
    trainingPercentage = .6
    trainingXs = X[trainingIdxs[0:int(math.floor(numRuns*trainingPercentage))]]
    validationXs = X[trainingIdxs[int(math.floor(numRuns*trainingPercentage)):numRuns]]
    trainingYs = Y[trainingIdxs[0:int(math.floor(numRuns * trainingPercentage))]]
    validationYs = Y[trainingIdxs[int(math.floor(numRuns * trainingPercentage)):numRuns]]
    return trainingXs, trainingYs, validationXs, validationYs

LoadData.main()
from LoadData import X,Y

#Pick a random seed to use
seed = random.randint(0, 1000)

#For consistency purposes try using:
seed = 841
print ("Seed = ", seed)
tX, tY, cX, cY = prepareData(X,Y, seed)

# print tX.shape
# print tY.shape


classifier = XGBClassifier()
classifier.fit(tX, tY)


yPred = classifier.predict(cX)

# print (yPred)
# print(cY)

print ("Percentage correct without using model: ", np.sum(tY)/tY.shape[0], '%')
print ("Misclassification rate: ", 1-np.sum(tY)/tY.shape[0], '%' )
print ("Percentage correct using model: ", 1-np.sum(np.absolute(yPred - cY))/cY.shape[0], "%")
print ("Misclassification rate: ", (np.sum(np.absolute(yPred - cY))/cY.shape[0]),  '%' )