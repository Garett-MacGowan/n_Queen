import bisect
import random

'''
Author: Garett MacGowan
Date of Revision: March 2, 2018
'''

''' Function handles execution of the generation phase and repair phase for a set of n-queen
problems.
'''
def main():
    problemList = readProblemFile()
    solutionList = []
    for item in problemList:
        #print("Board " + str(item) + "x" + str(item))
        currentBoard, occupiedPositiveDiagonals, occupiedNegativeDiagonals = createNChessBoard(item)
        #visualizer(currentBoard, item)
        result = solveNQueen(currentBoard, item, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
        while result == False:
            #print("Failed")
            currentBoard, occupiedPositiveDiagonals, occupiedNegativeDiagonals = createNChessBoard(item)
            result = solveNQueen(currentBoard, item, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
        #print("SUCCESS")
        #visualizer(result, item)
        solutionList.append(result)
    writeSolutions(solutionList)

'''Function writes the solution lists to a file in the working directory called nqueens_out.txt
'''
def writeSolutions(solutionList):
    try:
        file = open("nqueens_out.txt", 'w')
    except IOError:
        print("Cannot open nqueens_out.txt")
    else:
        for board in solutionList:
            file.write(str(board) + '\n')
        file.close()

''' Function reads nqueens.txt which is expected to be in the working directory
of nqueens.py, in order to determine the list of n-queen problems that should
be solved.
'''
def readProblemFile():
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
        file.close()
    return(problemList)

''' Function helpes visualize the board in console.
'''
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
    print(" ")

''' Function counts the amount of target items in a sorted list.
'''
# Binary search via bisect library
def searchList(space, target):
    conflictCount = 0
    index = bisect.bisect_left(space, (target, ))
    while index != len(space) and space[index][0] == target:
        conflictCount += 1
        index += 1
    return conflictCount

''' Function determines amount of diagonal conflicts given a target column and row.
'''
def costCheck(column, row, occupiedPositiveDiagonals, occupiedNegativeDiagonals):
    checkPositiveDiag = column + row
    checkNegativeDiag = row - column
    targetCost = searchList(occupiedPositiveDiagonals, checkPositiveDiag) + searchList(occupiedNegativeDiagonals, checkNegativeDiag)
    return targetCost

''' Function determines column placement for a queen on a given row (index).
'''
def smallGreedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n):
    targetIndex = random.randint(0, len(unchosen) - 1)
    targetColumn = unchosen[targetIndex]
    targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
    if targetCost == currentCost:
        return targetColumn, currentCost
    else:
        newPotentialCost = n
        tempUnvisited = list(unchosen)
        while len(tempUnvisited) > 0:
            targetIndex = random.randint(0, len(tempUnvisited) - 1)
            targetColumn = unchosen[targetIndex]
            targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
            if targetCost == currentCost:
                return targetColumn, currentCost
            else:
                if targetCost < newPotentialCost:
                    newPotentialCost = targetCost
                del(tempUnvisited[targetIndex])
        targetColumn, currentCost = smallGreedHelper(newPotentialCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
        return targetColumn, currentCost

''' Function determines column placement for a queen on a given row (index), optimized for large n.
'''
def largeGreedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n):
    targetIndex = random.randint(0, len(unchosen) - 1)
    targetColumn = unchosen[targetIndex]
    targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
    if targetCost == currentCost:
        return targetColumn
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
                    targetColumn = unchosen[i]
                    targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i += 1
            else:
                # Search right to left in the content left of the target, inclusive of the target
                i = targetIndex
                while i > -1:
                    targetColumn = unchosen[i]
                    targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn
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
                        targetColumn = unchosen[i]
                        targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i += 1
                else:
                    # Search right to left in the content right of the target, inclusive of the target
                    i = len(unchosen) - 1
                    while i > targetIndex - 1:
                        targetColumn = unchosen[i]
                        targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn
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
                        targetColumn = unchosen[i]
                        targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i += 1
                else:
                    # Search right to left in the content right of the target, inclusive of the target
                    i = len(unchosen) - 1
                    while i > targetIndex - 1:
                        targetColumn = unchosen[i]
                        targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                        # If found, return it
                        if targetCost == currentCost:
                            return targetColumn
                        elif targetCost < newPotentialCost:
                            newPotentialCost = targetCost
                        i -= 1
            randomizer = random.randint(0, 1)
            if randomizer == 0:
                # Search left to right in the content left of the target, inclusive of the target
                i = 0
                while i < targetIndex + 1:
                    targetColumn = unchosen[i]
                    targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i += 1
            else:
                # Search right to left in the content left of the target, inclusive of the target
                i = targetIndex
                while i > -1:
                    targetColumn = unchosen[i]
                    targetCost = costCheck(targetColumn, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals)
                    # If found, return it
                    if targetCost == currentCost:
                        return targetColumn
                    elif targetCost < newPotentialCost:
                        newPotentialCost = targetCost
                    i -= 1
        # Recursively call greedHelper since no column satisfying the current cost was found
        targetColumn = largeGreedHelper(newPotentialCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
        return targetColumn

''' Function handles the initial board configuration phase.
'''
def createNChessBoard(n):
    board = []
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
        #print("%" + str(index/n*100))

        if index/n*100 <= 66:
            targetColumn = largeGreedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
        else:
            targetColumn, currentCost = smallGreedHelper(currentCost, occupiedPositiveDiagonals, occupiedNegativeDiagonals, unchosen, index, n)
            currentCost = 0
        # Remove selected column from the list of unchosen columns
        delIndex = bisect.bisect_left(unchosen, targetColumn)
        del unchosen[delIndex]

        positiveDiag = (index + targetColumn, index, targetColumn)
        negativeDiag = (index - targetColumn, index, targetColumn)
        insertionIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + targetColumn, ))
        occupiedPositiveDiagonals.insert(insertionIndex, positiveDiag)
        insertionIndex = bisect.bisect_left(occupiedNegativeDiagonals, (index - targetColumn, ))
        occupiedNegativeDiagonals.insert(insertionIndex, negativeDiag)

        board.append(targetColumn)
    return board, occupiedPositiveDiagonals, occupiedNegativeDiagonals

