import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--output", default="data/MDP50_0.txt", type=str, help="Output file")
parser.add_argument("--randomseed", default=0, type=int, help="Seed to be used in rpi")
args = parser.parse_args()

np.random.seed(args.randomseed)

S = 50
A = 2

R = np.random.uniform(-1.0, 1.0, [S, A, S])
T = np.random.uniform(0.0, 1.0, [S, A, S])
T = np.divide(T, np.sum(T, axis=2, keepdims=True))

gamma = 0.99

output = ""
output += str(S) + "\n"
output += str(A) + "\n"

for s in range(0, S):
    for a in range(0, A):
        for sPrime in range(0, S):
            output += str(R[s][a][sPrime]) + "\t"
        output += "\n"

for s in range(0, S):
    for a in range(0, A):
        for sPrime in range(0, S):
            output += str(T[s][a][sPrime]) + "\t"
        output += "\n"

output += str(gamma) + "\n"

with open(args.output, 'w') as f:
    f.write(output)
