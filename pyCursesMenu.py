#!/usr/bin/python3
#
# pyCursesMenu
#
# By Pablo Niklas <pablo _dot_ niklas _at_ gmail _dot_ com>
#

import curses
from curses import ascii
from var_dump import var_dump
# import string
import sys, platform


def curses_init(scr: object) -> object:
    curses.initscr()
    curses.cbreak()
    curses.noecho()
    scr.keypad(True)

    # Defino los pares de colores
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # Pantalla
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Para ventanas fondo
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)  # Para ventanas titulo

    scr.bkgd(curses.color_pair(1))
    scr.clear()
    scr.bkgdset(' ')
    scr.bkgd(curses.color_pair(1))
    scr.refresh()

    return scr


def curses_end():
    curses.endwin()


def menu_hotkey_option(choices: list) -> list:
    hotkey_list = []

    # Walking the choices list.
    for opt in choices:

        # Walking the string
        for x in opt:

            # Empty list => I've just add.
            if len(hotkey_list) == 0:
                hotkey_list.append([opt, x, opt.find(x)])
                break
            else:
                # Stackoverflow to the rescue.
                # https://stackoverflow.com/questions/13728023/check-if-a-sublist-contains-an-item
                if any(x in i for i in hotkey_list):
                    continue
                else:  # Add if not exist.
                    hotkey_list.append([opt, x, opt.find(x)])
                    break

    return hotkey_list


def test_menu_hotkey_option(choices: list):
    var_dump(menu_hotkey_option(choices))


def status_bar(stdscr: object, txt: str):
    height, width = stdscr.getmaxyx()

    stdscr.addstr(height - 1, 0, txt, curses.color_pair(2))
    stdscr.addstr(height - 1, len(txt), " " * (width - len(txt) - 1), curses.color_pair(2))
    stdscr.refresh()


def menu_vertical(stdscr: object, choices: list, wx, wy) -> int:

    # Finding the max length between the menu options.
    max_length = 0
    for x in choices:
        if len(x) > max_length:
            max_length = len(x)

    # Discovering the hotkeys
    hotkey_list = menu_hotkey_option(choices)

    # Drawing the window
    window_menu = curses.newwin(len(choices) + 3, max_length + 5, wx, wy)
    window_menu.box()
    # rectangle(window_menu, 0, 0, len(choices) + 2, max_length + 3)
    window_menu.bkgd(' ', curses.color_pair(2))

    # Printing the choices.
    row = 0
    for x in choices:
        window_menu.addstr(row + 2, 1, " " + x.ljust(max_length + 1), curses.color_pair(2))

        window_menu.addstr(row + 2,
                           hotkey_list[row][2] + 2,
                           x[hotkey_list[row][2]:hotkey_list[row][2] + 1],
                           curses.color_pair(3))
        row += 1

    window_menu.refresh()

    # Submenu main cycle.
    highlight_option = 0
    window_menu.addstr(highlight_option + 2, 1, " " +
                       choices[highlight_option].ljust(max_length + 1), curses.color_pair(1))

    window_menu.addstr(highlight_option + 2,
                       hotkey_list[highlight_option][2] + 2,
                       choices[highlight_option][hotkey_list[highlight_option][2]:hotkey_list[highlight_option][2] + 1],
                       curses.color_pair(3))

    # Portability
    if platform.system() == 'Darwin':
        ENTER = curses.ascii.LF
    elif platform.system() == 'Windows':
        ENTER = curses.ascii.CR

    pressed = window_menu.getch()
    while pressed != 67 and \
            pressed != 68 and \
            pressed != ENTER:

        status_bar(stdscr, "Press 'ESC' to exit | STATUS BAR | pressed: {}".format(pressed))

        # 001000010 = 66
        # 100000010 = 258

        if pressed == 66:  # curses.KEY_DOWN:
            window_menu.addstr(highlight_option + 2, 1, " " +
                               choices[highlight_option].ljust(max_length + 1), curses.color_pair(2))

            window_menu.addstr(highlight_option + 2,
                               hotkey_list[highlight_option][2] + 2,
                               choices[highlight_option][
                               hotkey_list[highlight_option][2]:hotkey_list[highlight_option][2] + 1],
                               curses.color_pair(3))

            highlight_option += 1

            if highlight_option >= len(choices) - 1:
                highlight_option = len(choices) - 1

        # 001000001 = 65
        # 100000011 = 259

        if pressed == 65:  # curses.KEY_UP:
            window_menu.addstr(highlight_option + 2, 1, " " +
                               choices[highlight_option].ljust(max_length + 1), curses.color_pair(2))

            window_menu.addstr(highlight_option + 2,
                               hotkey_list[highlight_option][2] + 2,
                               choices[highlight_option][
                               hotkey_list[highlight_option][2]:hotkey_list[highlight_option][2] + 1],
                               curses.color_pair(3))

            highlight_option -= 1

            if highlight_option < 0:
                highlight_option = 0

        # Draw new option
        window_menu.addstr(highlight_option + 2, 1, " " +
                           choices[highlight_option].ljust(max_length + 1), curses.color_pair(1))

        window_menu.addstr(highlight_option + 2,
                           hotkey_list[highlight_option][2] + 2,
                           choices[highlight_option][
                           hotkey_list[highlight_option][2]:hotkey_list[highlight_option][2] + 1],
                           curses.color_pair(3))

        window_menu.refresh()
        pressed = window_menu.getch()

    window_menu.erase()

    return highlight_option + 1

# Main curses app
def myapp(scr):
    s = curses_init(scr)
    myops = ["Abrir", "Grabar", "Cerrar", "Salir"]
    ch = menu_vertical(s, myops, 10, 10)
    status_bar(s, f'Opcion: {ch}')
    sys.stdin.read(1)


# Python entry point
if __name__ == '__main__':
    curses.wrapper(myapp)

sys.exit(0)