''' Function validates the conflict costs in conflictingQueens.
'''
def validateConflicts(conflictingQueens, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals):
    # Conflicting queens = (column, cost, row)
    if len(conflictingQueens) == 0:
        return conflictingQueens
    validatedConflictingQueens = []
    for i in range(len(conflictingQueens)):
        checkPositiveDiag = conflictingQueens[i][2] + conflictingQueens[i][0]
        checkNegativeDiag = conflictingQueens[i][2] - conflictingQueens[i][0]
        conflictCount = costCheck(conflictingQueens[i][0], conflictingQueens[i][2], occupiedPositiveDiagonals, occupiedNegativeDiagonals) + occupiedVerticals[conflictingQueens[i][0] - 1][0] - 3
        if conflictCount == 0:
            continue
        if conflictCount != conflictingQueens[i][1]:
            validatedConflictingQueens.append((conflictingQueens[i][0], conflictCount, conflictingQueens[i][2]))
            continue
        if conflictCount == conflictingQueens[i][1]:
            validatedConflictingQueens.append(conflictingQueens[i])
    return validatedConflictingQueens

''' Function removes queens from the occupiedVerticals structure.
'''
def removeFromVerticals (occupiedVerticals, column, row):
    columnOccupantIndices = occupiedVerticals[column][1]
    i = 0
    while i < len(columnOccupantIndices):
        if columnOccupantIndices[i] == row:
            del columnOccupantIndices[i]
            break
        i += 1
    occupiedVerticals[column][1] = columnOccupantIndices
    return occupiedVerticals

''' Function creates the list of conflictingQueens given a particular board.
'''
def checkConflicts(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals):
    conflictingQueens = []
    for index in range(1, n + 1):
        checkPositiveDiag = index + currentBoard[index - 1]
        checkNegativeDiag = index - currentBoard[index - 1]
        # Don't count self as conflict
        conflictCount = costCheck(currentBoard[index - 1], index, occupiedPositiveDiagonals, occupiedNegativeDiagonals) + occupiedVerticals[currentBoard[index - 1] - 1][0] - 3
        if conflictCount == 0:
            continue
        else:
            conflictingQueens.append((currentBoard[index - 1], conflictCount, index))
    return conflictingQueens

''' Function returns a list of tuples which represent queens which should be conflicting
to a particular reference point.
'''
def conflictHelper(space, target, row, column):
    conflictList = []
    index = bisect.bisect_left(space, (target, ))
    while index != len(space) and space[index][0] == target:
        if space[index][1] == row and space[index][2] == column:
            conflictList.append((space[index][1], space[index][2]))
        index += 1
    return conflictList

