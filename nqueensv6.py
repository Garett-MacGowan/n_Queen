import bisect
import time
import random

def main():
    problemList = readProblemRequestor()
    solutionMatrices = []
    for item in problemList:
        currentBoard = createNChessBoard(item)
        print("Board " + str(item) + "x" + str(item))
        print(currentBoard)

''' Function reads nqueens.txt which is expected to be in the working directory
of nqueens.py, in order to determine the list of n-queen problems that should
be solved.
'''
def readProblemRequestor():
    problemList = []
    try:
        file = open("nqueens.txt", 'r')
    except IOError:
        print("Cannot open nqueens.txt")
    else:
        for line in file:
            # Converting string to integer, there should only be integers as input
            currentLine = int(line.strip('\n'))
            # Ensuring a chess board of at least 4x4 squares
            if currentLine < 4:
                continue
            problemList.append(currentLine)
    return(problemList)

# Binary search via bisect library
def searchList(space, target):
    conflictCount = 0
    index = bisect.bisect_left(space, target)
    while index != len(space) and space[index] == target:
        conflictCount += 1
        index += 1
    return conflictCount

def greedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n):
    targetIndex = random.randint(0, len(unchosen) - 1)
    targetColumn = unchosen[targetIndex]
    checkPositiveDiag = targetColumn + index
    checkNegativeDiag = index - targetColumn
    targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
    if targetCost == currentCost:
        return targetColumn, currentCost
    else:
        newPotentialCost = n
        # Since the targetCost is more costly than our curentCost, try and find a new targetColumn that has a targetCost matching currentCost
        randomizer = random.randint(0, 1)
        if randomizer == 0:
            for i in range(0, targetIndex + 1):
                targetColumn = unchosen[i]
                checkPositiveDiag = targetColumn + index
                checkNegativeDiag = index - targetColumn
                targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
                # If found, return it
                if targetCost == currentCost:
                    return targetColumn, currentCost
                elif targetCost < newPotentialCost:
                    newPotentialCost = targetCost
            # If the randomly selected column is the last column in the list of unselected columns, don't try and search after it
            if targetIndex != len(unchosen) - 1:
                for i in range(targetIndex + 1, len(unchosen)):
                    targetColumn = unchosen[i]
                    checkPositiveDiag = targetColumn + index
                    checkNegativeDiag = index - targetColumn
                    targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn, currentCost
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
        else:
            # If the randomly selected column is the last column in the list of unselected columns, don't try and search after it
            if targetIndex != len(unchosen) - 1:
                for i in range(targetIndex + 1, len(unchosen)):
                    targetColumn = unchosen[i]
                    checkPositiveDiag = targetColumn + index
                    checkNegativeDiag = index - targetColumn
                    targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn, currentCost
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
            for i in range(0, targetIndex + 1):
                targetColumn = unchosen[i]
                checkPositiveDiag = targetColumn + index
                checkNegativeDiag = index - targetColumn
                targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
                # If found, return it
                if targetCost == currentCost:
                    return targetColumn, currentCost
                elif targetCost < newPotentialCost:
                    newPotentialCost = targetCost

        #print(unchosen)
        #print(newPotentialCost)
        # Now we have new currentCost (newPotentialCost) and a new list of competitve unchosen columns so we can recursively call greedyHelper()
        targetColumn, currentCost = greedHelper(newPotentialCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
        return targetColumn, currentCost

def createNChessBoard(n):
    # Filling 0 indice with -1 (will be unused), helps with efficiency
    boardMatrix = [-1]
    # For negative diagonals: y-x (row - col) = occupiedDiagonals
    # For positive diagonals: y+x (row + col) = occupiedDiagonals
    occupiedPositiveDiagonals = []
    occupiedNegativeDiagonals = []
    unchosen = []
    for column in range(1, n + 1):
        unchosen.append(column)
    # We know the initial number of conflicts in each column will be zero, so the current cost to target is zero
    currentCost = 0
    for index in range(1, n + 1):
        print("%" + str(index/n*100))

        targetColumn, currentCost = greedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
        # Remove selected column from the list of unchosen columns
        delIndex = bisect.bisect_left(unchosen, targetColumn)
        del(unchosen[delIndex])

        bisect.insort_left(occupiedPositiveDiagonals, index + targetColumn)
        bisect.insort_left(occupiedNegativeDiagonals, index - targetColumn)

        # Removing obsolete diagonal indicators
        positivesObsolete = index + 1
        positiveLength = len(occupiedPositiveDiagonals)
        i = 0
        while i < positiveLength:
            if occupiedPositiveDiagonals[i] <= positivesObsolete:
                del occupiedPositiveDiagonals[i]
                positiveLength -= 1
            else:
                break
        negativesObsolete = (-1*n) + index
        negativeLength = len(occupiedNegativeDiagonals)
        i = 0
        while i < negativeLength:
            if occupiedNegativeDiagonals[i] <= negativesObsolete:
                del occupiedNegativeDiagonals[i]
                negativeLength -= 1
            else:
                break

        boardMatrix.append(targetColumn)

    return boardMatrix[1:]

#def solveNQueen():

main()
