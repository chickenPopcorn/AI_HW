

import numpy
# basic arithmetics
import matplotlib.pyplot as plt
# ploting

def dataPrep(path):
    # problem 1 part 1 a
    data = {}
    data["age"] = []
    data["weight"] = []
    data["height"] = []
    data["ageScaled"] = []
    data["weightScaled"] = []
    data["intercept"] = []
    dataFile = open(path, "rb")
    for line in dataFile.read().split("\r\n"):
        items = line.split(",")
        data["age"].append(float(items[0]))
        data["weight"].append(float(items[1]))
        data["height"].append(float(items[2]))

    dataStats = {}
    dataStats["ageMean"] = numpy.mean(data["age"])
    dataStats["weightMean"] = numpy.mean(data["weight"])
    dataStats["ageStd"] = numpy.std(data["age"])
    dataStats["weightStd"] = numpy.std(data["weight"])

    print "Mean age is ", dataStats["ageMean"]
    print "Mean weight is ", dataStats["weightMean"]
    print "Std of age is ", dataStats["ageStd"]
    print "Std of  weight is ", dataStats["weightStd"]

    # problem 1 part 1 b
    for index in range(len(data["age"])):
        data["ageScaled"].append((data["age"][index]-dataStats["ageMean"])/dataStats["ageStd"])

    for index in range(len(data["weight"])):
        data["weightScaled"].append((data["weight"][index]-dataStats["weightMean"])/dataStats["weightStd"])

    return data, dataStats


def gradientDescent(data, dataStats):
    # problem 2 part a
    alphaValues = [0.005, 0.001, 0.05, 0.1, 0.5, 1.0]
    iteration = 50
    costFunc = [[], [], [], [], [], []]
    n = len(data["age"])
    for alpha in alphaValues:
        beta0 = 0.0
        beta1 = 0.0
        beta2 = 0.0

        for iterIndex in range(iteration):
            sum0 = 0.0
            sum1 = 0.0
            sum2 = 0.0
            for i in range(n):
                divation =  (beta0 + beta1 * data["ageScaled"][i] +\
                beta2 * data["weightScaled"][i] - \
                data["height"][i])

                sum0 += divation
                sum1 += divation * data["ageScaled"][i]
                sum2 += divation * data["weightScaled"][i]

            # simultaneous update
            beta0 -= alpha/n * sum0
            beta1 -= alpha/n * sum1
            beta2 -= alpha/n * sum2
            leastSq = 0
            for i in range(n):
                leastSq += (data["height"][i] - (beta0 + beta1 * data["ageScaled"][i] + beta2 * \
                            data["weightScaled"][1])) ** 2
            print leastSq/(2*n)
            costFunc[alphaValues.index(alpha)].append(leastSq/(2*n))
        print "next iter"
    x = [i for i in range(iteration)]
    a = [0] * len(alphaValues)
    for i in range(len(alphaValues)):
        plt.plot(x, costFunc[i])
        a[i], = plt.plot(x,costFunc[i])
    plt.legend(a,["alpha = 0.005","alpha = 0.001","alpha = 0.05","alpha = 0.1","alpha = 0.5","alpha = 1.0"])
    plt.title('risk function at different learning rates')
    plt.xlabel('iteration')
    plt.ylabel('risk')
    plt.show()

    # problem 2 part d
    age = 5
    weight = 20
    ageScaled = (age - dataStats["ageMean"])/dataStats["ageStd"]
    weightScaled = (weight - dataStats["weightMean"])/dataStats["weightStd"]
    Ans = beta0 + beta1 * ageScaled + beta2 * weightScaled
    print "A "+str(age)+" years old girl weighing "+str(weight)+" kilos should have height "+str(Ans)+" meters"

if __name__ == "__main__":
    data, stats = dataPrep("girls_age_weight_height_2_8.csv")
    gradientDescent(data, stats)
