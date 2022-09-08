from random import sample
from termcolor import colored as c
from msvcrt import getch
from os import system

# 0::shown 1::hidden 2::flag

def spawn():

    table = [[] for _ in range(5)]
    colours = {1:"cyan",2:"green",3:"yellow",4:"magenta"}

    for f,state in zip(enumerate(blocks),overlay):
        if state == 2:
            table[f[0]//20].append(c("\u2691","red"))                            #flag
        elif state == 1:
            table[f[0]//20].append("o")                                          #hidden
        elif f[1] == 0:
            table[f[0]//20].append(c("\u00B7","grey"))                           #shown but 0
        elif f[1] == "M":
            table[f[0]//20].append(c("\u204E","red","on_red"))                   #hit mine
        else:               
            table[f[0]//20].append(c(f[1],colours[f[1]]) if f[1] in [1,2,3,4] else c(f[1],"blue"))

    table[cord//20][cord%20] = c(table[cord//20][cord%20],on_color="on_white")
    [print(*i) for i in table]
    print(f"Mines:",inp-overlay.count(2))
def init():
    for i in range(100):
        cord = refBlocks[i//20][i%20]

        if i in mines:
            blocks.append('M')
        else: #calculate mines around square
            count = 0
            for g in range(9):
                try:
                    x,y = g//3-1,g%3-1
                    if i+x*20+y in mines and refBlocks[i//20+x][i%20+y] in range(cord-2,cord+3):
                        count+=1
                except: pass
            blocks.append(count)
def round_check(c,reveal):

    element = refBlocks[c//20][c%20]
    flags, zeroElements = 0,[]

    for g in range(9):
        try:
            checking = refBlocks[c//20+g//3-1][c%20+g%3-1]
            pos_grid = c+(g//3-1)*20+(g%3-1)

            if checking in range(element-2,element+3):
                if overlay[pos_grid] == 2:
                    flags+=1
                elif reveal:
                    overlay[pos_grid] = 0
                    if blocks[pos_grid] == 0:
                        zeroElements.append(pos_grid)
        except: pass
    return(zeroElements,flags)
def chain_reveal(a):
    global gameState
    tocheck,checked = [a],[]
    for c in tocheck:
        checked.append(c)
        for i in round_check(c,True)[0]:
            if i not in (checked and tocheck):
                tocheck.append(i)
def get_input():
    global cord, gameState
    match ord(getch()):
        case 72: #up
            if cord not in range(0,20):
                cord-=20
        case 80: #down
            if cord not in range(80,100):
                cord+=20
        case 75: #left
            if cord not in range(0,81,20):
                cord-=1
        case 77: #right
            if cord not in range(19,100,20):
                cord+=1
        case 122|32: #z or spacebar (reveal)
            if overlay[cord] in [0,1]:
                if overlay[cord] == 0 and blocks[cord] == round_check(cord,False)[1]:
                    chain_reveal(cord)
                elif blocks[cord] == 0:
                    chain_reveal(cord)
                overlay[cord] = 0
        case 120: #x (flag)
            if overlay[cord] != 0:
                overlay[cord] = 1 if overlay[cord] == 2 else 2

system("cls") #initiation
print("Minesweeper!\n\nZ or spacebar: reveal\nX: Flag\n\npress any button to continue")
getch(),system('cls')

inp, cont = int(input("Number of mines -")), "y"

while cont == "y": #main loop

    overlay = [1 for _ in range(100)]
    mines = sorted(sample([i for i in range(100)],inp))
    refBlocks = [[i+f for i in range(20)] for f in range(5)]
    cord, gameState, blocks = 0, True, []

    init()

    while gameState: #game loop
        system('cls'); spawn(); get_input()
        if sorted([i for i in range(100) if overlay[i]!=0]) == mines: break
        if len([i for i in range(100) if overlay[i] == 0 and i in mines]): gameState = False
    
    system('cls'); spawn()

    if gameState:
        print("You won!")
        break
    else:
        print("You Lost")
        cont = input("Try again? (y|n)-")
