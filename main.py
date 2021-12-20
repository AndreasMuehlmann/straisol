from colorama import init, Fore, Back, Style

init(autoreset=True)

#TODO: debug is_possible
#TODO: debug range numbers can be in

MAXNUMBER = 9

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

    #for the square itself
    free_squares -= 1

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

    #for the square itself
    free_squares -= 1

    return numbers, free_squares

def give_interferring_numbers_and_free_squares(straights, x, y):
    numbers = set()
    free_squares = 0

    new_numbers, new_free_squares = give_numbers_horizontal(straights, y, range(x, MAXNUMBER, 1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    new_numbers, new_free_squares = give_numbers_horizontal(straights, y, range(x, -1, -1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    new_numbers, new_free_squares = give_numbers_vertical(straights, x, range(y, MAXNUMBER, 1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    new_numbers, new_free_squares = give_numbers_vertical(straights, x, range(y, -1, -1))
    free_squares += new_free_squares
    numbers.update(new_numbers)

    #for the square itself
    free_squares += 1

    return numbers, free_squares

def give_possible_numbers(interferring_numbers, free_squares):
    numbers = [i for i in range(1, MAXNUMBER + 1)]
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

def write_straights(straights, file):
        for line in straights:

            file.write('-------------------------------------------------------------\n')

            file.write('|')
            for square in line:
                file.write(f'\t{square}\t|')

            file.write('\n') 

        file.write('-------------------------------------------------------------\n')


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

def write_frohe_weihnachten(file):
    file.write('\t\t+-------------------------------------------+\n')
    file.write('\t\t |         FROHE WHEINACHTEN     |\n')
    file.write('\t\t+-------------------------------------------+\n\n')

def print_frohe_weihnachten():
    print(Fore.RED + '+-------------------------------+')
    print(Fore.RED + '|         FROHE WHEINACHTEN     |')
    print(Fore.RED + '+-------------------------------+\n')

def main():
    straights_empty = [
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
    ]

    straights = [
        ["e", "e", "1", "e", "e", "e", "e", "e", "."],
        ["e", "3", "e", "e", "e", "e", "e", "e", "e"],
        ["e", "e", "5", "6", "e", "e", ".", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "5", "e", "e"],
        ["e", "e", "e", ".4", "e", "e", "7", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "2", "e", ".4"],
        ["e", "e", ".", "e", ".", "e", "1", ".", "e"],
        ["e", "e", "9", "e", "e", "e", "6", "e", "e"],
        ["e", "e", "e", "e", "e", "e", "e", "e", "e"],
    ]

    solved_straights, possible = solve(straights, 0, 0)
    if possible:
        print_frohe_weihnachten()
        print_straights(solved_straights)
    else: 
        print('not solveable')

if __name__ == "__main__":
    main()