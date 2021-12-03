# https://adventofcode.com/2021/day/3

from enum import Enum

TEST_CASE = {
    "input": ["00100", "11110", "10110", "10111", "10101", "01111", "00111", "11100", "10000", "11001", "00010", "01010"],
    "part_one_result": 198,
    "part_two_result": 230,
}


class Common(Enum):
    MOST = 1
    LEAST = 2


def read_file_input(filename):
    with open(filename, 'r') as f:
        my_input = [val.strip('\n') for val in f.readlines()]
    return my_input


def read_column_at_index(my_input, i):
    # this can be replaced with the swap matrix thingy??
    column = ""
    for line in my_input:
        column += line[i]
    return column


def sum_column(column):
    total = 0
    for c in column:
        total += int(c)
    return total


def get_common_type_for_column(column, common_type):
    my_sum = sum_column(column)
    if my_sum >= (len(column) / 2):
        if common_type == Common.MOST:
            return "1"
        else:  # Common.LEAST
            return "0"
    else:
        if common_type == Common.MOST:
            return "0"
        else:  # Common.LEAST
            return "1"


def get_common_type_for_columns_in_range(my_input, common_type, range_start, range_end):
    result = ""
    for x in range(range_start, range_end):
        column = (read_column_at_index(my_input, x))
        result += get_common_type_for_column(column, common_type)
    return result


def part_one_calc_rate(my_input, common_type):
    bin_len = len(my_input[0])
    rate = get_common_type_for_columns_in_range(my_input, common_type, 0, bin_len)
    return int(rate, 2)


def part_one(my_input):
    gamma_rate = part_one_calc_rate(my_input, Common.MOST)
    epsilon_rate = part_one_calc_rate(my_input, Common.LEAST)
    # print(f"gamma rate {gamma_rate}, epsilon rate {epsilon_rate}")
    return gamma_rate * epsilon_rate


def filter_list_for_value_at_x(list_to_filter, index, value):
    iterable_list = list_to_filter.copy()
    for line in iterable_list:
        if line[index] != value:
            list_to_filter.remove(line)


def part_two_calc_rate(my_input, common_type):
    bin_len = len(my_input[0])
    filtered_list = my_input.copy()
    for x in range(bin_len):
        val = get_common_type_for_columns_in_range(filtered_list, common_type, x, x + 1)
        filter_list_for_value_at_x(filtered_list, x, val)
        if len(filtered_list) == 1:
            break
    return int(filtered_list[0], 2)


def part_two(my_input):
    oxy_gen_rate = part_two_calc_rate(my_input, Common.MOST)
    co2_scrub_rate = part_two_calc_rate(my_input, Common.LEAST)
    # print(f"oxy_gen_rate {oxy_gen_rate}, co2_scrub_rate {co2_scrub_rate}")
    return oxy_gen_rate * co2_scrub_rate

if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_input("input.txt"))}')  # 3882564
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_input("input.txt"))}') #3385170
