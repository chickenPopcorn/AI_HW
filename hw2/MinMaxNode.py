from Grid import Grid
import copy
import math
import time
from Heuristic import Heuristic
import random

BOARDSIZE = 4
PLAYER = True
COMPUTER = False
POSIBILETILEVALUE= [2, 4]

import sys

sys.setrecursionlimit(400)
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
            return -1, Heuristic.calculateHeuristic(grid)
        if player:
            moves = grid.getAvailableMoves()
            if len(moves) == 0:
                return direct, Heuristic.calculateHeuristic(grid)

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
            # cell = random.choice( grid.getAvailableCells())
            cells = grid.getAvailableCells()
            if len(cells) > 2:
                depth -= 1
            '''
            elif len(cells) == 0:
                    return -1, Heuristic.calculateHeuristic(grid)
            '''
            for cell in cells:
                for value in POSIBILETILEVALUE :
                    child = MinMaxNode.makeGridCell(grid, cell, value)
                    score = MinMaxNode.alphabeta(child, depth, alpha, beta,
                                                     True)[1]

                    beta = min(beta, score)
            score = beta
        return direct, score

    @staticmethod
    def getBestMove(grid, depth):
         result = MinMaxNode.alphabeta(grid, depth, -float('inf'), float('inf'), True)
         return result

if __name__ == "__main__":
    g = Grid()
    g.map[0] = [0, 0, 0, 0]
    g.map[1] = [0, 2, 0, 0]
    g.map[2] = [0, 2, 0, 32]
    g.map[3] = [2, 4, 2, 16]

    start = time.time()
    print MinMaxNode.getBestMove(g, 5)

    print time.time()-start

