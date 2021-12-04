#include <stdio.h>
#include <assert.h>

#define RIDDLE_LENGTH 9

char* get_straights(FILE* file);

//TODO: reading a straights is not working properly
/*
int solve(riddle);
int solve_helper(riddle, columm, row);
int is_filled(char*);
int is_possible(char*, int, int);
*/

int main(int argc, char *argv[])
{
    
    assert(argc == 2 && "the file of the riddle has to be given");

    FILE * file = fopen(argv[1], "r") ;
    if(file == NULL) {
      printf("Error in opening file");
      exit(1);
    }

    char* riddle = get_straights(file);

    return 0;
}

char* get_straights(FILE* file)
{
    int size_of_line;
    char c, last;
    char riddle[RIDDLE_LENGTH];
    char line[RIDDLE_LENGTH];
    char blocking_number[2];

    for (int row = 0; row < RIDDLE_LENGTH; ++row)
    {
        size_of_line = 0;
        if (c == EOF)
        {
            printf("not enough expressions were entered");
            exit(1);
        }

        while ((c = fgetc(file)) != EOF)
        {
            if (c == ' '){
                if (last == '.') 
                    line[size_of_line++] = last;
            }

            else if (c == '\t'){
                if (last == '.') 
                    line[size_of_line++] = last;
            }
    
            else if (c <= '9' && c >= '1')
                if (last == '.')
                {
                    blocking_number[0] = last;
                    blocking_number[1] = c;
                    line[size_of_line++] = blocking_number;
                }
                else
                {
                    line[size_of_line++] = c;
                }

            else if (c == '.')
                ;

            else if (c == '\n'){
                if (last == '.'){
                    if (size_of_line != RIDDLE_LENGTH - 1)
                    {
                        printf("in row %d there are %d expressions, %d are needed", row + 1, size_of_line + 1, RIDDLE_LENGTH);
                        exit(1);
                    }
                }
                else if (size_of_line != RIDDLE_LENGTH)
                {
                    printf("in row %d there are %d expressions, %d are needed", row + 1, size_of_line + 1, RIDDLE_LENGTH);
                    exit(1);
                }
                break;
            }
            else
            {
                printf("the character %c is not allowed (allowed: 1-9, . , .1-9", c);
                exit(1);
            }
            last = c;
        }

        if (last == '.')
            line[size_of_line] = last;
        last = '\0';
            
        riddle[row] = *line;
    }
    return *riddle;
}

/*
int solve(riddle)
{
    return solve_helper(riddle, 0, 0);
}

int solve_helper(char *riddle, int columm, int row){

    if (is_filled(riddle[row][columm]))
        int newRiddle, is_solved = solve_helper(riddle, columm + 1, row);

    for (int number = 1; i <= RIDDLE_LENGTH){
        if (is_possible(riddle, number, columm, row))

            if (row == RIDDLE_LENGTH - 1)
                int newRiddle, int is_solved = solve_helper(riddle, 0, row + 1);
                if (is_solved)
                    return newRiddle, true;

            else
                int newRiddle, is_solved = solve_helper(riddle, columm + 1, row);
                if (is_solved)
                    return newRiddle, true;
    }

    if (columm == RIDDLE_LENGTH - 1 && row == RIDDLE_LENGTH - 1 && isdigit(riddle[RIDDLE_LENGTH - 1][RIDDLE_LENGTH - 1]))
        return riddle, true;
}

int is_filled(char * index)
{
    if (index == '.')
        return 0;
    else 
        return 1;
}

int is_possible(riddle, number, columm, row)
{
    
}

int show()
*/