import operator
import random
import ujson
import util


class MDP:
    def __init__(self):
        self.bins = ujson.load(open('data\problemBank.json', 'r'))
        self.FEATURE_TUPLE_LIMIT = self.bins['state_limit']
        self.num_states = self.bins['num_states']
        self.BASE_PROBLEM_KEY = tuple([-1] * self.num_states)
        self.problem = None
        self.curr_state_response_time = 0

        self.status = None
        self.sim_student = None

    def start_state(self):
        self.problem = (random.choice(self.bins[str(self.BASE_PROBLEM_KEY)]))
        return self.BASE_PROBLEM_KEY

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

    def successor(self, state, action):
        nxt_state = tuple(map(operator.add, state, action))
        self.problem = random.choice(self.bins[str(nxt_state)])
        return nxt_state

    def reward(self, state, action, next_state):
        reward = 0
        if self.sim_student is not None:
            val, nxt_state_response_time = util.students(self.sim_student, next_state, self.problem)
        else:
            val, nxt_state_response_time = util.usr_input(self.problem)

        response = nxt_state_response_time - self.curr_state_response_time

        self.curr_state_response_time = nxt_state_response_time

        if val == 'q':
            if self.sim_student is None:
                self.status = 'Quit'
            return 0

        if val == 'n':
            reward = -abs(response)
            if self.sim_student is None:
                self.status = 'Next'
            print("Next Question!")

        if val != 'q' and val != 'n':
            if int(val) == (self.problem[0] + self.problem[1]):
                reward = response
                if self.sim_student is None:
                    print("Correct! it took you " + str(int(reward)) + " seconds longer than the last problem!")
            else:
                reward = -abs(response)
                if self.sim_student is None:
                    print("Incorrect! it took you " + str(int(reward)) + " seconds longer than the last problem!")

        return reward

    def isEnd(self, state):
        if self.status == 'Quit':
            return True
        else:
            return False
