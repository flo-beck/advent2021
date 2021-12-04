
def read_file_lines(filename):
    with open(filename, 'r') as f:
        my_input = [val.strip('\n') for val in f.readlines()]
    return my_input

def read_file_to_list_int(filename):
    with open(filename, 'r') as f:
        my_input = [int(val) for val in f.readlines()]
    # print(my_input)
    return my_input