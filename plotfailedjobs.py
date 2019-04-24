#!/usr/bin/python3
import numpy as np
import sys
import matplotlib
import matplotlib.pyplot as plt
#%matplotlib inline
matplotlib.style.use('ggplot')
f=open("failedjobs", "r")
contents = f.read()
jobs=[]
for line in contents.splitlines():
    jobs.append(line.split()[0])

num_bins = 60
n, bins, patches = plt.hist(jobs, num_bins, facecolor='blue', alpha=0.5)
plt.show()
