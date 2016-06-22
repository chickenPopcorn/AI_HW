
import numpy
# basic arithmetics
import matplotlib.pyplot as plt
# ploting

def openDataPlot(path):
    data = {}
    data["A"] = []
    data["B"] = []
    data["label"] = []
    dataFile = open(path, "rb")
    dataFile = dataFile.read().split("\r")
    for line in dataFile[1:]:
        items = line.split(",")
        data["A"].append(float(items[0]))
        data["B"].append(float(items[1]))
        data["label"].append(int(items[2]))

    cData = {}
    cData["A1"] =[]
    cData["B1"] =[]
    cData["A0"] =[]
    cData["B0"] =[]


    for i in range(len(data["label"])):
        if data["label"][i] == 1:
            cData["A1"].append(data["A"][i])
            cData["B1"].append(data["B"][i])
        else :
            cData["A0"].append(data["A"][i])
            cData["B0"].append(data["B"][i])

    plotlabel0 = plt.scatter(cData["A0"], cData["B0"], marker='o', color = 'black')
    plotlabel1 = plt.scatter(cData["A1"], cData["B1"], marker = 'x', color = 'red')
    plt.legend((plotlabel0, plotlabel1), ('label 0', 'label 1'), scatterpoints = 1)
    plt.title("Scatter Plot Of Chessboard Data")
    plt.xlabel('A')
    plt.ylabel('B')
    plt.show()



if __name__ == "__main__":
    openDataPlot("chessboard.csv")
