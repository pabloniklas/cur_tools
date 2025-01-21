#!/usr/bin/env python3
import curses
import sys

from modules import cur_tools
from modules import const
import time


# import lorem
# import sqlite3


def myapp(scr: curses.window):
    """Main Function

    Args:
        scr (curses): Screen curses object.
    """
    s = cur_tools.curses_init(scr)

    myops = {
        "File": {
            "Load": {"description": "Load a file."},
            "Save": {"description": "Save a file."},
            "Save As": {"description": "Save a file with a new name."},
            "Exit": {"description": "Exit this demo."}
        },
        "Demos": {
            "Browse": {"description": "Text browsing demo."},
            "Input": {
                "description": "Some input demo.",
                "submenu": {
                    "Normal": {"description": "Normal input demo"},
                    "Password": {"description": "Password input demo"}
                }
            },
            "Bar Chart": {"description": "Bar chart."},
            "Progress Bar": {"description": "A simple progress bar."},
            "Editor": {"description": "A simple text editor."},
            "Forms (WIP)": {"description": "Forms demo"}
        },
        "Help": {
            "About": {"description": "About this app."}
        }
    }

    cur_tools.status_bar(s, "Press Enter or ALT+KEY to start the demo.")
    m, mm = cur_tools.menu_bar(s, myops)

    while m != 1 or mm != 4:  # File->Exit

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
                cur_tools.text_browser(s, "Browsing demo", line)
                file.close()
        elif m == 2 and mm == 102:
            data = cur_tools.input_box(s, "Name", 40, "Enter your name",
                                       const.INPUT_TYPE_ALPHANUMERIC)
            cur_tools.info_win(s, data)
        elif m == 2 and mm == 103:
            data = cur_tools.input_box(s, "Password", 40, "Type your most important password =)",
                                       const.INPUT_TYPE_ALPHANUMERIC, True)
            cur_tools.info_win(s, data)
        elif m == 2 and mm == 3:
            win,sha = cur_tools.init_win(10,40,10,25,"Bar Chart")
            cur_tools.bar_chart(win, [("A", 10), ("B", 20), ("C", 30), ("D", 40), ("E", 50)])
            cur_tools.end_win(win,sha)
        elif m == 2 and mm == 4:
            pbw,pbs=cur_tools.progress_bar_create(s, 100, "Progress Bar")
            for i in range(101):
                cur_tools.progress_bar_update(pbw,i,100)
                time.sleep(100 / 1000)
                
            cur_tools.progress_bar_close(pbw,pbs)
        elif m == 2 and mm == 5:
            cur_tools.simple_text_editor(s, "sample.txt")            
            
        elif m == 2 and mm == 6:
            data = cur_tools.form_win(s, "Form demo", [
                {"label": "Name", "placeholder": "Enter your name", "type": const.INPUT_TYPE_ALPHANUMERIC, "length": 20},
                {"label": "Age", "placeholder": "Enter your age", "type": const.INPUT_TYPE_NUMERIC, "length": 3},
                {"label": "Email", "placeholder": "Enter your email", "type": const.INPUT_TYPE_EMAIL, "length": 30}
            ])

            cur_tools.info_win(s, data)
        elif m == 3 and mm == 1:
            cur_tools.info_win(s, "Demo for cur tools. By Pablo Niklas")
        else:
            cur_tools.info_win(s, ":: Men at work ::")

        m, mm = cur_tools.menu_bar(s, myops)


# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)

print("█▓▒░⡷⠂By TTУs9⠐⢾░▒▓█")
print("[~]")
sys.exit(0)
