# https://adventofcode.com/2021/day/9

from advent2021.common.read_input import read_file_lines, str_numbers_to_list
from collections import namedtuple

TEST_CASE = {
    "input": ["2199943210", "3987894921", "9856789892", "8767896789", "9899965678"],
    "part_one_result": 15,
    "part_two_result": 1134,
}

Point = namedtuple("Point", "y x")


def is_low_point(my_input, y, x, num_columns, num_rows):
    above = int(my_input[y - 1][x]) if y > 0 else 11
    below = int(my_input[y + 1][x]) if y < num_rows - 1 else 11
    left = int(my_input[y][x - 1]) if x > 0 else 11
    right = int(my_input[y][x + 1]) if x < num_columns - 1 else 11

    point_value = int(my_input[y][x])
    return point_value < above and point_value < below and point_value < left and point_value < right


def calc_risk_level(my_input, low_points):
    total_risk = 0
    for low_point in low_points:
        total_risk += (int(my_input[low_point.y][low_point.x]) + 1)
    return total_risk


def get_low_points(my_input, num_rows, num_columns):
    low_points = []

    for y in range(num_rows):
        for x in range(num_columns):
            if is_low_point(my_input, y, x, num_columns, num_rows):
                low_points.append(Point(y=y, x=x))
    return low_points


def part_one(my_input):
    #  setup input
    #  do actions
    num_rows = len(my_input)
    num_columns = len(my_input[0])
    low_points = get_low_points(my_input, num_rows, num_columns)

    # get result
    return calc_risk_level(my_input, low_points)


# ----------------------------- part 2 ------------------------------


def recursive_find_basin(my_input, locations, point, num_rows, num_columns, low_value):
    if point.y < 0 or point.y >= num_rows or point.x < 0 or point.x >= num_columns:
        return

    point_value = int(my_input[point.y][point.x])
    if point_value != 9 and point_value >= low_value:
        locations.add(point)
        # go up
        if point.y > 0:
            recursive_find_basin(my_input, locations, Point(y=point.y - 1, x=point.x), num_rows, num_columns, point_value)
        # go down
        if point.y < num_rows - 1:
            recursive_find_basin(my_input, locations, Point(y=point.y + 1, x=point.x), num_rows, num_columns, point_value)
        # go left
        if point.x > 0:
            recursive_find_basin(my_input, locations, Point(y=point.y, x=point.x - 1), num_rows, num_columns, point_value)
        # go right
        if point.x < num_columns - 1:
            recursive_find_basin(my_input, locations, Point(y=point.y, x=point.x + 1), num_rows, num_columns, point_value)
    return


def get_basin_size(my_input, low_point, num_rows, num_columns):
    locations = set()
    recursive_find_basin(my_input, locations, low_point, num_rows, num_columns, 0)
    return len(locations)


def product(lst):
    p = 1
    for i in lst:
        p *= i
    return p


def three_largest_basins(basin_sizes):
    basin_sizes.sort()
    largest_three = basin_sizes[-3:]
    return product(largest_three)


def part_two(my_input):
    # setup input
    num_rows = len(my_input)
    num_columns = len(my_input[0])
    low_points = get_low_points(my_input, num_rows, num_columns)

    #  do actions
    basin_sizes = []
    for low_point in low_points:
        basin_sizes.append(get_basin_size(my_input, low_point, num_rows, num_columns))

    # get result
    return three_largest_basins(basin_sizes)


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #603
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #
