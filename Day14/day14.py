# https://adventofcode.com/2021/day/14
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list, str_to_list_chars
import math
from collections import namedtuple
import copy
import time

TEST_CASE = {
    "input": ["NNCB", "", "CH -> B", "HH -> N", "CB -> H", "NH -> C", "HB -> C", "HC -> B", "HN -> C", "NN -> C",
              "BH -> H", "NC -> B", "NB -> B", "BN -> B", "BB -> N", "BC -> B", "CC -> N", "CN -> C"],
    "part_one_result": 1588,
    "part_two_result": 2188189693529,
}


def parse_rules(my_input):
    rule_dict = {}
    for line in my_input:
        split = line.split(' -> ')
        rule_dict[split[0]] = split[1]
    return rule_dict


def insert_polymers(polymers, rules):
    new_polymers = [polymers[0]]
    for i in range(len(polymers) - 1):
        pair = polymers[i:i + 2]
        pair_str = pair[0] + pair[1]
        if pair_str in rules:
            new_polymers.append(rules[pair_str])
        new_polymers.append(pair[1])
    return new_polymers


def calc_result(polymers):
    # count all polymers in the chain
    counter = {}
    for polymer in polymers:
        if polymer in counter:
            counter[polymer] += 1
        else:
            counter[polymer] = 1

    max_value = max(counter.values())
    min_value = min(counter.values())
    return max_value - min_value


def part_one(my_input):
    #  setup input
    polymers = str_to_list_chars(my_input[0])
    rules = parse_rules(my_input[2::])

    #  do actions
    for x in range(10):
        polymers = insert_polymers(polymers, rules)

    # get result
    return calc_result(polymers)


# ----------------------------- part 2 ------------------------------

class Counter:
    def __init__(self, current, next_round):
        self.current = current
        self.next = next_round

    def __gt__(self, counter2):
        return self.current > counter2.current

    def __lt__(self, counter2):
        return self.current < counter2.current


def init_counter_dict(polymers):
    counter_dict = {}
    for i in range(len(polymers) - 1):
        pair = polymers[i:i + 2]
        pair_str = pair[0] + pair[1]
        if pair_str in counter_dict:
            counter_dict[pair_str].current += 1
        else:
            counter_dict[pair_str] = Counter(1, 0)
    return counter_dict


def insert_new_pair_to_counter(counters, pair, num):
    if pair in counters:
        counters[pair].next += num
    else:
        counters[pair] = Counter(0, num)


def replace_current_by_next(counters):
    for pair in counters.keys():
        counters[pair].current = counters[pair].next
        counters[pair].next = 0


def insert_polymers_with_counter(counters, rules):
    for pair in list(counters):
        if pair in rules:
            new_left_pair = pair[0] + rules[pair]
            new_right_pair = rules[pair] + pair[1]
            insert_new_pair_to_counter(counters, new_left_pair, counters[pair].current)
            insert_new_pair_to_counter(counters, new_right_pair, counters[pair].current)
        else:
            print(f"No rule for {pair}!")
            counters[pair].next = counters[pair].current
    replace_current_by_next(counters)
    return


def append_to_dict(my_dict, key, value):
    if key in my_dict:
        my_dict[key] += value
    else:
        my_dict[key] = value


def calc_result_from_counters(counters, start, end):
    # count all occurrences of each letter
    letters = {}
    for key in counters.keys():
        append_to_dict(letters, key[0], counters[key].current)
        append_to_dict(letters, key[1], counters[key].current)

    # half them because they are pairs
    for key, val in letters.items():
        real_val = val / 2
        if key == start or key == end:  # accounting for not shared first and last letters
            real_val += 0.5
        letters[key] = real_val

    max_count = max(letters.values())
    min_count = min(letters.values())
    return max_count - min_count


def part_two(my_input):
    #  setup input
    polymers = str_to_list_chars(my_input[0])
    rules = parse_rules(my_input[2::])

    #  do actions
    # for x in range(40):
    #     polymers = insert_polymers(polymers, rules)

    # calc len at x rounds
    # my_len = len(polymers)
    # for x in range(10):
    #     num_pairs = my_len - 1
    #     my_len += num_pairs

    counters = init_counter_dict(polymers)

    for x in range(40):
        insert_polymers_with_counter(counters, rules)

    # get result
    return calc_result_from_counters(counters, polymers[0], polymers[len(polymers) - 1])


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]}')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #

    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]}')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #
