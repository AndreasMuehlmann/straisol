import sys
from colorama import init, Fore

init(autoreset=True)

MAXNUMBER = 9

def read_straights(file):
    straights = []
    for row_count, row in enumerate(file):
        row = row.strip().split()
        assert len(row) <= 9, f'There can only be 9 columms (row: {row_count + 1})'
        if not row:
            continue

        for columm_count, square in enumerate(row):
            assert len(square) <= 2, f'One square can only contain two symbols (row: {row_count + 1}, columm: {columm_count + 1}.'

            if len(square) == 1:
                assert square.isdigit() or square == '.' or square == 'e',\
                    f'A square with one symbol can only contain an "e", a ".", a digit from "1" to "9" (row: {row_count + 1}, columm: {columm_count + 1}).'
                if square.isdigit():
                    assert 1 <= int(square) <= 9,\
                        f'Numbers can only be digits from "1" to "9" (row: {row_count + 1}, columm: {columm_count + 1}).'

            else: 
                assert square[0] == '.',\
                    f'A square with two symbols can only contain a "." as first character (row: {row_count + 1}, columm: {columm_count + 1}).'
                assert square[1].isdigit(),\
                    f'A square with two symbols can only contain a digit from "1" to "9" as a second symbol (row: {row_count + 1}, columm: {columm_count + 1}).'
                assert 1 <= int(square[1]) <= 9,\
                    f'Numbers can only be digits from "1" to "9" (row: {row_count + 1}, columm: {columm_count + 1}).'

        straights.append(row)

    assert len(straights) <= 9, f'There can only be 9 rows.'
    return straights

def is_valid(straights):
    for y in range(MAXNUMBER):
        for x in range(MAXNUMBER):
            if  straights[y][x] == 'e':
                continue

            if  straights[y][x] == '.':
                continue

            if len(straights[y][x]) == 2:
                number = int(straights[y][x][1])

                interferring_numbers_v, interferring_numbers_in_bound_v, free_squares_v =\
                    give_interferring_in_bound_and_freesquares_v(straights, x, y)
                interferring_numbers_h, interferring_numbers_in_bound_h, free_squares_h =\
                    give_interferring_in_bounds_and_freesquares_h(straights, x, y)

                if  number in interferring_numbers_v or number in interferring_numbers_h:
                    return False, x + 1, y + 1
                continue

            else:
                number = int(straights[y][x])

            interferring_numbers_v, interferring_numbers_in_bound_v, free_squares_v =\
                give_interferring_in_bound_and_freesquares_v(straights, x, y)
            if not number in give_possible_numbers(interferring_numbers_v, interferring_numbers_in_bound_v, free_squares_v):
                return False, x + 1, y + 1
                
            interferring_numbers_h, interferring_numbers_in_bound_h, free_squares_h =\
            give_interferring_in_bounds_and_freesquares_h(straights, x, y)
            if not number in give_possible_numbers(interferring_numbers_h, interferring_numbers_in_bound_h, free_squares_h):
                return False, x + 1, y + 1

            if  number in interferring_numbers_v or number in interferring_numbers_h:
                return False, x + 1, y + 1

    return True, -1, -1

def give_numbers_h(straights, static_index, search_range):
    numbers = []
    numbers_in_bound = []
    in_bound = True
    free_squares = 0
    for changing_index in search_range:
        if straights[static_index][changing_index].isdigit():
            numbers.append(int(straights[static_index][changing_index]))
            if in_bound:
                numbers_in_bound.append(int(straights[static_index][changing_index]))

        elif straights[static_index][changing_index] == '.':
            in_bound = False
            continue

        elif len(straights[static_index][changing_index]) == 2:
            numbers.append(int(straights[static_index][changing_index][1]))
            in_bound = False
            continue

        elif in_bound:
            free_squares += 1

    return numbers, numbers_in_bound, free_squares

def give_numbers_v(straights, static_index, search_range):
    numbers = []
    numbers_in_bound = []
    in_bound = True
    free_squares = 0
    for changing_index in search_range:
        if straights[changing_index][static_index].isdigit():
            numbers.append(int(straights[changing_index][static_index]))
            if in_bound:
                numbers_in_bound.append(int(straights[changing_index][static_index]))

        elif straights[changing_index][static_index] == '.':
            in_bound = False
            continue

        elif len(straights[changing_index][static_index]) == 2:
            numbers.append(int(straights[changing_index][static_index][1]))
            in_bound = False
            continue

        elif in_bound:
            free_squares += 1

    return numbers, numbers_in_bound, free_squares

def give_interferring_in_bound_and_freesquares_v(straights, x, y):
    numbers = set()
    numbers_in_bound = set()
    free_squares = 0

    new_numbers, new_numbers_in_bound, new_free_squares = give_numbers_v(straights, x, range(y + 1, MAXNUMBER, 1))
    free_squares += new_free_squares
    numbers.update(new_numbers)
    numbers_in_bound.update(new_numbers_in_bound)

    new_numbers, new_numbers_in_bound, new_free_squares = give_numbers_v(straights, x, range(y - 1, -1, -1))
    free_squares += new_free_squares
    numbers.update(new_numbers)
    numbers_in_bound.update(new_numbers_in_bound)

    return numbers, numbers_in_bound, free_squares

