import numpy as np
import sys
import matplotlib.pyplot as plt

if len(sys.argv)<2:
    print "image_draw.py plots the system configuration in a 2D grid specified in a numpy saved file of form mcs_<>.csv"
    print "usage : python image_draw.py <filename>"
    exit(0)

filename = sys.argv[1]

img = np.loadtxt(filename)

plt.imshow(img)
plt.show() 
