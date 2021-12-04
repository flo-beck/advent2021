# https://adventofcode.com/2021/day/4
from typing import List

TEST_CASE = {
    "input": ["7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1","","22 13 17 11  0", "8  2 23  4 24","21  9 14 16  7", "6 10  3 18  5", "1 12 20 15 19","", "3 15  0  2 22", "9 18 13 17  5","19  8  7 25 23","20 11 10 24  4","14 21 16 12  6","","14 21 17 24  4","10 16 15  9 19","18  8 23 26 20","22 11 13  6  5", "2  0 12  3  7",],
    "part_one_result": 4512,
    "part_two_result": 1924,
}


def read_file_lines(filename):
    with open(filename, 'r') as f:
        my_input = [val.strip('\n') for val in f.readlines()]
    return my_input


def make_obj_from_int(int_val):
    return {
        "val": int_val,
        "called": False
    }


def str_numbers_to_list(line, char) -> List[int]:
    my_split = line.split(char)
    my_list = [int(val) for val in my_split]
    return my_list


def str_numbers_to_list_obj(line, char):
    return [make_obj_from_int(val) for val in str_numbers_to_list(line, char)]


def parse_boards(lines):
    boards = [[]]
    x = 0
    for line in lines:
        if line != "":  # a new board
            numbers_from_str = str_numbers_to_list_obj(line, None)
            boards[x].append(numbers_from_str)
        else:
            x += 1
            boards.append([])

    return boards


def print_board(board):
    for row in board:
        for number in row:
            if number["called"]:
                print('|' + str(number["val"]).rjust(2) + '|', end=' ')
            else:
                print(' ' + str(number["val"]).rjust(2) + ' ', end=' ')

        print(' ')


def print_boards(boards):
    for board in boards:
        print_board(board)
        print(' ')


def apply_num_to_boards(boards, number_to_find):
    for board in boards:
        for row in board:
            for number in row:
                if number["val"] == number_to_find:
                    number["called"] = True


def get_uncalled(row):
    return list(filter(lambda num: not num["called"], row))


def has_winning_row(board):
    for row in board:
        not_called_nums = get_uncalled(row)
        if len(not_called_nums) == 0:
            return True

    return False


def has_winning_column(board):
    # rotate the matrix so that the columns become rows
    rotated = list(zip(*board[::-1]))
    return has_winning_row(rotated)


def return_first_winning_board(boards):
    for board in boards:
        if has_winning_row(board) or has_winning_column(board):
            return board

    return


def calc_sum_unmarked(board):
    total = 0
    for row in board:
        not_called_nums = get_uncalled(row)
        total += sum(num["val"] for num in not_called_nums)

    return total


def calc_board(board, called_num):
    return calc_sum_unmarked(board) * called_num


def part_one(my_input):
    called_numbers = str_numbers_to_list(my_input[0], ',')
    my_boards = parse_boards(my_input[2:])

    # print_boards(my_boards)

    for number in called_numbers:
        # print_boards(my_boards)
        # print(f"------ new round - number is {number}--------")

        apply_num_to_boards(my_boards, number)
        winner = return_first_winning_board(my_boards)
        if winner:
            # print("------ winner--------")
            # print_board(winner)
            return calc_board(winner, number)

    return "There were no winners"


def remove_winning_boards(boards):
    for board in boards.copy():
        if has_winning_row(board) or has_winning_column(board):
            boards.remove(board)


def get_ongoing_boards(all_boards):
    return [board for board in all_boards if not (has_winning_row(board) or has_winning_column(board))]


def part_two(my_input):
    called_numbers = str_numbers_to_list(my_input[0], ',')
    my_boards = parse_boards(my_input[2:])

    for number in called_numbers:
        apply_num_to_boards(my_boards, number)
        if len(my_boards) == 1:
            winner = return_first_winning_board(my_boards)
            if winner:
                print(f"------ last winner----number is {number}----")
                print_board(my_boards[0])
                return calc_board(my_boards[0], number)
        else:
            # remove_winning_boards(my_boards)
            my_boards = get_ongoing_boards(my_boards)

    return "There was no final board -- how ?"


if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  # 45031
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}') #30268 - incorrect // 2568 is correct
