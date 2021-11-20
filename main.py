#!/usr/bin/env python3
import curses
from src.cur_tools import cur_tools
import sys
import lorem

# Main curses app


def myapp(scr):
    s = cur_tools.curses_init(scr)

    myops = {"File": ["Exit"],
             "Demos": ["Browse", "Demo 2", "Demo 3"],
             "Help": ["About"]}

    m, mm = cur_tools.curses_horizontal_menu(s, myops)

    while m != 1 or mm != 1    :     # File->Exit

        cur_tools.curses_status_bar(s, f'Opcion: ({m} , {mm})')

        # Option branch.
        if m == 2 and mm == 1:
            cur_tools.text_browse(s, lorem.paragraph())
        else:
            cur_tools.info_win(s, "Men at work")

        m, mm = cur_tools.curses_horizontal_menu(s, myops)



# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)

print(" ==== Bye ===== ")
sys.exit(0)
