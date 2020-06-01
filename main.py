# Main file to run the multistate-ising optimization routine
# Written by Bhaskar Kumawat for PH354 as a part of the multistate-ising package

from config import cConfig
from simulated_annealing import SimulatedAnneal
from monte_carlo import MonteCarlo
import sys
import datetime 
import numpy as np
import os

def main(args):
    # Get configuration from the cConfig.py file
    conf = cConfig()
    
    if not os.path.exists('results'):
         os.makedirs('results')


    # Start an output file where all the results will be stored
    ofile = open("results/summary.csv","w+")
    WriteHeader(ofile,conf)

    if conf.MODE == 0:
        MonteCarlo(conf,ofile)
    elif conf.MODE == 1: 
        SimulatedAnneal(conf,ofile)




################################## ACCESORY FUNCTIONS
## FUNCTION TO WRITE OUTPUT FILE HEADER
def WriteHeader(ofile,conf):
    ofile.write("# OUTPUT FILE FOR MULTISTATE-ISING SOLVER \n")
    ofile.write("# Written by Bhaskar Kumawat (github.com/aVeryStrangeLoop)\n")

    ofile.write("# RUN STARTED AT,"+str(datetime.datetime.now())+"\n")

    ofile.write("# WORLD_X,%d\n" % conf.WORLD_X)
    ofile.write("# WORLD_Y,%d\n" % conf.WORLD_Y)
    ofile.write("# START OF OPTIMIZER OUTPUTS #\n")

if __name__=="__main__":
    main(sys.argv)


