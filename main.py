#!/usr/bin/env python3
import curses
from src.cur_tools import cur_tools
import sys


# import lorem
# import sqlite3


def myapp(scr: curses.window):
    """Main Function

    Args:
        scr (curses): Screen curses object.
    """
    s = cur_tools.curses_init(scr)

    myops = {
        "File": [
            ["Exit", "Exit this demo."]
        ],
        "Demos": [
            ["Browse", "Text browsing demo."],
            ["Forms", "Forms demo."],
            ["Demo 3", "Demo 3"]
        ],
        "Help": [
            ["About", "About this app."]
        ]
    }

    cur_tools.status_bar(s, "Press Enter or ALT+KEY to start the demo.")
    m, mm = cur_tools.menu_bar(s, myops)

    while m != 1 or mm != 1:  # File->Exit

        cur_tools.status_bar(s, f'Option: ({m} , {mm})')

        # Option branch.
        if m == 2 and mm == 1:
            file = "sample.txt"
            try:
                file = open(file)
            except FileNotFoundError:
                cur_tools.error_win(s, f"File '{file}' not found")
            else:
                line = file.read().replace("\n", " ")
                cur_tools.text_browser(s,"Browsing demo", line)
                file.close()
        elif m == 2 and mm == 2:
            w = cur_tools.init_win(15, 50, 5, 5, "Form Demo")
            data = cur_tools.simple_input_text_field(s, w, 3, 3, "Nombre", 20, "Text input demo.")
            cur_tools.info_win(w, data)
            cur_tools.end_win(w)

        else:
            cur_tools.info_win(s, ":: Men at work ::")

        m, mm = cur_tools.menu_bar(s, myops)


# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)

print(" ===== Bye ===== ")
sys.exit(0)
