#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI
from MiniMax import MiniMax
import time



class PlayerAI(BaseAI):
    def getMove(self, grid):
        start = time.time()
        return MiniMax.getBestMove(grid)[0]