''' Function adds coflicting queens that are absent from conflictingQueens into conflictingQueens.
'''
def repairConflicts(column, row, conflictingQueens, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals):
    # Check for new vertical conflicts and add them to conflictingQueens if there are any
    # For each queen within the column,
    for i in range(len(occupiedVerticals[column - 1][1])):
        # If we are looking at the moved queen, skip it, it is already known to be a conflicting queen
        if occupiedVerticals[column - 1][1][i] == row:
            continue
        else:
            # if the queen is not in coflictingQueens, add it
            newConflict = (column, len(occupiedVerticals[column - 1][1]) - 1, occupiedVerticals[column - 1][1][i])
            found = False
            for item in conflictingQueens:
                if item[0] == column and item[2] == occupiedVerticals[column - 1][1][i]:
                    found = True
                    break
            if found == False:
                conflictingQueens.append(newConflict)
    # Check for diagonal conflicts and add them to conflictingQueens if there are any
    checkPositiveDiag = row + column
    checkNegativeDiag = row - column
    # positive and negative DiagPossibilities = (row, column) and represent possible conflicts
    positiveDiagPossibles = conflictHelper(occupiedPositiveDiagonals, checkPositiveDiag, row, column)
    negativeDiagPossibles = conflictHelper(occupiedNegativeDiagonals, checkNegativeDiag, row, column)
    # For each possible conflict, check if it already exists in conflictingQueens
    for pDiag in positiveDiagPossibles:
        # (column, cost, row)
        newConflict = (pDiag[1], 1, pDiag[0])
        found = False
        for item in conflictingQueens:
            # row, column
            if pDiag[0] == item[2] and pDiag[1] == item[0]:
                found = True
                break
        if found == False:
            conflictingQueens.append(newConflict)
    for nDiag in negativeDiagPossibles:
        newConflict = (nDiag[1], 1, nDiag[0])
        found = False
        for item in conflictingQueens:
            # row, column
            if nDiag[0] == item[2] and nDiag[1] == item[0]:
                found = True
                break
        if found == False:
            conflictingQueens.append(newConflict)
    return conflictingQueens

''' Function handles the repair phase for the n-queen problem.
'''
def solveNQueen(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals):
    maxSteps = n
    occupiedVerticals = []
    # Declare the ammount of occupants in each column, and the rows which are occupied in the column
    for _ in range(n):
        occupiedVerticals.append([1, []])
    for i in range(n):
        occupiedVerticals[currentBoard[i] - 1][1].append(i + 1)
    lastQueenMoved = None
    panicMode = False
    lastLenConflicting = None
    stuckCounter = 0
    conflictingQueens = checkConflicts(currentBoard, n, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals)
    sorted(conflictingQueens, key=lambda x: x[1], reverse = True)
    for _ in range(maxSteps):
        #print(len(conflictingQueens))
        if len(conflictingQueens) == 0:
            return currentBoard
        if stuckCounter == 25:
            panicMode = True
            #print("panic")
        if panicMode != True:
            conflictingIndex = 0
            selectedQueen = conflictingQueens[conflictingIndex][0]
            conflicted = conflictingQueens[conflictingIndex][1]
            if lastLenConflicting == None:
                lastLenConflicting = len(conflictingQueens)
            index = conflictingQueens[conflictingIndex][2]
        else:
            conflictingIndex = random.randint(0, len(conflictingQueens) - 1)
            selectedQueen = conflictingQueens[conflictingIndex][0]
            conflicted = conflictingQueens[conflictingIndex][1]
            index = conflictingQueens[conflictingIndex][2]

        if len(conflictingQueens) != lastLenConflicting:
            stuckCounter = 0
            lastLenConflicting = len(conflictingQueens)
        else:
            stuckCounter += 1
        columnDecider = []
        queenSwapped = False
        for column in range(1, n + 1):
            conflictCount = costCheck(column, index, occupiedPositiveDiagonals, occupiedNegativeDiagonals) + occupiedVerticals[column - 1][0]
            # don't count self as conflict
            if column == selectedQueen:
                conflictCount -= 3
            if conflictCount == 0:
                # Move the queen into the column and remove the old conflict indicators
                currentBoard[index - 1] = column

                positiveDiag = (index + column, index, column)
                negativeDiag = (index - column, index, column)
                insertionIndex = bisect.bisect_left(occupiedPositiveDiagonals, (index + column, ))
                occupiedPositiveDiagonals.insert(insertionIndex, positiveDiag)
                insertionIndex = bisect.bisect_left(occupiedNegativeDiagonals, (index - column, ))
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

                del conflictingQueens[conflictingIndex]

                queenSwapped = True
                break
            # Select next best column to move the queen to
            if conflictCount <= conflicted:
                columnDecider.append((column, conflictCount))
        if queenSwapped == True:
            #visualizer(currentBoard, n)
            continue
        sorted(columnDecider, key=lambda x: x[1])
        columnChoices = []
        requiredConflicts = columnDecider[0][1]
        for item in columnDecider:
            if item[1] == requiredConflicts:
                columnChoices.append(item)
            else:
                break
        selectedColumn = columnChoices[random.randint(0, len(columnChoices) - 1)]
        currentBoard[index - 1] = selectedColumn[0]

        positiveDiag = (index + selectedColumn[0], index, selectedColumn[0])
        negativeDiag = (index - selectedColumn[0], index, selectedColumn[0])
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

        del conflictingQueens[conflictingIndex]
        conflictingQueens.append((selectedColumn[0], selectedColumn[1], index))

        conflictingQueens = repairConflicts(selectedColumn[0], index, conflictingQueens, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals)
        conflictingQueens = validateConflicts(conflictingQueens, occupiedPositiveDiagonals, occupiedNegativeDiagonals, occupiedVerticals)

        sorted(conflictingQueens, key=lambda x: x[1], reverse = True)
        #visualizer(currentBoard, n)
    return False

main()
