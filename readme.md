# cur_tools
By Pablo Niklas 

<img src=https://img.shields.io/github/license/pabloniklas/CurTools> <img src=https://img.shields.io/github/v/release/pabloniklas/CurTools> <img src=https://img.shields.io/github/languages/top/pabloniklas/CurTools> <img src=https://img.shields.io/github/downloads/pabloniklas/cur_tools/total>


![Demo](https://raw.githubusercontent.com/pabloniklas/pyCursesMenu/main/screenshots/demo.gif "demo")

## Introduction

The idea behind this library is to provide DOS like interface using curses.

## Prerequisites

*  curses package

## Functions

### curses_info_win()

A simple information window.

#### Usage

```python
curses_info_win(screen, txt)
```

*  screen: curses's screen object
*  txt: text to be displayed.

#### Screenshot

![Windows](https://raw.githubusercontent.com/pabloniklas/pyCursesMenu/main/screenshots/windows.png "window")


### curses_horizontal_menu()

It creates a horizontal menu bar.

#### Screnshots

![Menu](https://raw.githubusercontent.com/pabloniklas/pyCursesMenu/main/screenshots/static_menu01.png "Menu bar")

with submenus

![Menu](https://raw.githubusercontent.com/pabloniklas/pyCursesMenu/main/screenshots/static_menu02.png "Submenu")

#### Usage

```python
ops = {
    "Menu Option 1": [
        ["Submenu option 1", "Submenu option 1 status bar help"],
        ["Submenu option 2", "Submenu option 2 status bar help"]
    ],
    "Menu Option 2": [
        ["Submenu option 3" "Submenu option 1 status bar help"]
    ]
}

user_choice = pyCurses.menu_bar(s, myops)
```

#### Example

```python
import curses
from src.cur_tools import cur_tools
import sys


def myapp(scr):
    s = cur_tools.curses_init(scr)

    myops = {
        "File": [
            ["Exit", "Exit this demo."]
        ],
        "Demos": [
            ["Browse", "Database browsing demo."],
            ["Demo 2", "Demo 2"],
            ["Demo 3", "Demo 3"]
        ],
        "Help": [
            ["About", "About this app."]
        ]
    }

    ch = cur_tools.menu_bar(s, myops)
    cur_tools.status_bar(s, f'Opcion: {ch}')
    sys.stdin.read(1)


# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)
```

## License

MIT

