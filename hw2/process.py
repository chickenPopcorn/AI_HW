#!/usr/bin/env python
#coding:utf-8

import os
import sys
def main():
    stats = {}
    numOfTrials = 0
    with open(sys.argv[1]) as fp:
        for line in fp:
            try:
                result = int(line)
                numOfTrials += 1
                if result in stats.keys():
                    stats[result] += 1
                else:
                    stats[result] = 1
            except:
                pass

    print str(numOfTrials) +" test run stats"
    accumStats = []
    l =  stats.keys()
    l.sort()
    for i in l:
        accumStats.append([i, stats[i]])
    for i in range(len(accumStats)):
        for n in range(i+1, len(accumStats)):
            accumStats[i][1] += accumStats[n][1]

    for i in accumStats:
        print "% of the games reached "+ str(i[0])+" and above: " + \
        str(round(i[1]/float(numOfTrials)*100.0, 2))+"%"

if __name__ == '__main__':
    main()
