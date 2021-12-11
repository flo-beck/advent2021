# https://adventofcode.com/2021/day/11

from advent2021.common.read_input import read_file_lines, str_digits_to_list
import math
from collections import namedtuple


TEST_CASE = {
    "input": ["5483143223", "2745854711", "5264556173", "6141336146", "6357385478", "4167524645", "2176841721", "6882881134", "4846848554", "5283751526"],
    # "input": ["11111", "19991", "19191", "19991", "11111"],
    "part_one_result": 1656,
    "part_two_result": 195,
}

Point = namedtuple("Point", "y x")
Octopus = namedtuple("Octopus", "val has_flashed")


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            print(str(grid[y][x]["val"]).rjust(2), end=' ')
        print('')
    print('')


def init_grid(my_input):
    list_nums = [str_digits_to_list(line) for line in my_input]
    grid = []
    for y in range(len(list_nums)):
        grid.append([])
        for x in range(len(list_nums[0])):
            new_octopus = {
                "val": list_nums[y][x],
                "has_flashed": False
            }
            grid[y].append(new_octopus)
    return grid


def add_num_to_all(grid, num):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            grid[y][x]["val"] += num


def add_num_to_point(grid, num, y, x):
    grid[y][x]["val"] += num


def energize_above(grid, y, x):
    if y == 0:
        return
    if x > 0:
        add_num_to_point(grid, 1, y - 1, x - 1)  # above left
    add_num_to_point(grid, 1, y - 1, x)          # above middle
    if x < len(grid[y]) - 1:
        add_num_to_point(grid, 1, y - 1, x + 1)  # above right


def energize_row(grid, y, x):
    if x > 0:
        add_num_to_point(grid, 1, y, x - 1)  # left
    if x < len(grid[y]) - 1:
        add_num_to_point(grid, 1, y, x + 1)  # right


def energize_below(grid, y, x):
    if y >= len(grid) - 1:
        return
    if x > 0:
        add_num_to_point(grid, 1, y + 1, x - 1)  # below left
    add_num_to_point(grid, 1, y + 1, x)          # below middle
    if x < len(grid[y]) - 1:
        add_num_to_point(grid, 1, y + 1, x + 1)  # below right


def do_flash(grid, y, x):
    grid[y][x]["has_flashed"] = True
    energize_above(grid, y, x)
    energize_row(grid, y, x)
    energize_below(grid, y, x)


def do_flashes(grid):
    flash_num = 0
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x]["val"] > 9 and not grid[y][x]["has_flashed"]:
                do_flash(grid, y, x)
                flash_num += 1
    return flash_num


def reset_flashes(grid):
    for y in range(len(grid)):
        for x in range(len(grid[0])):
            if grid[y][x]["has_flashed"]:
                grid[y][x]["val"] = 0
                grid[y][x]["has_flashed"] = False


def do_step(grid):
    add_num_to_all(grid, 1)  # adds one to every step
    flash_num = do_flashes(grid)
    total_flashes = flash_num
    while flash_num > 0:  # keep going while still have flashes
        flash_num = do_flashes(grid)
        total_flashes += flash_num
    reset_flashes(grid)
    return total_flashes


def part_one(my_input):
    #  setup input
    grid = init_grid(my_input)

    #  do actions
    flashes = 0
    for i in range(100):
        flashes += do_step(grid)
        # print_grid(grid)
    # get result
    return flashes


# ----------------------------- part 2 ------------------------------


def part_two(my_input):
    #  setup input
    grid = init_grid(my_input)

    #  do actions
    for i in range(10000):
        flashes = do_step(grid)
        if flashes == 100:
            # print_grid(grid)
            return i + 1
    return "never ending"


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #1694
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #2776842859
