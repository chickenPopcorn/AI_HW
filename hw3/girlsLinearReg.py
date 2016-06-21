

import numpy as np


# problem 1 part 1 a
def dataPrepA():
    data = {}
    data["age"] = []
    data["weight"] = []
    data["height"] = []
    data["ageScaled"] = []
    data["weightScaled"] = []

    dataFile = open("girls_age_weight_height_2_8.csv", "rb")
    for line in dataFile.read().split("\r\n"):
        items = line.split(",")
        data["age"].append(float(items[0]))
        data["weight"].append(float(items[1]))
        data["height"].append(float(items[2]))

    dataStats = {}
    dataStats["ageMean"] = numpy.mean(data["age"])
    dataStats["weightMean"] = numpy.mean(data["weight"])
    dataStats["ageStd"] = numpy,std(data["age"])
    dataStats["weightStd"] = numpy,std(data["weight"])

    print "Mean age is ", dataStats["ageMean"]
    print "Mean weight is ", dataStats["weightMean"]
    print "Std of age is ", dataStats["ageStd"]
    print "Std of  weight is ", dataStats["weightStd"]













if __name__ == "__main__":
    dataPrepA()
