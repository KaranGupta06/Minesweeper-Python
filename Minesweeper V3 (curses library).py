from random import sample
import curses                               #if on windows, install windows-curses
from curses.textpad import rectangle        #used for terminal formatting

print("Minesweeper!\n\nZ or spacebar: reveal\nX: Flag\n")

mines_input = int(input("Number of mines -"))
l = int(input("Length -"))                  #length of grid
b = int(input("Breadth -"))                 #breadth of grid

cont = "y"
colours = {"1":1, "2":2, "3":3, "4":4, "5":4, "6":4, "7":4, "8":4, "⚑":11, "o":12, "\u2800":12, "\u272e":13}

stdscr = curses.initscr()

curses.noecho()
curses.curs_set(0)
stdscr.keypad(1)

curses.start_color()
curses.init_pair(1,curses.COLOR_CYAN,curses.COLOR_BLACK)
curses.init_pair(2,curses.COLOR_GREEN,curses.COLOR_BLACK)
curses.init_pair(3,curses.COLOR_YELLOW,curses.COLOR_BLACK)
curses.init_pair(4,curses.COLOR_MAGENTA,curses.COLOR_BLACK)
curses.init_pair(11,curses.COLOR_RED,curses.COLOR_BLACK)
curses.init_pair(12,curses.COLOR_WHITE,curses.COLOR_BLACK)
curses.init_pair(13,curses.COLOR_BLACK,curses.COLOR_RED)

def spawn():
    stdscr.clear()
    stdscr.addstr(b+2,0,f"Mines : {mines_input-overlay.count(2)}")
    rectangle(stdscr,0,0,b+1,l*2)

    for i,f,g in zip(range(l*b),blocks,overlay):

        if   g == 2:   element = "⚑"        #flag
        elif g == 1:   element = "o"        #hidden
        elif f == 0:   element = "\u2800"   #shown but 0
        elif f == "M": element = "\u272e"   #hit mine
        else:          element = str(f)     #numbers

        if x == i//l and y == i%l:
            stdscr.addstr(i//l+1,(i%l)*2+1, element, curses.color_pair(colours[element]) | curses.A_STANDOUT)
        else:
            stdscr.addstr(i//l+1,(i%l)*2+1, element, curses.color_pair(colours[element]))
        
    stdscr.refresh()

def init():

    for i in range(l*b):
        cord = refBlocks[i//l][i%l]
        if i in mines:
            blocks.append('M')          #placeholder for mine
        else:                           #calculate mines around square
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

    # OVERLAY 0::shown 1::hidden 2::flag

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

    match stdscr.getch():
        case 450:        #up
            if x!=0: x-=1
        case 456:        #down
            if x!=b-1: x+=1
        case 452:        #left
            if y!=0: y-=1
        case 454:        #right
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

while cont == "y": #main loop

    overlay = [1 for _ in range(l*b)]
    blocks, mines = [], sorted(sample([i for i in range(l*b)],mines_input))
    refBlocks = [[i+f for i in range(l)] for f in range(b)]
    x = y = 0

    init()
    spawn()

    while True: #game loop
        
        get_input()
        spawn()
        
        if sorted([i for i in range(l*b) if overlay[i]!=0]) == mines:
            stdscr.addstr(b+3,l//2+1,"VICTORY",curses.color_pair(2)|curses.A_BOLD)
            break
        elif len([i for i in range(l*b) if overlay[i] == 0 and i in mines]):
            stdscr.addstr(b+3,l//2+1,"GAME OVER",curses.color_pair(11)|curses.A_BOLD)
            break

    stdscr.addstr(b+4,l//2-1,"Play Again? (y/n)")
    stdscr.refresh()
    
    if chr(stdscr.getch()) == "y": continue
    break

curses.endwin()
