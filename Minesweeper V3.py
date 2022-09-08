from msvcrt import getch
from os import system
from random import sample
from tabulate import tabulate
from termcolor import colored as c

# 0::shown 1::hidden 2::flag

def spawn():

    table = [[] for _ in range(b)]
    colours = {1:"cyan", 2:"green", 3:"yellow", 4:"magenta"}

    for i,f,state in zip(range(l*b),blocks,overlay):
        if state == 2:
            table[i//l].append(c("\u2691","red"))                            #flag
        elif state == 1:
            table[i//l].append("o")                                          #hidden
        elif f == 0:
            table[i//l].append(c("\u00B7","grey"))                           #shown but 0
        elif f == "M":
            table[i//l].append(c("\u204E","red","on_red"))                   #hit mine
        else:
            table[i//l].append(c(f,colours[f]) if f in [1,2,3,4] else c(f,"blue"))

    table[x][y] = c(table[x][y],on_color="on_white")
    print(f"{tabulate(table)}\n\t\t\b|Mines: {inp-overlay.count(2)}|")

def init():
    for i in range(l*b):

        cord = refBlocks[i//l][i%l]

        if i in mines:
            blocks.append('M')
        else: #calculate mines around square
            count = 0
            for g in range(9):
                try:
                    x,y = g//3-1,g%3-1
                    if i+x*l+y in mines and refBlocks[i//l+x][i%l+y] in range(cord-2,cord+3):
                        count+=1
                except: pass
            blocks.append(count)

def round_check(c,reveal):

    element = refBlocks[c//l][c%l]
    flags, zeroElements = 0,[]

    for g in range(9):
        try:
            checking = refBlocks[c//l+g//3-1][c%l+g%3-1]
            pos_grid = c+(g//3-1)*l+(g%3-1)

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
    global x, y, gameState
    cord = x*l + y

    match ord(getch()):
        case 72:        #up
            if x!=0: x-=1
        case 80:        #down
            if x!=b-1: x+=1
        case 75:        #left
            if y!=0: y-=1
        case 77:        #right
            if y!=l-1: y+=1
        case 122|32:    #z or spacebar (reveal)
            if overlay[cord] != 2:
                if overlay[cord] == 0 and blocks[cord
                    ] == round_check(cord,False)[1] or blocks[cord] == 0:
                        chain_reveal(cord)
                overlay[cord] = 0
        case 120: #x (flag)
            if overlay[cord] != 0:
                overlay[cord] = 1 if overlay[cord] == 2 else 2

system("cls") #initiation
print("Minesweeper!\n\nZ or spacebar: reveal\nX: Flag\n\npress any button to continue")
getch(),system('cls')

inp, cont = int(input("Number of mines -")), "y"
l ,b = int(input("Length -")), int(input("Breadth -"))

while cont == "y": #main loop

    overlay = [1 for _ in range(l*b)]
    mines = sorted(sample([i for i in range(l*b)],inp))
    refBlocks = [[i+f for i in range(l)] for f in range(b)]
    gameState, blocks = True, []
    x = y = 0

    init()

    while gameState: #game loop
        system('cls'); spawn(); get_input()
        if sorted([i for i in range(l*b) if overlay[i]!=0]) == mines: break
        if len([i for i in range(l*b) if overlay[i] == 0 and i in mines]): gameState = False
    
    system('cls'); spawn()
    if gameState:
        print(c("\t\tYou won!","green"))
        break
    else:
        print(c("\t\tGAME OVER","red"))
        cont = input("Try again? (y|n)-")
