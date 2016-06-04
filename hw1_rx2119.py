import copy
import random
import time
import math
import signal
import sys
from collections import deque
from sets import Set
import Queue
import argparse

def Exit_gracefully(signal, frame):
    print
    sys.exit(0)

DIRECTION = Set(("UP", "RIGHT", "DOWN", "LEFT"))
METHODS = ["BFS", "DFS","ASTAR"]

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
        return board[:-1]

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

    # randomly shuffle board for a move for 100 times
    def shuffle(self):
        moves = random.random()*100
        for i in range (int(moves)):
            self.makeMove(random.sample(DIRECTION.difference(self.move), 1)[0])

    # do bfs search on current instance using queue
    # returns triple tuple of goalstate,
    # max size of queue, and num of nodes expanded
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
        del visitedStates
        if current is not None:
            return current, maxSize, nodeExpand
        else:
            return "Not Found", maxSize, nodeExpand

    # do bfs search on current instance using queue
    # returns triple tuple of goalstate,
    # max size of queue, and num of nodes expanded
    def bfs(self):
        # record visited configuration
        visitedStates = Set()
        # max size of the stack/queue
        maxSize = 1
        que = deque()
        nodeExpand = 0
        current = self
        que.append(self)
        while not current.isGoalState() and len(que) != 0:
            current = que.popleft()
            nodeExpand += 1
            visitedStates.add(tuple(current.list))
            for direct in DIRECTION:
                childNode = current.simulateMove(direct)
                if childNode !=  None:
                    # added to the queue only if current config is not visited
                    if not tuple(childNode.list) in visitedStates:
                        que.append(childNode)
            # compare for max size of the queue
            maxSize = max(len(que),maxSize)
        if current is not None:
            return current, maxSize, nodeExpand
        else:
            return "Not Found", maxSize, nodeExpand

        '''
        if i != 0:
                result += math.fabs(self.list.index(i)% self.n - i%self.n)
                result += math.fabs(self.list.index(i)/ self.n - i/self.n)
        '''

    # calculate total manhattan distance for the config as heuristic value
    def hFun(self):
        result = 0
        for i in self.list:
            if i != 0:
                result += math.fabs(self.list.index(i)% self.n - i%self.n)
                result += math.fabs(self.list.index(i)/ self.n - i/self.n)

        # print "h function is for this move "+str(result)
        return result

    # do A* search on current instance using priority queue
    # and hFun as heuristic function
    # returns triple tuple of goalstate,
    # max size of queue, and num of nodes expanded
    def astar(self):
        visitedStates = Set()
        maxSize = 1
        que = Queue.PriorityQueue()
        nodeExpand = 0
        current = self
        que.put((self.hFun(), self))
        while not current.isGoalState() and que.qsize() > 0:
            current = que.get()[1]
            nodeExpand += 1
            visitedStates.add(tuple(current.list))
            for direct in DIRECTION:
                childNode = current.simulateMove(direct)
                if childNode !=  None:
                    if not tuple(childNode.list) in visitedStates:
                        que.put((childNode.hFun(), childNode))
            maxSize = max(que.qsize(), maxSize)
        if current is not None:
            return current, maxSize, nodeExpand
        else:
            return "Not Found", maxSize, nodeExpand

    # return path from goalState to origin state as a list
    def getPath(Node):
        path = []
        while Node.parent != None:
            path.append(Node.move)
            Node = Node.parent
        path.reverse()
        return path

    # solving N-puzzle using BFS, DFS, or ASTAR
    # and return the stats for the method specified
    def solving(self, method):
        startTime =time.time()
        current = None
        if method.upper() == "BFS":
            current, size, nodeExpand = self.bfs()
        elif method.upper() == "DFS":
            current, size, nodeExpand = self.dfs()
        elif method.upper() == "ASTAR":
            current, size, nodeExpand = self.astar()
        else:
            return
        print ("--- %s milliseconds --" % ((time.time() - startTime)*1000))
        if current != "Not Found":
            print "n = "+ str(self.n)
            path = State.getPath(current)
            if len(path)< 50:
                print "path to solution is " + str(path)
            print "Cost of path = " + str(len(path))
            print "nodes expanded = "+ str(nodeExpand)
            print "max stack/queue size = "+str(size)
        else:
            print "Solution not found"
        return path

    # validates the solution produced
    def validateSolution(a, path):
        solution = State(a.n, list(a.list))
        for i in path:
            solution.makeMove(i)
        if solution.isGoalState():
            return True
        else:
            return False


def Main():
    parser = argparse.ArgumentParser(description="Choose how test n-puzzle")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", "-random",type=int, help="random trials for N-Puzzle")
    group.add_argument("-t", "-test", type=list, help="test specific"+
                       "configuration")
    args = parser.parse_args()
    if args.r:
        intR = int(args.r)
        if intR < 1:
            raise argparse.ArgumentError(None, "invalid input")
        n = 0
        for i in range(args.r):
            n += 1
            bfsPath = []
            print "TEST CASE "+str(n)
            a = State(3)
            a.shuffle()
            print a
            print
            for method in METHODS:
                print method.upper()+" search"
                path = a.solving(method)
                if State.validateSolution(a, path):
                    print "the solution is valid\n"
                else:
                    print "invalided solution!\n"

                if method == "BFS":
                    bfsPath = path
                elif method == "ASTAR":
                    print "ASTAR is optimun "+ str(bfsPath == path)
    elif args.t:
        bfsPath =[]
        testCases = [(math.sqrt(len(args.t)), map(int, args.t))]
        for case in testCases:
            for method in ["BFS", "DFS","ASTAR","ASTAR"]:
                a = State(int(case[0]), case[1])
                print "initializing for "+method.upper()
                print a
                path = a.solving(method)
                for i in path:
                    a.makeMove(i)

                if method == "BFS":
                    bfsPath = path
                elif method == "ASTAR":
                    print "ASTAR is optimun "+ str(bfsPath == path)

                print "the solution is "+ str(a.isGoalState()) +"\n"
                del a



if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    Main()

