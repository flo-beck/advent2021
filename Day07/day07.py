# https://adventofcode.com/2021/day/7

from advent2021.common.read_input import read_file_lines, str_numbers_to_list

TEST_CASE = {
    "input": ["16,1,2,0,4,2,7,1,2,14"],
    "part_one_result": 37,
    "part_two_result": 168,
}


def setup_empty_counter(val):
    result = []
    for x in range(val + 1):
        result.append(0)
    return result


def init_counter(counter, crab_list):
    for crab in crab_list:
        counter[crab] += 1
    return counter


def get_diff(pos_a, pos_b):
    return abs(pos_a - pos_b)


def calc_cost(crab_counter, align_to):
    total = 0
    for position, frequency in enumerate(crab_counter):
        fuel_cost = get_diff(position, align_to)
        total += (fuel_cost * frequency)
    return total


def part_one(my_input):
    #  setup input
    my_crabs = str_numbers_to_list(my_input[0], ',')
    max_crab_position = max(my_crabs)
    crab_counter = init_counter(setup_empty_counter(max_crab_position), my_crabs)

    # print(crab_counter)
    # print(len(crab_counter))

    fuel_cost_counter = setup_empty_counter(max_crab_position)

    #  do actions
    for x in range(len(crab_counter)):
        cost = calc_cost(crab_counter, x)
        fuel_cost_counter[x] = cost

    # print(fuel_cost_counter)

    # get result
    return min(fuel_cost_counter)


# ----------------------------- part 2 ------------------------------

def calc_partial_sum(x):
    return int((x * (x+1))/2)


def calc_expensive_cost(pos_a, pos_b):
    diff = get_diff(pos_a, pos_b)
    return calc_partial_sum(diff)


def calc_cost2(crab_counter, align_to):
    total = 0
    for position, frequency in enumerate(crab_counter):
        fuel_cost = calc_expensive_cost(position, align_to)
        total += (fuel_cost * frequency)
    return total


def part_two(my_input):
    #  setup input
    my_crabs = str_numbers_to_list(my_input[0], ',')
    max_crab_position = max(my_crabs)
    crab_counter = init_counter(setup_empty_counter(max_crab_position), my_crabs)

    fuel_cost_counter = setup_empty_counter(max_crab_position)

    #  do actions
    for x in range(len(crab_counter)):
        cost = calc_cost2(crab_counter, x)
        fuel_cost_counter[x] = cost

    # get result
    return min(fuel_cost_counter)


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  # 347509
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  # 98257206
