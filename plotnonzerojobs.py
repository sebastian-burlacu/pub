#!/usr/bin/python3
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
matplotlib.style.use('ggplot')
f=open("times/0423", "r")
contents = f.read()
jobs=[]
for line in contents.splitlines():
    jobs.append(line.split()[0])

num_bins = 1440
n, bins, patches = plt.hist(jobs, num_bins, facecolor='blue', alpha=0.5)
plt.show()

#from collections import Counter
#counted = Counter(jobs)
#print(counted)
