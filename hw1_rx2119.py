import copy
import random
import time
import math
import signal
import sys
from collections import deque
from sets import Set
import argparse
import heapq

def Exit_gracefully(signal, frame):
    print
    sys.exit(0)

DIRECTION = Set(("UP", "RIGHT", "DOWN", "LEFT"))
METHODS = ["BFS", "DFS","ASTAR"] #, "IDASTAR"]

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
            self.move = move
        else:
            self.move = None
        self.parent = parent
        self.child = []

    def __str__(self):
        board = " "
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                num = self.list[l+i*self.n]
                if num != 0:
                    board += str(num)+" "
                else :
                    board += "  "
            board+="\n "
        return board[:-2]

    def __eq__(self, other):
        return self.list == other.list



    def simulateMove(self, direct):
        tempList = list(self.list)
        pos = tempList.index(0)
        if (direct == "RIGHT" and pos %self.n !=self.n-1) or \
           (direct == "LEFT" and pos %self.n != 0) or \
           (direct == "DOWN" and pos <= (self.n-1)*self.n-1) or \
            direct == "UP" and pos >= self.n:
            if direct == "RIGHT":
                tempList[pos], tempList[pos+1] = \
                tempList[pos+1], tempList[pos]
            elif direct == "LEFT":
                tempList[pos-1], tempList[pos] = \
                tempList[pos], tempList[pos-1]
            elif direct == "DOWN":
                tempList[pos+self.n], tempList[pos] = \
                tempList[pos], tempList[pos+self.n]
            else:
                tempList[pos-self.n], tempList[pos] = \
                tempList[pos], tempList[pos-self.n]
            return tempList
        else:
            return None




    # making an actual make from an original node
    def makeMove(self, direct):
        pos = self.list.index(0)
        if (direct == "RIGHT" and pos %self.n !=self.n-1) or \
           (direct == "LEFT" and pos %self.n != 0) or \
           (direct == "DOWN" and pos <= (self.n-1)*self.n-1) or \
            direct == "UP" and pos >= self.n:
            if direct == "RIGHT":
                self.list[pos], self.list[pos+1] = \
                self.list[pos+1], self.list[pos]
            elif direct == "LEFT":
                self.list[pos-1], self.list[pos] = \
                self.list[pos], self.list[pos-1]
            elif direct == "DOWN":
                self.list[pos+self.n], self.list[pos] = \
                self.list[pos], self.list[pos+self.n]
            else:
                self.list[pos-self.n], self.list[pos] = \
                self.list[pos], self.list[pos-self.n]

    # testing whether a state reached goal state or not
    def isGoalState(self):
        if self.list == range(0, self.full_size):
            return True
        else:
            return False

    # randomly shuffle board for a move for 100 times
    def shuffle(self):
        moves = random.random()*500
        for i in range (int(moves)):
            self.makeMove(random.sample(DIRECTION.difference(self.move), 1)[0])


    # do bfs search on current instance using deque
    # returns triple tuple of goal state, max size of queue, and num of nodes expanded
    def bfs(self):
        # record visited configuration
        visitedStates = Set()
        # max size of the stack/queue
        maxSize = 1
        que = deque()
        nodeExpand = 0
        current = self
        que.append(self)
        foundGoal = False

        if current.isGoalState():
            return True, current, maxSize, nodeExpand

        while len(que) != 0:
            current = que.popleft()
            nodeExpand += 1
            for direct in DIRECTION:
                childList = current.simulateMove(direct)
                if childList !=  None:
                    # added to the queue only if current config is not visited
                    if tuple(childList) not in visitedStates:
                        current.child.append(State(self.n, childList, current, direct))
                        que.append(current.child[-1])
                        visitedStates.add(tuple(current.child[-1].list))
                        maxSize = max(len(que),maxSize)
                        if current.child[-1].isGoalState():
                            current = current.child[-1]
                            foundGoal = True
                            break
            # compare for max size of the queue
            if foundGoal:
                break

        return foundGoal, current, maxSize, nodeExpand


    # do bfs search on current instance using a list implemented as a stack
    # returns triple tuple of goal state, max size of queue, and num of nodes expanded
    def dfs(self):
        visitedStates= Set()
        stack = []
        maxSize = 1
        current = self
        stack.append(self)
        nodeExpand = 1
        foundGoal = False

        if current.isGoalState():
            return True, current, maxSize, nodeExpand

        while len(stack) != 0:
            current = stack.pop()
            nodeExpand += 1
            for direct in DIRECTION:
                childList = current.simulateMove(direct)
                if childList != None:
                   if tuple(childList) not in visitedStates:
                        current.child.append(State(self.n, childList, current, direct))
                        stack.append(current.child[-1])
                        visitedStates.add(tuple(current.child[-1].list))
                        maxSize = max(len(stack),maxSize)
                        if current.child[-1].isGoalState():
                            current = current.child[-1]
                            foundGoal = True
                            break
            # compare for max size of the queue
            if foundGoal:
                break

        return foundGoal, current, maxSize, nodeExpand


    # moves made from original state to current state
    def gFun(self):
        count = 0
        current = self
        while current != None:
            current = current.parent
            count += 1
        return count


    # calculate total manhattan distance for the config as heuristic value
    # min moves need to make to reach goal state from current state
    def hFun(self):
        result = 0
        for i in self.list:
            if i != 0:
                result += abs(self.list.index(i)% self.n - i%self.n)
                result += abs(self.list.index(i)/ self.n - i/self.n)

        # print "h function is for this move "+str(result)
        return result

    # do A* search on current instance using list implemented as a heap
    # and hFun as heuristic function and gFun as previous cost function
    # returns triple tuple of goal state, max size of queue, and num of nodes expanded
    def astar(self):
        visitedStates = Set()
        maxSize = 1
        heap = []
        nodeExpand = 0
        current = self
        foundGoal = False

        if current.isGoalState():
            return True, current, maxSize, nodeExpand

        f = self.hFun()+self.gFun()
        heapq.heappush(heap, (f, self))
        while len(heap) > 0:
            current = heapq.heappop(heap)[1]
            nodeExpand += 1
            for direct in DIRECTION:
                childList = current.simulateMove(direct)
                if childList !=  None:
                    if tuple(childList) not in visitedStates:
                        current.child.append(State(self.n, childList, current, direct))
                        heapq.heappush(heap, (current.child[-1].hFun() + current.child[-1].gFun(), current.child[-1]))
                        visitedStates.add(tuple(current.list))
                        if current.child[-1].isGoalState():
                            current = current.child[-1]
                            foundGoal = True
                            break
            # compare for max size of the queue
            if foundGoal:
                break

        return foundGoal, current, maxSize, nodeExpand



    # return path from goalState to origin state as a list
    def getPath(Node):
        path = []
        while Node.parent != None:
            path.append(Node.move)
            Node = Node.parent
        path.reverse()
        return path

    def countDepth(self):
        count = 0
        while self.parent != None:
            count += 1
        return count

    # do A* search on current instance using list implemented as a heap
    # and hFun as heuristic function and gFun as previous cost function
    # returns triple tuple of goal state, max size of queue, and num of nodes expanded

    def idastar(self):
        found = False
        count = 0
        while not found:
            current, size, expand = self.dastar(count)
            count += 1
            if current == "Not Found":
                continue
            else:
                found = True
        return current, size, expand

    def dastar(self, depth):
        visitedStates = Set()
        maxSize = 1
        heap = []
        nodeExpand = 0
        current = self
        f = self.hFun()+self.gFun()
        heapq.heappush(heap, (f, self))
        print "current "+ str(depth)
        while not current.isGoalState() and len(heap) > 0:
            current = heapq.heappop(heap)[1]
            nodeExpand += 1
            visitedStates.add(tuple(current.list))
            for direct in DIRECTION:
                print "     direct is "+ direct
                childNode = current.simulateMove(direct)
                if childNode !=  None:
                    if not tuple(childNode.list) in visitedStates:
                       heapq.heappush(heap, (childNode.hFun()+childNode.gFun(), childNode))
            maxSize = max(len(heap), maxSize)
            print "      node depth is "+ str(current.countDepth())
            if current.countDepth() >= depth:
                break
        if current is not None and current.isGoalState():
            print "returned a node"
            return current, maxSize, nodeExpand
        else:
            print "returned not found"
            return "Not Found", maxSize, nodeExpand


    # solving N-puzzle using BFS, DFS, or ASTAR
    # and return the stats for the method specified
    def solving(self, method):
        startTime =time.time()
        if method.upper() == "BFS":
            found, current, size, nodeExpand = self.bfs()
        elif method.upper() == "DFS":
            found, current, size, nodeExpand = self.dfs()
        elif method.upper() == "ASTAR":
            found, current, size, nodeExpand = self.astar()
        elif method.upper() == "IDASTAR":
            found, current, size, nodeExpand = self.idastar()
        else:
            return

        print ("--- %s milliseconds --" % ((time.time() - startTime)*1000))
        if found:
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

