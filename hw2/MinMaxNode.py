from Grid import Grid
import copy

class MinMaxNode:
    def __init__(self, grid, direct= None, hValue = None):
        self.grid = copy.deepcopy(grid)
        self.hValue = MinMaxNode.getEmptyTile(grid) + MinMaxNode.getMaxTile(grid)[0]
        self.children = []
        self.direct = direct

    def makeChild(self):
        self.children.append(MinmaxTree(self.grid, direct))

    @staticmethod
    def getEmptyTile(grid):
        count = 0
        for i in range(len(grid.map)):
            for n in range(len(grid.map[i])):
                if grid.map[i][n] == 0:
                    count += 1
        return count

    @staticmethod
    def getMaxTile(grid):
        maxTile = 0
        pos = (0, 0)
        for i in range(len(grid.map)):
            for n in range(len(grid.map[i])):
                maxTile = max(maxTile, grid.map[i][n])
                pos = (i, n)
        return (maxTile, pos)


    def __str__(self):
        string = ""
        for i in range(len(self.grid.map)):
            for n in range(len(self.grid.map[i])):
                string += str(self.grid.map[i][n]) + " "
            string += "\n"
        string += "it's hValue is "+ str(self.hValue)+ "\n"
        string += "children are"
        if len(self.children) > 0:
            for i in self.children:
                string += i.direct +" "
            string += "\n"
        else:
            string += " None"
        return string

if __name__ == "__main__":
    g = Grid()
    g.map[3][0] = 4
    node = MinMaxNode(g)
    print node

