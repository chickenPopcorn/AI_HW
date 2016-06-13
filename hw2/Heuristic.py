import math
from Grid import Grid

BOARDSIZE = 4
directionVectors = (UP_VEC, DOWN_VEC, LEFT_VEC, RIGHT_VEC) = ((-1, 0), (1, 0), (0, -1), (0, 1))

class Heuristic:

    @staticmethod
    def calculateHeuristic(grid):

        smoothWeight = 0.1
        mono2Weight = 1.0
        emptyWeight = 2.7
        maxWeight = 1.0

        numOfEmptyCells = Heuristic.countAvailableCells(grid)
        calculatedScore = Heuristic.smoothness(grid) * smoothWeight + \
                          Heuristic.monotonicytiy2(grid) * mono2Weight + \
                          math.log(numOfEmptyCells) if numOfEmptyCells != 0 \
                          else 0 * emptyWeight+ \
                          grid.getMaxTile() * maxWeight

        return calculatedScore

    @staticmethod
    def monotonicytiy2(grid):
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

        '''
        smoothness = 0
        for rown in range(BOARDSIZE):
            for column in range(BOARDSIZE):
                cell = grid.map[row][column]
                if cell > 0:
                    value = math.log(cell) / math.log(2)
                    target = directionVectors[1]
                    targetCell = Heuristic.findFarthestAway()

                    if target > 0:
                        smoothness -= abs(value - math.log(target)/math.log(2))
        return smoothness
        '''

    @staticmethod
    def findFarthestAway(grid, cell, vector):
        previous = cell
        cell = [previous[0] + vector[0], previous[1] + vector[1]]
        while grid.gridInsertOk(cell) and grid.map[cell[0]][cell[1]] == 0:
            previous = cell
            cell = [previous[0] + vector[0], previous[1] + vector[1]]

        if self.gridInsertOk(cell) == False:
            cell = previous

        return cell

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
    g.map[0] = [0, 0, 64, 0]
    g.map[1] = [0, 128, 0, 0]
    g.map[2] = [0, 2, 0, 0]
    g.map[3] = [32, 0, 0, 0]


    print Heuristic.calculateHeuristic(g)

    g.map[0] = [128, 64, 0, 0]
    g.map[1] = [32, 0, 0, 0]
    g.map[2] = [2, 0, 0, 0]
    g.map[3] = [0, 0, 0, 0]

    print Heuristic.calculateHeuristic(g)
