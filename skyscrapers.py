'''
GitHub link: https://github.com/linvieson/skyscrapers_project
This modue checks if the skyscrapers combination on the board in winning or
not.
'''

def read_input(path: str) -> list:
    """
    Read game board file from path.
    Return list of str.

    >>> read_input("check.txt")
    ['***21**', '412453*', '423145*', '*543215', '*35214*', '*41532*',\
 '*2*1***']
    >>> read_input("input.txt")
    ['***21**', '4?????*', '4?????*', '*?????5', '*?????*', '*?????*',\
 '*2*1***']
    """
    with open(path, 'r', encoding='utf-8') as lines_file:
        lines = lines_file.readlines()

    for ind, line in enumerate(lines):
        if line.__contains__('\n'):
            lines[ind] = line[:-1]

    return lines


def left_to_right_check(input_line: str, pivot: int) -> bool:
    """
    Check row-wise visibility from left to right.
    Return True if number of building from the left-most hint is visible
    looking to the right, False otherwise.

    input_line - representing board row.
    pivot - number on the left-most hint of the input_line.

    >>> left_to_right_check("412453*", 4)
    True
    >>> left_to_right_check("452453*", 3)
    False
    """
    pure_line = input_line[1:-1]
    index = pure_line.index(str(pivot))

    for elem in pure_line[:index]:
        if elem == '*':
            pure_line[pure_line.index('*')] = 0
        if int(pivot) < int(elem):
            return False
    return True


def check_not_finished_board(board: list) -> bool:
    """
    Check if skyscraper board is not finished, i.e., '?' present on the game
    board.

    Return True if finished, False otherwise.

    >>> check_not_finished_board(['***21**', '4?????*', '4?????*', '*?????5',\
 '*?????*', '*?????*', '*2*1***'])
    False
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*543215',\
 '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_not_finished_board(['***21**', '412453*', '423145*', '*5?3215',\
 '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        if '?' in line:
            return False
    return True


def check_uniqueness_in_rows(board: list) -> bool:
    """
    Check buildings of unique height in each row.

    Return True if buildings in a row have unique length, False otherwise.

    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*543215',\
 '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_uniqueness_in_rows(['***21**', '452453*', '423145*', '*543215',\
 '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_uniqueness_in_rows(['***21**', '412453*', '423145*', '*553215',\
 '*35214*', '*41532*', '*2*1***'])
    False
    """
    for line in board:
        saw = []
        for elem in line[1:-1]:
            if elem == '*':
                continue
            if elem not in saw:
                saw.append(elem)
            else:
                return False
    return True


def check_horizontal_visibility(board: list) -> bool:
    """
    Check row-wise visibility (left-right and vice versa)

    Return True if all horizontal hints are satisfiable,
     i.e., for line 412453* , hint is 4, and 1245 are the four buildings
      that could be observed from the hint looking to the right.

    >>> check_horizontal_visibility(['***21**', '412453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    True
    >>> check_horizontal_visibility(['***21**', '452453*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    >>> check_horizontal_visibility(['***21**', '452413*', '423145*',\
 '*543215', '*35214*', '*41532*', '*2*1***'])
    False
    """
    lst = []
    pure_board = board[1:-1]

    for elem in pure_board:
        counter = 0

        for symb in elem[1:-1]:
            if left_to_right_check(elem, symb):
                counter += 1

        if elem[0] != '*' and counter == int(elem[0]):
            lst.append(True)
        elif elem[0] == '*':
            lst.append(True)
        else:
            lst.append(False)

        rev_elem = elem[::-1]
        counter = 0

        for symb in rev_elem[1:-1]:
            if left_to_right_check(rev_elem, symb):
                counter += 1

        if rev_elem[0] != '*' and counter == int(rev_elem[0]):
            lst.append(True)
        elif rev_elem[0] == '*':
            lst.append(True)
        else:
            lst.append(False)

    return all(lst)


def check_columns(board: list) -> bool:
    """
    Check column-wise compliance of the board for uniqueness (buildings of
    unique height) and visibility (top-bottom and vice versa).

    Same as for horizontal cases, but aggregated in one function for vertical
    case, i.e. columns.

    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*',\
 '*41532*', '*2*1***'])
    True
    >>> check_columns(['***21**', '412453*', '423145*', '*543215', '*35214*',\
 '*41232*', '*2*1***'])
    False
    >>> check_columns(['***21**', '412553*', '423145*', '*543215', '*35214*',\
 '*41532*', '*2*1***'])
    False
    """
    # turn the table 90 degreees clockwise so that columns are rows
    reversed_arr = [[board[lines][ind] for lines in range(len(board[0]))]\
                     for ind in range(len(board))]
    return check_uniqueness_in_rows(reversed_arr)\
     | check_horizontal_visibility(reversed_arr)


def check_skyscrapers(input_path: str) -> bool:
    """
    Main function to check the status of skyscraper game board.
    Return True if the board status is compliant with the rules,
    False otherwise.

    >>> check_skyscrapers("check.txt")
    True
    >>> check_skyscrapers("input.txt")
    False
    """
    board = read_input(input_path)
    return check_not_finished_board(board)\
     & check_uniqueness_in_rows(board) & check_horizontal_visibility(board)\
     & check_columns(board)


if __name__ == "__main__":
    print(check_skyscrapers("check.txt"))
