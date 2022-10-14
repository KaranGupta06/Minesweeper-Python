import curses                                       # if on windows, install windows-curses
from curses.textpad import rectangle                # used for terminal formatting
from random import sample

colours = {
    "1": 1, "2": 2, "3": 3,
    "4": 4, "5": 4, "6": 4,
    "7": 4, "8": 4, "o": 12,
    "\u2691": 11, "\u2800": 12, "\u272e": 13
}
difficulty = {
    "easy": [9, 9, 10],
    "medium": [16, 16, 40],
    "hard": [31, 20, 100],
    "carrot": [10, 10, 100]
}

print("""
      -=< MINESWEEPER >=-

    Z/Spacebar :: Reveal
         X     ::  Flag

Select difficulty (hard|medium|easy|custom):""")

if (dif_inp := input(">>> ")) == "custom":
    l, b, mines_input = [int(input(i)) for i in ["\nlength -", "breadth -", "mines -"]]
else:
    l, b, mines_input = difficulty[dif_inp]

stdscr = curses.initscr()
stdscr.keypad(1)
curses.noecho()

curses.start_color()                                #initialising colour pairs
curses.init_pair(1, curses.COLOR_CYAN, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)
curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK)
curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_BLACK)
curses.init_pair(11, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(12, curses.COLOR_WHITE, curses.COLOR_BLACK)
curses.init_pair(13, curses.COLOR_BLACK, curses.COLOR_RED)

def spawn():
    stdscr.clear()
    stdscr.addstr(b + 2, 0, f"Mines : {mines_input - overlay.count(2)}")
    rectangle(stdscr, 0, 0, b + 1, l*2)

    for i, f, g in zip(range(l*b), blocks, overlay):

        if g == 2: element = "\u2691"      #flag
        elif g == 1: element = "o"         #hidden
        elif f == 0: element = "\u2800"    #shown but 0
        elif f == "M": element = "\u272e"  #hit mine
        else: element = str(f)             #numbers

        is_Highlighted = curses.A_STANDOUT if x == i//l and y == i%l else 0
        stdscr.addstr(
            i//l + 1, (i%l)*2 + 1, element,
            curses.color_pair(colours[element]) | is_Highlighted
            )

    stdscr.refresh()

def round_check(c, reveal):

    flags = 0
    for g in range(9):
        x, y = g//3 - 1, g%3 - 1
        pos_grid = c + x*l + y

        if c%l + y in range(l) and c//l + x in range(b):
            if overlay[pos_grid] == 2:
                flags += 1
            elif reveal:                            #recursion based chain reveal
                overlay[pos_grid] = 0
                checked.append(c)
                if blocks[pos_grid] == 0 and pos_grid not in checked:
                    round_check(pos_grid, True)

    return flags

def get_input():
    global x, y
    cord = x*l + y

    match stdscr.getch():
        case 450:               #up
            if x != 0: x-=1
        case 456:               #down
            if x != b-1: x+=1
        case 452:               #left
            if y != 0: y-=1
        case 454:               #right
            if y != l-1: y+=1
        case 122|32:            #z or spacebar (reveal)
            if overlay[cord] != 2:
                if (overlay[cord] == 0 and
                    blocks[cord] == round_check(cord,False) or
                    blocks[cord] == 0):
                        round_check(cord,True)
                overlay[cord] = 0
        case 120: #x (flag)
            if overlay[cord] != 0:
                overlay[cord] = 1 if overlay[cord] == 2 else 2 


try:                                                #screen_size error test
    stdscr.addstr(b + 4, l*2 + 1, "*")
except curses.error:
    raise ValueError("ERROR: please try to resize terminal")
finally:
    curses.endwin()


while True:                                         #main loop

    mines = sorted(sample([i for i in range(l*b)], mines_input))
    overlay = [1 for _ in range(l*b)]               #0 → shown; 1 → hidden; 2 → flag
    blocks  = [0 for _ in range(l*b)]
    checked = []

    for i in range(l*b):                            #initialisation of map
        if i in mines:
            blocks[i] = 'M'                         #placeholder for mine
            for g in range(9):
                x_d, y_d = g//3-1, g%3-1
                if i + x_d*l + y_d not in mines and i%l + y_d in range(l) and i//l + x_d in range(b):
                    blocks[i + x_d*l + y_d] += 1
    x = y = 0
    spawn()

    while True:                                     #game loop

        get_input()
        spawn()

        if sorted([i for i in range(l*b) if overlay[i]!=0]) == mines:
            stdscr.addstr(b + 3, l//2 + 2, "VICTORY", curses.color_pair(2)|curses.A_BOLD)
            break
        elif len([i for i in range(l*b) if overlay[i] == 0 and i in mines]):
            stdscr.addstr(b + 3, l//2 + 2, "GAME OVER", curses.color_pair(11)|curses.A_BOLD)
            break

    stdscr.addstr(b + 4, l//2 - 1, "Play Again? (y/n)")
    stdscr.refresh()
    
    while (play_again := chr(stdscr.getch())) not in ["y", "n"]: pass
    if play_again == "n": break

curses.endwin()
