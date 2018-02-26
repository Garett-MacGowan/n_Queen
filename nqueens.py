import bisect
import time

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

def greedHelper(occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals, index, n):
    # If there have been no queens placed, place the first queen at col 1
    if len(occupiedVerticals) == 0:
        return 1
    else:
        # Consider column one over from last queen placed
        targetColumn = occupiedVerticals[-1]
        if targetColumn >= n:
            targetColumn = 1
        else:
            targetColumn += 1
        checkPositiveDiag = targetColumn + index
        checkNegativeDiag = index - targetColumn
        while searchList(occupiedPositiveDiagonals, checkPositiveDiag) == True or searchList(occupiedNegativeDiagonals, checkNegativeDiag) == True:
            targetColumn = targetColumn + 1
            if targetColumn >= n:
                targetColumn = 1
            checkPositiveDiag = targetColumn + index
            checkNegativeDiag = index - targetColumn
        return targetColumn

def createNChessBoard(n):
    # Filling 0 indice with -1 (will be unused), helps with efficiency
    boardMatrix = [-1]
    # For negative diagonals: y-x (row - col) = occupiedDiagonals
    # For positive diagonals: y+x (row + col) = occupiedDiagonals
    occupiedPositiveDiagonals = []
    occupiedNegativeDiagonals = []
    occupiedVerticals = []
    for index in range(1, n+1):
        print("%" + str(index/n*100))
        targetColumn = greedHelper(occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals, index, n)
        '''
        if (n % (n/4)) == 0:
            occupiedNegativeDiagonals = []
            occupiedPositiveDiagonals = []
            occupiedVerticals = []
        '''
        #print(targetColumn)
        bisect.insort_left(occupiedVerticals, targetColumn)
        bisect.insort_left(occupiedPositiveDiagonals, index + targetColumn)
        bisect.insort_left(occupiedNegativeDiagonals, index - targetColumn)
        boardMatrix.append(targetColumn)
    print(occupiedPositiveDiagonals)
    print(len(occupiedPositiveDiagonals))
    print(occupiedNegativeDiagonals)
    print(len(occupiedNegativeDiagonals))
    return boardMatrix[1:]

#def solveNQueen():

main()
