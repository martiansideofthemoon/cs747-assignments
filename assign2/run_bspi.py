import numpy as np
import subprocess

all_iterations = []

batch_sizes = [1, 2, 3, 4, 5, 8, 10, 15, 20, 25, 50]

for j in batch_sizes:
    iterations = []
    for i in range(0, 100):
        command = "./planner.sh --algorithm bspi --mdp data/MDP50_%d.txt --batchsize %d" % (i, j)
        it = int(subprocess.check_output(command, shell=True))
        print("File %d, Size %d - %d iterations" % (i, j, it))
        iterations.append(it)
    print("Mean (Size %d) - %.6f" % (j, np.mean(iterations)))
    print("Std (Size %d) - %.6f" % (j, np.std(iterations)))
