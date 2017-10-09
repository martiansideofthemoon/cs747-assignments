import numpy as np

actions = ['up', 'down', 'left', 'right']


class RandomAgent:
    def __init__(self):
        self.step = 0

    def getAction(self):
        '''samples actions in a round-robin manner'''
        self.step = (self.step + 1) % 4
        return 'up down left right'.split()[self.step]

    def observe(self, newState, reward, event):
        pass


class SarsaAgent:
    def __init__(self, gamma, lamb, numStates, state):
        self.gamma = gamma
        self.lamb = lamb
        self.numStates = numStates
        self.q_value = np.zeros((numStates, 4))
        self.e_trace = np.zeros((numStates, 4))
        self.start_state = self.current_state = state
        self.episodes = 1
        self.next_action = self.computeNextAction(state)

    def computeNextAction(self, state):
        new_epsilon = 1.0 / self.episodes
        if np.random.rand() < new_epsilon:
            action = np.random.randint(0, 4)
        else:
            action = np.argmax(self.q_value[state])
        return action

    def getAction(self):
        return actions[self.next_action]

    def observe(self, newState, reward, event):
        mode = 'accumalating'
        alpha = 0.1
        current_action = self.next_action
        self.next_action = self.computeNextAction(newState)

        if mode == 'accumalating':
            self.e_trace[self.current_state][current_action] += 1
        elif mode == 'replacing':
            self.e_trace[self.current_state][current_action] = 1

        increment = reward \
            + self.gamma * self.q_value[newState][self.next_action] \
            - self.q_value[self.current_state][current_action]

        self.q_value += alpha * increment * self.e_trace

        if event == 'continue':
            self.current_state = newState
            self.e_trace = self.gamma * self.lamb * self.e_trace
        elif event == 'terminated' or event == 'goal':
            self.current_state = self.start_state
            self.next_action = self.computeNextAction(self.start_state)
            self.episodes += 1
            self.e_trace = np.zeros((self.numStates, 4))


class QLearningAgent:
    def __init__(self, gamma, numStates, state):
        self.gamma = gamma
        self.numStates = numStates
        self.q_value = np.zeros((numStates, 4))
        self.start_state = self.current_state = state
        self.episodes = 1

    def getAction(self):
        new_epsilon = 1.0 / self.episodes
        if np.random.rand() < new_epsilon:
            self.current_action = np.random.randint(0, 4)
        else:
            self.current_action = np.argmax(self.q_value[self.current_state])
        return actions[self.current_action]

    def observe(self, newState, reward, event):
        alpha = 0.1
        current_val = self.q_value[self.current_state][self.current_action]
        self.q_value[self.current_state][self.current_action] += \
            alpha * (reward + self.gamma * np.max(self.q_value[newState]) - current_val)
        if event == 'continue':
            self.current_state = newState
        elif event == 'terminated' or event == 'goal':
            self.episodes += 1
            self.current_state = self.start_state


class Agent:
    def __init__(self, numStates, state, gamma, lamb, algorithm, randomseed):
        '''
        numStates: Number of states in the MDP
        state: The current state
        gamma: Discount factor
        lamb: Lambda for SARSA agent
        '''
        np.random.seed(randomseed)
        if algorithm == 'random':
            self.agent = RandomAgent()
        elif algorithm == 'qlearning':
            self.agent = QLearningAgent(gamma, numStates, state)
        elif algorithm == 'sarsa':
            self.agent = SarsaAgent(gamma, lamb, numStates, state)

    def getAction(self):
        '''returns the action to perform'''
        return self.agent.getAction()

    def observe(self, newState, reward, event):
        '''
        event:
            'continue'   -> The episode continues
            'terminated' -> The episode was terminated prematurely
            'goal'       -> The agent successfully reached the goal state
        '''
        self.agent.observe(newState, reward, event)

