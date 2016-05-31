import copy 

class state:
    def __init__(self, n, parent=None, child=None):
        self.n = n
        self.full_size = n**2
        self.list = range(0,self.full_size)

        self.parent = parent
        self.child = child
        
    def printState(self):
        for i in range(0, self.n):
            row = []
            for l in range(0, self.n):
                row.append(self.list[l+i*self.n])
            print row

    def move(self, direct):
        blank_pos = self.list.index(0)
        if direct == "LEFT" and blank_pos % self.n != self.n-1:
            self.parent = copy.deepcopy(self)
            self.parent.child = self
            self.list[blank_pos], self.list[blank_pos+1] = \
            self.list[blank_pos+1], self.list[blank_pos]
            
        elif direct == "RIGHT" and blank_pos % self.n != 0:
            self.parent = copy.deepcopy(self)
            self.list[blank_pos-1], self.list[blank_pos] = \
            self.list[blank_pos], self.list[blank_pos-1]
        elif direct == "DOWN" and blank_pos <= (self.n-1)*self.n-1:
            self.parent = copy.deepcopy(self)
            self.list[blank_pos+self.n], self.list[blank_pos] = \
            self.list[blank_pos], self.list[blank_pos+self.n]  
        elif direct == "UP" and blank_pos >= self.n:
            self.parent = copy.deepcopy(self)
            self.list[blank_pos-self.n], self.list[blank_pos] = \
            self.list[blank_pos], self.list[blank_pos-self.n]
        else:
            print "Can't Make That Move"
    

if __name__ == "__main__":
    a = state(3)
    a.printState()
    print
    print "moving left"
    a.move("LEFT")
    a.printState()
    print
    a.move("LEFT")
    a.printState()
    print
    a.move("LEFT")
    a.printState()
    print
    print "moving right"
    a.move("RIGHT")
    a.printState()
    print
    a.move("RIGHT")
    a.printState()
    print
    a.move("RIGHT")
    a.printState()
    print
    print "moving down"
    a.move("DOWN")
    a.printState()
    print
    a.move("DOWN")
    a.printState()
    print
    a.move("DOWN")
    a.printState()
    print
    print "moving up"
    a.move("UP")
    a.printState()
    print
    a.move("UP")
    a.printState()
    print
    a.move("UP")
    a.printState() 
    print
    print "the parent table"
    a.parent.parent.parent.printState()
    