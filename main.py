
import curses
from src.cur_tools import cur_tools
import sys

# Main curses app


def myapp(scr):
    s = cur_tools.curses_init(scr)

    myops = {"File": ["Open", "Close", "Exit"],
             "Edit": ["Copy", "Paste", "Options"],
             "View": ["As PDF", "As TXT"],
             "Help": ["About"]}

    m, mm = cur_tools.curses_horizontal_menu(s, myops)
    cur_tools.curses_status_bar(s, f'Opcion: ({m} , {mm})')

    # Option branch.
    if m == 1 and s == 1:
        cur_tools.curses_info_win(s, "Open")
    else:
        cur_tools.curses_info_win(s, "Not detected")


# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)

sys.exit(0)
