from typing import List


def read_file_lines(filename):
    with open(filename, 'r') as f:
        my_input = [val.strip('\n') for val in f.readlines()]
    return my_input


def read_file_to_list_int(filename):
    with open(filename, 'r') as f:
        my_input = [int(val) for val in f.readlines()]
    # print(my_input)
    return my_input


def str_numbers_to_list(line, char) -> List[int]:
    my_split = line.split(char)
    my_list = [int(val) for val in my_split]
    return my_list


def str_digits_to_list(line) -> List[int]:
    my_list = [int(val) for val in line]
    return my_list
