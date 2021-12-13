# https://adventofcode.com/2021/day/12
from functools import lru_cache

from advent2021.common.read_input import read_file_lines, str_digits_to_list
import math
from collections import namedtuple
import copy
import time


TEST_CASE = {
    "inputA": ["start-A", "start-b", "A-c", "A-b", "b-d", "A-end", "b-end"],
    "inputB": ["dc-end", "HN-start", "start-kj", "dc-start", "dc-HN", "LN-dc", "HN-end", "kj-sa", "kj-HN", "kj-dc"],
    "inputC": ["fs-end", "he-DX", "fs-he", "start-DX", "pj-DX", "end-zg", "zg-sl", "zg-pj", "pj-he", "RW-he", "fs-DX", "pj-RW", "zg-RW", "start-pj", "he-WI", "zg-he", "pj-fs", "start-RW"],
    "part_one_resultA": 10,
    "part_one_resultB": 19,
    "part_one_resultC": 226,
    "part_two_resultA": 36,
    "part_two_resultB": 103,
    "part_two_resultC": 3509,
}


class Node:
    def __init__(self, name, node_type):
        self.children = set()
        self.name = name
        self.type = node_type
        self.visited = 0


def is_upper(word):
    return word.upper() == word


def create_node(name):
    return Node(name, "big" if is_upper(name) else "small")


def add_new_node(my_nodes, name):
    if name not in my_nodes:
        my_nodes[name] = create_node(name)


def init_tree(my_input):
    my_nodes = {}
    for line in my_input:
        split = line.split('-')
        lhs_name = split[0]
        rhs_name = split[1]

        add_new_node(my_nodes, lhs_name)
        add_new_node(my_nodes, rhs_name)

        my_nodes[lhs_name].children.add(rhs_name)
        my_nodes[rhs_name].children.add(lhs_name)
    return my_nodes


def print_my_nodes(my_nodes):
    for node in my_nodes.values():
        child_str = [child for child in node.children]
        print(f"{node.name} -> {child_str}")


def print_node_details(node):
    print(f"name: {node.name}, type: {node.type}, visited: {node.visited}")


def print_nodes_details(my_nodes):
    for node in my_nodes.values():
        print_node_details(node)


def print_paths(paths):
    for i, path in enumerate(paths):
        path_str = [node.name for node in path]
        print(f" Path {i} - {path_str}")


# --------------------------------- setup and prints ^


def can_visit_node(my_nodes, node_name, max_small_visits):
    if node_name == "start":
        return False
    node = my_nodes[node_name]
    return not (node.type == "small" and node.visited >= max_small_visits)

@lru_cache
def get_path(my_nodes, max_small_visits, all_paths, curr_name, path_so_far):
    curr_node = my_nodes[curr_name]
    curr_node.visited += 1
    if curr_node.type == "small" and curr_node.visited == max_small_visits:
        max_small_visits = 1
    path_so_far.append(curr_node)
    if curr_node.name == "end":
        all_paths.append(path_so_far)
    else:
        for child in curr_node.children:
            if can_visit_node(my_nodes, child, max_small_visits):
                branch_tree = copy.deepcopy(my_nodes)
                branch_path = copy.deepcopy(path_so_far)
                get_path(branch_tree, max_small_visits, all_paths, child, branch_path)


def get_paths(my_nodes, max_small_visits):
    start_node = my_nodes["start"]
    start_node.visited = 1
    paths = []
    path_so_far = [start_node]
    for child in start_node.children:
        get_path(copy.deepcopy(my_nodes), max_small_visits, paths, child, copy.deepcopy(path_so_far))
    return paths


def part_one(my_input):
    #  setup input
    # my_nodes = init_tree(my_input)

    #  do actions
    paths = get_paths(init_tree(my_input), 1)
    # print_paths(paths)

    # get result
    return len(paths)


# ----------------------------- part 2 ------------------------------


def part_two(my_input):
    #  setup input

    #  do actions
    paths = get_paths(init_tree(my_input), 2)
    # print_paths(paths)

    # get result
    return len(paths)


if __name__ == '__main__':
    start_time = time.time()
    print(f'My part one Test Case A answer is {part_one(TEST_CASE["inputA"])}, expecting {TEST_CASE["part_one_resultA"]} - took {round(time.time() - start_time, 3)}')  # 0.002s
    start_time = time.time()
    print(f'My part one Test Case B answer is {part_one(TEST_CASE["inputB"])}, expecting {TEST_CASE["part_one_resultB"]} - took {round(time.time() - start_time, 3)}')  # 0.006s
    start_time = time.time()
    print(f'My part one Test Case C answer is {part_one(TEST_CASE["inputC"])}, expecting {TEST_CASE["part_one_resultC"]} - took {round(time.time() - start_time, 3)}')  # 0.173s
    start_time = time.time()
    print(f'My part one real answer is {part_one(read_file_lines("input.txt"))} - took {round(time.time() - start_time, 3)}')  # 3713 - 2.488s


    print("------------")
    start_time = time.time()
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputA"])}, expecting {TEST_CASE["part_two_resultA"]} - took {round(time.time() - start_time, 3)}')  # 0.008s
    start_time = time.time()
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputB"])}, expecting {TEST_CASE["part_two_resultB"]} - took {round(time.time() - start_time, 3)}')  # 0.03s
    start_time = time.time()
    print(f'My part two Test Case answer is {part_two(TEST_CASE["inputC"])}, expecting {TEST_CASE["part_two_resultC"]} - took {round(time.time() - start_time, 3)}')  # 3.303s
    start_time = time.time()
    print(f'My part two real answer is {part_two(read_file_lines("input.txt"))} - took {round(time.time() - start_time, 3)}')  # 91292 - 71.698s

    # ideas tp improve perf
    # remove class - calc visited by looking at previous path and make an immutable tuple
    # make only one tree with all possible paths on it

