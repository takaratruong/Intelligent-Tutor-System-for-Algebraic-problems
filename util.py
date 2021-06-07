import time
import collections
import ujson
import random

def usr_input(problem):
    prompt = "{} + {} = \n".format(problem[0], problem[1])
    start_time = time.time()

    val = ""
    while val != 'q' and val != 'n' and not val.isdigit():
        val = input(prompt)

    response_time = time.time() - start_time

    return val, response_time


def students(student, state, problem):
    gauss = student[str(state)]
    response_time = random.gauss(gauss[0], gauss[1])

    if random.random() < gauss[2]:
        # Make val an incorrect answer
        val = problem[0] + problem[1] + 1
    else:
        val = problem[0] + problem[1]

    return val, abs(response_time)


def load_student(load_student_filename):
    if load_student_filename is not None:
        student = ujson.load(open(load_student_filename, 'r'))
    else:
        student = None
    return student


def load_q(load_q_filename):
    if load_q_filename is None:
        q_init = collections.defaultdict(lambda: 0)
    else:
        q_init = collections.defaultdict(int, ujson.load(open(load_q_filename, 'r')))
    return q_init


def save_q(save_q_filename, q_dict):
    if save_q_filename is not None:
        with open(save_q_filename, "w") as outfile:
            ujson.dump(q_dict, outfile)
