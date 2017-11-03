import numpy as np
import sys

np.random.seed(0)

gamma = 0.99
approx = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 0, 0, 0, 1],
    [0, 0, 2, 0, 0, 0, 0, 1],
    [0, 0, 0, 2, 0, 0, 0, 1],
    [0, 0, 0, 0, 2, 0, 0, 1],
    [0, 0, 0, 0, 0, 2, 0, 1],
    [0, 0, 0, 0, 0, 0, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0]
])


def print_estimate(weights):
    output = ""
    for i in range(1, 7):
        output += str(np.dot(weights, approx[i])) + " "
    print output


def next_state(start):
    if start in [1, 2, 3, 4, 5]:
        return 6
    elif start == 6:
        random_number = np.random.rand()
        if random_number <= 0.99:
            return 6
        else:
            return 7
    elif start == 7:
        sys.exit(0)


def expt1(n, weights):
    alpha = 0.001
    for i in range(n):
        start = (i % 6) + 1
        next = next_state(start)
        update = 0 + gamma * np.dot(weights, approx[next]) - np.dot(weights, approx[start])
        weights = weights + alpha * update * approx[start]
        print_estimate(weights)
    return weights


def expt2(n, weights, lmbda):
    alpha = 0.001
    updates = 0
    while updates <= n:
        state = np.random.randint(1, 6)
        e_trace = np.zeros(8)
        while state != 7:
            next = next_state(state)
            update = 0 + gamma * np.dot(weights, approx[next]) - np.dot(weights, approx[state])
            e_trace = gamma * lmbda * e_trace + approx[state]
            weights = weights + alpha * update * e_trace
            state = next
            updates += 1
            print_estimate(weights)
    return weights


expt = int(sys.argv[1])
n = int(sys.argv[2])
lmbda = float(sys.argv[3])
# Assume weights[0] is a dummy placeholder
weights = np.array([0] + [float(x) for x in sys.argv[4:11]])

if expt == 1:
    weights = expt1(n, weights)
else:
    weights = expt2(n, weights, lmbda)
