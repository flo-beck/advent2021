# https://adventofcode.com/2021/day/6

from advent2021.common.read_input import read_file_lines, str_numbers_to_list

TEST_CASE = {
    "input": ["3,4,3,1,2"],
    "part_one_result": 5934,
    "part_two_result": 26984457539,
}


def propagate_fish(list_fish):
    fish_len = len(list_fish)
    for x in range(fish_len):
        if list_fish[x] == 0:
            list_fish[x] = 6
            list_fish.append(8)
        else:
            list_fish[x] -= 1


def part_one(my_input):
    #  setup input
    my_lanterns = str_numbers_to_list(my_input[0], ',')

    #  do actions
    for x in range(80):
        propagate_fish(my_lanterns)

    # get result
    return len(my_lanterns)


# ----------------------------- part 2 ------------------------------


def setup_counter(list_lanterns):
    counter = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    for val in list_lanterns:
        counter[val] += 1
    return counter


def propagate_fish_with_counter(counter):
    zeros = counter[0]
    for x in range(1, 9):
        counter[x-1] = counter[x]
    counter[8] = zeros
    counter[6] += zeros
    return counter


def part_two(my_input):
    #  setup input
    list_lanterns = str_numbers_to_list(my_input[0], ',')
    my_counter = setup_counter(list_lanterns)

    #  do actions
    for _ in range(256):
        my_counter = propagate_fish_with_counter(my_counter)

    # get result
    return sum(my_counter)


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  # 353079
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  # 1605400130036
