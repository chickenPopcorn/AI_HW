import copy
import random
import time
import math
import signal
import sys
from collections import deque
from sets import Set

def Exit_gracefully(signal, frame):
    print
    sys.exit(0)

DIRECTION = ["UP", "RIGHT", "DOWN", "LEFT"]

class State:
    def __init__(self, n, original=None, parent=None, move=None):
        self.n = n
        self.full_size = n**2
        if original == None:
            self.list = range(0,self.full_size)
        else:
            assert self.full_size == len(original)
            self.list = list(original)
        if move != None:
            self.move = ''.join(move)
        else:
            self.move = None
        self.parent = parent
        self.child = []

    def __str__(self):
        board = ""
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                row.append(self.list[l+i*self.n])
            board+=str(row)+"\n"
        return board

    def __eq__(self, other):
        return self.list == other.list

    def returnState(self):
        result = []
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                row.append(self.list[l+i*self.n])
            result.append(row)
        return result

    def legalMove(self, direct, pos):
        if (direct == "RIGHT" and pos %self.n !=self.n-1) or \
           (direct == "LEFT" and pos %self.n != 0) or \
           (direct == "DOWN" and pos <= (self.n-1)*self.n-1) or \
            direct == "UP" and pos >= self.n:
                return direct
        else:
            return "illegal move"

    def simulateMove(self, direct):
        blank_pos = self.list.index(0)
        move = self.legalMove(direct, blank_pos)
        if move != "illegal move":
            self.child.append(State(self.n, self.list, self))
            self.child[-1].move = move
            if move == "RIGHT":
                self.child[-1].list[blank_pos], self.child[-1].list[blank_pos+1] = \
                self.child[-1].list[blank_pos+1], self.child[-1].list[blank_pos]
            elif move == "LEFT":
                self.child[-1].list[blank_pos-1], self.child[-1].list[blank_pos] = \
                self.child[-1].list[blank_pos], self.child[-1].list[blank_pos-1]
            elif direct == "DOWN":
                self.child[-1].list[blank_pos+self.n], self.child[-1].list[blank_pos] = \
                self.child[-1].list[blank_pos], self.child[-1].list[blank_pos+self.n]
            else:
                self.child[-1].list[blank_pos-self.n], self.child[-1].list[blank_pos] = \
                self.child[-1].list[blank_pos], self.child[-1].list[blank_pos-self.n]
            return self.child[-1]
        else:
            return None

    def makeMove(self, direct):
        blank_pos = self.list.index(0)
        move = self.legalMove(direct, blank_pos)
        if move != "illegal move":
            if move == "RIGHT":
                self.list[blank_pos], self.list[blank_pos+1] = \
                self.list[blank_pos+1], self.list[blank_pos]
            elif move == "LEFT":
                self.list[blank_pos-1], self.list[blank_pos] = \
                self.list[blank_pos], self.list[blank_pos-1]
            elif direct == "DOWN":
                self.list[blank_pos+self.n], self.list[blank_pos] = \
                self.list[blank_pos], self.list[blank_pos+self.n]
            else:
                self.list[blank_pos-self.n], self.list[blank_pos] = \
                self.list[blank_pos], self.list[blank_pos-self.n]

    def isGoalState(self):
        if self.list == range(0, self.full_size):
            return True
        else:
            return False

    def shuffle(self):
        moves = random.random()*32
        for i in range (int(moves)):
            self.makeMove(random.choice(DIRECTION))

    def dfs(self):
        visitedStates= Set()
        stack = []
        maxSize = 1
        current = self
        stack.append(self)
        nodeExpand = 0
        while not current.isGoalState() and len(stack) != 0:
            current = stack.pop()
            nodeExpand += 1
            visitedStates.add(tuple(current.list))
            for direct in DIRECTION:
                childNode = current.simulateMove(direct)
                if childNode != None:
                    if not tuple(childNode.list) in visitedStates:
                        stack.append(childNode)
            maxSize = max(len(stack),maxSize)

        if current is not None:
            return current, maxSize, nodeExpand
        else:
            return "Not Found", maxSize, nodeExpand

    def bfs(self):
        visitedStates = []
        maxSize = 1
        que = deque()
        nodeExpand = 0
        current = self
        que.append(self)
        while not current.isGoalState() and len(que) != 0:
            current = que.popleft()
            nodeExpand += 1
            if current.list not in visitedStates:
                visitedStates.append(copy.deepcopy(current.list))
            for direct in DIRECTION:
                childNode = current.simulateMove(direct)
                if childNode !=  None:
                    if not childNode.list in visitedStates:
                        que.append(childNode)
            maxSize = max(len(que),maxSize)
        if current is not None:
            return current, maxSize, nodeExpand
        else:
            return "Not Found", maxSize, nodeExpand

    def getPath(Node):
        path = []
        while Node.parent != None:
            path.append(Node.move)
            Node = Node.parent
        path.reverse()
        return path

    def solving(self, method):
        startTime =time.time()
        current = None
        if method.upper() == "BFS":
           current, size, nodeExpand = self.bfs()
        elif method.upper() == "DFS":
            current, size, nodeExpand = self.dfs()
        else:
            return
        print ("--- %s milliseconds --" % ((time.time() - startTime)*1000))
        if current != "Not Found":
            print "n = "+ str(self.n)
            path = State.getPath(current)
            print "Cost of path = " + str(len(path))
            print "nodes expanded = "+ str(nodeExpand)
            print "max stack/queue size = "+str(size)
            # print "path to solution:" + str(path)
        else:
            print "Solution not found"
        return path

if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    testCases = [
        (2, [2,0,3,1]),
        (3, [1,2,5,3,0,4,6,7,8]),
    ]

    methods = [
        "bfs", "dfs"
    ]
    '''
    for case in testCases:
        for method in methods:
            a = State(case[0], case[1])
            print "initializing for BFS"
            print a
            path = a.solving(method)
            for i in path:
                a.makeMove(i)
            print "the solution is "+ str(a.isGoalState()) +"\n"
            del a
    '''
    n = 0
    for i in range(5):
        n += 1
        print "test case "+str(n)
        for method in methods:
            a = State(3)
            a.shuffle()
            print "initializing for "+method.upper()
            print a
            path = a.solving(method)
            for i in path:
                a.makeMove(i)
            print "the solution is "+ str(a.isGoalState()) +"\n"
            del a

