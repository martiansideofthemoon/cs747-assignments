"""This script conducts a brute force over algos / seeds."""
import itertools
import os
import subprocess
import time

num_arms = ["5", "25"]
seed = [str(i) for i in range(100)]
algorithm = ["rr", "epsilon-greedy", "UCB", "KL-UCB", "Thompson-Sampling"]
SKIP = 607

lists = [num_arms, algorithm, seed]
lists = list(itertools.product(*lists))

for i, job in enumerate(lists):
    if i < SKIP:
        continue
    job_str = job[0] + "_" + job[1] + "_" + job[2]
    print "Job #" + str(i) + " - " + job_str
    os.chdir("server")
    args = ["./startserver.sh", job[0], "100000", "5001", "../data/instance-" + job[0] + ".txt", job[2], job_str + ".txt"]
    p_server = subprocess.Popen(args)
    time.sleep(0.1)
    os.chdir("../client")
    args = ["./startclient.sh", job[0], "100000", "localhost", "5001", job[2], job[1], "0.1"]
    p_client = subprocess.Popen(args)
    os.chdir("..")
    p_server.wait()
