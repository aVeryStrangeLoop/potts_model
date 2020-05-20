# Part of the multistate-ising solver package written by Bhaskar Kumawat (@aVeryStrangeLoop)
# Filename : config.py
# Contains : configuration for running the solver
# Dependencies : numpy
import copy
import numpy as np
import random
import math

class cConfig:
    ### Configuration class contains all user-define parameters required during runtime  
    ### Change the following parameters as per liking
     
    STATES = np.array([0,1,2]) # Possible states of the system, given as a numpy array, each state type has an idx 
    ### Light = 0 , Dark = 1, Medium = 2    
 
    CONSERVED = False # If this is set to true, the mutator ensures that the total number of each state is conserved during the run
    
    FLIP_MODE = 0 #If conserved is False, a cell can be flipped in three ways #TODO
    # Global flip : mode = 0 - flip to any state
    # Four nearest neighbor flip : mode = 1 - flip to state of one of the four neighbors
    # Eight nearest neighbor flip : mode = 2 - flip to state of one of the eight neighbors     

    EXCHANGE_MODE = 0 # If Conserved is true, cells can be exchanged in three ways
    # Global exchange : mode= 0 
    # Four nearest neighbor exchange : mode = 1
    # Eight nearest neighbor exchange : mode = 2 


    DEBUG_MODE = False # Set to True to get a verbose output

    WORLD_X = 50 # Cells in X direction
    WORLD_Y = 50 # Cells in y direction

    MODE = 0 # Monte-carlo mode (0 = Constant temperature, 1 = cooling)

    MAX_MCS = 400

    steps = MAX_MCS*16.*WORLD_X*WORLD_Y # Total number of steps for monte_carlo(mode=0)/simulated annealing(mode=1)

    save_every = 10000 # Save system state every <save_every> steps

    ## Monte-Carlo temperature (if mode==0)
    temp_constant = 10.0
    
    ## Cooling properties (if mode ==1)
    temp_init = 1000.0 # Initial temperature (Only applicable if mode==1)
    temp_final = 0.1 # Final temperature (Only applicable if mode==1)

    def H(self,Z):
        # Hamiltonian calculation for a given grid Z
        # Z is a numpy array

        # Write your own code here to output the hamiltonian given a system configuration
        if self.DEBUG_MODE:
            print "Calculating hamiltonian"
        
        # Parameters for glazier model
        def J(s1,s2):
            J00 = 14. # Surface energy between 0-0 (light-light)
            J11 = 2. # Surface energy between 1-1 (dark-dark)
            J22 = 0. # Surface energy between 2-2 (med-med)


            J01 = 11. # Surface energy between 0-1 (light-dark)
        
            J12 = 16. # Surface energy between 1-2 (dark-medium)
            J02 = 16. # Surface energy between 0-2 (light-medium)
            
            if (s1==0 and s2==0):
                return J00
            elif (s1==1 and s2==1):
                return J11
            elif (s1==2 and s2==2):
                return J22
            elif (s1==0 and s2==1) or (s1==1 and s2==0):
                return J01
            elif (s1==1 and s2==2) or (s1==2 and s2==1):
                return J12
            elif (s1==0 and s2==2) or (s1==2 and s2==0):
                return J02

        lambda_area = 1. # Strength of area constraint

        target_areas = [100.,100.,-1] # Target area for the three cell types (light,dark,med)

        def theta(target_area):
            if target_area > 0:
                return 1.
            elif target_area < 0 :
                return 0.
        # Hamiltonian = summation (1 - delta(i,j,i',j'))
        h = 0.0

        X = Z.shape[0]
        Y = Z.shape[1]

        areas = [0.,0.,0.] #light,dark,medium

        # Add interaction energies (and count area of each state)
        for i in range(X):
            for j in range(Y):
                self_state = Z[i,j] # Get i,j's state 
                areas[self_state]+=1 # add to total area of this state
                neighbor_states = []
                #left neighbor
                if i-1>=0:
                    left_state = Z[i-1,j]
                else:
                    left_state = Z[X-1,j]
                neighbor_states.append(left_state)

                # right neighbor
                if i+1<=X-1:
                    right_state = Z[i+1,j]
                else:
                    right_state = Z[0,j]
                neighbor_states.append(right_state)

                # bottom neighbor
                if j-1>=0:
                    bot_state = Z[i,j-1]
                else:
                    bot_state = Z[i,Y-1]
                neighbor_states.append(bot_state)

                # top neighbor
                if j+1<=Y-1:
                    top_state = Z[i,j+1]
                else:
                    top_state = Z[i,0]    
                neighbor_states.append(top_state)

                for state in neighbor_states:
                    h += J(self_state,state)

        h = h/2. # compensate for double counting of neighbor pairs
                
        # Add area constraint energies
        for state in range(len(areas)):
            a = areas[state]
            A = target_areas[state]
            h += lambda_area * theta(A) * math.pow(a-A,2.)


        return h
    
    def StateMutator(self,cur_state):
        # Defines how a cell's state is mutated

        # For now we assume it's chosen randomly out of the given states, but it can also be constructed from cur_state
        new_state = random.choice(self.STATES)

        while new_state==cur_state:
            new_state = random.choice(self.STATES)      

        if self.DEBUG_MODE:
            print "%d state mutated to %d" % (cur_state,new_state)
        return new_state
        

    def Mutator(self,Z):
        ## If conserved status is false, mutate only one cell
        if not self.CONSERVED:
            # Give the system state derived after a monte-carlo step from Z
            # Coordinate of random cell
            i = random.randrange(0,Z.shape[0])
            j = random.randrange(0,Z.shape[1])
            # Choose any cell in Z and change its contents randomly to one of the states
            target_state = self.StateMutator(Z[i,j]) 
            if self.DEBUG_MODE:
                print "Conserved state mode OFF, randomly switching the cell state at (%d,%d) from %d to %d" % (i,j,Z[i,j],target_state)
            mut = np.copy(Z)
            mut[i,j] = target_state
            return mut

        ## If conserved status is true, swap two cells instead of just mutating one:
        elif self.CONSERVED:
            states_exchanged = False # This variable just makes sure we don't select the same cell index to exchange
            while not states_exchanged:             
                i1 = random.randrange(0,Z.shape[0])
                j1 = random.randrange(0,Z.shape[1])
   				
                if self.EXCHANGE_MODE==0: # Choose random cell         
                    i2 = random.randrange(0,Z.shape[0])
                    j2 = random.randrange(0,Z.shape[1])
                elif self.EXCHANGE_MODE==1: # Choose out of four nearest neighbors
                    direction = random.randrange(0,4)
                    if direction == 0: # Top
                        i2 = i1
                        j2 = j1+1
                        if j2>=Z.shape[1]:
                            j2 = j1
                    elif direction == 1: #Right
                        i2 = i1+1
                        j2 = j1
                        if i2>=Z.shape[0]:
                            i2 = i1
                    elif direction == 2: #Bottom
                        i2 = i1
                        j2 = j1-1
                        if j2<0:
                            j2 = j1
                    elif direction == 3: #Left
                        i2 = i1-1
                        j2 = j1
                        if i2<0:
                            i2 = i1
                elif self.EXCHANGE_MODE==2: # Choose out of four nearest neighbors
                    i2 = i1 + random.randrange(-1,2) # -1 to 1 
                    j2 = j1 + random.randrange(-1,2) # -1 to 1
                    if i2>=Z.shape[0] or i2<0 or j2>=Z.shape[1] or j2<0: 
                        i2 = i1
                        j2 = j1
               
                if not (Z[i1,j1]==Z[i2,j2]):
                    states_exchanged == True
                    state_1 = Z[i1,j1]
                    state_2 = Z[i2,j2]
                    
                    mut = np.copy(Z)
                    mut[i1,j1] = state_2
                    mut[i2,j2] = state_1

                    if self.DEBUG_MODE:
                        print "Conserved state mode ON, exchanging states %d and %d at (%d,%d) and (%d,%d) resp." % (state_1,state_2,i1,j1,i2,j2)
                    return mut
            

    def InitSys(self):
        # Sets the initial configuration of the system
        # For now it is chosen randomly from given states, change this function to change the initial config
        init = np.random.choice(self.STATES,(self.WORLD_X,self.WORLD_Y))
        if self.DEBUG_MODE:
            print "Initialised configuration,"
            print init
        return init
        

    # Sanity check to make sure all elements of Z are in self.STATES, private method 
    def __SanityCheck(self,Z):
        check = np.isin(Z,self.STATES)
        return np.all(check)

