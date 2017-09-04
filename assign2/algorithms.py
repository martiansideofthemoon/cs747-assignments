import numpy as np
from pulp import *


class MDP(object):
    def __init__(self, filename):
        with open(filename, 'r') as f:
            data = f.read().split()
        self.states = states = int(data[0])
        self.actions = actions = int(data[1])
        index = 2

        self.rewards = np.zeros((states, actions, states))
        for i in range(states):
            for j in range(actions):
                for k in range(states):
                    self.rewards[i][j][k] = float(data[index])
                    index += 1

        self.transitions = np.zeros((states, actions, states))
        for i in range(states):
            for j in range(actions):
                for k in range(states):
                    self.transitions[i][j][k] = float(data[index])
                    index += 1

        # This tensor stores the value of R[s][a], which is a weighted summation of R[s][a][s'] and T[s][a][s']
        self.expected_rewards = np.sum(np.multiply(self.rewards, self.transitions), axis=2)
        self.discount = float(data[index])


def value_to_policy(mdp, values):
    policy = []
    for i in range(mdp.states):
        best_action = -1
        best_q = float("-inf")
        for j in range(mdp.actions):
            # Calculate Q[s][a] for value function `values`
            q_value = mdp.expected_rewards[i][j]
            for k in range(mdp.states):
                q_value += (mdp.discount * mdp.transitions[i][j][k]) * values[k]
            # argmax over Q[s][a]
            if q_value > best_q:
                best_action = j
                best_q = q_value
        policy.append(best_action)
    return policy


def policy_to_value(mdp, policy):
    b = np.array([mdp.expected_rewards[i][policy[i]] for i in range(mdp.states)])
    A = np.zeros((mdp.states, mdp.states))
    for i in range(mdp.states):
        A[i][i] += 1
        for j in range(mdp.states):
            A[i][j] += -1 * mdp.discount * mdp.transitions[i][policy[i]][j]
    values = np.linalg.solve(A, b)
    return values


def linear_program(mdp, args):
    prob = LpProblem("Optimal MDP Value Function", LpMinimize)
    values = [LpVariable("Value %d" % i) for i in range(mdp.states)]
    # Defining the objective function
    objective = 0
    for i in range(mdp.states):
        objective += values[i]
    prob += objective, "The sum of all value functions at different states"
    for i in range(mdp.states):
        for j in range(mdp.actions):
            future_reward = 0
            for k in range(mdp.states):
                future_reward += (mdp.discount * mdp.transitions[i][j][k]) * values[k]
            prob += values[i] >= mdp.expected_rewards[i][j] + future_reward, "constraint %d, %d" % (i, j)
    prob.solve()
    optimal_values = [v.varValue for v in values]
    optimal_policy = value_to_policy(mdp, optimal_values)
    # Recomputing optimal values from optimal policy to obtain higher precision
    optimal_values = policy_to_value(mdp, optimal_policy)
    return optimal_policy, optimal_values


def get_improvable_states(mdp, policy, values):
    improvable_states = []
    for i in range(mdp.states):
        current_q = mdp.expected_rewards[i][policy[i]]
        for k in range(mdp.states):
            current_q += (mdp.discount * mdp.transitions[i][policy[i]][k]) * values[k]
        # This function assumes a 2-action MDP only
        other_a = int(not policy[i])
        alternate_q = mdp.expected_rewards[i][other_a]
        for k in range(mdp.states):
            alternate_q += (mdp.discount * mdp.transitions[i][other_a][k]) * values[k]
        if alternate_q > current_q:
            improvable_states.append(i)
    return improvable_states


def howard_pi(mdp, args):
    policy = [0 for i in range(mdp.states)]
    values = policy_to_value(mdp, policy)
    improvable_states = get_improvable_states(mdp, policy, values)
    iterations = 0
    while len(improvable_states) > 0:
        for i in improvable_states:
            policy[i] = int(not policy[i])
        values = policy_to_value(mdp, policy)
        improvable_states = get_improvable_states(mdp, policy, values)
        iterations += 1
    return policy, values, iterations


def random_pi(mdp, args):
    np.random.seed(args.randomseed)
    policy = [0 for i in range(mdp.states)]
    values = policy_to_value(mdp, policy)
    improvable_states = get_improvable_states(mdp, policy, values)
    iterations = 0
    while len(improvable_states) > 0:
        for i in improvable_states:
            # This emulates a binomial distribution with p = 0.5
            if np.random.randint(2) == 1:
                policy[i] = int(not policy[i])
        values = policy_to_value(mdp, policy)
        improvable_states = get_improvable_states(mdp, policy, values)
        iterations += 1
    return policy, values, iterations


def batch_pi(mdp, args):
    batch_size = args.batchsize
    policy = [0 for i in range(mdp.states)]
    values = policy_to_value(mdp, policy)
    improvable_states = get_improvable_states(mdp, policy, values)
    iterations = 0
    while len(improvable_states) > 0:
        # `improvable_states` is always a sorted list
        # solving the leftmost batch first, equivalent to solving the right batches first,
        # since we can reorder batches to match exact algorithm
        active_batch = int(improvable_states[0] / batch_size)
        for i in improvable_states:
            if i >= active_batch * batch_size and i < (active_batch + 1) * batch_size:
                policy[i] = int(not policy[i])
        values = policy_to_value(mdp, policy)
        improvable_states = get_improvable_states(mdp, policy, values)
        iterations += 1
    return policy, values, iterations
