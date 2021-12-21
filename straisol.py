import sys
from colorama import init, Fore, Back, Style

#TODO: make an executable

init(autoreset=True)

MAXNUMBER = 9

def read_straights(file):
    straights = []
    empty_rows = 0
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

            else:
                number = int(straights[y][x])

            interferring_numbers, _ = give_interferring_numbers_and_free_squares(straights, x, y)
            if  number in interferring_numbers:
                return False, y + 1, x + 1

    return True, -1, -1

def give_numbers_horizontal(straights, static_index, search_range):
    numbers = []
    free_squares = 0
    for changing_index in search_range:
        if straights[static_index][changing_index].isdigit():
            numbers.append(int(straights[static_index][changing_index]))

        elif straights[static_index][changing_index] == '.':
            break

        elif len(straights) == 2:
            if straights[static_index][changing_index][1].isdigit():
                numbers.append(int(straights[static_index][changing_index][1]))
            break

        else:
            free_squares += 1

    return numbers, free_squares

def give_numbers_vertical(straights, static_index, search_range):
    numbers = []
    free_squares = 0
    for changing_index in search_range:
        if straights[changing_index][static_index].isdigit():
            numbers.append(int(straights[changing_index][static_index]))

        elif straights[changing_index][static_index] == '.':
            break

        elif len(straights) == 2:
            if straights[changing_index][static_index][1].isdigit():
                numbers.append(int(straights[changing_index][static_index][1]))
            break
        
        else:
            free_squares += 1

    return numbers, free_squares

def give_interferring_numbers_and_free_squares(straights, x, y):
    numbers = set()
    free_squares = 0

    new_numbers, new_free_squares = give_numbers_horizontal(straights, y, range(x + 1, MAXNUMBER, 1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    new_numbers, new_free_squares = give_numbers_horizontal(straights, y, range(x - 1, -1, -1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    new_numbers, new_free_squares = give_numbers_vertical(straights, x, range(y + 1, MAXNUMBER, 1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    new_numbers, new_free_squares = give_numbers_vertical(straights, x, range(y - 1, -1, -1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    #for the square itself
    free_squares += 1

    return numbers, free_squares

def give_possible_numbers(interferring_numbers, free_squares):
    numbers = [i for i in range(1, MAXNUMBER + 1)]
    if not interferring_numbers:
        return numbers
    numbers = filter(lambda number : (min(interferring_numbers) - free_squares <= number <= max(interferring_numbers) + free_squares), numbers)
    numbers = filter(lambda number : (number not in interferring_numbers), numbers)
    return numbers
    

def solve(straights, x , y):
    if y >= MAXNUMBER:
        return straights, True

    if straights[y][x] != 'e':
        if x == 8:
            return solve(straights, 0, y + 1)
        return solve(straights, x + 1, y)

    interferring_numbers, free_squares = give_interferring_numbers_and_free_squares(straights, x, y)
    for number in give_possible_numbers(interferring_numbers, free_squares):
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

def print_frohe_weihnachten():
    print(Fore.RED + '+-------------------------------+')
    print(Fore.RED + '|         FROHE WHEINACHTEN     |')
    print(Fore.RED + '+-------------------------------+\n')

def main():
    assert len(sys.argv) == 2, f'The programm takes one argument, the input file. {len(sys.argv) - 1} where given.'
    with open(sys.argv[1], 'r') as file:
        straights = read_straights(file)

    valid, x, y = is_valid(straights)
    assert valid, f'A number is conflicting with the number in row: {y} and columm: {x}.'

    solved_straights, possible = solve(straights, 0, 0)
    if possible:
        print_frohe_weihnachten()
        print_straights(solved_straights)
    else: 
        print('not solveable')

if __name__ == "__main__":
    main()