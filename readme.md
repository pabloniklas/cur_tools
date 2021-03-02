# pyCursesMenu
By Pablo Niklas 

## Introduction

The idea behind this library is to provide a menu bar (DOS style).

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
```

### Example


```python
def myapp(scr):
    s = curses_init(scr)

    myops = {"File": ["Open", "Close", "Exit"],
             "Edit": ["Copy", "Paste", "Options"],
             "View": ["As PDF", "As TXT"],
             "Help": ["About"]}

    ch = curses_horizontal_menu(s, myops)
    curses_status_bar(s, f'Opcion: {ch}')
    sys.stdin.read(1)


# Python's entry point
if __name__ == '__main__':
    curses.wrapper(myapp)
```

