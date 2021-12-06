# https://adventofcode.com/2021/day/6
from typing import List

from advent2021.common.read_input import read_file_lines, str_numbers_to_list
from collections import namedtuple
TEST_CASE = {
    "input": ["3,4,3,1,2"],
    "part_one_result": 5934,
    "part_two_result": '?',
}


def propagate_fish(list_fish):
    fish_len = len(list_fish)
    for x in range(fish_len):
        if list_fish[x] == 0:
            list_fish[x] = 6
            list_fish.append(8)
        else:
            list_fish[x] -= 1


def part_one(my_input):
    #  setup input
    my_lanterns = str_numbers_to_list(my_input[0], ',')

    #  do actions
    for x in range(80):
        propagate_fish(my_lanterns)

    # get result
    return len(my_lanterns)

#
# def part_two(my_input):
#     #  setup input
#
#
#     #  do actions
#
#
#     # get result


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #353079
    print("------------")
    # print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    # print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}') #
