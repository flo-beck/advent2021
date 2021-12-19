# https://adventofcode.com/2021/day/18
import itertools
import sys
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list, str_to_list_chars
import math
from collections import namedtuple
import copy
import time

TEST_CASE = {
    "input": ["[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]", "[[[5,[2,8]],4],[5,[[9,9],0]]]",
              "[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]", "[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]",
              "[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]", "[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]",
              "[[[[5,4],[7,7]],8],[[8,3],8]]", "[[9,3],[[9,9],[6,[4,9]]]]", "[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]",
              "[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]"],
    "part_one_result": "4140",
    "part_two_result": '3993',
}


class Digit:
    def __init__(self, val, depth):
        self.value = val
        self.depth = depth

    def __str__(self):
        return str(self.value) + "(" + str(self.depth) + ")"


def parse_str_to_list(number_str):
    number = []
    depth = -1
    for char in number_str:
        if char == ',':
            continue
        elif char == '[':
            depth += 1
        elif char == ']':
            depth -= 1
        else:
            number.append(Digit(int(char), depth))
    return number


def print_list(my_list):
    print(f"{my_list[0]}", end='')
    for elem in my_list[1:]:
        print(f", {elem}", end='')
    print('')


def is_need_explode(number):
    for digit in number:
        if digit.depth > 3:
            return True
    return False


def is_need_split(number):
    for digit in number:
        if digit.value > 9:
            return True
    return False


def is_need_reduce(number):
    for digit in number:
        if digit.depth > 3 or digit.value > 9:
            return True
    return False


def concatenate_two_numbers(number1, number2):
    result = []
    for digit in number1 + number2:
        digit.depth += 1
        result.append(digit)
    return result


def add_new_digit(lhs_list, digit, rhs_list):
    lhs_list.append(digit)
    return lhs_list + rhs_list


def add_new_pair(lhs_list, pair_list, rhs_list):
    return lhs_list + pair_list + rhs_list


def do_explode(number):
    for idx, digit in enumerate(number):
        if digit.depth > 3:
            left_idx = idx
            right_idx = idx + 1
            # add to left
            if left_idx > 0:
                number[left_idx - 1].value += number[left_idx].value
            # add to right
            if right_idx < len(number) - 1:
                number[right_idx + 1].value += number[right_idx].value
            # create new list lhs + 0(3) + rhs
            return add_new_digit(number[:left_idx], Digit(0, 3), number[right_idx + 1:])
    return number


def do_split(number):
    for idx, digit in enumerate(number):
        if digit.value > 9:
            new_left_val = math.floor(digit.value / 2)
            new_right_val = math.ceil(digit.value / 2)
            new_pair = [Digit(new_left_val, digit.depth + 1), Digit(new_right_val, digit.depth + 1)]
            return add_new_pair(number[:idx], new_pair, number[idx + 1:])
    return number


def get_max_depth(number):
    max_depth = 0
    for digit in number:
        max_depth = digit.depth if digit.depth > max_depth else max_depth
    return max_depth


def do_implode(number, max_depth):
    for idx, digit in enumerate(number):
        if digit.depth == max_depth:
            left_idx = idx
            right_idx = idx + 1
            new_val = (number[left_idx].value * 3) + (number[right_idx].value * 2)
            return add_new_digit(number[:left_idx], Digit(new_val, max_depth - 1), number[right_idx + 1:])
    return number


def calc_magnitude(number):
    max_depth = get_max_depth(number)
    while max_depth > 0:
        number = do_implode(number, max_depth)
        max_depth = get_max_depth(number)
    return (3 * number[0].value) + (2 * number[1].value)


def add_two_numbers(number1, number2):
    new_num = concatenate_two_numbers(number1, number2)
    while is_need_reduce(new_num):
        if is_need_explode(new_num):
            new_num = do_explode(new_num)
        elif is_need_split(new_num):
            new_num = do_split(new_num)
    return new_num


def part_one(my_input):
    #  setup input
    raw_nums = [parse_str_to_list(number) for number in my_input]

    #  do actions
    curr_num = raw_nums[0]
    for number in raw_nums[1:]:
        curr_num = add_two_numbers(curr_num, number)
    # print_list(curr_num)

    # get result
    return calc_magnitude(curr_num)

# ----------------------------- part 2 ------------------------------


def part_two(my_input):
    #  setup input
    all_perms = list(itertools.permutations(my_input, 2))

    #  do actions
    max_magnitude = 0
    for perm in all_perms:
        final = add_two_numbers(parse_str_to_list(perm[0]), parse_str_to_list(perm[1]))
        total = calc_magnitude(final)
        max_magnitude = max(total, max_magnitude)
    # get result
    return max_magnitude


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]}')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  # 3675

    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]}')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  # 4650
