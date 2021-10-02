#!/usr/bin/python3
#
# CurTools
#
# By Pablo Niklas <pablo _dot_ niklas _at_ gmail _dot_ com>
#

import curses
import platform
import sys
import re
from curses import ascii

#from var_dump import var_dump


def curses_init(scr: object) -> object:
    curses.initscr()
    curses.cbreak()
    curses.noecho()
    scr.keypad(True)

    # Defino los pares de colores
    curses.start_color()
    curses.init_pair(1, curses.COLOR_YELLOW, curses.COLOR_BLUE)  # Pantalla
    # Para ventanas fondo
    curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # Para ventanas titulo
    curses.init_pair(3, curses.COLOR_RED, curses.COLOR_WHITE)

    scr.bkgd(curses.color_pair(1))
    scr.clear()
    scr.bkgdset(' ')
    scr.bkgd(curses.color_pair(1))
    scr.refresh()

    return scr


def curses_end():
    curses.endwin()


def curses_info_win(s, txt):
    mh, mw = s.getmaxyx()
    w = len(txt) + 6

    if w < 30:
        w = 30

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)
    wininfo = curses_initwin(h, w, wx, wy, "INFO")
    wininfo.addstr(3, 3, txt)
    wininfo.getch()
    curses_delwin(wininfo)


def curses_initwin(height, width, wx, wy, title: str = "") -> object:
    w = curses.newwin(height, width, wx, wy)
    w.box()
    w.bkgd(' ', curses.color_pair(2))

    if title != "":
        col = int((width - len(title) - 4) / 2)
        w.addstr(0, col, f'[ {title} ]', curses.A_REVERSE)

    return w


def curses_delwin(w: object):
    w.bkgd(' ', curses.color_pair(1))
    w.erase()
    w.refresh()
    del w


def _curses_menu_hotkey_option(choices: list) -> list:
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
                else:  # Add if not exists.
                    hotkey_list.append([opt, x, opt.find(x)])
                    break

    return hotkey_list


def _test_menu_hotkey_option(choices: list):
    var_dump(_curses_menu_hotkey_option(choices))


def curses_status_bar(stdscr: object, txt: str):
    height, width = stdscr.getmaxyx()

    txt += " "

    stdscr.addstr(height - 1, 0, txt, curses.color_pair(2))
    stdscr.addstr(height - 1, len(txt) - 1, " " *
                  (width - len(txt)), curses.color_pair(2))
    stdscr.refresh()


def curses_vertical_menu(stdscr: object, choices: list, wx, wy) -> int:
    # Finding the max length between the menu options.
    max_length = 0
    for x in choices:
        if len(x) > max_length:
            max_length = len(x)

    # Discovering the hotkeys
    hotkey_list = _curses_menu_hotkey_option(choices)

    # Drawing the window
    window_menu = curses_initwin(len(choices) + 3, max_length + 5, wx, wy)

    # Printing the choices.
    row = 0
    for x in choices:
        window_menu.addstr(row + 2, 1, " " +
                           x.ljust(max_length + 1), curses.color_pair(2))

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
                       hotkey_list[highlight_option][1],
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

        curses_status_bar(stdscr, "STATUS BAR | pressed: {}".format(pressed))

        # getch(): 001000010 = 66
        # curses.KEY_DOWN: 100000010 = 258

        if pressed == 66:  # curses.KEY_DOWN:
            window_menu.addstr(highlight_option + 2, 1, " " +
                               choices[highlight_option].ljust(max_length + 1), curses.color_pair(2))

            window_menu.addstr(highlight_option + 2,
                               hotkey_list[highlight_option][2] + 2,
                               hotkey_list[highlight_option][1],
                               curses.color_pair(3))

            highlight_option += 1

            if highlight_option >= len(choices) - 1:
                highlight_option = len(choices) - 1

        # getch(): 001000001 = 65
        # curses.KEY_UP: 100000011 = 259

        if pressed == 65:  # curses.KEY_UP:
            window_menu.addstr(highlight_option + 2, 1, " " +
                               choices[highlight_option].ljust(max_length + 1), curses.color_pair(2))

            window_menu.addstr(highlight_option + 2,
                               hotkey_list[highlight_option][2] + 2,
                               hotkey_list[highlight_option][1],
                               curses.color_pair(3))

            highlight_option -= 1

            if highlight_option < 0:
                highlight_option = 0

        # Draw new option
        window_menu.addstr(highlight_option + 2, 1, " " +
                           choices[highlight_option].ljust(max_length + 1), curses.color_pair(1))

        window_menu.addstr(highlight_option + 2,
                           hotkey_list[highlight_option][2] + 2,
                           hotkey_list[highlight_option][1],
                           curses.color_pair(3))

        window_menu.refresh()
        pressed = window_menu.getch()

    curses_delwin(window_menu)

    if pressed == 67:
        return -10
    elif pressed == 68:
        return -11
    else:
        return highlight_option + 1


def _search_in_list(list: list, item) -> int:

    x = -1

    try:
        x = list.index(item.lower())
    except ValueError:
        pass

    try:
        x = list.index(item.upper())
    except ValueError:
        pass

    return x


def curses_horizontal_menu(stdscr: object, options_dict: dict):
    menubar_options = []

    for k in options_dict:
        menubar_options.append(k)

    height, width = stdscr.getmaxyx()

    list_cols = []
    col = 0
    list_cols.append(col)

    # Drawing the bar
    curses_status_bar(stdscr, " MenuBar DEMO | Make your choice ==)")
    hotkey_list = _curses_menu_hotkey_option(menubar_options)
    idx = 0
    for opc in menubar_options:
        stdscr.addstr(0, col, " " + opc + " ", curses.color_pair(2))
        stdscr.addstr(
            0, col + hotkey_list[idx][2] + 1, hotkey_list[idx][1], curses.color_pair(3))

        col += len(opc) + 2
        idx += 1
        list_cols.append(col)

    stdscr.addstr(0, col, " " * (width - col), curses.color_pair(2))
    stdscr.refresh()

    # Creating a new list to keep the code simple
    hotkeys = []
    for h in hotkey_list:
        hotkeys.append(h[1])

    submenu_choice = -1

    # Main cycle
    key = stdscr.getkey()

    curses_status_bar(stdscr, "KEY == "+str(key))  # DEBUG

    if _search_in_list(hotkey_list, key) != -1:
        idx = hotkeys.index(key)

        _idx = menubar_options[idx]

        curses_status_bar(stdscr, "** ENTRE **")  # DEBUG

        submenu_options = options_dict[_idx]
        submenu_choice = curses_vertical_menu(
            stdscr, submenu_options, 1, list_cols[idx])

        while (submenu_choice == -10) or (submenu_choice == -11) or (submenu_choice == -1):

            # Going to the right
            if submenu_choice == -10:
                if idx < len(menubar_options) - 1:
                    idx += 1

            # Going to the left
            elif submenu_choice == -11:
                if idx > 0:
                    idx -= 1

            key = stdscr.getkey()
            if any(key in i for i in hotkey_list):
                try:
                    idx = hotkeys.index(key)
                except ValueError:
                    pass

            submenu_options = options_dict[menubar_options[idx]]
            submenu_choice = curses_vertical_menu(
                stdscr, submenu_options, 1, list_cols[idx])

    return idx + 1, submenu_choice
