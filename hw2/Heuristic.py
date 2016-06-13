import math
from Grid import Grid

BOARDSIZE = 4
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))
'''
GRADIENT = [
    [[ 3,  2,  1,  0],
     [ 2,  1,  0, -1],
     [ 1,  0, -1, -2],
     [ 0, -1, -2, -3]],
    [[ 0,  1,  2,  3],
     [-1,  0,  1,  2],
     [-2, -1,  0,  1],
     [-3, -2, -1, -0]],
    [[ 0, -1, -2, -3],
     [ 1,  0, -1, -2],
     [ 2,  1,  0, -1],
     [ 0, -1, -2, -3]],
    [[-3, -2, -1,  0],
     [-2, -1,  0,  1],
     [-1,  0,  1,  2],
     [ 0,  1,  2,  3]]
    ]
'''
GRADIENT = [
    [[ 0.135759,  0.121925,  0.102812,  0.099937],
     [ 0.09997992,  0.0888405,  0.076711, 0.0724143],
     [ 0.060654,  0.0562579, 0.037116, 0.0161889],
     [ 0.0125498, 0.00992495, 0.00575871, 0.00335193]]]

'''
    [[0.0125498, 0.060654, 0.09997992, 0.135759],
     [0.00992495, 0.0562579, 0.0888405, 0.121925],
     [0.00575871, 0.037116, 0.076711, 0.102812],
     [0.00335193, 0.0161889, 0.0724143, 0.099937]],

    [[0.00335193, 0.00575871, 0.00992495, 0.0125498],
     [0.0161889, 0.037116, 0.0562579, 0.060654],
     [0.0724143, 0.076711, 0.0888405, 0.09997992],
     [0.099937, 0.102812, 0.121925, 0.135759]],

    [[0.099937, 0.0724143, 0.0161889, 0.00335193],
     [0.102812, 0.076711, 0.037116, 0.00575871],
     [0.121925, 0.0888405, 0.0562579, 0.00992495],
     [0.135759, 0.09997992, 0.060654, 0.0125498]]
    ]
    '''



class Heuristic:

    @staticmethod
    def calculateHeuristic(grid):

        '''
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

    @staticmethod
    def gradient(grid):
        values = [0, 0, 0, 0]
        for i in range(len(GRADIENT)):
            for row in range(BOARDSIZE):
                for column in range(BOARDSIZE):
                    cell = grid.map[row][column]
                    if cell != 0:
                        values[i] += GRADIENT[i][row][column] * cell
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
