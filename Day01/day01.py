# https://adventofcode.com/2021/day/1
from advent2021.common.read_input import read_file_to_list_int

TEST_CASE = {
    "numbers": [199, 200, 208, 210, 200, 207, 240, 269, 260, 263],
    "part_one_result": 7,
    "part_two_result": 5,
}


def part_one(my_input):
    my_increases = 0
    for i, val in enumerate(my_input):
        if (i > 0) and (val > my_input[i - 1]):
            my_increases += 1
    return my_increases


# def part_two_geraud(my_input):
    # my_3window_sums = []
    # for i in range(len(my_input[:-2])):
    #     my_3window_sums.append(sum(my_input[i:i+3]))
    # return part_one(my_3window_sums)

def part_two_geraud(my_input):
    # comprehension list
    my_3window_sums = [sum(my_input[i:i+3]) for i in range(len(my_input[:-2]))]
    return part_one(my_3window_sums)

def part_two(my_input):
    list_len = len(my_input)
    my_3window_sums = []
    for i, val in enumerate(my_input):
        if i + 2 < list_len:
            my_sum = val + my_input[i + 1] + my_input[i + 2]
            my_3window_sums.append(my_sum)
    return part_one(my_3window_sums)


def read_file_input(filename):
    with open(filename, 'r') as f:
        my_input = [int(val) for val in f.readlines()]
    # print(my_input)
    return my_input


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["numbers"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_to_list_int("input.txt"))}')
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["numbers"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_input("input.txt"))}')
