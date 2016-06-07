import random
import time
import math
import signal
import sys
from collections import deque
from sets import Set
import heapq
import resource

def Exit_gracefully(signal, frame):
    print
    sys.exit(0)

DIRECTION = Set(("UP", "DOWN", "LEFT", "RIGHT"))
METHODS = ["BFS", "DFS","ASTAR", "IDASTAR"]
OPDIRECT = { "DOWN":"UP", "UP":"DOWN", "RIGHT":"LEFT","LEFT":"RIGHT"}


class State:
    def __init__(self, n, original=None, parent=None, move=None):
        self.n = n
        self.full_size = n**2
        if original == None:
            self.list = range(0,self.full_size)
        else:
            try:
                assert self.full_size == len(original)
            except AssertionError:
                print "the input list size is incorrect"
                sys.exit(0)
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
        moves = random.random()*200
        for i in range (int(moves)):
            self.makeMove(random.sample(DIRECTION.difference(self.move), 1)[0])


    # do bfs search on current instance using deque
    # returns tuple of found goal, goal state, max size of queue, and num of nodes expanded
    def bfs(self):
        #mem = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
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
            mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
            return True, current, maxSize, nodeExpand, mem

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
        mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
        return foundGoal, current, maxSize, nodeExpand, mem


    # do dfs search on current instance using a list implemented as a stack
    # returns tuple found goal, goal state, max size of queue, and num of nodes expanded
    def dfs(self):
        visitedStates= Set()
        stack = []
        maxSize = 1
        current = self
        stack.append(self)
        nodeExpand = 1
        foundGoal = False

        if current.isGoalState():
            mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
            return True, current, maxSize, nodeExpand, mem

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
        mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
        return foundGoal, current, maxSize, nodeExpand, mem


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
    # returns tuple of found goal, goal state, max size of queue, and num of nodes expanded
    def astar(self):
        visitedStates = Set()
        maxSize = 1
        heap = []
        nodeExpand = 0
        current = self
        foundGoal = False

        if current.isGoalState():
            mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
            return True, current, maxSize, nodeExpand, mem

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
                        maxSize = max(len(heap),maxSize)
                        if current.child[-1].isGoalState():
                            current = current.child[-1]
                            foundGoal = True
                            break
            # compare for max size of the queue
            if foundGoal:
                break

        mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
        return foundGoal, current, maxSize, nodeExpand, mem



    # return path from goalState to origin state as a list
    def getPath(Node):
        path = []
        while Node.parent != None:
            path.append(Node.move)
            Node = Node.parent
        path.reverse()
        return path

    def countDepth(Node):
        count = 0
        while Node.parent != None:
            count += 1
            Node = Node.parent
        return count

    # do iterative deepening A* search on current instance using list implemented as a heap
    # and hFun as heuristic function and gFun as previous cost function
    # returns a tuple of found goal, goal state, max size of queue, and num of nodes expanded
    def idastar(self):
        depth = self.hFun() + self.gFun()
        found = False
        expand = 0
        while not found:
            current = State(self.n, self.list)
            found, current, size, expand = current.dastar(depth, expand)
            depth += 1
            if found:
                 mem  = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1000
        return True, current, size, expand, mem

    def dastar(self, depth, nodeExpand):
        maxSize = 1
        stack = []
        current = self
        foundGoal = False

        if current.isGoalState():
            return True, current, maxSize, nodeExpand

        stack.append(current)
        while len(stack) > 0:
            maxSize = max(len(stack),maxSize)
            current = stack.pop()
            nodeExpand += 1
            for direct in DIRECTION:
                if current.move == None or direct != OPDIRECT[current.move]:
                    childlist = current.simulateMove(direct)
                    if childlist !=  None:
                        current.child.append(State(self.n, childlist, current, direct))
                        if current.child[-1].gFun() + current.child[-1].hFun() <= depth:
                            stack.append(current.child[-1])
                            if current.child[-1].isGoalState():
                                current = current.child[-1]
                                foundGoal = True
                                break
            if foundGoal:
                break
        return foundGoal, current, maxSize, nodeExpand


    # solving N-puzzle using BFS, DFS, or ASTAR
    # and return the stats for the method specified
    def solving(self, method):
        startTime =time.time()
        if method.upper() == "BFS":
            found, current, size, nodeExpand, memory = self.bfs()
        elif method.upper() == "DFS":
            found, current, size, nodeExpand, memory = self.dfs()
        elif method.upper() == "ASTAR":
            found, current, size, nodeExpand, memory = self.astar()
        elif method.upper() == "IDASTAR":
            found, current, size, nodeExpand, memory = self.idastar()
        else:
            return

        print ("--- %s milliseconds --" % ((time.time() - startTime)*1000))
        if found:
            print "n = "+ str(self.n)
            path = State.getPath(current)
            if len(path)< 50:
                print "path to solution is " + str(path)
            print "Cost of path = " + str(len(path))
            print "Memory Usage: " + str(memory)+" KB"
            print "nodes expanded = "+ str(nodeExpand)
            print "max stack/queue size = "+str(size)
            print "max depth of the stack/ queue "+ str(len(path)+1)
        else:
            print "Solution not found"
            sys.exit(0)
        return found, size, nodeExpand, path

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
def main():
    arguments = {}
    random = False
    test = True
    if len(sys.argv) == 4:
        # random option
        if sys.argv[1] in [ "-random", "-r"]:
            try:
                n = int(sys.argv[2])
                r = int(sys.argv[3])
                assert r > 0 and n > 0
                random = True
                arguments["random"] = (n, r)
            except:
                print "argument for random is invalid"
                sys.exit(0)
        # testing option
        elif sys.argv[1] in ["-test", "-t"] and (sys.argv[2].upper()[1:] in
                                                 METHODS or sys.argv[2] == "-a"):
            test = True
            try:
                temp = map(int, sys.argv[3].split(","))
                n = int(math.sqrt(len(temp)))
                assert n**2 == len(temp)
                temp.sort()
                assert range(n**2) == temp
                arguments["test"] = (sys.argv[2][1:], map(int, sys.argv[3].split(",")))
            except:
                print "invalid input list "+ sys.argv[3]
                sys.exit(0)
        else:
            print "invalid input"
            sys.exit(0)
    else:
        print "usage: python hw1_rx2119.py (-random N-size R-num | -test -method LIST)"
        sys.exit(0)

    # random trials
    if random:
        n = arguments["random"][0]
        r = arguments["random"][1]
        for i in range(r):
            stats = {}
            print "\nTEST CASE "+str(i+1)
            a = State(n)
            a.shuffle()
            print a
            print
            for method in METHODS:
                print method.upper()+" search"
                current = State(a.n, a.list)
                found, size, nodeExpand, path = a.solving(method)
                print
                if found:
                    for i in path:
                        current.makeMove(i)
                    # validate solution through the game
                    assert current.isGoalState() == True
                    stats[method] = (len(path), size, nodeExpand)
                    del current
            # asserting BFS has better or equivalent solution
            # asserting A* solution has the same cost as BFS
            assert stats["BFS"][0] <= stats["DFS"][0]
            assert stats["BFS"][0] == stats["ASTAR"][0]
            assert stats["IDASTAR"][0] == stats["BFS"][0]
            assert stats["ASTAR"][1] >= stats["IDASTAR"][1]
            del a
    # controlled tests
    elif test:
        stats = {}
        runWith = []
        if arguments["test"][0] == "a":
            runWith = METHODS
        else:
            runWith.append(arguments["test"][0])
        for method in runWith:
            a = State(int(math.sqrt(len(arguments["test"][1]))) ,map(int, arguments["test"][1]) )
            print "\ninitializing for "+method.upper()
            print a
            found, size, nodeExpand, path = a.solving(method)
            if found:
                for i in path:
                    a.makeMove(i)
                # validate solution through the game
                assert a.isGoalState() == True


if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    main()

