#!/usr/bin/env python
#coding:utf-8

from random import randint
from BaseAI import BaseAI

class PlayerAI(BaseAI):
	def getMove(self, grid):
		# I'm too naive, please change me!
		moves = grid.getAvailableMoves()
		return moves[randint(0, len(moves) - 1)] if moves else None