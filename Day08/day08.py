# https://adventofcode.com/2021/day/8

from advent2021.common.read_input import read_file_lines, str_numbers_to_list

TEST_CASE = {
    "input": ["be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe", "edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc", "fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg", "fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb", "aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea", "fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb", "dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe", "bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef", "egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb", "gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"],
    # "input": ["acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"],
    "part_one_result": 26,
    "part_two_result": 61229,
}


def filter_input_for_output_only(my_input):
    # for line in input:
    #     index = line.find('|')
    #     new_line = line[index::]

    return [line[line.find('|') + 1:].strip() for line in my_input]


def part_one(my_input):
    #  setup input
    # parse only output
    lines = filter_input_for_output_only(my_input)
    my_figures = [2, 4, 3, 7]

    #  do actions
    #  count number of times there are combos with 1 (2), 4(4), 7(3), 8(7)
    total = 0
    for line in lines:
        my_split = line.split()
        for word in my_split:
            my_len = len(word)
            total += 1 if my_len in my_figures else 0

    # get result
    return total


# ----------------------------- part 2 ------------------------------

def find_signal_with_length(all_signals, length):
    return [signal for signal in all_signals if len(signal) == length]


def get_common_char_count(str1, str2):
    total = 0
    for char in str1:
        if char in str2:
            total += 1
    return total


def find_three(five_signals, signal_1):
    for signal in five_signals:
        if get_common_char_count(signal, signal_1) == 2:
            five_signals.remove(signal)
            return signal


def find_five(two_and_five, signal_4):
    for signal in two_and_five:
        if get_common_char_count(signal, signal_4) == 3:
            two_and_five.remove(signal)
            return signal


def find_six(six_signals, signal_1):
    for signal in six_signals:
        if get_common_char_count(signal, signal_1) == 1:
            six_signals.remove(signal)
            return signal


def find_nine(nine_zero, signal_4):
    for signal in nine_zero:
        if get_common_char_count(signal, signal_4) == 4:
            nine_zero.remove(signal)
            return signal


def order_signals(all_signals):
    result = [None] * 10

    # set the easy ones
    result[1] = find_signal_with_length(all_signals, 2)[0]
    result[4] = find_signal_with_length(all_signals, 4)[0]
    result[7] = find_signal_with_length(all_signals, 3)[0]
    result[8] = find_signal_with_length(all_signals, 7)[0]

    # set 5s (2, 3, 5)
    fives = find_signal_with_length(all_signals, 5)
    result[3] = find_three(fives, result[1])
    result[5] = find_five(fives, result[4])
    result[2] = fives[0]

    # set 6s (0, 6, 9)
    sixes = find_signal_with_length(all_signals, 6)
    result[6] = find_six(sixes, result[1])
    result[9] = find_nine(sixes, result[4])
    result[0] = sixes[0]

    return result


def get_number_from_signal(signals, to_find):
    for i, signal in enumerate(signals):
        if (len(signal) == len(to_find)) and (get_common_char_count(signal, to_find) == len(to_find)):
            return i


def decode_output(signals, outputs):
    result = ""
    for output in outputs:
        result += str(get_number_from_signal(signals, output))
    return result


def part_two(my_input):
    #  setup input
    displays = []
    for line in my_input:
        display = {
            "signals": [],
            "outputs": [],
            "decoded_output": ""
        }

        split_signals_output = line.split('|')

        signal_split = split_signals_output[0].split()
        all_signals = [signal for signal in signal_split]
        display["signals"] = order_signals(all_signals)

        output_split = split_signals_output[1].split()
        display["outputs"] = [output for output in output_split]
        display["decoded_output"] = decode_output(display["signals"], display["outputs"])

        displays.append(display)

    #  do actions
    # get result

    total = 0
    for display in displays:
        total += int(display["decoded_output"])
    return total



if __name__ == '__main__':
    print(f'My part one Test Case answer is {part_one(TEST_CASE["input"])}, expecting {TEST_CASE["part_one_result"]} ')
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))}')  # 272
    print("------------")
    print(f'My part two Test Case answer is {part_two(TEST_CASE["input"])}, expecting {TEST_CASE["part_two_result"]} ')
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))}')  #1007675
