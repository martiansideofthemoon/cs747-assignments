import numpy as np
import subprocess

iterations = []
for i in range(0, 100):
    command = "./planner.sh --algorithm hpi --mdp data/MDP50_%d.txt" % i
    it = int(subprocess.check_output(command, shell=True))
    print("File %d - %d iterations" % (i, it))
    iterations.append(it)

print("Mean - %.6f" % np.mean(iterations))
print("Std - %.6f" % np.std(iterations))
