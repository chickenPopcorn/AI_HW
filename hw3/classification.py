
import numpy
# basic arithmetics
import matplotlib.pyplot as plt
# ploting
from sklearn import cross_validation
from sklearn import svm
from sklearn.metrics import accuracy_score
import sklearn
from sklearn import linear_model
from sklearn import tree

def loadData(path):
    A = []
    B = []
    label = []
    dataFile = open(path, "rb")
    dataFile = dataFile.read().split("\r")
    for line in dataFile[1:]:
        items = line.split(",")
        A.append(float(items[0]))
        B.append(float(items[1]))
        label.append(int(items[2]))

    A1 = []
    B1 = []
    A0 = []
    B0 = []
    AB = []

    for i in range(len(label)):
        AB.append((A[i], B[i]))
        if label[i] == 1:
            A1.append(A[i])
            B1.append(B[i])
        else :
            A0.append(A[i])
            B0.append(B[i])
    return A0, A1, B0, B1, AB, label, A, B

def splitData(AB, label):
    # split data stratified sampling
    X_train = []
    X_test = []
    y_train = []
    y_test = []
    X_train, X_test, y_train, y_test = \
        cross_validation.train_test_split(AB, label, test_size=0.4, random_state=42, stratify=label)

    print "Total data entries", len(label)
    print "X training entries: ", len(X_train), " "
    print "y training entries: ", len(y_train), " "
    print "X testing entries: ", len(X_test), " "
    print "y testing entries: ", len(y_test), " "
    return X_train, X_test, y_train, y_test

def plotData(A0, A1, B0, B1):
    plotlabel0 = plt.scatter(A0, B0, marker = 'o', color = 'black')
    plotlabel1 = plt.scatter(A1, B1, marker = 'x', color = 'red')
    plt.legend((plotlabel0, plotlabel1), ('label 0', 'label 1'), scatterpoints = 1)
    plt.title("Scatter Plot of Chessboard Data")
    plt.xlabel('A')
    plt.ylabel('B')
    plt.show()

def plotDB(svmModel, A0, B0, A1, B1, title):
    xx, yy = numpy.meshgrid(numpy.arange(0, 4.2, 0.02), numpy.arange(0, 4.2, 0.02))
    plt.subplots_adjust(wspace=0.4, hspace=0.4)
    Z = svmModel.predict(numpy.c_[xx.ravel(), yy.ravel()])
    Z = Z.reshape(xx.shape)
    plot0 = plt.scatter(A0, B0, marker = "x", color = "red")
    plot1 = plt.scatter(A1, B1, marker = "o", color = "black")
    plt.legend((plot0, plot1), ('label 0', 'label 1'), scatterpoints = 1)
    plt.xlabel('A')
    plt.ylabel('B')
    plt.title(title.title() + " Kernel SVM")
    plt.contourf(xx, yy, Z, cmap=plt.cm.Paired, alpha=0.8)
    plt.show()


if __name__ == "__main__":
    A0, A1, B0, B1, AB, label, A, B = loadData("chessboard.csv")
    # plotData(A0, A1, B0, B1)
    X_train, X_test, y_train, y_test = splitData(AB, label)

    cValue = [1.0, 10.0, 100.0]

    print "-------------linear-------------------"
    bestC = 0
    bestScore = 0
    for c in cValue:
        print "linear SVM c = ", c
        clf = svm.SVC(kernel='linear', C=c)
        score = numpy.mean(cross_validation.cross_val_score(clf, X_train, y_train, cv=5))
        print "Average Score is ", score
        if score > bestScore:
            bestScore = score
            bestC = c
    clf = linear_model.LogisticRegression(C=bestC).fit(X_train, y_train)
    print "When c = ", bestC, "the linear kernel on test data accuracy:", accuracy_score(y_test, clf.predict(X_test))
    plotDB(clf, A0, B0, A1, B1, "linear")

    print "------------polynomial----------------"
    bestC = 0
    bestD = 0
    bestScore = 0
    degree = [2, 3, 4, 5]
    for c in cValue:
        for d in degree:
            print "poly SVM c = ", c, " degree = ", d
            clf = svm.SVC(C=c, kernel="poly", degree=d)
            score = numpy.mean(cross_validation.cross_val_score(clf, X_train, y_train, cv=5))
            print "Average Score is ", score
            if score > bestScore:
                bestScore = score
                bestC = c
                bestD = d
    clf = svm.SVC(C=bestC, kernel="poly", degree=bestD).fit(X_train, y_train)
    print "When c = ", bestC, "degree =", bestD, "the poly kernel on test data accuracy:", accuracy_score(y_test, clf.predict(X_test))
    plotDB(clf, A0, B0, A1, B1, "poly")

    print "---------------rbf--------------------"
    bestC = 0
    bestG = 0
    bestScore = 0
    gamma = [0.1, 1.0, 5.0, 10.0]
    for c in cValue:
        for g in gamma:
            print "rbf SVM c = ", c, " gamma = ", g
            clf = svm.SVC(C=c, kernel='rbf', gamma=g)
            score = numpy.mean(cross_validation.cross_val_score(clf, X_train, y_train, cv=5))
            print "Average Score is ", score
            if score > bestScore:
                bestScore = score
                bestC = c
                bestG = g
    clf = svm.SVC(C=bestC, kernel='rbf', gamma=bestG).fit(X_train, y_train)
    print "When c = ", bestC, "gamma =", bestG, "the rbf kernel on test data accuracy:", accuracy_score(y_test, clf.predict(X_test))
    plotDB(clf, A0, B0, A1, B1, "RBF")

    print "--------logistic regression-----------"
    bestC = 0
    bestScore = 0
    for c in cValue:
        print "logistic regression c = ", c
        clf = linear_model.LogisticRegression(C=c)
        score = numpy.mean(cross_validation.cross_val_score(clf, X_train, y_train, cv=5))
        print "Average Score is ", score
        if score > bestScore:
            bestScore = score
            bestC = c
    clf = linear_model.LogisticRegression(C=bestC).fit(X_train, y_train)
    print "When c = ", bestC, "the logistic regression model on test data accuracy:", accuracy_score(y_test, clf.predict(X_test))
    plotDB(clf, A0, B0, A1, B1, "Logistic Regression")

    print "--------decision tree-----------"
    bestDepth = 0
    bestScore = 0
    depths = [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0]
    for depth in depths:
        print "decision tree depth = ", depth
        clf = tree.DecisionTreeClassifier(max_depth=depth)
        score = numpy.mean(cross_validation.cross_val_score(clf, X_train, y_train, cv=5))
        print "Average Score is ", score
        if score > bestScore:
            bestScore = score
            bestDepth = depth
    clf = tree.DecisionTreeClassifier(max_depth=bestDepth).fit(X_train, y_train)
    print "When depth = ", bestDepth, "the decision tree model on test data accuracy:", accuracy_score(y_test, clf.predict(X_test))
    plotDB(clf, A0, B0, A1, B1, "Decision Tree")
