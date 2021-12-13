# https://adventofcode.com/2021/day/13
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list
import math
from collections import namedtuple
import copy
import time


TEST_CASE = {
    "input": ["6,10", "0,14", "9,10", "0,3", "10,4", "4,11", "6,0", "6,12", "4,1", "0,13", "10,12", "3,4", "3,0", "8,4", "1,10", "2,14", "8,10", "9,0", "", "fold along y=7", "fold along x=5"],
    "part_one_result": 17 ,
    "part_two_result": '?',
    }

Point = namedtuple("Point", "y x")
Fold = namedtuple("Fold", "axis val")


def parse_fold(line):
    split = line.split()
    axis = split[2].split('=')[0]
    val = split[2].split('=')[1]
    return Fold(axis=axis, val=val)


def parse_input(my_input):
    context = {
        'x': [],
        'y': [],
        'folds': []
    }
    folds_flag = False
    for line in my_input:
        if folds_flag:
            context['folds'].append(parse_fold(line))
        else:
            if line == "":
                folds_flag = True
                continue
            else:
                my_split = line.split(',')
                context['x'].append(int(my_split[0]))
                context['y'].append(int(my_split[1]))
    return context


def init_grid(max_y, max_x):
    grid = []
    for y in range(max_y + 1):
        grid.append([])
        for x in range(max_x + 1):
            grid[y].append(0)
    return grid


def set_points_in_grid(grid, context):
    for i in range(len(context['x'])):
        y = context['y'][i]
        x = context['x'][i]
        grid[y][x] = 1
    return grid


def create_grid(context):
    max_x = max(context['x'])
    max_y = max(context['y'])
    grid = init_grid(max_y, max_x)
    return set_points_in_grid(grid, context)


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            char = '#' if grid[y][x] == 1 else '.'
            # print(char.rjust(2), end=' ')
            print(char, end=' ')
        print('')
    print('')


def print_folds(context):
    for fold in context['folds']:
        print(f"fold {fold.axis} on {fold.val}")


def part_one(my_input):
    #  setup input
    context = parse_input(my_input)
    grid = create_grid(context)

    #  do actions
    print_grid(grid)
    print_folds(context)

    # get result
    return


# ----------------------------- part 2 ------------------------------


# def part_two(my_input):
    #  setup input

    #  do actions

    # get result


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]}')
    # print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #

    print("------------")
    # print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_resultA"]}')
    # print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  # 91292


