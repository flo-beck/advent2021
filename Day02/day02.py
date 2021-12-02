# https://adventofcode.com/2021/day/2

TEST_CASE = {
    "input": ["forward 5", "down 5", "forward 8", "up 3", "down 8", "forward 2"],
    "part_one_result": 150,
    "part_two_result": 900,
}


def read_file_input(filename):
    with open(filename, 'r') as f:
        my_input = [val for val in f.readlines()]
    # print(my_input)
    return my_input


def parse_line(line):
    return {
        "direction": line.split()[0],
        "value": line.split()[1]
    }


def part_one(my_input):
    position = {
        "horizontal": 0,
        "depth": 0,
    }

    for line in my_input:
        pline = parse_line(line)
        value = int(pline["value"])
        direction = pline["direction"]
        if direction == 'forward':
            position["horizontal"] += value
        elif direction == 'down':
            position["depth"] += value
        elif direction =='up':
            position["depth"] -= value
        else :
            return "Something's wrong with the input"
    return position["horizontal"] * position["depth"]


def part_two(my_input):
    position = {
        "horizontal": 0,
        "depth": 0,
        "aim": 0,
    }

    for line in my_input:
        pline = parse_line(line)
        value = int(pline["value"])
        direction = pline["direction"]
        if direction == 'forward':
            position["horizontal"] += value
            position["depth"] += position["aim"] * value
        elif direction == 'down':
            position["aim"] += value
        elif direction == 'up':
            position["aim"] -= value
        else:
            return "Something's wrong with the input"
    return position["horizontal"] * position["depth"]


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_input("input.txt"))}')
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_input("input.txt"))}')