def give_interferring_in_bounds_and_freesquares_h(straights, x, y):
    numbers = set()
    numbers_in_bound = set()
    free_squares = 0

    new_numbers, new_numbers_in_bound, new_free_squares = give_numbers_h(straights, y, range(x + 1, MAXNUMBER, 1))
    free_squares += new_free_squares
    numbers.update(new_numbers)
    numbers_in_bound.update(new_numbers_in_bound)

    new_numbers, new_numbers_in_bound, new_free_squares = give_numbers_h(straights, y, range(x - 1, -1, -1))
    free_squares += new_free_squares
    numbers.update(new_numbers)
    numbers_in_bound.update(new_numbers_in_bound)

    return numbers, numbers_in_bound, free_squares

def give_to_fill_up(interferring_numbers_in_bound):
    to_fill_up = 0
    for number in range(min(interferring_numbers_in_bound), max(interferring_numbers_in_bound)):
        if number not in interferring_numbers_in_bound:
            to_fill_up += 1
    return to_fill_up

def give_possible_numbers(interferring_numbers, interferring_numbers_in_bound, free_squares):
    numbers = [number for number in range(1, MAXNUMBER + 1)]
    if interferring_numbers_in_bound:
        to_fill_up = give_to_fill_up(interferring_numbers_in_bound)
        numbers = list(filter(lambda number : (min(interferring_numbers_in_bound) - free_squares + to_fill_up <= number\
            and number <= max(interferring_numbers_in_bound) + free_squares - to_fill_up), numbers))

    if interferring_numbers:
        numbers = list(filter(lambda number : (number not in interferring_numbers), numbers))

    return numbers
    

def solve(straights, x , y):
    if y >= MAXNUMBER:
        return straights, True

    if straights[y][x] != 'e':
        if x == 8:
            return solve(straights, 0, y + 1)
        return solve(straights, x + 1, y)
    

    interferring_numbers_h, interferring_numbers_in_bound_h, free_squares_h = give_interferring_in_bounds_and_freesquares_h(straights, x, y)
    #for the square itself
    free_squares_h += 1
    possible_numbers_h = give_possible_numbers(interferring_numbers_h, interferring_numbers_in_bound_h, free_squares_h)

    interferring_numbers_v, interferring_numbers_in_bound_v, free_squares_v = give_interferring_in_bound_and_freesquares_v(straights, x, y)
    #for the square itself
    free_squares_v += 1
    possible_numbers_v = give_possible_numbers(interferring_numbers_v, interferring_numbers_in_bound_v, free_squares_v)

    possible_numbers = [number for number in range(1, MAXNUMBER + 1)\
        if number in possible_numbers_h and number in possible_numbers_v]

    for number in possible_numbers:
        temp = straights[y][x]
        straights[y][x] = str(number)

        if x == 8:
            straights, possible = solve(straights, 0, y  + 1)
            if possible:
                return straights, True
            straights[y][x] = temp

        else:
            straights, possible = solve(straights, x + 1, y)
            if possible:
                return straights, True
            straights[y][x] = temp

    return straights, False 

def give_hints(straights):
    print('"exit" to exit the programm.')
    print('"solution" to see the solution.')
    print('A number from 1 to 9 as koordinates to get the content.')
    print('For example "3 5" shows the content of the square in columm 3 and row 5.')
    while True:
        message = input('Enter a message\n')
        if message == 'exit':
            sys.exit(0)

        elif message == 'solution':
            return

        else:
            message = message.split()
            if len(message) != 2:
                print('There must be two koordinates.')
                continue
            
            elif not message[0].isdigit() and not message[1].isdigit():
                print('Koodinates have to be numbers.')
                continue

            elif not 1 <= int(message[0]) <= 9 and not 1 <= int(message[0]) <= 9:
                print('Koordinates have to be from 1 to 9.')
                continue
            
            else:
                print(f'\nsquare in row: {message[1]} and columm: {message[0]}')
                print(f'\t{straights[int(message[1]) - 1][int(message[0]) - 1]}\n')

def print_straights(straights):
        for line in straights:

            print('-------------------------------------')

            print('|', end='')
            for square in line:
                if len(square) == 1:
                    print(f' {square} |', end='')
                else:
                    print(f' {square}|', end='')
            print() 

        print('-------------------------------------')

def print_STRAIGHTS():
    print(Fore.BLUE + '      +---------------------+')
    print(            '      |       STRAIGHTS     |')
    print(Fore.BLUE + '      +---------------------+\n')

def main():
    assert len(sys.argv) <= 3, f'The programm takes one argument, the input file. {len(sys.argv) - 1} where given.'
    with open(sys.argv[1], 'r') as file:
        straights = read_straights(file)

    valid, x, y = is_valid(straights)
    assert valid, f'A number is conflicting with the number in row: {y} and columm: {x}.'

    solved_straights, possible = solve(straights, 0, 0)


    if possible:
        if len(sys.argv) == 3 and sys.argv[2] == '-h':
            give_hints(straights)

        print_STRAIGHTS()
        print_straights(solved_straights)

    else: 
        print('not solveable')

if __name__ == "__main__":
    main()