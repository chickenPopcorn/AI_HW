import math
from Grid import Grid

BOARDSIZE = 4


# This is the gradient I started with
# however It's performance was subpar

GRADIENT = [
    [[ 15,  14, 13,  12],
     [ 8,  9,  10, 11],
     [ 4,  5, 6, 7],
     [ 3, 2, 1, 0]],

    [[3, 4, 8, 15],
     [2, 5, 9, 14],
     [1, 6, 10, 13],
     [0, 7, 11, 12]],

    [[0, 1, 2, 3],
     [7, 6, 5, 4],
     [11, 10, 9, 8],
     [12, 13, 14, 15]],

    [[12, 11, 7, 0],
     [13, 10, 6, 1],
     [14, 9, 5, 2],
     [15, 8, 4, 3]]
    ]
'''

GRADIENT = [
    [[1357, 1219, 1028, 999],
    [999, 888, 767, 724],
    [606, 562, 371, 161],
    [125, 99, 57, 33]],

    [[125, 606, 999, 1357],
    [99, 562, 888, 1219],
    [57, 371, 767, 1028],
    [33, 161, 724, 999]],

    [[33, 57, 99, 125],
    [161, 371, 562, 606],
    [724, 767, 888, 999],
    [999, 1028, 1219, 1357]],

    [[999, 724, 161, 33],
    [1028, 767, 371, 57],
    [1219, 888, 562, 99],
    [1357, 999, 606, 125]]
    ]
'''

class Heuristic:

    @staticmethod
    def calculateHeuristic(grid):


        smoothWeight = 0.1
        monoWeight = 1.0
        emptyWeight = 2.7
        maxWeight = 1.0
        maxEdgeWeight = 1.0
        numOfEmptyCells = Heuristic.countAvailableCells(grid)

        if numOfEmptyCells != 0:
            emptyValue =math.log(numOfEmptyCells)
        else:
            emptyValue = 0

        calculatedScore = Heuristic.smoothness(grid) * smoothWeight + \
                          Heuristic.monotonicity(grid) * monoWeight + \
                          emptyValue * emptyWeight+ \
                          grid.getMaxTile() * maxWeight + \
                          Heuristic.maxOnEdge(grid) * maxEdgeWeight

        return calculatedScore
        return  Heuristic.monotonicity(grid) * monoWeight +\
        Heuristic.gradient(grid)* 0.1
        '''
        return Heuristic.gradient(grid)
        '''

    @staticmethod
    def gradient(grid):
        values = [0, 0, 0, 0]
        for i in range(len(GRADIENT)):
            for row in range(BOARDSIZE):
                for column in range(BOARDSIZE):
                    cell = grid.map[row][column]
                    if cell != 0:
                        values[i] += math.log(GRADIENT[i][row][column])/math.log(2) * cell
        return max(values)


    @staticmethod
    def maxOnEdge(grid):
        ls = [cell for row in grid.map for cell in row]
        ls.sort()
        ls = ls[-2:]
        edge = [0, 3]
        count = 2
        for row in edge:
            for cell in grid.map[row]:
                if cell == ls[1]:
                    count += 1
                elif cell == ls[0]:
                    count += 0.3

        for column in edge:
            for row in grid.map:
                if row[column] == ls[1]:
                    count += 1
                elif row[column] == ls[0]:
                    count += 0.5
        return math.log(count * sum(ls))/math.log(2)-1

    @staticmethod
    def monotonicity(grid):
        totals = [0,0,0,0]
        for row in range(BOARDSIZE):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[row][next] == 0:
                    next += 1
                if next >= 4:
                    next  -= 1
                currentValue = math.log(grid.map[row][current])/math.log(2) \
                        if grid.map[row][current] != 0 else 0
                nextValue = math.log(grid.map[row][next])/math.log(2) \
                        if grid.map[row][next] != 0 else 0
                if currentValue > nextValue:
                    totals[0] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[1] += currentValue - nextValue
                current = next;
                next += 1

        for column in range(BOARDSIZE):
            current = 0
            next = current + 1
            while next < 4:
                while next < 4 and grid.map[next][column] == 0:
                    next += 1
                if next >= 4:
                    next  -= 1
                currentValue = math.log(grid.map[current][column])/math.log(2) \
                        if grid.map[current][column] != 0 else 0
                nextValue = math.log(grid.map[next][column])/math.log(2) \
                        if grid.map[next][column] != 0 else 0
                if currentValue > nextValue:
                    totals[2] += nextValue - currentValue
                elif nextValue > currentValue:
                    totals[3] += currentValue - nextValue
                current = next;
                next += 1

        return max(totals[0], totals[1]) + max(totals[2], totals[3])

    @staticmethod
    def smoothness(grid):
        smoothvalue = 0
        for x in xrange(grid.size):
            for y in xrange(grid.size):
                if grid.map[x][y]!=0:
                    v = math.log(grid.map[x][y])/math.log(2)
                    fary = y+1
                    while (fary<grid.size) and (grid.map[x][fary]==0):
                        fary = fary+1
                    if fary<grid.size:
                        v1 = math.log(grid.map[x][y])/math.log(2)
                        smoothvalue = smoothvalue-abs(v1-v)
                    farx = x+1
                    while (farx<grid.size) and (grid.map[farx][y]==0):
                        farx = farx+1
                    if farx<grid.size:
                        v1 = math.log(grid.map[farx][y])/math.log(2)
                        smoothvalue = smoothvalue-abs(v1-v)
        return smoothvalue


    @staticmethod
    def countAvailableCells(grid):
        count = 0
        for i in range(len(grid.map)):
            for n in range(len(grid.map[i])):
                if grid.map[i][n] == 0:
                    count += 1
        return count

if __name__=="__main__":
    g = Grid()
    g.map[0] = [16, 2, 8, 1024]
    g.map[1] = [8, 4, 64, 2]
    g.map[2] = [4, 2, 32, 64]
    g.map[3] = [0, 4, 2, 8]

    # had score 3194
    print Heuristic.calculateHeuristic(g)

    g.map[0] = [128, 0, 0, 0]
    g.map[1] = [64, 0, 0, 0]
    g.map[2] = [2, 0, 0, 0]
    g.map[3] = [0, 0, 0, 32]

    print Heuristic.calculateHeuristic(g)

    g.map[0] = [512, 0, 0, 0]
    g.map[1] = [128, 128, 0, 0]
    g.map[2] = [0, 0, 64, 0]
    g.map[3] = [0, 0, 0, 32]

    print Heuristic.calculateHeuristic(g)
