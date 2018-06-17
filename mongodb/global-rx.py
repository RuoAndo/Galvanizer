#!/usr/bin/env python
# -*- coding:utf-8 -*-

import csv
import sys 
import os

argvs = sys.argv

f = open(str(argvs[1]), 'r')

for l in f:
    l = l.rstrip()
    try:
        comstr = "global -rx " + l
        # print l
        os.system(comstr)
    except:
        pass
f.close()
