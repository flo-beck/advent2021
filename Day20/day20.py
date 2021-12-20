# https://adventofcode.com/2021/day/20
import sys
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list, str_to_list_chars
import math
from collections import namedtuple
import copy
import time

TEST_CASE = {
    "input": ["..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#", "", "#..#.", "#....", "##..#", "..#..", "..###"],
    "part_one_result": "35",
    "part_two_result": '3351',
}

Point = namedtuple("Point", "y x")


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            print(grid[y][x], end='')
        print('')
    print('')


def get_empty_row(len_x):
    row = {}
    for x in range(len_x):
        row[x] = '.'
    return row


def init_empty_grid(size_x, size_y):
    new_grid = {}
    for y in range(size_y):
        new_grid[y] = get_empty_row(size_x)
    return new_grid


def parse_grid(my_input, loops):
    loops += 10
    grid = {}
    len_x = len(my_input[0])
    pad_len_x = len_x + (loops * 2)  # for the expansion of loops number of rounds
    curr_y = 0
    for y_start in range(loops):
        grid[y_start] = get_empty_row(pad_len_x)
    for y, line in enumerate(my_input):
        grid[y + loops] = {}
        curr_x = 0
        for x_start in range(loops):
            grid[y + loops][x_start] = '.'
        for x, char in enumerate(str_to_list_chars(line)):
            grid[y + loops][x + loops] = char
            curr_x = x + loops
        curr_x += 1
        for x_end in range(loops):
            grid[y + loops][curr_x] = '.'
            curr_x += 1
        curr_y = y + loops
    for y_end in range(loops):
        curr_y += 1
        grid[curr_y] = get_empty_row(pad_len_x)
    return grid


def get_three_points_in_row(grid, y, x):
    my_three = []
    if x > 0:
        my_three.append(Point(x=x - 1, y=y))
    my_three.append(Point(x=x, y=y))
    if x < len(grid[0]) - 1:
        my_three.append(Point(x=x + 1, y=y))
    return my_three


def get_three_in_row(grid, y, x, turn):
    my_three = ""
    if x > 0:
        my_three += grid[y][x - 1]
    else:
        if turn % 2 == 0:
            my_three += "."
        else:
            my_three += "#"
        # my_three += "."
    my_three += grid[y][x]
    if x < len(grid[0]) - 1:
        my_three += grid[y][x + 1]
    else:
        if turn % 2 == 0:
            my_three += "."
        else:
            my_three += "#"
        # my_three += "."
    return my_three


def get_three_above_points(grid, my_point):
    if my_point.y == 0:
        return []
    return get_three_points_in_row(grid, my_point.y - 1, my_point.x)


def get_three_above_string(grid, my_point):
    if my_point.y == 0:
        return "..."
    return get_three_points_in_row(grid, my_point.y - 1, my_point.x)


def get_three_middle_points(grid, my_point):
    y = my_point.y
    return get_three_points_in_row(grid, y, my_point.x)


def get_three_below_points(grid, my_point):
    if my_point.y >= len(grid) - 1:
        return []
    return get_three_points_in_row(grid, my_point.y + 1, my_point.x)


def get_nine_points(grid, my_point):
    return get_three_above_points(grid, my_point) \
           + get_three_middle_points(grid, my_point) \
           + get_three_below_points(grid, my_point)


def get_nine_points_string(grid, my_point, turn):
    my_str = ""
    # get above
    if my_point.y == 0:
        if turn % 2 == 0:
            my_str += "..."
        else:
            my_str += "###"
    else:
        my_str += get_three_in_row(grid, my_point.y - 1, my_point.x, turn)
    # get middle
    my_str += get_three_in_row(grid, my_point.y, my_point.x, turn)
    # get below
    if my_point.y >= len(grid) - 1:
        if turn % 2 == 0:
            my_str += "..."
        else:
            my_str += "###"
    else:
        my_str += get_three_in_row(grid, my_point.y + 1, my_point.x, turn)

    return my_str


def make_str_binary(my_str):
    result = ""
    for char in my_str:
        my_bin = '0' if char == '.' else '1'
        result += my_bin
    return result


def calc_enhanced_pixel(grid, y, x, enhancement_algo, turn):
    my_str = get_nine_points_string(grid, Point(y=y, x=x), turn)
    bin_str = make_str_binary(my_str)
    index = int(bin_str, 2)
    return enhancement_algo[index]


def do_enhance(old_grid, new_grid, enhancement_algo, turn):
    for y in range(len(old_grid)):
        for x in range(len(old_grid[y])):
            new_grid[y][x] = calc_enhanced_pixel(old_grid, y, x, enhancement_algo, turn)


def calc_light(grid):
    total = 0
    # for y in range(60, len(grid) - 60):
    for y in range(len(grid) - 1):
        # for x in range(60, len(grid[y]) - 60):
        for x in range(len(grid[y]) - 1):
            total += 1 if grid[y][x] == '#' else 0
    return total


def part_one(my_input):
    #  setup input
    enhance_loops = 2
    enhancement_algo = str_to_list_chars(my_input[0])
    original_grid = parse_grid(my_input[2:], enhance_loops)
    # print_grid(original_grid)
    enhanced_grid = init_empty_grid(len(original_grid[0]), len(original_grid))

    #  do actions
    for loop in range(enhance_loops):
        do_enhance(original_grid, enhanced_grid, enhancement_algo)
        # print("new grid")
        # print_grid(enhanced_grid)
        save = original_grid
        original_grid = enhanced_grid
        enhanced_grid = save

    # get result
    return calc_light(original_grid)

# ----------------------------- part 2 ------------------------------


def part_two(my_input):
    #  setup input
    enhance_loops = 50
    enhancement_algo = str_to_list_chars(my_input[0])
    original_grid = parse_grid(my_input[2:], enhance_loops)
    # print_grid(original_grid)
    enhanced_grid = init_empty_grid(len(original_grid[0]), len(original_grid))

    #  do actions
    for loop in range(enhance_loops):
        do_enhance(original_grid, enhanced_grid, enhancement_algo, loop)
        # print("new grid")
        # print_grid(enhanced_grid)
        save = original_grid
        original_grid = enhanced_grid
        enhanced_grid = save

    # get result
    print_grid(original_grid)
    return calc_light(original_grid)


if __name__ == '__main__':
    # print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]}')
    # print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  # it is not 5280 NOR 5452 - answer 5339

    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]}')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  # it is not 20408 25020 26620
    # -50 on each side = 18395
    # add cleanup dur to flashes, and get 18395
