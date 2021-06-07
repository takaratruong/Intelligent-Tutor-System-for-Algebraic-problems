import json
from collections import defaultdict
import math
import ujson

MAX_NUM = 999
FEATURE_TUPLE_LIMIT = list()
BASE_PROBLEM_KEY = ()
bins = defaultdict(lambda: [])


def num_carry_ops(val_1, val_2):
    num1_str = str(val_1)
    num1_str = num1_str[::-1]

    num2_str = str(val_2)
    num2_str = num2_str[::-1]
    i = 0
    j = 0
    carry_val = 0
    carry_count = 0

    while i < len(num1_str) or j < len(num2_str):
        x = 0
        y = 0

        if i < len(num1_str):
            x = int(num1_str[i])  # + int('0');
            i += 1

        if j < len(num2_str):
            y = int(num2_str[j])  # + int('0');
            j += 1

        currentVal = x + y + carry_val

        if currentVal >= 10:
            carry_count += 1
            carry_val = math.floor(currentVal / 10)

    return carry_count


def count_zeros(val_1, val_2):
    zero_count_1 = str(val_1).count('0')
    zero_count_2 = str(val_2).count('0')

    return zero_count_1 + zero_count_2


def non_trailing_zero_count(val_1, val_2):
    total_zero_1 = str(val_1).count('0')
    total_zero_2 = str(val_2).count('0')

    num1_str = str(val_1)
    num2_str = str(val_2)

    trail_1 = len(num1_str) - len(num1_str.rstrip('0'))
    trail_2 = len(num2_str) - len(num2_str.rstrip('0'))

    return ((len(num1_str) - trail_1) == 1 and (
            len(num2_str) - trail_2) == 1 and val_1 != 0 and val_2 != 0 and total_zero_1 != 0 and total_zero_2 != 0)


def feature_extractor(val_1, val_2):
    # val2 will always be larger than val1
    if val_1 > val_2:
        temp = val_1
        val_1 = val_2
        val_2 = temp

    carry_ops = num_carry_ops(val_1, val_2)
    zero_count = count_zeros(val_1, val_2)

    num_1_digit = len(str(val_1))
    num_2_digit = len(str(val_2))

    # Count not leading zeros

    if int(val_1) == 0 or int(val_2) == 0:
        num_1_digit = -1
        num_2_digit = -1
        carry_ops = -1
        zero_count = -1

    feature = (num_1_digit, num_2_digit, carry_ops, zero_count)

    return feature


def generate_bins_and_constants():
    for i in range(4):
        FEATURE_TUPLE_LIMIT.append(list())
    for num_1 in range(0, MAX_NUM + 1):
        for num_2 in range(0, MAX_NUM + 1):
            key = feature_extractor(num_1, num_2)
            for feature_index in range(len(key)):
                if key[feature_index] not in FEATURE_TUPLE_LIMIT[feature_index]:
                    FEATURE_TUPLE_LIMIT[feature_index].append(key[feature_index])
            bins[key].append((num_1, num_2))
    return bins, FEATURE_TUPLE_LIMIT


def show_stats():
    # Bin statistics
    print("Total number of math problems: " + str((MAX_NUM + 1) ** 2))
    print("Total number of bins: " + str(len(bins)))
    print("")

    for key in bins:
        print("Bin Name: " + str(key) + "   Bin Count: " + str(len(bins[key])))
        print(bins[key][0:100])
        print("")


def save_json(dictionary):
    with open("data/problemBank.json", "w") as outfile:
        ujson.dump(dictionary, outfile)


def load_json():
    return json.load(open('data/problemBank.json', 'r'))


def main():
    bins, FEATURE_TUPLE_LIMIT = generate_bins_and_constants()
    bins['state_limit'] = FEATURE_TUPLE_LIMIT
    for key in bins:
        bins['num_states'] = len(key)
        break

    for key in bins:
        print(key)
        print(bins[key])

    save_json(bins)


if __name__ == '__main__':
    main()
