from Grid import Grid
import copy
import math
import time
from Heuristic import Heuristic
import random
import sys
import time

BOARDSIZE = 4
PLAYER = True
COMPUTER = False
POSSIBILETILEVALUE= [2, 4]

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
    def minimax(grid, depth, player):
        direct = -1
        if depth == 0:
            return -1, Heuristic.calculateHeuristic(grid)
        if player:
            score = -float('inf')
            moves = grid.getAvailableMoves()
            if len(moves) == 0:
                return -1, Heuristic.calculateHeuristic(grid)
            for d in moves:
                child = MinMaxNode.makeGridDirect(grid, d)
                childScore = MinMaxNode.minimax(child, depth-1, COMPUTER)[1]
                if score < childScore:
                    score = childScore
                    direct = d
            return direct, score
        else:
            score = float('inf')
            cells = grid.getAvailableCells()
            if len(cells) == 0:
                return direct, Heuristic.calculateHeuristic(grid)
            for cell in cells:
                for value in POSSIBILETILEVALUE:
                    child = MinMaxNode.makeGridCell(grid, cell, value)
                    childScore = MinMaxNode.minimax(child, depth-1, PLAYER)[1]
                    if score > childScore:
                        score = childScore
            return direct, score


    @staticmethod
    def alphabeta(grid, depth, alpha, beta, player, timeLimit):
        direct = -1
        score = 0
        if time.time() >= timeLimit:
            return -1, None
        if depth == 0:
            return direct, Heuristic.calculateHeuristic(grid)
        if player:
            moves = grid.getAvailableMoves()
            if len(moves) == 0:
                return direct, Heuristic.calculateHeuristic(grid)

            for d in moves:
                child = MinMaxNode.makeGridDirect(grid, d)
                score = MinMaxNode.alphabeta(child, depth-1, alpha, beta,
                                             False, timeLimit)[1]
                if score == None:
                    return direct, None
                if alpha < score or score == -float('inf'):
                    direct = d
                alpha = max(alpha,score )
                if beta <= alpha:
                    break
            score = alpha

        else:
            cells = grid.getAvailableCells()
            depth -= 1
            if len(cells) == 0:
                    return -1, Heuristic.calculateHeuristic(grid)
            for cell in cells:
                for value in POSSIBILETILEVALUE :
                    child = MinMaxNode.makeGridCell(grid, cell, value)
                    score = MinMaxNode.alphabeta(child, depth, alpha, beta,
                                                     True, timeLimit)[1]
                    if score == None:
                        return direct, None
                    beta = min(beta, score)
            score = beta
        return direct, score

    @staticmethod
    def getBestMove(grid):
        depth = 1
        timeLimit = time.time() + 0.28
        lastRound = None
        while time.time()<timeLimit:
            result = MinMaxNode.alphabeta(grid, depth, -float('inf'),
                                          float('inf'), PLAYER, timeLimit)
            if result[1] == None:
                return lastRound
            else:
                lastRound = result

            depth += 1
        return result


if __name__ == "__main__":
    g = Grid()
    g.map[0] = [2, 16, 4, 0]
    g.map[1] = [4, 2, 0, 16]
    g.map[2] = [8, 0, 128, 32]
    g.map[3] = [0, 8, 8, 16]


    start = time.time()
    print MinMaxNode.getBestMove(g), "mm score"
    print time.time() - start

    g.map[0] = [0, 0, 0, 0]
    g.map[1] = [0, 2, 0, 0]
    g.map[2] = [0, 2, 0, 0]
    g.map[3] = [0, 0, 0, 0]

    start = time.time()
    print MinMaxNode.getBestMove(g), "mm score"
    print time.time() - start
