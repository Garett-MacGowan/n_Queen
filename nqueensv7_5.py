import bisect
import time
import random

def main():
    problemList = readProblemRequestor()
    solutionMatrices = []
    for item in problemList:
        print("Board " + str(item) + "x" + str(item))
        currentBoard, occupiedPositiveDiagonals, occupiedNegativeDiagonals = createNChessBoard(item)
        #print(currentBoard)
        visualizer(currentBoard, item)
        result = solveNQueen(currentBoard, item, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
        if result == False:
            print("Failed")
        else:
            visualizer(currentBoard, item)
            print("SUCCESS")
        #solutionMatrices.append(solveNQueen(currentBoard, item))

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

def visualizer(board, n):
    i = 0
    currentRow = []
    while i < n:
        for _ in range(n-1):
            currentRow.append(" ")
        currentRow.insert(board[i] - 1, "X")
        print(currentRow)
        currentRow = []
        i += 1

# Binary search via bisect library
def searchList(space, target):
    conflictCount = 0
    index = bisect.bisect_left(space, (target, ))
    while index != len(space) and space[index][0] == target:
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
        # Since the targetCost is more costly than our curentCost, try and find a new targetColumn that has a targetCost matching currentCost
        randomizer = random.randint(0, 1)
        if randomizer == 0:
            rrandomizer = random.randint(0, 1)
            if randomizer == 0:
                # Search left to right through the content left of the target, inclusive of the target
                i = 0
                while i < targetIndex + 1:
                    targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn, currentCost
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i += 1
            else:
                # Search right to left in the content left of the target, inclusive of the target
                i = targetIndex
                while i > -1:
                    targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn, currentCost
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i -= 1
            # If the randomly selected column is the last column in the list of unselected columns, don't try and search to the right of it
            if targetIndex != len(unchosen) - 1:
                randomizer = random.randint(0, 1)
                if randomizer == 0:
                    # Search left to right in the content right of the target, inclusive of the target
                    i = targetIndex
                    while i < len(unchosen):
                        targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn, currentCost
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i += 1
                else:
                    # Search right to left in the content right of the target, inclusive of the target
                    i = len(unchosen) - 1
                    while i > targetIndex - 1:
                        targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn, currentCost
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i -= 1
        else:
            # If the randomly selected column is the last column in the list of unselected columns, don't try and search after it
            if targetIndex != len(unchosen) - 1:
                randomizer = random.randint(0, 1)
                if randomizer == 0:
                    # Search left to right in the content right of the target, inclusive of the target
                    i = targetIndex
                    while i < len(unchosen):
                        targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn, currentCost
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i += 1
                else:
                    # Search right to left in the content right of the target, inclusive of the target
                    i = len(unchosen) - 1
                    while i > targetIndex - 1:
                        targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn, currentCost
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i -= 1
            randomizer = random.randint(0, 1)
            if randomizer == 0:
                # Search left to right in the content left of the target, inclusive of the target
                i = 0
                while i < targetIndex + 1:
                    targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn, currentCost
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i += 1
            else:
                # Search right to left in the content left of the target, inclusive of the target
                i = targetIndex
                while i > -1:
                    targetCost, targetColumn = costCheck(i, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn, currentCost
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i -= 1
        # Recursively call greedHelper since no column satisfying the current cost was found
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
        del unchosen[delIndex]

        positiveDiag = (index + targetColumn, index)
        negativeDiag = (index - targetColumn, index)
        insertionIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + targetColumn, ))
        occupiedPositiveDiagonals.insert(insertionIndex, positiveDiag)
        insertionIndex = bisect.bisect_left(occupiedNegativeDiagonals, (index - targetColumn, ))
        occupiedNegativeDiagonals.insert(insertionIndex, negativeDiag)

        '''
        # Removing obsolete diagonal indicators
        '''

        boardMatrix.append(targetColumn)
    return boardMatrix, occupiedPositiveDiagonals, occupiedNegativeDiagonals

def validateConflicts(conflictingQueens, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals):
    if len(conflictingQueens) == 0:
        return conflictingQueens
    validatedConflictingQueens = []
    for i in range(len(conflictingQueens)):
        checkPositiveDiag = conflictingQueens[i][2] + conflictingQueens[i][0]
        checkNegativeDiag = conflictingQueens[i][2] - conflictingQueens[i][0]
        conflictCount = searchList(occupiedPositiveDiagonals, checkPositiveDiag) - 1 + searchList(occupiedNegativeDiagonals, checkNegativeDiag) - 1 + occupiedVerticals[conflictingQueens[i][0] - 1][0] - 1
        if conflictCount == 0:
            continue
        if conflictCount != conflictingQueens[i][1]:
            validatedConflictingQueens.append((conflictingQueens[i][0], conflictCount, conflictingQueens[i][2]))
            continue
        if conflictCount == conflictingQueens[i][1]:
            validatedConflictingQueens.append(conflictingQueens[i])

    return validatedConflictingQueens

def checkConflicts(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals):
    conflictingQueens = []
    for index in range(1, n + 1):
        checkPositiveDiag = index + currentBoard[index - 1]
        checkNegativeDiag = index - currentBoard[index - 1]
        # Don't count self as conflict
        conflictCount = searchList(occupiedPositiveDiagonals, checkPositiveDiag) - 1 + searchList(occupiedNegativeDiagonals, checkNegativeDiag) - 1 + occupiedVerticals[currentBoard[index - 1] - 1][0] - 1
        if conflictCount <= 0: ##################################################################### Why is this producing negative
            continue
        else:
            conflictingQueens.append((currentBoard[index - 1], conflictCount, index))
    return conflictingQueens

