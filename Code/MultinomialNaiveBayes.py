import numpy as np
import random
import LoadData
import math

def prepareData(X, Y, seed = None):
    np.random.seed(seed)
    numPredictors = X.shape[1]
    numRuns = X.shape[0]
    trainingIdxs = np.random.choice(numRuns, numRuns, replace=False)
    trainingPercentage = .8
    trainingXs = X[trainingIdxs[0:int(math.floor(numRuns * trainingPercentage))]]
    validationXs = X[trainingIdxs[int(math.floor(numRuns * trainingPercentage)):numRuns]]
    trainingYs = Y[trainingIdxs[0:int(math.floor(numRuns * trainingPercentage))]]
    validationYs = Y[trainingIdxs[int(math.floor(numRuns * trainingPercentage)):numRuns]]
    return trainingXs, trainingYs, validationXs, validationYs

def calculateThetaPi(X, Y):
    numFeatures = X.shape[1]
    numRuns = X.shape[0]

    if not numRuns==Y.shape[0]:
        print "X and Y not the same length..."
        exit(1)

    pi_1 = np.sum(Y)/numRuns

    # theta = np.zeros((2,numFeatures))
    countOfAllCardsInWins = np.sum(np.dot(Y, X))
    countOfAllCardsInLosses = np.sum(X) - countOfAllCardsInWins

    # print "Cards in Loses = ", countOfAllCardsInLosses
    # print "Cards in Wins = ", countOfAllCardsInWins
    # print "Average cards per run = ", (countOfAllCardsInWins+countOfAllCardsInLosses)/numRuns

    # print "Num Unique Cards: ", numFeatures
    # print "Num runs: ", numRuns


    theta = np.zeros((2, numFeatures))

    # print X.shape
    for i in range(numRuns):
        if Y[i] == 0:
            theta[0] = np.add(theta[0], X[i])
        else:
            theta[1] = np.add(theta[1], X[i])
    theta = theta + 1
    theta[0] = theta[0]/(countOfAllCardsInLosses + numFeatures)
    theta[1] = theta[1]/(countOfAllCardsInWins + numFeatures)

    # theta[0] =
    # theta[1] =
    #
    # for j in range(numFeatures):
    #     print theta[0][j], ' ', theta[1][j]
    #
    # print pi_1

    return theta, pi_1

def predictYs(Xs, theta, pi_1):
    # print Xs.shape
    Ys = np.zeros((Xs.shape[0],1))
    for i in range(Ys.shape[0]):
        if (np.prod(np.power(theta[0], Xs[i]))*(1-pi_1) < np.prod(np.power(theta[1], Xs[i]))*(pi_1)):
            Ys[i] = 1
    # print np.sum(Ys)/Ys.shape[0]
    return Ys

def testingOnly(X):
    print X.shape[0]
    exit(0)

def main():
    LoadData.main()
    from LoadData import X,Y

#Used for finding min and max card counts **Testing and curiosity only**
    # min = 100
    # max = 0
    # cumCount = 0
    # for run in range(X.shape[0]):
    #     count = np.sum(X[run])
    #     cumCount += count
    #     if min > count:
    #         min = count
    #     if max < count:
    #         max = count
    # print min, max, cumCount/X.shape[0]
    # exit(0)

    testingOnly(X)

    # Pick a random seed to use
    seed = random.randint(0, 1000)

    # For consistency purposes try using:
    seed = 841
    print "Seed = ", seed
    testX, testY, checkX, checkY = prepareData(X, Y, seed)

    theta, pi_1 = calculateThetaPi(testX, testY)

    predictedYs = predictYs(checkX, theta, pi_1)

    countCorrect = 0
    for i in range(predictedYs.shape[0]):
        if(predictedYs[i] == checkY[i]):
            countCorrect = countCorrect + 1
    print "Percentage guessed correctly: ", 1.0*countCorrect/predictedYs.shape[0]
    print "Percentage by guessing based on Wins/total: ", np.sum(testY)/testY.shape[0]

if __name__ == '__main__':
    main()