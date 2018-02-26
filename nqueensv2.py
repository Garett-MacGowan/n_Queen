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
    index = bisect.bisect_left(space, target)
    if index != len(space) and space[index] == target:
        return True
    else:
        return False

def greedHelper(occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals, index, currentConflict):
    # Assume the current lowest conflict item is the first column
    currentLeastConf = [(currentConflict[0], 1)]
    for i in range(1, len(currentConflict)):
        # If the conflict value of the current square is lower than the current lowest conflict square, fix the currentSmallList to represent this
        if currentConflict[i] < currentLeastConf[0][0]:
            currentLeastConf = [(currentConflict[i], i + 1)]
        # If the conflict value of the current square is as low as the current lowest conflict square, add it to the small conflict list
        elif currentConflict[i] == currentLeastConf[0][0]:
            currentLeastConf.append((currentConflict[i], i + 1))
    # Randomly select the one of the least conflicting columns to place a queen from the list of least onflicting columns
    targetColumn = random.choice(currentLeastConf)[1]

    occupiedVerticals.append(targetColumn)
    occupiedPositiveDiagonals.append(index + targetColumn)
    occupiedNegativeDiagonals.append(index - targetColumn)

    # Determine the nextConflict vector
    nextConflict = []
    # Vector is initially all zeros
    for _ in range(len(currentConflict)):
        nextConflict.append(0)
    # Add 1 to vector components containing queens
    for item in occupiedVerticals:
        nextConflict[item - 1] += 1
    for item in occupiedPositiveDiagonals:
        conflictColumn = item - index - 1
        #print(conflictColumn)
        if conflictColumn < 1 or conflictColumn >= len(currentConflict):
            continue
        nextConflict[conflictColumn - 1] += 1
    for item in occupiedNegativeDiagonals:
        conflictColumn = index - item + 1
        #print(conflictColumn)
        if conflictColumn < 1 or conflictColumn >= len(currentConflict):
            continue
        nextConflict[conflictColumn - 1] += 1

    return targetColumn, nextConflict

def createNChessBoard(n):
    # Filling 0 indice with -1 (will be unused), helps with efficiency
    boardMatrix = [-1]
    # For negative diagonals: y-x (row - col) = occupiedDiagonals
    # For positive diagonals: y+x (row + col) = occupiedDiagonals
    occupiedPositiveDiagonals = []
    occupiedNegativeDiagonals = []
    occupiedVerticals = []
    # All values in the initial currentConflict vector are 0 since no queens have been placed
    currentConflict = []
    for _ in range(n):
        currentConflict.append(0)
    for index in range(1, n+1):
        print("%" + str(index/n*100))
        targetColumn, currentConflict = greedHelper(occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals, index, currentConflict)

        boardMatrix.append(targetColumn)

    return boardMatrix[1:]

#def solveNQueen():

main()