def removeFromVerticals (occupiedVerticals, column, index):
    columnOccupantIndices = occupiedVerticals[column][1]
    i = 0
    while i < len(columnOccupantIndices):
        if columnOccupantIndices[i] == index:
            del columnOccupantIndices[i]
            break
        i += 1
    occupiedVerticals[column][1] = columnOccupantIndices
    return occupiedVerticals

def solveNQueen(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals):
    maxSteps = 25
    occupiedVerticals = []
    # Declare the ammount of occupants in each column, and the rows which are occupied in the column
    for _ in range(n):
        occupiedVerticals.append([1, []])
    for i in range(n):
        occupiedVerticals[currentBoard[i] - 1][1].append(i + 1)
    conflictingQueens = checkConflicts(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals)
    for _ in range(maxSteps):
        conflictingQueens = checkConflicts(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals)
        #print(len(conflictingQueens))
        if len(conflictingQueens) == 0:
            return currentBoard
        conflictingIndex = random.randint(0, len(conflictingQueens) - 1)
        selectedQueen = conflictingQueens[conflictingIndex][0]
        conflicted = conflictingQueens[conflictingIndex][1]
        index = conflictingQueens[conflictingIndex][2]
        print("Queen and Index selected")
        print(selectedQueen)
        print(index)
        # Maybe change index to be descending
        columnDecider = []
        queenSwapped = False
        for column in range(1, n + 1):
            checkPositiveDiag = column + index
            checkNegativeDiag = index - column
            #print(occupiedVerticals[column - 1][0])
            conflictCount = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag) + occupiedVerticals[column - 1][0]
            # don't count self as conflict
            if column == selectedQueen:
                conflictCount -= 3
            print("This is the conflictCount")
            print(conflictCount)
            if conflictCount == 0:
                # Move the queen into the column and remove the old conflict indicators
                currentBoard[index - 1] = column

                positiveDiag = (index + column, index)
                negativeDiag = (index - column, index)
                insertionIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + column, ))
                occupiedPositiveDiagonals.insert(insertionIndex, positiveDiag)
                insertionIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index - column, ))
                occupiedNegativeDiagonals.insert(insertionIndex, negativeDiag)

                occupiedVerticals[column - 1][0] += 1
                # Append the index for use in tracing new conflicting queens
                occupiedVerticals[column - 1][1].append(index)

                delIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + selectedQueen, ))
                del occupiedPositiveDiagonals[delIndex]
                delIndex = bisect.bisect_left(occupiedNegativeDiagonals, (index - selectedQueen, ))
                del occupiedNegativeDiagonals[delIndex]

                occupiedVerticals[selectedQueen - 1][0] -= 1
                occupiedVerticals = removeFromVerticals(occupiedVerticals, selectedQueen - 1, index)
                print("Here are occupied verticals")
                print(occupiedVerticals)
                queenSwapped = True
                break
            # Select next best column to move the queen to
            if conflictCount <= conflicted:
                columnDecider.append((column, conflictCount))
        if queenSwapped == True:
            print("This is conflicting Queens")
            print(conflictingQueens)
            print("this is positiveDiag")
            print(occupiedPositiveDiagonals)
            print("this is negativeDiag")
            print(occupiedNegativeDiagonals)
            continue
        sorted(columnDecider, key=lambda x: x[1])
        columnChoices = []
        requiredConflicts = columnDecider[0][1]
        for item in columnDecider:
            if item[1] == requiredConflicts:
                columnChoices.append(item)
            else:
                break
        print("column choices to move to")
        print(columnChoices)
        selectedColumn = columnChoices[random.randint(0, len(columnChoices) - 1)]
        currentBoard[index - 1] = selectedColumn[0]

        positiveDiag = (index + selectedColumn[0], index)
        negativeDiag = (index - selectedColumn[0], index)
        insertionIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + selectedColumn[0], ))
        occupiedPositiveDiagonals.insert(insertionIndex, positiveDiag)
        insertionIndex = bisect.bisect_left(occupiedNegativeDiagonals, (index - selectedColumn[0], ))
        occupiedNegativeDiagonals.insert(insertionIndex, negativeDiag)

        occupiedVerticals[selectedColumn[0] - 1][0] += 1
        # Append the index for use in tracing new conflicting queens
        occupiedVerticals[selectedColumn[0] - 1][1].append(index)

        delIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + selectedQueen, ))
        del occupiedPositiveDiagonals[delIndex]
        delIndex = bisect.bisect_left(occupiedNegativeDiagonals, (index - selectedQueen, ))
        del occupiedNegativeDiagonals[delIndex]

        occupiedVerticals[selectedQueen - 1][0] -= 1
        occupiedVerticals = removeFromVerticals(occupiedVerticals, selectedQueen - 1, index)
        print("Here are occupied verticals")
        print(occupiedVerticals)
        print()
        print("These are the conflicting Queens")
        print(conflictingQueens)
        print("this is positiveDiag")
        print(occupiedPositiveDiagonals)
        print("this is negativeDiag")
        print(occupiedNegativeDiagonals)
        visualizer(currentBoard, n)
        time.sleep(0.25)
    return False

main()
