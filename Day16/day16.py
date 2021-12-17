# https://adventofcode.com/2021/day/16
import sys
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list, str_to_list_chars
import math
from collections import namedtuple
import copy
import time

TEST_CASE = {
    "inputA": ["8A004A801A8002F478"],
    "inputB": ["620080001611562C8802118E34"],
    "inputC": ["C0015000016115A2E0802F182340"],
    "inputD": ["A0016C880162017C3686B18A3D4780"],
    "inputE": ["C200B40A82"],
    "inputF": ["04005AC33890"],
    "inputG": ["880086C3E88112"],
    "inputH": ["CE00C43D881120"],
    "inputI": ["D8005AC2A8F0"],
    "inputJ": ["F600BC2D8F"],
    "inputK": ["9C005AC2F8F0"],
    "inputL": ["9C0141080250320F1802104A08"],
    "part_oneA_result": 16,
    "part_oneB_result": 12,
    "part_oneC_result": 23,
    "part_oneD_result": 31,
    "part_twoE_result": 3,
    "part_twoF_result": 54,
    "part_twoG_result": 7,
    "part_twoH_result": 9,
    "part_twoI_result": 1,
    "part_twoJ_result": 0,
    "part_twoK_result": 0,
    "part_twoL_result": 1,

    "part_two_result": '?',
}

BINARY = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


class Packet:
    def __init__(self, version, my_type, value):
        self.version = version
        self.type = my_type
        self.value = value
        self.children = []
        self.len = 6


def convert_to_binary(my_input):
    bin_str = ""
    for char in my_input:
        bin_str += BINARY[char]
    return bin_str


def get_version(bin_str):
    return int(bin_str[:3], 2)


def get_type(bin_str):
    return int(bin_str[3:6], 2)


def read_part_4_res(binary_num):
    return int(binary_num, 2)


def parse_type_4(bin_str, packet):
    five_bits = bin_str[6:11]
    bin_result = ""
    i = 6

    # calc value of packet
    while i < len(bin_str):
        bin_result += five_bits[1:]
        i += 5
        if five_bits[0] == '1':
            five_bits = bin_str[i: i + 5]
        else:
            break
    packet.value = read_part_4_res(bin_result)

    # calc len of packet
    # next_mul_4 = i + (4 - (i % 4))
    # trailing_zeros = next_mul_4 - i
    trailing_zeros = 0
    packet.len = i + trailing_zeros
    return packet


def is_padding(my_str):
    char_list = ["0"]
    matched_list = [characters in char_list for characters in my_str]
    return all(matched_list)


def parse_type_op(bin_str, packet):
    len_id_type = bin_str[6]
    len_so_far = 7  # header + len_id_type

    if len_id_type == '0':               # 15 bits type
        len_so_far += 15
        sub_packet_len = int(bin_str[7:len_so_far], 2)
        packet.len = len_so_far + sub_packet_len
        while len_so_far < packet.len:
            sub_packet = parse_packet(bin_str[len_so_far:])
            if sub_packet:
                len_so_far += sub_packet.len
                packet.children.append(sub_packet)
            else:
                break

    else:                               # 11 bits type
        len_so_far += 11
        num_packets = int(bin_str[7:len_so_far], 2)
        for i in range(num_packets):
            sub_packet = parse_packet(bin_str[len_so_far:])
            if sub_packet:
                len_so_far += sub_packet.len
                packet.children.append(sub_packet)
        packet.len = len_so_far

    return packet


def parse_packet(bin_str):
    if len(bin_str) < 7 or is_padding(bin_str):
        return None
    header = bin_str[0:6]
    version = get_version(header)
    my_type = get_type(header)
    packet = Packet(version, my_type, None)
    if my_type == 4:  # literal value
        return parse_type_4(bin_str, packet)
    else:             # operator
        return parse_type_op(bin_str, packet)


def calc_version_total(packet):
    if len(packet.children) == 0:
        return int(packet.version)
    else:
        total = 0
        for child in packet.children:
            total += calc_version_total(child)
        return total + int(packet.version)


def part_one(my_input):
    #  setup input
    my_bits = convert_to_binary(my_input[0])

    #  do actions
    packets = parse_packet(my_bits)

    # get result
    total = calc_version_total(packets)
    return total


# ----------------------------- part 2 ------------------------------

def sum_value(packet):
    total = 0
    for child in packet.children:
        total += calc_values(child)
    packet.value = total
    return total


def prod_value(packet):
    total = 1
    for child in packet.children:
        total *= calc_values(child)
    packet.value = total
    return total


def min_value(packet):
    child_vals = []
    for child in packet.children:
        child_vals.append(calc_values(child))
    packet.value = min(child_vals)
    return packet.value


def max_value(packet):
    child_vals = []
    for child in packet.children:
        child_vals.append(calc_values(child))
    packet.value = max(child_vals)
    return packet.value


def gt_value(packet):
    child_vals = []
    for child in packet.children:
        child_vals.append(calc_values(child))
    packet.value = 1 if child_vals[0] > child_vals[1] else 0
    return packet.value


def lt_value(packet):
    child_vals = []
    for child in packet.children:
        child_vals.append(calc_values(child))
    packet.value = 1 if child_vals[0] < child_vals[1] else 0
    return packet.value


def eq_value(packet):
    child_vals = []
    for child in packet.children:
        child_vals.append(calc_values(child))
    packet.value = 1 if child_vals[0] == child_vals[1] else 0
    return packet.value


def get_value(packet):
    return packet.value


TAB_FT = {
    0: sum_value,
    1: prod_value,
    2: min_value,
    3: max_value,
    4: get_value,
    5: gt_value,
    6: lt_value,
    7: eq_value,
}


def calc_values(packet):
    return TAB_FT[packet.type](packet)


def part_two(my_input):
    #  setup input
    my_bits = convert_to_binary(my_input[0])

    #  do actions
    packets = parse_packet(my_bits)

    # get result
    total = calc_values(packets)
    return total


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["inputA"])}, expecting {TEST_CASE["part_oneA_result"]}')
    print(f'My part one Test Case answer is {part_one(TEST_CASE["inputB"])}, expecting {TEST_CASE["part_oneB_result"]}')
    print(f'My part one Test Case answer is {part_one(TEST_CASE["inputC"])}, expecting {TEST_CASE["part_oneC_result"]}')
    print(f'My part one Test Case answer is {part_one(TEST_CASE["inputD"])}, expecting {TEST_CASE["part_oneD_result"]}')

    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #989

    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputE"])}, expecting {TEST_CASE["part_twoE_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputF"])}, expecting {TEST_CASE["part_twoF_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputG"])}, expecting {TEST_CASE["part_twoG_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputH"])}, expecting {TEST_CASE["part_twoH_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputI"])}, expecting {TEST_CASE["part_twoI_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputJ"])}, expecting {TEST_CASE["part_twoJ_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputK"])}, expecting {TEST_CASE["part_twoK_result"]}')
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputL"])}, expecting {TEST_CASE["part_twoL_result"]}')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #
