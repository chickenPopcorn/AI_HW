import copy 

class state:
    def __init__(self, n, parent=None, child=None):
        self.n = n
        self.full_size = n**2
        self.list = range(0,self.full_size)
        self.move = ""
        self.parent = parent
        self.child = child

    def printState(self):
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                row.append(self.list[l+i*self.n])
            print row

    def returnState(self):
        result = []
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                row.append(self.list[l+i*self.n])
            result.append(row)
        return result

    def moveDirect(self, direct):
        blank_pos = self.list.index(0)
        if direct == "LEFT" and blank_pos % self.n != self.n-1:
            self.child = copy.deepcopy(self)
            self.child.parent = self
            self.child.list[blank_pos], self.child.list[blank_pos+1] = \
            self.child.list[blank_pos+1], self.child.list[blank_pos]
        elif direct == "RIGHT" and blank_pos % self.n != 0:
            self.child = copy.deepcopy(self)
            self.child.parent = self
            self.child.list[blank_pos-1], self.child.list[blank_pos] = \
            self.child.list[blank_pos], self.child.list[blank_pos-1]
        elif direct == "DOWN" and blank_pos <= (self.n-1)*self.n-1:
            self.child = copy.deepcopy(self)
            self.child.parent = self
            self.child.list[blank_pos+self.n], self.child.list[blank_pos] = \
            self.child.list[blank_pos], self.child.list[blank_pos+self.n]
        elif direct == "UP" and blank_pos >= self.n:
            self.child = copy.deepcopy(self)
            self.child.parent = self
            self.child.list[blank_pos-self.n], self.child.list[blank_pos] = \
            self.child.list[blank_pos], self.child.list[blank_pos-self.n]
        return self.child

if __name__ == "__main__":
    a = state(3)
    print a
    a.printState()
    current = a
    current = current.moveDirect("LEFT")
    current.printState()
