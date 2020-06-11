# Find the bulk boundary length between spin-type interfaces
# Made for potts_model respository by Bhaskar Kumawat (github.com/aVeryStrangeLoop)
# Works only for the three state system implemented for PH 354 project.
import sys
import numpy as np

def GetBoundaries(type_array):
    # Given a 2D numpy array containing spin types, get the boundary values
    # Assumes periodic boundaries
    B01 = 0 # light-dark
    B12 = 0 # dark-medium
    B02 = 0 # light-medium

    X_MAX = type_array.shape[0]
    Y_MAX = type_array.shape[1]

    for i in range(X_MAX):
        for j in range(Y_MAX):
            my_type    = type_array[i,j]
            n_types    = []

            n_types.append(type_array[i-1,j] if i-1>=0 else type_array[X_MAX-1,j]) # left
            n_types.append(type_array[i+1,j] if i+1<X_MAX else type_array[0,j])    # right
            n_types.append(type_array[i,j-1] if j-1>=0 else type_array[i,Y_MAX-1]) # bottom
            n_types.append(type_array[i,j+1] if j+1<Y_MAX else type_array[i,0])    # top

            if my_type == 0:
                for ntype in n_types:
                    if ntype == 1:
                        B01 += 1
                    elif ntype == 2:
                        B02 += 1
            
            elif my_type == 1:
                for  ntype in n_types:
                    if ntype == 0:
                        B01 += 1
                    elif ntype == 2:
                        B12 += 1
            
            elif my_type == 2:
                for ntype in n_types:
                    if ntype == 1:
                        B12 += 1
                    elif ntype == 0:
                        B02 += 1

    # Calculate total lengths
    B0 = B01 + B02
    B1 = B01 + B12
    B2 = B12 + B02

    return [[B0,B1,B2],[B01,B12,B02]] # Return value consists of two numpy arrays


if __name__=="__main__":
    foldername = sys.argv[1]
    init = int(sys.argv[2])
    fin  = int(sys.argv[3])
    step = int(sys.argv[4])

    outfile = open("boundaries.csv","w+")
    outfile.write("mcs,b0,b1,b2,b01,b12,b02\n")
    for mcs in range(init,fin+1,step):
        print("Calculating for mcs = %d" % mcs)
        arr = np.loadtxt(foldername+"/mcs_"+str(mcs)+".csv")
        bounds = GetBoundaries(arr)
        outfile.write("%d,%d,%d,%d,%d,%d,%d\n" % (mcs,bounds[0][0],bounds[0][1],bounds[0][2],bounds[1][0],bounds[1][1],bounds[1][2]))

    outfile.close()
