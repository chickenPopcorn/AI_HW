#!/usr/bin/env python
#coding:utf-8


import os
n = 0
while n < 10:
    os.system("python test.py >> output.txt")
    n += 1
