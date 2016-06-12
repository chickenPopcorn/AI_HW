from Grid import Grid
import copy
import math
import time
import random
from random import randint
BOARDSIZE = 4
PLAYER = True
COMPUTER = False
POSIBILETILEVALUE= [2, 4]

class MinMaxNode:

    @staticmethod
    def makeGridDirect(grid, direct):
        newGrid = grid.clone()
        newGrid.move(direct)
        return newGrid

    @staticmethod
    def makeGridCell(grid, pos, value):
        newGrid = grid.clone()
        newGrid.insertTile(pos, value)
        return newGrid

    @staticmethod
    def countAvailableCells(grid):
        count = 0
        for i in range(len(grid.map)):
            for n in range(len(grid.map[i])):
                if grid.map[i][n] == 0:
                    count += 1
        return count

    @staticmethod
    def calculateHeuristic(grid):
        l = [cell for row in grid.map for cell in row]
        l.sort()
        topTiles = sum(l[-4:])
        calculatedScore = (topTiles*0.8 +
                           5000*MinMaxNode.countAvailableCells(grid) +
                           2*MinMaxNode.calculatedWeightedDist(grid))

        return calculatedScore

    @staticmethod
    def calculatedWeightedDist(grid):
        weightedDist = 0
        for row in range(BOARDSIZE):
            for column in range(BOARDSIZE):
                weightedDist += grid.map[row][column]*(row-column)*3.0
        return weightedDist

    @staticmethod
    def __str__(grid):
        string = "-----------------\n"
        for i in range(len(grid.map)):
            for n in range(len(grid.map[i])):
                string += str(grid.map[i][n]) + " "
            string += "\n"
        return string

    @staticmethod
    def alphabeta(grid, depth, alpha, beta, player):
        direct = -1
        score = 0
        if depth == 0:
            return -1, MinMaxNode.calculateHeuristic(grid)
        if player:
            moves = grid.getAvailableMoves()
            if len(moves) == 0:
                direct, score

            for d in moves:
                child = MinMaxNode.makeGridDirect(grid, d)
                score = MinMaxNode.alphabeta(child, depth-1, alpha, beta, False)[1]
                if alpha < score or score == -float('inf'):
                    direct = d
                alpha = max(alpha,score )
                if beta <= alpha:
                    break
            score = alpha

        else:
            cell = random.choice( grid.getAvailableCells())
            if not cell:
                return -1, score
            for value in POSIBILETILEVALUE :
                child = MinMaxNode.makeGridCell(grid, cell, value)
                score = MinMaxNode.alphabeta(child, depth-1, alpha, beta,
                                                     True)[1]

                beta = min(beta, score)
            score = beta
        return direct, score

    @staticmethod
    def getBestMove(grid, depth):
         result = MinMaxNode.alphabeta(grid, depth, -float('inf'), float('inf'), True)
         return result[0]

if __name__ == "__main__":
    g = Grid()
    g.map[0] = [0, 0, 0, 0]
    g.map[1] = [0, 2, 0, 0]
    g.map[2] = [0, 0, 0, 0]
    g.map[3] = [0, 0, 0, 0]

    print MinMaxNode.calculateHeuristic(g)
    start = time.time()
    print MinMaxNode.getBestMove(g, 12 )
    print time.time()-start

