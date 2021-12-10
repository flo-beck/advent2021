# https://adventofcode.com/2021/day/9

from advent2021.common.read_input import read_file_lines, str_numbers_to_list
import math

TEST_CASE = {
    "input": ["[({(<(())[]>[[{[]{<()<>>", "[(()[<>])]({[<{<<[]>>(", "{([(<{}[<>[]}>{[]{[(<()>",
              "(((({<>}<{<{<>}{[]{[]{}", "[[<[([]))<([[{}[[()]]]", "[{[{({}]{}}([{[{{{}}([]", "{<[[]]>}<{[{[{[]{()[[[]",
              "[<(<(<(<{}))><([]([]()", "<{([([[(<>()){}]>(<<{{", "<{([{{}}[<[[[<>{}]]]>[]]"],
    "part_one_result": 26397,
    "part_two_result": 288957,
}


def is_opener(char):
    return char == '(' or char == '[' or char == '{' or char == '<'


def get_closer(char):
    if char == '(':
        return ')'
    if char == '[':
        return ']'
    if char == '{':
        return '}'
    else:
        return '>'


def is_correct_closer(opens, c):
    return get_closer(opens[-1]) == c


def get_index_first_error(line):
    opens = []
    for i, c in enumerate(line):
        if is_opener(c):
            opens.append(c)
        else:
            if is_correct_closer(opens, c):
                opens.pop()
            else:
                return i
    return -1


def is_line_corrupted(line):
    error_index = get_index_first_error(line)
    if error_index >= 0:
        return True
    else:
        return False


def calc_errors(points, errors):
    total = 0
    for key, value in errors.items():
        total += value * points[key]
    return total


def part_one(my_input):
    #  setup input
    po_input = my_input.copy()

    points = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    # remove any non-corrupted lines
    for line in my_input:
        if not is_line_corrupted(line):
            po_input.remove(line)

    #  do actions
    errors = {
        ')': 0,
        ']': 0,
        '}': 0,
        '>': 0
    }
    for line in po_input:
        error = line[get_index_first_error(line)]
        errors[error] += 1

    # get result
    return calc_errors(points, errors)


# ----------------------------- part 2 ------------------------------

def get_list_opens(line):
    opens = []
    for c in line:
        if is_opener(c):
            opens.append(c)
        else:
            if is_correct_closer(opens, c):
                opens.pop()
            else:
                return "ERROR"
    return opens


def get_list_closers(line):
    opens = get_list_opens(line)
    return [get_closer(char) for char in reversed(opens)]


def calc_score_closer(closer, points):
    total = 0
    for c in closer:
        total = total * 5
        total += points[c]
    return total


def get_middle_score(scores):
    middle_index = int(math.ceil(len(scores)/2) - 1)
    return sorted(scores)[middle_index]


def part_two(my_input):
    # setup input
    points = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    pt_input = my_input.copy()

    for line in my_input:
        if is_line_corrupted(line):
            pt_input.remove(line)
    #  do actions
    closers = [get_list_closers(line) for line in pt_input]
    # get result
    scores = [calc_score_closer(closer, points) for closer in closers]
    return get_middle_score(scores)


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  #167379
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #2776842859
