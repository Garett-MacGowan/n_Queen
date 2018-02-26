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

def costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen):
    targetColumn = unchosen[i]
    checkPositiveDiag = targetColumn + index
    checkNegativeDiag = index - targetColumn
    targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
    return targetCost, targetColumn

def greedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n):
    targetIndex = random.randint(0, len(unchosen) - 1)
    targetCost, targetColumn = costCheck(targetIndex, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
    if targetCost == currentCost:
        return targetColumn, currentCost
    else:
        newPotentialCost = n
        tempUnvisited = list(unchosen)
        while len(tempUnvisited) > 0:
            targetIndex = random.randint(0, len(tempUnvisited) - 1)
            targetCost, targetColumn = costCheck(targetIndex, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, tempUnvisited)
            if targetCost == currentCost:
                return targetColumn, currentCost
            else:
                if targetCost < newPotentialCost:
                    newPotentialCost = targetCost
                del(tempUnvisited[targetIndex])
        targetColumn, currentCost = greedHelper(newPotentialCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
        return targetColumn, currentCost

def createNChessBoard(n):
    boardMatrix = []
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

        '''
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
        '''

        boardMatrix.append(targetColumn)

    return boardMatrix[1:]

#def solveNQueen():

main()
