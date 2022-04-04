BOARD_X = 0
BOARD_Y = 0
COUNT = 0
UNDERSCORES = 0
FORMAT = '{:2}'
FORMAT_2 = '{:1}'
MOVES = [[-2, 1], [-2, -1], [1, 2], [-1, 2],
         [2, 1], [2, -1], [1, -2], [-1, -2]]


def main():
    global BOARD_Y, BOARD_X, UNDERSCORES, COUNT
    BOARD_X, BOARD_Y = get_two_ints('Enter your board dimensions:', 1, 100, 1, 100)
    UNDERSCORES = len(str(BOARD_Y * BOARD_X))
    get_format()
    field = [['_' * UNDERSCORES for x in range(BOARD_X)]for y in range(BOARD_Y)]
    x, y = get_two_ints('Enter the knight\'s starting position:', 1, BOARD_X, 1, BOARD_Y, 'Invalid position!')
    field[y - 1][x - 1] = ' ' * (UNDERSCORES - 1) + 'X'
    if not see_the_solution(field, y-1, x-1):
        COUNT += 1
        print('\nHere are the possible moves:')
        flag = get_possible_places(field, [y-1, x-1])
        print_interface(field)

        while are_moves_possible(field):
            x, y = get_next_move('\nEnter your next move: ', field)
            flag = get_possible_places(field, [y - 1, x - 1])
            print_interface(field)

            if not flag:
                print('No more possible moves!')
                print(f'Your knight visited {COUNT} squares!')
                break
        else:
            print('What a great tour! Congratulations!')


def see_the_solution(field, x, y):
    while True:
        print('Do you want to try the puzzle? (y/n):', end=' ')
        choice = input()
        if choice != 'n' and choice != 'y':
            print('Invalid input!')
        elif choice == 'n':
            show_solution(field, x, y)
            return True
        else:
            return False


def show_solution(field, x, y):
    global BOARD_X, BOARD_Y, UNDERSCORES
    field = [[0 for x in range(BOARD_X)] for y in range(BOARD_Y)]
    field[x][y] = 1
    pos = 2
    if not solve_grid(field, x, y, pos):
        print("No solution exists!")
    else:
        print("\nHere's the solution!")
        print_interface(field)


def solve_grid(field, x, y, pos):
    global BOARD_X, BOARD_Y, MOVES
    for i in range(8):
        if pos > BOARD_X * BOARD_Y:
            make_field_beautiful(field)
            return True
        new_x = x + MOVES[i][0]
        new_y = y + MOVES[i][1]
        if is_move_possible(field, new_x, new_y):
            field[new_x][new_y] = pos
            if solve_grid(field, new_x, new_y, pos+1):
                return True
            field[new_x][new_y] = 0
    return False


def make_field_beautiful(field):
    global BOARD_Y, BOARD_X, UNDERSCORES
    for i in range(BOARD_Y):
        for j in range(BOARD_X):
            if 0 < field[i][j] < 10:
                field[i][j] = ' ' * (UNDERSCORES - 1) + str(field[i][j])
            elif 9 < field[i][j] < 100:
                field[i][j] = ' ' * (UNDERSCORES - 2) + str(field[i][j])
            else:
                field[i][j] = ' ' * (UNDERSCORES - 3) + str(field[i][j])


def is_move_possible(field, row, column):
    global BOARD_X, BOARD_Y
    if (0 <= row < BOARD_Y) and (0 <= column < BOARD_X) and (field[row][column] == 0):
        return True
    return False


def are_moves_possible(field):
    global UNDERSCORES
    for item in field:
        if '_' * UNDERSCORES in item:
            return True
    return False


def get_next_move(prompt, field):
    global UNDERSCORES, COUNT
    while True:
        try:
            print(prompt, end='')
            x, y = input().split()
            x = int(x)
            y = int(y)
            if (field[y-1][x-1] != '_' * UNDERSCORES) and (field[y-1][x-1] != ' ' * (UNDERSCORES - 1) + '*') and (field[y-1][x-1] != ' ' * (UNDERSCORES - 1) + 'X'):
                clean_field(field)
                field[y-1][x-1] = ' ' * (UNDERSCORES - 1) + 'X'
                COUNT += 1
                return x, y
            else:
                raise
        except:
            print('Invalid move!', end='')


def clean_field(field):
    for i in range(BOARD_Y):
        for j in range(BOARD_X):
            if field[i][j] == ' ' * (UNDERSCORES - 1) + 'X':
                field[i][j] = ' ' * (UNDERSCORES - 1) + '*'
            elif field[i][j] == ' ' * (UNDERSCORES - 1) + '*':
                pass
            elif field[i][j] != '_' * UNDERSCORES:
                field[i][j] = '_' * UNDERSCORES


def get_possible_places(field, item):
    global MOVES, BOARD_Y, BOARD_X
    flag = False
    for i in MOVES:
        if 0 <= item[0] + i[0] < BOARD_Y and 0 <= item[1] + i[1] < BOARD_X and field[item[0] + i[0]][item[1] + i[1]] != ' ' * (UNDERSCORES - 1) + '*':
            field[item[0] + i[0]][item[1] + i[1]] = ' ' * (UNDERSCORES - 1) + str(get_count_of_possible_moves(field, [item[0] + i[0], item[1] + i[1]], item))
            flag = True
    return flag


def get_count_of_possible_moves(field, item, main_):
    count = 0
    global MOVES, BOARD_Y, BOARD_X
    for i in MOVES:
        if 0 <= item[0] + i[0] < BOARD_Y and 0 <= item[1] + i[1] < BOARD_X and (field[item[0] + i[0]][item[1] + i[1]] != field[main_[0]][main_[1]]):
            count += 1
    return count


def get_two_ints(prompt, lower_board, higher_board, l_b_2, h_b_2, error_text='Invalid dimensions!'):
    while True:
        try:
            print(prompt, end=' ')
            x, y = input().split()
            x = int(x)
            y = int(y)
            if (x < lower_board) or (x > higher_board) or (y < l_b_2) or (y > h_b_2):
                raise
            return x, y
        except:
            print(error_text)


def print_interface(field):
    global BOARD_Y, BOARD_X, UNDERSCORES, FORMAT, FORMAT_2
    print(FORMAT_2.format(' '), end='')
    print('-' * (BOARD_X * (UNDERSCORES + 1) + 3))
    for i in range(BOARD_Y - 1, -1, -1):
        print(FORMAT_2.format(i + 1), end='| ')
        for j in range(BOARD_X):
            print(field[i][j], end=' ')
        print('|')
    print(FORMAT_2.format(' '), end='')
    print('-' * (BOARD_X * (UNDERSCORES + 1) + 3))
    print(FORMAT.format(' '), end=' ')
    for i in range(1, BOARD_X + 1):
        print(FORMAT.format(i), end=' ')
    print()


def get_format():
    global UNDERSCORES, FORMAT, FORMAT_2
    if UNDERSCORES == 2:
        FORMAT = '{:2}'
        FORMAT_2 = '{:1}'
    elif UNDERSCORES == 3:
        FORMAT = '{:3}'
        FORMAT_2 = '{:2}'


if __name__ == '__main__':
    main()
