# Generate a movie of the run using outputs in the results folder
import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

if len(sys.argv)<3:
    print "movie_gen.py generates a movie using the mcs_.csv system configuration files in the given folder"
    print "usage : python movie_gen <folder> <save_every>"
    print "NOTE: The given folder must contain the summary.csv file containing temperature and energy data about mcs steps"
    exit(0)

folder = sys.argv[1]
save_every = int(sys.argv[2])

mcs = []
temps = []
energies = []

# Get metadata from summary.csv
with open(folder+"/summary.csv") as sfile:
    for line in sfile:
        words = line.split(",")
        if line[0]!="#" and line[0]!="\n" and words[0]!="cur_step":
            cur_mcs = int(words[0])
            cur_temp = float(words[1])
            cur_ener = float(words[2])
            mcs.append(cur_mcs)
            temps.append(cur_temp)
            energies.append(cur_ener)


def GetSys(mcs):
    print "getting data for mcs %d" % mcs
    img = np.loadtxt(folder+"/mcs_"+str(mcs)+".csv")
    return img

fig = plt.figure()
ax = plt.axes()
plot = ax.imshow(GetSys(0))

def init():
    plot.set_data(GetSys(0))
    return [plot]

def animate(step):
    print "animating step %d" % step
    data = GetSys(step)
    plot.set_data(data)
    cur_mcs = step
    cur_temp = temps[mcs.index(cur_mcs)]
    cur_energy = energies[mcs.index(cur_mcs)]
    ax.set_title("mcs = %d , temp = %f , energy = %f" % (cur_mcs,cur_temp,cur_energy))
    return [plot]

saves= []
for step in mcs:
    if step%save_every==0:
        saves.append(step)

Writer = animation.writers['ffmpeg']
writer = Writer(fps=15,bitrate=1800)

anim = FuncAnimation(fig,animate,init_func=init,frames=saves,blit=True)

anim.save('test.mp4',writer=writer)




