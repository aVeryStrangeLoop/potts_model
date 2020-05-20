# Constant temperature monte carlo subroutine for multistate-ising solver
import numpy as np
import random
import math

	
def MonteCarlo(conf,ofile):
    
    MCheader(ofile) # Write header for summary file

    InitState = conf.InitSys() # Initialize a state using function specified in config

    optState = np.copy(InitState) # Stores the most optimal state ever encountered
    optEnergy = conf.H(optState)
 
    curState = np.copy(InitState) # Stores the current state in the Monte-Carlo run
    curEnergy = conf.H(curState)
	
    cur_step = 0

    while conf.steps >= cur_step:
		
        T_cur = conf.temp_constant

        PrintState(ofile,cur_step,T_cur,curEnergy,optEnergy)
        print(cur_step,T_cur,curEnergy,optEnergy)

        if cur_step%conf.save_every == 0 or cur_step==conf.steps:
            np.savetxt("results/mcs_"+str(cur_step)+".csv",curState)
        
        accepted = False
        
        neighborState = conf.Mutator(curState)
        neighborEnergy = conf.H(neighborState)
            
        isaccepted = ToAccept(curEnergy,neighborEnergy,T_cur)
            
        if isaccepted:
            curState = neighborState
            curEnergy = neighborEnergy
        
        if curEnergy < optEnergy:
            optState = curState
            optEnergy = curEnergy


        cur_step += 1

    np.savetxt("results/final_optimal_state.csv",optState)

def ToAccept(E_cur,E_new,T): # Acceptance probability
    if E_new < E_cur:
        return True
    else:
        delta = E_new-E_cur
        prob =  np.exp(-delta/T)
        if prob>random.random():
            return True
        else:
            return False


def MCheader(ofile):
    ofile.write("# RUNNING MONTE_CARLO MODULE##\n")
    ofile.write("# Written by Bhaskar Kumawat (@aVeryStrangeLoop)\n")
    ofile.write("cur_step,T,cur_energy,opt_energy\n")

def PrintState(ofile,step,T,cur_energy,opt_energy):
    ofile.write("%d,%f,%f,%f\n" % (step,T,cur_energy,opt_energy))
