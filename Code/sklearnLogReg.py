from sklearn.linear_model import LogisticRegression
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
# seed = 652
print "Seed = ", seed
tX, tY, cX, cY = prepareData(X,Y, seed)

# print tX.shape
# print tY.shape



log = LogisticRegression(penalty='l1', solver = 'liblinear', random_state=seed, multi_class='ovr')
log.fit(tX,tY)
# print "Check1"
# print cX.shape
predicted = log.predict(cX)
# print predicted
# print "Check2"
# print cY

print "Percentage correct without using model: ", np.sum(tY)/tY.shape[0], '%'
print "Percentage correct using model: ", 1-np.sum(np.absolute(predicted - cY))/cY.shape[0], "%"
