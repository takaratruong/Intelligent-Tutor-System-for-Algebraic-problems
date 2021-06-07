import MDP
import QLearning
import util
import copy


# Simulation
def simulate(load_q_filename=None, save_q_filename=None, sim_student_filename=None, step_mode="decay",
             convergence_mode=None, optimal_states=None, consecutive_counter_limit=10,
             max_iter=100000, verbose=True):

    if sim_student_filename is None:
        print("commands: q to quit, n for next question")

    # load data
    q_init = util.load_q(load_q_filename)
    sim_student = util.load_student(sim_student_filename)

    # initialize MDP and RL
    mdp = MDP.MDP()
    mdp.sim_student = sim_student
    ql = QLearning.QLearning(mdp.actions, q_init, step_mode)

    # initialize loop variables
    Q_old = copy.deepcopy(q_init)
    for key in Q_old:
        Q_old[key] = 1
    consecutive_counter = 0

    # Main Q-learning functionality
    cur_state = mdp.start_state()
    for _ in range(max_iter):
        action = ql.getAction(cur_state)
        nxt_state = mdp.successor(cur_state, action)
        reward = mdp.reward(cur_state, action, nxt_state)
        ql.updateQ(cur_state, action, reward, nxt_state)

        cur_state = nxt_state

        # convergence criteria for finding optimal policy, approx relative error between iterations
        if convergence_mode == 'find_optimal_policy':
            ea = max([abs(ql.Q[key] - Q_old[key]) / (Q_old[key] if Q_old[key] != 0 else 1) for key in ql.Q])
            if ea < .001:
                consecutive_counter += 1
            else:
                consecutive_counter = 0
            Q_old = copy.deepcopy(ql.Q)

        # convergence criteria for determining if algorithm hovers around appropriate state
        if convergence_mode == 'evaluate_algorithm':
            flag = 0
            for optimal_state in optimal_states:
                # get all state action pairs from the appropriate states where the Q value is greater than 0
                action_value = [(ql.Q[str((optimal_state, a))], a) for a in mdp.actions(optimal_state) if
                                ql.Q[str((optimal_state, a))] > 0]

                # check if the action is to stay
                if len(action_value) > 0:
                    optimal_action_for_optimal_state = max(action_value)[1]

                    if optimal_action_for_optimal_state == (0, 0, 0, 0):
                        flag = 1
                        break
            if flag == 1:
                consecutive_counter += 1
            else:
                consecutive_counter = 0

        # break upon consecutive counts or if mdp ends
        if (consecutive_counter >= consecutive_counter_limit) and convergence_mode is not None or mdp.isEnd(cur_state):
            break

    # useful information to print, only for simulation
    if verbose and convergence_mode is not None:
        print("----------------------------------------------")
        if sim_student is not None:
            print("Converged in: " + str(ql.num_iterations) + " iterations\n")

            optimal_states = sorted(
                [(sim_student[key][0], sim_student[key][2], key) for key in sim_student if sim_student[key][0] > 0],
                reverse=True)

            print("Optimal States:")
            print(optimal_states)

        print("\nOptimal Policy")
        optimal_policy = ql.optimalPolicy()
        for key in sorted(optimal_policy):
            print(str(key) + ": " + str(optimal_policy[key]))
        print("----------------------------------------------")

    if sim_student_filename is None:
        return

    util.save_q(save_q_filename, ql.Q)
    return ql.num_iterations, ql.optimalPolicy()


# How quickly can the algorithm give an appropriate level problem?
def experiment1(sim_student, runs):
    results = []
    for _ in range(runs):
        iter, pol = simulate(sim_student_filename=sim_student, step_mode="decay",
                             convergence_mode='find_optimal_policy', consecutive_counter_limit=50, verbose=False)
        opt = [key for key in pol if pol[key] == (0, 0, 0, 0)]
        if opt is not None:
            iter_eval, pol2 = simulate(sim_student_filename=sim_student, step_mode="const",
                                       convergence_mode='evaluate_algorithm', optimal_states=opt,
                                       consecutive_counter_limit=5, verbose=False)
            results.append(iter_eval)
    return results


# Can we use pre-training to make the algorithm faster?
def experiment2(load_student, sim_student, runs):
    results = []
    for _ in range(runs):
        iter1, pol = simulate(sim_student_filename=sim_student, step_mode="decay",
                             convergence_mode='find_optimal_policy', consecutive_counter_limit=50, verbose=False)
        opt = [key for key in pol if pol[key] == (0, 0, 0, 0)]

        iter2, pol_combined = simulate(sim_student_filename=load_student, save_q_filename = 'data/combined_q.json', step_mode="decay",
                             convergence_mode='find_optimal_policy', consecutive_counter_limit=50, verbose=False)

        if opt is not None:
            iter_eval, pol2 = simulate(load_q_filename='data/combined_q.json', sim_student_filename=sim_student, step_mode="const",
                                       convergence_mode='evaluate_algorithm', optimal_states=opt,
                                       consecutive_counter_limit=5, verbose=False)
            results.append(iter_eval)
    return results


if __name__ == '__main__':

    # give it a try! Pre-trained
    #simulate(load_q_filename='data/combined_takara_cortney_normalzied.json', step_mode="const", verbose=False)

    # start fresh!
    simulate(step_mode="const", verbose=False)

    # Experiment 1 ##################################################
    """
    conv_a = experiment1('data/student_amanda.json', 100)
    print(conv_a)

    conv_c = experiment1('student_cortney.json', 100)
    print(conv_c)

    conv_t = experiment1('data/student_takara.json', 100)
    print(conv_t)    
    """

    # Experiment 2 ##################################################
    """
    conv_a = experiment2('data/combined_takara_cortney_normalzied.json', 'data/student_amanda.json', 100)
    print(conv_a)
    """