# observed_states: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
# environment_states: (the actual problem associated with the observed states, number of problems passed, game_status: skip, quit, continue )
# STATE STRUCTURE a tuple consisting of 2 tuples : ( (observed_states), (environment_states) )
import operator
import random
import time
import collections
import json
import pprint
import util
from SimulatedStudent import student1

class MDP:
    def __init__(self):
        self.bins = json.load(open('../data/problemBank.txt', 'r'))
        self.FEATURE_TUPLE_LIMIT = self.bins['state_limit']
        self.num_states = self.bins['num_states']
        self.BASE_PROBLEM_KEY = tuple([-1] * self.num_states)
        self.number_of_passed = 1
        self.problem = None
        self.curr_state_time = 0

        #Temporary
        self.status = None
        self.useSimulatedStudent = True
    # Amanda
    def startState(self):
        self.problem = (random.choice(self.bins[str(self.BASE_PROBLEM_KEY)]))
        return self.BASE_PROBLEM_KEY

    # Cortney
    # observed_state: (num_1_digit, num_2_digit, carry_ops, zero_count, isTrail)
    def actions(self, state):
        valid_actions = list()
        stay = tuple([0] * self.num_states)

        valid_actions.append(stay)
        # if BASE_PROBLEM_KEY the next problem will (deterministically) be a 1-digit + 1-digit (no carry op) question
        if state == self.BASE_PROBLEM_KEY:
            valid_actions.append((2, 2, 1, 1))
            return valid_actions
        # otherwise we can try to increment/decrement every feature
        for i in range(self.num_states):
            for j in [-1, 1]:
                if state[i] + j in self.FEATURE_TUPLE_LIMIT[i]:
                    action = tuple([j if k == i else 0 for k in range(self.num_states)])
                    if str(tuple(map(operator.add, state, action))) in self.bins.keys():
                        valid_actions.append(action)

        return valid_actions

    # Amanda
    #def create_problem(self, state):
        #try:
            #if state in self.bins and len(self.bins[state]) > 0:
       # new_problem = random.choice(self.bins[str(state)])
        #print("Create Problem Successfully!", new_problem)
        #return Problem(new_problem[0], new_problem[1])
        #except:
        #    raise Exception('Cannot find matching tuple in problem bank for next state : ', state)

    #def successor_state(self, state, action):
    #    try:
    #        add_result = tuple(map(operator.add, state, action))
    #        return add_result
    #    except:
    #       raise Exception("Operation add failed for next state")

    def successor(self, state, action):
        nxt_state = tuple(map(operator.add, state, action))
        self.problem = random.choice(self.bins[str(nxt_state)])
        self.number_of_passed += 1
        return nxt_state

    # Takara
    def reward(self, state, action, next_state):
        print(next_state)

        if self.number_of_passed % 100 == 0:
            self.isStudent(state)

        if self.useSimulatedStudent:
            reward = student1(self.problem[0], self.problem[1])
            return reward

        prompt = "{} + {} = \n".format(self.problem.x, self.problem.y)
        start_time = time.time()

        val = ""
        while val == "":
            val = input(prompt)

        next_state_time = time.time() - start_time

        reward = self.curr_state_time - next_state_time
        self.curr_state_time = next_state_time
        val, response_time = util.usr_input(Pr)
        if val == 'q':
            self.status = 'Quit'
            return 0

        if val == 'n':
            self.status = 'Next'
            print("Next Question!")
            return -abs(reward)

        if int(val) == (self.problem.x + self.problem.y):
            print("Correct! it took you " + str(int(reward)) + " seconds!")
            reward = reward
        else:
            print("Incorrect!")
            reward = -abs(reward)

        return reward

    def isStudent(self, state):
        prompt = "continue simulation?"
        val = input(prompt)
        if val == 'y':
            return
        else:
            self.useSimulatedStudent = False
            return

    # Takara
    def isEnd(self, state):
        if self.status == 'Quit':
            return True
        else:
            return False

class QLearning:
    def __init__(self, mdp_actions, q_init):
        self.actions = mdp_actions
        self.gamma = 0.95   # discount rate
        self.epsilon = 0.3  # exploration rate
        self.numIters = 0
        self.Q = q_init

    def getAction(self, state):
        if random.random() < self.epsilon:
            return random.choice(self.actions(state))
        else:
            return max((self.Q[(state, a)], a) for a in self.actions(state))[1]

    def stepsize(self):
        return .5

    def updateQ(self, curr_state, action, reward, nxt_state):
        Q_max = max((self.Q[(nxt_state, a)], a) for a in self.actions(nxt_state))[0]
        self.Q[(curr_state, action)] = self.Q[(curr_state, action)] + self.stepsize() * (
                reward + self.gamma * Q_max - self.Q[(curr_state, action)])

#Simulation
def simulate(loadPath=None, savePath=None):

        if loadPath is None:
            q_init = collections.defaultdict(lambda: 0)
        else:
            q_init = collections.defaultdict(lambda: 0)

        mdp = MDP()
        ql = QLearning(mdp.actions, q_init)
        episode_rewards = []

        cur_state = mdp.startState()
        while mdp.isEnd(cur_state) is False:

            action = ql.getAction(cur_state)

            nxt_state = mdp.successor(cur_state, action)
            reward = mdp.reward(cur_state, action, nxt_state)
            ql.updateQ(cur_state, action, reward, nxt_state)

            cur_state = nxt_state
            episode_rewards.append(reward)

        return ql.Q

if __name__ == '__main__':

    Q_table = simulate()
    pprint.pprint(Q_table, width=1)



