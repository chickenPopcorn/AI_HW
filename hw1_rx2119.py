import copy
import random
import Queue
import time
import math
import signal
import sys

def Exit_gracefully(signal, frame):
    print
    sys.exit(0)

DIRECTION = ["UP", "RIGHT", "DOWN", "LEFT"]
DIRECT_DICT = {"UP":"DOWN", "RIGHT":"LEFT", "DOWN":"UP", "LEFT":"RIGHT"}
class State:
    def __init__(self, n):
        self.n = n
        self.full_size = n**2
        self.list = range(0,self.full_size)
        self.move = ""
        self.parent = None
        self.child = []

    def __str__(self):
        board = ""
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                row.append(self.list[l+i*self.n])
            board+=str(row)+"\n"
        return board

    def takeList(self, newList):
        assert len(newList) == self.full_size
        self.list = newList

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

    def legalMove(self, direct, blank_pos):
        if (direct == "RIGHT" and blank_pos %self.n !=self.n-1) or \
           (direct == "LEFT" and blank_pos %self.n != 0) or \
           (direct == "DOWN" and blank_pos <= (self.n-1)*self.n-1) or \
            direct == "UP" and blank_pos >= self.n:
                return direct
        else:
            return "illegal move"

    def cloneSelf(self):
        self.child.append(copy.deepcopy(self))
        self.child[-1].parent = self


    def moveDirect(self, direct):
        blank_pos = self.list.index(0)
        move = self.legalMove(direct, blank_pos)
        if move != "illegal move":
            self.cloneSelf()
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


    def isGoalState(self):
        if self.list == range(0, self.full_size):
            return True
        else:
            return False

    def shuffle(self):
        lastMove = None
        for i in range (100):
            random.choice(DIRECTION)

    def dfs(self):
        stack = []
        maxSize = 1
        current = self
        stack.append(self)
        nodeExpand = 0
        while not current.isGoalState() and len(stack) != 0:
            current = stack.pop()
            nodeExpand += 1
            '''
            if current != None:
                current.printState()
                print "moved "+ current.move
                print
            else:
                print "this one is None"
                print
            '''
            for direct in DIRECTION:
                childNode = current.moveDirect(direct)
                if childNode is not None and DIRECT_DICT[childNode.move] != current.move :
                    stack.append(childNode)
            maxSize = max(len(stack),maxSize)
            print "stakc has size "+ str(len(stack))
        if current is not None:
            return current, maxSize, nodeExpand
        else:
            return "Not Found", maxSize, nodeExpand

    def bfs(self):
        maxSize = 1
        que = Queue.Queue()
        nodeExpand = 0
        current = self
        que.put(self)
        while not current.isGoalState() and not que.empty():
            current = que.get()
            nodeExpand += 1
            '''
            if current != None:
                current.printState()
                print "moved "+ current.move
                print
            else:
                print "this one is None"
                print
            '''
            for direct in DIRECTION:
                childNode = current.moveDirect(direct)
                if childNode is not None and DIRECT_DICT[childNode.move] != current.move:
                    que.put(childNode)
            maxSize = max(que.qsize(),maxSize)
            print "que has size "+ str(que.qsize())
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
            print "path to solution:" + str(path)
        else:
            print "Solution not found"





if __name__ == "__main__":
    signal.signal(signal.SIGINT, Exit_gracefully)
    a = State(2)
    print "initializing for BFS"
    a.takeList([2,0,3,1])
    print a
    a.solving('bfs')
    del a

    print
    a = State(2)
    print "initializing fro DFS"
    a.takeList([2,0,3,1])
    print a
    a.solving('dfs')
    del a



    print
    a = State(3)
    print "initializing fro BFS"
    a.takeList([1,2,5,3,4,0,6,7,8])
    print a
    a.solving('bfs')
    del a

    print
    a = State(3)
    print "initializing fro DFS"
    a.takeList([1,2,5,3,4,0,6,7,8])
    print a
    a.solving('dfs')
    del a
