# https://adventofcode.com/2021/day/5
from typing import List

from advent2021.common.read_input import read_file_lines
from collections import namedtuple
TEST_CASE = {
    "input": ["0,9 -> 5,9", "8,0 -> 0,8", "9,4 -> 3,4", "2,2 -> 2,1", "7,0 -> 7,4", "6,4 -> 2,0", "0,9 -> 2,9", "3,4 -> 1,4", "0,0 -> 8,8", "5,5 -> 8,2"],
    "part_one_result": 5,
    "part_two_result": 12,
}

Point = namedtuple("Point", "y x")


# a = [1,2, 3]
# b = (1, 2, 3)
# c = Point(y=1, x=2)


def parse_line_to_obj(line):
    split_start_end = line.split(' -> ')
    return {
        "x0": int(split_start_end[0].split(',')[0]),
        "y0": int(split_start_end[0].split(',')[1]),
        "x1": int(split_start_end[1].split(',')[0]),
        "y1": int(split_start_end[1].split(',')[1])
    }


def parse_input_to_one_list(my_input):
    return [parse_line_to_obj(line) for line in my_input]


def add_line_to_obj(my_obj, line):
    split_start_end = line.split(' -> ')
    my_obj["x0"].append(int(split_start_end[0].split(',')[0]))
    my_obj["y0"].append(int(split_start_end[0].split(',')[1]))
    my_obj["x1"].append(int(split_start_end[1].split(',')[0]))
    my_obj["y1"].append(int(split_start_end[1].split(',')[1]))

    return my_obj


def parse_input_to_four_lists(my_input):
    my_obj = {
        "x0": [],
        "y0": [],
        "x1": [],
        "y1": []
    }
    for line in my_input:
        add_line_to_obj(my_obj, line)
    return my_obj


def get_min_max(vent_list):
    max_x = max(max(vent_list["x0"]), max(vent_list["x1"]))
    max_y = max(max(vent_list["y0"]), max(vent_list["y1"]))
    min_x = min(min(vent_list["x0"]), min(vent_list["x1"]))
    min_y = min(min(vent_list["y0"]), min(vent_list["y1"]))

    return {
        "min_x": min_x,
        "min_y": min_y,
        "max_x": max_x,
        "max_y": max_y
    }


def get_grid_size(input):
    vent_lists = parse_input_to_four_lists(input)
    return get_min_max(vent_lists)


def print_grid(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] == 0:
                print(".".rjust(2), end=' ')
            else:
                print(str(grid[y][x]).rjust(2), end=' ')
        print(" ")


def create_empty_grid(min_max):
    my_grid = []
    for y in range(min_max["max_y"] + 1):
        row = []
        for x in range(min_max["max_x"] + 1):
            row.append(0)
        my_grid.append(row)
    return my_grid


def is_horizontal(vent):
    return vent["x1"] != vent["x0"] and vent["y0"] == vent["y1"]


def is_vertical(vent):
    return vent["x1"] == vent["x0"] and vent["y0"] != vent["y1"]


def get_start_end(i0, i1):
    if i0 < i1:
        return {
            "start": i0,
            "end": i1
        }
    else:
        return {
            "start": i1,
            "end": i0
        }


def insert_horizontal(vent, grid):
    y = vent["y0"]
    se = get_start_end(vent["x0"], (vent["x1"]))
    for x in range(se["start"], se["end"] + 1):
        grid[y][x] += 1


def insert_vertical(vent, grid):
    x = vent["x0"]
    se = get_start_end(vent["y0"], (vent["y1"]))
    for y in range(se["start"], se["end"] + 1):
        grid[y][x] += 1


def insert_line(vent, grid):  # horizontal, vertical and diagonal
    delta_x = vent["x0"] - vent["x1"]
    delta_y = vent["y0"] - vent["y1"]

    x_increment = -1 if delta_x > 0 else 1 if delta_x < 0 else 0
    y_increment = -1 if delta_y > 0 else 1 if delta_y < 0 else 0
    x = vent["x0"]
    y = vent["y0"]
    for i in range(max(abs(delta_y), abs(delta_x)) + 1):
        grid[y][x] += 1
        x += x_increment
        y += y_increment


def insert_vents_in_grid(vents, grid):
    for vent in vents:
        insert_line(vent, grid)


def filter_vents_for_straight_lines(vents):
    return [vent for vent in vents if (vent["x0"] == vent["x1"] or vent["y0"] == vent["y1"])]


def calc_2_or_more(grid):
    total = 0
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            if grid[y][x] >= 2:
                total += 1
    return total


def part_one(my_input):
    #  setup input
    grid_size = get_grid_size(my_input)
    my_grid = create_empty_grid(grid_size)
    vents = parse_input_to_one_list(my_input)

    #  do actions
    vents = filter_vents_for_straight_lines(vents)
    insert_vents_in_grid(vents, my_grid)
    print_grid(my_grid)

    # get result
    return calc_2_or_more(my_grid)


def part_two(my_input):
    #  setup input
    grid_size = get_grid_size(my_input)
    my_grid = create_empty_grid(grid_size)
    vents = parse_input_to_one_list(my_input)

    #  do actions
    insert_vents_in_grid(vents, my_grid)
    print_grid(my_grid)

    # get result
    return calc_2_or_more(my_grid)


if __name__ == '__main__':
    # print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #7142
    print("------------")
    # print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}') #20012
