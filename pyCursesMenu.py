#!/usr/bin/python3

import curses
from curses.textpad import Textbox, rectangle
from var_dump import var_dump
import string
import sys


def curses_init(scr):
    curses.initscr()
    curses.start_color()
    curses.cbreak()
    curses.noecho()

    # Defino los pares de colores
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # Pantalla
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)  # Para ventanas fondo
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)  # Para ventanas titulo

    scr.bkgd(curses.color_pair(1))
    scr.erase()
    scr.bkgdset(' ')
    scr.bkgd(curses.color_pair(1))


def curses_end():
    curses.endwin()


def menu_hotkey_option(choices: list) -> list:
    hotkey_list = []
    for opt in choices:
        for x in opt:
            if len(hotkey_list) > 0:
                n = 0
                print(f'{n} < {len(hotkey_list)} and {x} != {hotkey_list[n][1]}')
                while n < len(hotkey_list) and x != hotkey_list[n][1]:

                    hotkey_list.append([opt, x, opt.find(x)])

                    n += 1
                break
            else:
                hotkey_list.append([opt, x, opt.find(x)])
                break

    return hotkey_list


def test_menu_hotkey_option(choices):
    var_dump(menu_hotkey_option(choices))


def menu_vertical(choices: list):

    # Finding the max length between the menu options.
    max_length = 0
    for x in choices:
        if len(x) > max_length:
            max_length = len(x)

    # Discovering the hotkeys
    hotkey_dict = menu_hotkey_option(choices)

    # Drawing the window
    window_menu = curses.newwin(len(choices) + 3, max_length + 5, 5, 5)
    rectangle(window_menu, 0, 0, len(choices) + 2, max_length + 3)
    window_menu.bkgd(' ', curses.color_pair(2))

    row = 0
    for x in choices:
        window_menu.addstr(row + 2, 1, " " + x.ljust(max_length + 1), curses.color_pair(2))
        window_menu.addstr(row + 2,
                           hotkey_dict[x][1] + 2,
                           x[hotkey_dict[x][1]:hotkey_dict[x][1] + 1],
                           curses.color_pair(1))
        row += 1

    window_menu.refresh()
    window_menu.getch()


if __name__ == '__main__':
    myops = ["Acerca de", "Creditos", "Ayuda"]
    test_menu_hotkey_option(myops)
    # curses.wrapper(curses_init)
    # menu_vertical(myops)

sys.exit(0)