# main function
def Main():
    parser = argparse.ArgumentParser(description="Choose how to test n-puzzle solver")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("-r", type=int, help="R number of random trials for N-Puzzle solver")
    group.add_argument("-t", type=list, help="The specific configuration T for N-Puzzle solver")
    args = parser.parse_args()
    # random trials
    if args.r:
        intR = int(args.r)
        if intR < 1:
            raise argparse.ArgumentError(None, "invalid input")
        n = 0
        for i in range(args.r):
            n += 1
            bfsPath = []
            print "\nTEST CASE "+str(n)
            a = State(3)
            a.shuffle()
            print a
            print
            for method in METHODS:
                print method.upper()+" search"
                current = State(a.n, a.list)
                path = current.solving(method)
                print
                for i in path:
                    current.makeMove(i)
                # asserting A* solution has the same cost as BFS
                if method == "BFS":
                    bfsPath = len(path)
                elif method == "ASTAR":
                    assert bfsPath == len(path)
                # validate solution through the game
                assert current.isGoalState() == True
                del current

    # controlled tests
    elif args.t:
        bfsPath =[]
        testCases = [(math.sqrt(len(args.t)), map(int, args.t))]
        for case in testCases:
            for method in METHODS:
                a = State(int(case[0]), case[1])
                print "\ninitializing for "+method.upper()
                print a
                path = a.solving(method)
                for i in path:
                    a.makeMove(i)
                # asserting A* solution has the same cost as BFS
                if method == "BFS":
                    bfsPath = len(path)
                elif method == "ASTAR":
                    assert bfsPath == len(path)
                # validate solution through the game
                assert a.isGoalState() == True
                del a

if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    Main()

