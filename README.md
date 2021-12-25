Straisol

License: MIT
Creator: Andreas Mühlmann
Also on Github for latest changes: https://github.com/AndreasMuehlmann/straisol

Straisol is a programm to solve a straights riddle or to give you hints while solving one. If you don't know what straights is or how it works,
look here: https://de.wikipedia.org/wiki/Str8ts

Quickstart:
    - Make a riddle to be solved:
	- Create a new file.
        - Type the riddle that you want to have solved into the file.
        - one line is one row.
        - seperate the columms by spaces
        - Every square can contain an "e" for an empty square,
           a "." for a blocked square,
           a "." with a number from 1 to 9 behind it for a blocked square with a number in it and
           a number from 1 to 9 for a number.
        - The file has to be in the same directory as the programm

    Example:
    e 3 e . e e e e e 
    e e e 4 e e e 2 e 
    e . e e e e e . e 
    e e e . e e e e e 
    . e e . e e e e e 
    e e e . . e e e e 
    . e e 5 e e e e e 
    e e 3 . e e e e . 
    e 2 e e e e . 8 e 

    -open a terminal and make sure your in the directory of the programm
    -run the programm by typing ".\straisol.exe <filename>" into the terminal
    -to get hints run the programm with ".\straisol.exe <filename> -h"