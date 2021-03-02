# pyCursesMenu
By Pablo Niklas 

## Introduction

The idea behind this library is to provide a menu bar (DOS style).

## Prerequisites

*  curses package

## curses_info_win()

A simple information window.

### Usage

```python
curses_info_win(screen, txt)
```

*  screen: curses's screen object
*  txt: text to be displayed.

## curses_horizontal_menu()

It creates a horizontal menu bar.

### Screnshots

![Menu](https://raw.githubusercontent.com/pabloniklas/pyCursesMenu/main/screenshots/static_menu01.png "Menu bar")

with submenus

![Menu](https://raw.githubusercontent.com/pabloniklas/pyCursesMenu/main/screenshots/static_menu02.png "Submenu")

### Usage

```python
ops = {"Menu Option 1": [ "Submenu option 1", "Submenu option 2"],
       "Menu Option 2": [ "Submenu option 3"]}

user_choice = pyCurses.curses_horizontal_menu(s, myops)
```

### Example

```python
import curses
import cur_tools
import sys


def myapp(scr):
    s = cur_tools.curses_init(scr)

    myops = {"File": ["Open", "Close", "Exit"],
             "Edit": ["Copy", "Paste", "Options"],
             "View": ["As PDF", "As TXT"],
             "Help": ["About"]}

    ch = cur_tools.curses_horizontal_menu(s, myops)
    cur_tools.curses_status_bar(s, f'Opcion: {ch}')
    sys.stdin.read(1)


# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)
```

