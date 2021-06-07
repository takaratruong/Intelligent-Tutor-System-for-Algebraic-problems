import random
import time
import ujson
from collections import defaultdict


def main():
    bins = ujson.load(open('data/problemBank.txt', 'r'))
    val = ""
    while val == "":
        val = input("Type your name so I can save your result and differentiate from other:")
    name = val
    result = defaultdict(lambda: [])

    for problem in bins:
        if problem == 'state_limit' or problem == "num_states":
            continue
        problem_lst = bins[problem]
        value = list()
        while len(value) != 4:
            try:
                next = random.choice(problem_lst)
            except TypeError:
                continue
            prompt = "{} + {} = \n".format(next[0], next[1])
            start_time = time.time()
            # print(prompt)

            val = ""
            while val == "":
                val = input(prompt)
            state_time = time.time() - start_time
            print("Time:", state_time)

            if val == 'q':
                return result

            if int(val) == (next[0] + next[1]):
                print("Correct! it took you " + str(int(state_time)) + " seconds!")
                value.append(state_time)
            else:
                print("Incorrect!")
                value.append(state_time * (-1))

        result[problem] = value
        print("Next Level, result", result[problem])

    print("Saving your result to file......")
    save_json(result, name)
    print("Successfully save the file!")


def save_json(dictionary, name):
    with open("data_" + name + ".txt", "w") as outfile:
        ujson.dump(dictionary, outfile)


if __name__ == '__main__':
    print(main())
