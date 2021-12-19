# https://adventofcode.com/2021/day/17
import sys
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list, str_to_list_chars
import math
from collections import namedtuple
import copy
import time

TEST_CASE = {
    "input": ["target area: x=20..30, y=-10..-5"],
    "part_one_result": "45",
    "part_two_result": '112',
}

Point = namedtuple("Point", "y x")
Area = namedtuple("Area", "min max")


class Probe:
    def __init__(self, x, y, x_velocity, y_velocity):
        self.x = x
        self.y = y
        self.x_velocity = x_velocity
        self.y_velocity = y_velocity


def parse_target(input_str):
    my_split = input_str[13:].split(', ')  # remove 13 for "target area: "
    my_x_split = my_split[0][2:].split('..')  # remove 2 for "x="
    my_y_split = my_split[1][2:].split('..')  # remove 2 for "y="

    my_x_min = int(my_x_split[0])
    my_x_max = int(my_x_split[1])
    my_y_min = int(my_y_split[0])
    my_y_max = int(my_y_split[1])

    min_point = Point(x=int(my_x_split[0]), y=int(my_y_split[0]))
    max_point = Point(x=int(my_x_split[1]), y=int(my_y_split[1]))
    return Area(min=min_point, max=max_point)


def init_probe(velocity):
    return Probe(0, 0, velocity.x, velocity.y)


def do_step(probe):
    probe.x += probe.x_velocity
    probe.y += probe.y_velocity
    probe.y_velocity -= 1
    probe.x_velocity += 1 if probe.x_velocity < 0 else -1 if probe.x_velocity > 0 else 0
    return probe


def print_probe(probe, area):
    max_x = max(probe.x, area.max.x)
    max_y = max(probe.y, area.max.y)
    min_y = min(probe.y, area.min.y)

    for y in range(max_y, min_y, -1):
        for x in range(max_x):
            icon = '.'
            if probe.x == x and probe.y == y:
                icon = '#'
            elif (area.max.x >= x >= area.min.x) and (area.max.y >= y >= area.min.y):
                icon = 'T'
            print(icon.rjust(1), end='')  # icon.rjust(2)
        print('')
    print('')


def get_max_probe_val(probe_position, axis):
    my_max = -sys.maxsize
    for position in probe_position:
        if axis == 'x':
            my_max = max(my_max, position.x)
        else:
            my_max = max(my_max, position.y)
    return my_max


def get_min_probe_val(probe_position, axis):
    my_min = sys.maxsize
    for position in probe_position:
        if axis == 'x':
            my_min = min(my_min, position.x)
        else:
            my_min = min(my_min, position.y)
    return my_min


def print_probe_journey(probe_positions, area):
    max_x = max(get_max_probe_val(probe_positions, 'x'), area.max.x)
    max_y = max(get_max_probe_val(probe_positions, 'y'), area.max.y)
    min_y = min(get_min_probe_val(probe_positions, 'y'), area.min.y)

    for y in range(max_y, min_y - 2, -1):
        print(f"({str(y)}) ".rjust(7), end='')
        for x in range(max_x + 2):
            icon = '.'
            my_point = Point(x=x, y=y)
            if my_point in probe_positions:
                icon = '#'
            elif (area.max.x >= x >= area.min.x) and (area.max.y >= y >= area.min.y):
                icon = 'T'
            print(icon.rjust(1), end='')  # icon.rjust(2)
        print('')
    print('')


def add_probe_position(probe_positions, probe):
    probe_positions.append(Point(x=probe.x, y=probe.y))


def probe_in_target(probe, target):
    if (target.max.x >= probe.x >= target.min.x) and (target.max.y >= probe.y >= target.min.y):
        return True
    return False


def probe_passed_target(probe, target):
    if probe.x > target.max.x or probe.y < target.min.y:
        return True
    return False


def stop_probe(probe, target):
    return probe_in_target(probe, target) or probe_passed_target(probe, target)


