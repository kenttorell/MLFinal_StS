import LoadData
import numpy as np
import random
import math

def S(y, l):
    return np.sign(y)*max(np.absolute(y)-l,0)

def ytk(y, betas, k, x):
    sum = 0
    for j in range(betas):
        if not j==k:
            sum = sum + (betas[j] * x[j])
    return y - sum

def betaKNew(k, xs, ys, betas):
    return S(np.dot(x[k].T, ytk(ys[k], betas, k, x[k]))/ np.dot(x[k].T, x[k]), ys)

def prepareData(X, Y, seed=None):
    random.seed(seed)
    numPredictors = X.shape[1]
    numRuns = X.shape[0]
    trainingIdxs = np.random.choice(numRuns, numRuns, replace=False)
    trainingPercentage = .6
    trainingXs = X[trainingIdxs[0:int(math.floor(numRuns*trainingPercentage))]]
    validationXs = X[trainingIdxs[int(math.floor(numRuns*trainingPercentage)):numRuns]]
    trainingYs = Y[trainingIdxs[0:int(math.floor(numRuns * trainingPercentage))]]
    validationYs = Y[trainingIdxs[int(math.floor(numRuns * trainingPercentage)):numRuns]]
    return trainingXs, trainingYs, validationXs, validationYs

def penalizedLogLikelihood(betas, X, y, l):
    # beta0 = betas[0]
    # betas = betas[:0]

    tmp = 1 + np.exp(-y*(np.dot(X,betas)))
    return -np.sum(np.log(tmp)) - l*np.sum(np.absolute(betas[1:]))


def lasso():
    # print X
    # print Y
    prepareData("random")

if __name__ == '__main__':
    LoadData.main()
    # Y = LoadData.Y
    # X = LoadData.X
    from LoadData import X, Y #FOUND IN LoadData.loadVars()**SLOW**, winningRuns, losingRuns, cards, relics
    lasso()