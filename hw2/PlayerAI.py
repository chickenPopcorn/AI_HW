#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
from MinMaxNode import MinMaxNode
import time



class PlayerAI(BaseAI):
    def getMove(self, grid):
        '''        
        # I'm too naive, please change me!
        moves = grid.getAvailableMoves()
        return moves[randint(0, len(moves) - 1)] if moves else None
        '''
        start = time.time()
        move, score = MinMaxNode.getBestMove(grid, 4)
        print "------"+ str(time.time()-start) +" seconds-----\n"
        print "Boardscore chose is ", score
        return move