def fire_probe(probe, target):
    probe_positions = []
    add_probe_position(probe_positions, probe)
    while not stop_probe(probe, target):
        do_step(probe)
        add_probe_position(probe_positions, probe)

    return probe_positions


# def adjust_velocity(last_pos, target, velocity):
#     if last_pos.x < target.min.x:
#         return Point(x=velocity.x + 1, y=velocity.y + 1)
#     elif last_pos.x > target.max.x:
#         return Point(x=velocity.x, y=velocity.y + 1)


def adjust_velocity_basic(last_pos, target, velocity):
    if velocity.x < target.max.x:
        return Point(x=velocity.x + 1, y=velocity.y)
    elif last_pos.x > target.max.x:
        return Point(x=velocity.x, y=velocity.y + 1)


def adjust_velocity_highest(last_pos, target, velocity):
    velocity_x_delta = 0
    velocity_y_delta = 0
    if last_pos.x < target.max.x:  # not far enough
        velocity_x_delta += 1
    elif probe_in_target(last_pos, target):  # try to get as high as possible
        velocity_y_delta += 1
    elif last_pos.x > target.max.x:
        return Point(x=velocity.x, y=velocity.y + 1)
    return Point(x=velocity.x + velocity_x_delta, y=velocity.y + velocity_y_delta)


def adjust_velocity_brute_force(velocity):
    if velocity.y < 150:
        return Point(x=velocity.x, y=velocity.y + 1)
    elif velocity.x < 300:
        return Point(x=velocity.x + 1, y=-150)
    # if velocity.x < 300:
    #     return Point(x=velocity.x + 1, y=velocity.y)
    # elif velocity.y < 300:
    #     return Point(x=0, y=velocity.y + 1)
    else:
        return None


def set_probe_velocity(probe, velocity):
    probe.x_velocity = velocity.x
    probe.y_velocity = velocity.y


def shoot_loop(velocity, result_positions, target, adjust_ft):
    hit_target = True
    while hit_target:
        probe = init_probe(velocity)
        probe_positions = fire_probe(probe, target)
        result_positions = probe_positions
        print_probe_journey(probe_positions, target)
        last_pos = probe_positions[len(probe_positions) - 1]
        hit_target = probe_in_target(last_pos, target)
        if not hit_target:
            velocity = adjust_ft(last_pos, target, velocity)
    return velocity, result_positions


def shoot_all_possible_velocities(target):
    hits_target = {}
    velocity = adjust_velocity_brute_force(Point(y=0, x=0))
    while velocity:
        probe = init_probe(velocity)
        probe_positions = fire_probe(probe, target)
        last_pos = probe_positions[len(probe_positions) - 1]
        hit_target = probe_in_target(last_pos, target)
        if hit_target:
            hits_target[velocity] = probe_positions
        velocity = adjust_velocity_brute_force(velocity)
    return hits_target


def find_highest_point(winners):
    highest_pos = -sys.maxsize
    for list_positions in winners.values():
        for position in list_positions:
            highest_pos = position.y if position.y > highest_pos else highest_pos
    return highest_pos


def part_one(my_input):
    #  setup input
    target = parse_target(my_input[0])
    # velocity = Point(x=0, y=0)
    result_positions = []

    #  do actions
    # find the target
    # (velocity, result_positions) = shoot_loop(velocity, result_positions, target, adjust_velocity_basic)
    # fin the highest y
    # (velocity, result_positions) = shoot_loop(velocity, result_positions, target, adjust_velocity_basic)
    winners = shoot_all_possible_velocities(target)

    # get result
    return find_highest_point(winners)


# ----------------------------- part 2 ------------------------------


def part_two(my_input):
    #  setup input
    target = parse_target(my_input[0])

    #  do actions
    winners = shoot_all_possible_velocities(target)

    # get result
    return len(winners)


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]}')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #

    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]}')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #
