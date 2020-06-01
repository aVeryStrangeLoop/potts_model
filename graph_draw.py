# Draw a graph of system energy over MCS
import sys
import matplotlib.pyplot as plt

folder = sys.argv[1]

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


color = "tab:red"
fig,ax1 = plt.subplots()
ax1.set_xlabel("MCS")
ax1.set_ylabel("Energy")
ax1.plot(mcs,energies,color=color)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

color = 'tab:blue'
ax2.set_ylabel('Temperature', color=color)  # we already handled the x-label with ax1
ax2.plot(mcs, temps, color=color)
ax2.tick_params(axis='y', labelcolor=color)

fig.tight_layout()  # otherwise the right y-label is slightly clipped
plt.show()
