import numpy as np
import subprocess

all_iterations = []

for j in range(0, 10):
    iterations = []
    for i in range(0, 100):
        command = "./planner.sh --algorithm rpi --mdp data/MDP50_%d.txt --randomseed %d" % (i, j)
        it = int(subprocess.check_output(command, shell=True))
        print("File %d, Seed %d - %d iterations" % (i, j, it))
        iterations.append(it)
        all_iterations.append(it)
    print("Mean (Seed %d) - %.6f" % (j, np.mean(iterations)))
    print("Std (Seed %d) - %.6f" % (j, np.std(iterations)))

print("Mean - %.6f" % np.mean(all_iterations))
print("Std - %.6f" % np.std(all_iterations))
