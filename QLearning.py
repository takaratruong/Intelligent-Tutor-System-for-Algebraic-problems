import ast
import math
import random


class QLearning:
    def __init__(self, mdp_actions, q_init, step_mode):
        self.actions = mdp_actions
        self.gamma = 0.95  # discount rate
        self.epsilon = 0.3  # exploration rate
        self.num_iterations = 0
        self.Q = q_init
        self.step_mode = step_mode

    def getAction(self, state):
        self.num_iterations += 1
        if random.random() < self.epsilon:
            return random.choice(self.actions(state))
        else:
            return max((self.Q[str((state, a))], a) for a in self.actions(state))[1]

    def stepsize(self):
        if self.step_mode == 'decay':
            return 1 / math.sqrt(self.num_iterations)
        else:
            return .5

    def updateQ(self, curr_state, action, reward, nxt_state):
        Q_max = max((self.Q[str((nxt_state, a))], a) for a in self.actions(nxt_state))[0]
        self.Q[str((curr_state, action))] = self.Q[str((curr_state, action))] + self.stepsize() * (
                reward + self.gamma * Q_max - self.Q[str((curr_state, action))])

    def optimalPolicy(self):
        states_actions = [ast.literal_eval(key) for key in self.Q]
        states = [val[0] for val in states_actions]
        policy = {}
        for state in states:
            policy[state] = max((self.Q[str((state, a))], a) for a in self.actions(state))[1]
        return policy
