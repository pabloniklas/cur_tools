#!/usr/bin/env python3
#
# CurTools
#
# By Pablo Niklas <pablo _dot_ niklas _at_ gmail _dot_ com>
#

import curses
from curses import ascii
# import time
import string

from var_dump import var_dump

_STATUSBAR_PREFIX = " MenuBar DEMO | "

# Color pair constants. Curses doesn't have them =(
_PAIR_SCREEN_BG = 1

_PAIR_WINDOW_BG = 2
_PAIR_WINDOW_TITLE = 3
_PAIR_WINDOW_SHADOW = 4

_PAIR_ITEM_SELECTED = 5
_PAIR_HOTKEY_SELECTED = 6
_PAIR_HOTKEY_UNSELECTED = 7
_PAIR_ITEM_UNSELECTED = 8


def curses_init(scr: curses) -> curses:
    """Initialize curses.

    Args:
        scr (curses): Curses screen object.

    Returns:
        curses: Curses screen object.
    """
    curses.initscr()
    curses.cbreak()
    curses.noecho()
    curses.curs_set(0)  # make cursor invisible

    scr.keypad(True)

    # Defining color pairs
    curses.start_color()

    # Screen
    curses.init_pair(_PAIR_SCREEN_BG, curses.COLOR_YELLOW, curses.COLOR_BLUE)

    # Windows BG
    curses.init_pair(_PAIR_WINDOW_BG, curses.COLOR_BLACK, curses.COLOR_WHITE)

    # Window shadow
    curses.init_pair(_PAIR_WINDOW_SHADOW, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Window title
    curses.init_pair(_PAIR_WINDOW_TITLE, curses.COLOR_RED, curses.COLOR_WHITE)

    # Menu Items
    curses.init_pair(_PAIR_ITEM_SELECTED, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(_PAIR_ITEM_UNSELECTED, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(_PAIR_HOTKEY_SELECTED, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(_PAIR_HOTKEY_UNSELECTED, curses.COLOR_RED, curses.COLOR_WHITE)

    scr.bkgd(curses.color_pair(_PAIR_SCREEN_BG))
    scr.clear()
    scr.bkgdset(' ')
    scr.bkgd(curses.color_pair(_PAIR_SCREEN_BG))
    scr.refresh()

    return scr


def curses_end():
    """Ends curses environment"""
    curses.endwin()


def info_win(s: curses, txt: string):
    """Creates an info window

    Args:
        s (curses) : Curses scrren object.
        txt (string) : Text to be displayed.

    """
    mh, mw = s.getmaxyx()
    w = len(txt) + 6

    if w < 30:
        w = 30

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)
    wininfo = init_win(h, w, wx, wy, "INFO")
    wininfo.addstr(3, 3, txt)
    wininfo.getch()
    del_win(wininfo)


def init_win(height: int, width: int, wx: int, wy: int, title: str = "", border_type: int = 0):
    """Creates a windows dialog.

    Args:
        height (int): Window height.
        width (int): Windows width.
        wx (int): x coor.
        wy (int): y coor.
        title (string): Title (could be empty).
        border_type (int): 0 for simple border, 1 for double border. Other values are ignored.

    Returns:
        curses: Curses screen object.
    """

    w = curses.newwin(height, width, wx, wy)

    if border_type == 0:
        w.box()
    else:
        """
        ls - left side,
        rs - right side,
        ts - top side,
        bs - bottom side,
        tl - top left-hand corner,
        tr - top right-hand corner,
        bl - bottom left-hand corner, and
        br - bottom right-hand corner. 
        """
        w.border(chr(186), chr(186), chr(186), chr(186), chr(201), chr(187), chr(200), chr(188))

    w.bkgd(' ', curses.color_pair(_PAIR_WINDOW_BG))

    # Shadow
    # https://stackoverflow.com/questions/17096352/ncurses-shadow-of-a-window
    # w.attron(PAIR_WINDOW_SHADOW)
    #
    # for i in range(wy + 2, wy + width + 1):
    #     w.move((wx + height), i)
    #     w.addch(' ')
    #
    # for i in range(wx + 1, wx + height + 1):
    #     w.move(i, (wy + width))
    #     w.addch(' ')
    #     w.move(i, (wy + width + 1))
    #     w.addch(' ')

    w.attroff(_PAIR_WINDOW_SHADOW)

    if title != "":
        col = int((width - len(title) - 4) / 2)
        w.addstr(0, col, f'[ {title} ]', curses.A_REVERSE)

    return w


def del_win(w: curses):
    """Closes a curses window.

    Args:
        w (curses): curses window object.
    """
    w.bkgd(' ', curses.color_pair(_PAIR_SCREEN_BG))
    w.erase()
    w.refresh()
    del w


def _curses_menu_hotkey_option(choices: list) -> list:
    """INTERNAL - Given a list of options, returns a list of the hotkeys for every option. 

    Args:
        choices (list): The list of choices.

    Returns:
        list: The list of hotkeys for every option.
    """
    hotkey_list = []

    # Walking the choices list.
    for opt in choices:

        # Walking the string
        for x in opt[0]:

            # Empty list => I've just add.
            if len(hotkey_list) == 0:
                hotkey_list.append([opt[0], x, opt[0].find(x)])
                break
            else:
                # Stackoverflow to the rescue.
                # https://stackoverflow.com/questions/13728023/check-if-a-sublist-contains-an-item
                if any(x in i for i in hotkey_list):
                    continue
                else:  # Add if not exists.
                    hotkey_list.append([opt[0], x, opt[0].find(x)])
                    break

    return hotkey_list


def status_bar(stdscr: curses, intxt: str):
    """Creates a status bar for informational purposes.

    Args:
        stdscr (curses): Curses screen object.
        intxt (str): Text to be displayed.
    """
    height, width = stdscr.getmaxyx()

    txt = _STATUSBAR_PREFIX

    # Case dictionary
    switcher = {
        13: ">ENTER<"
    }

    for c in intxt:
        if c in string.printable:
            txt += c
        else:
            asc = ord(c)
            txt += switcher.get(asc, f"ASCII not found ==> {asc}")

    txt += " "

    stdscr.addstr(height - 1, 0, txt, curses.color_pair(_PAIR_WINDOW_BG))
    stdscr.addstr(height - 1, len(txt) - 1, " " *
                  (width - len(txt)), curses.color_pair(_PAIR_WINDOW_BG))
    stdscr.refresh()


def curses_vertical_menu(stdscr: curses, choices: list, wx: int, wy: int) -> int:
    """Creates a vertical menu of options, allowing the user to choose between them.

    Args:
        stdscr (curses): Curses screen object.
        choices (list): List of choices.
        wx (int): x coor.
        wy (int): y coor.

    Returns:
        int: The index of the choice that has been choosen.
    """

    # Finding the max length between the menu options.
    max_length = 0
    for x in choices:
        if len(x[0]) > max_length:
            max_length = len(x[0])

    # Discovering the hotkeys
    hotkey_list = _curses_menu_hotkey_option(choices)

    # Drawing the window
    window_menu = init_win(len(choices) + 3, max_length + 5, wx, wy)

    # Printing the choices of the submenu
    row = 0
    for x in choices:

        # First option selected
        if row == 0:
            window_menu.addstr(row + 2, 1, " " +
                               x[0].ljust(max_length + 1), curses.color_pair(_PAIR_ITEM_SELECTED))

            window_menu.addstr(row + 2,
                               hotkey_list[row][2] + 2,
                               x[0][hotkey_list[row][2]:hotkey_list[row][2] + 1],
                               curses.color_pair(_PAIR_HOTKEY_SELECTED))
        else:
            window_menu.addstr(row + 2, 1, " " +
                               x[0].ljust(max_length + 1), curses.color_pair(_PAIR_ITEM_UNSELECTED))

            window_menu.addstr(row + 2,
                               hotkey_list[row][2] + 2,
                               x[0][hotkey_list[row][2]:hotkey_list[row][2] + 1],
                               curses.color_pair(_PAIR_HOTKEY_UNSELECTED))

        row += 1

    window_menu.refresh()

    # Submenu main cycle.
    highlight_option = 0
    window_menu.addstr(highlight_option + 2, 1, " " +
                       choices[highlight_option][0].ljust(max_length + 1), curses.color_pair(_PAIR_ITEM_SELECTED))

    window_menu.addstr(highlight_option + 2,
                       hotkey_list[highlight_option][2] + 2,
                       hotkey_list[highlight_option][1],
                       curses.color_pair(_PAIR_HOTKEY_SELECTED))

    status_bar(stdscr, choices[highlight_option][1])

    ENTER = curses.ascii.NL

    pressed = window_menu.getch()
    while pressed != 67 and \
            pressed != 68 and \
            pressed != ENTER:

        # curses_status_bar(stdscr, "STATUS BAR | pressed: {}".format(pressed))

        # getch(): 001000010 = 66
        # curses.KEY_DOWN: 100000010 = 258

        if pressed == 66:  # curses.KEY_DOWN:
            window_menu.addstr(highlight_option + 2, 1, " " +
                               choices[highlight_option][0].ljust(max_length + 1),
                               curses.color_pair(_PAIR_ITEM_UNSELECTED))

            window_menu.addstr(highlight_option + 2,
                               hotkey_list[highlight_option][2] + 2,
                               hotkey_list[highlight_option][1],
                               curses.color_pair(_PAIR_HOTKEY_UNSELECTED))

            status_bar(stdscr, choices[highlight_option][1])

            highlight_option += 1

            if highlight_option >= len(choices) - 1:
                highlight_option = len(choices) - 1

        # getch(): 001000001 = 65
        # curses.KEY_UP: 100000011 = 259

        if pressed == 65:  # curses.KEY_UP:
            window_menu.addstr(highlight_option + 2, 1, " " +
                               choices[highlight_option][0].ljust(max_length + 1),
                               curses.color_pair(_PAIR_ITEM_UNSELECTED))

            window_menu.addstr(highlight_option + 2,
                               hotkey_list[highlight_option][2] + 2,
                               hotkey_list[highlight_option][1],
                               curses.color_pair(_PAIR_HOTKEY_UNSELECTED))

            status_bar(stdscr, choices[highlight_option][1])

            highlight_option -= 1

            if highlight_option < 0:
                highlight_option = 0

        # Draw the new option
        window_menu.addstr(highlight_option + 2, 1, " " +
                           choices[highlight_option][0].ljust(max_length + 1), curses.color_pair(_PAIR_ITEM_SELECTED))

        status_bar(stdscr, choices[highlight_option][1])

        window_menu.addstr(highlight_option + 2,
                           hotkey_list[highlight_option][2] + 2,
                           hotkey_list[highlight_option][1],
                           curses.color_pair(_PAIR_HOTKEY_SELECTED))

        window_menu.refresh()
        pressed = window_menu.getch()

    del_win(window_menu)

    if pressed == 67:
        return -10
    elif pressed == 68:
        return -11
    else:
        return highlight_option + 1


def _search_in_list(list: list, key: string, idx: int) -> int:
    """INTERNAL - Search a string in a list of arrays.

    Args:
        list (list): The list.
        key (string): The string to be searched in the list.
        idx (int): 

    Returns:
        int: [description]
    """
    x = 0

    for item in list:
        if item[idx] == key.lower() or item[idx] == key.upper():
            return x
        else:
            x = x + 1

    return x


def curses_horizontal_menu(stdscr: curses, options_dict: dict) -> (int, string):
    """Generates the classic menu bar.

    Args:
        stdscr (curses): Curses screen object.
        options_dict (dict): The list of options and suboptions.

    Returns:
        int: index value of the choice of the menu bar,
        int: index value of the choice of the submenu.
    """
    menubar_options = []

    for k in options_dict:
        menubar_options.append(k)

    height, width = stdscr.getmaxyx()

    list_cols = []
    col = 0
    list_cols.append(col)

    # Drawing the bar
    # status_bar(stdscr, " MenuBar DEMO | Make your choice =)")
    hotkey_list = _curses_menu_hotkey_option(menubar_options)
    idx = 0
    for opc in menubar_options:
        stdscr.addstr(0, col, " " + opc + " ", curses.color_pair(_PAIR_WINDOW_BG))
        stdscr.addstr(
            0, col + hotkey_list[idx][2] + 1, hotkey_list[idx][1], curses.color_pair(_PAIR_WINDOW_TITLE))

        col += len(opc) + 2
        idx += 1
        list_cols.append(col)

    stdscr.addstr(0, col, " " * (width - col), curses.color_pair(_PAIR_WINDOW_BG))
    status_bar(stdscr, "Make a choice.")
    stdscr.refresh()

    # Creating a new list to keep the code simple
    hotkeys = []
    for h in hotkey_list:
        hotkeys.append(h[1])

    submenu_choice = -1

    # Main cycle
    key = stdscr.getkey()
    stdscr.nodelay(True)
    if key == chr(27):
        key = stdscr.getkey()
    else:
        key = hotkey_list[0][1]

    stdscr.nodelay(False)

    if _search_in_list(hotkey_list, key, 2) != -1:
        try:
            idx = hotkeys.index(key.upper())
        except ValueError:
            pass

        _idx = menubar_options[idx]

        # Calling the vertical menu
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

            # Enter
            elif submenu_choice >= 0 and submenu_choice < len(submenu_options):
                return idx + 1, submenu_choice

            # Any other key
            elif stdscr.getkey() == chr(27):
                stdscr.nodelay(True)
                key = stdscr.getkey()
                if any(key in i for i in hotkey_list):
                    try:
                        idx = hotkeys.index(key.upper())
                    except ValueError:
                        pass

            submenu_options = options_dict[menubar_options[idx]]
            submenu_choice = curses_vertical_menu(
                stdscr, submenu_options, 1, list_cols[idx])
    else:
        info_win(stdscr, f"Letra '{key}' no encontrada en la lista {hotkey_list}")

    return idx + 1, submenu_choice


def text_justification(text: string, width: int) -> list:
    """Justifity a text inside the desired width.

    Args:
        text (string): Text to be justified
        width (int): Width of the justification.

    Returns:
        list[str]: list of rows for the justied text.
    """
    current_cursor = 0
    list = []

    # Split the text into a list
    while current_cursor < len(text) - 1:

        end_cursor = current_cursor + width - 1
        if end_cursor > len(text) - 1:
            end_cursor = len(text) - 1

        aux = text[current_cursor:end_cursor + 1]

        # Truncate only where a space is detected
        while aux[end_cursor - current_cursor] != " " \
                and end_cursor > current_cursor:  # last space detected
            end_cursor -= 1

        if end_cursor == current_cursor:  # big word detected
            end_cursor = current_cursor + width
            if end_cursor > len(text) - 1:
                end_cursor = len(text) - 1

        aux = text[current_cursor:end_cursor] \
            .strip() \
            .ljust(width)  # up to the last space within width

        list.append(aux)  # up to the last space within width
        current_cursor = end_cursor

    # TODO: Justification

    return list


# TODO: End this function.
def text_browser(title: string, text: string):
    """Browsing text

    Args:
        title (string): Title of thw window.
        text (string): Text to be browsed.
    """

    width = 50
    max_height = 20
    text_list = text_justification(text, width)

    start_idx = 0
    end_idx = start_idx + max_height - 1 - 2

    if end_idx > len(text_list):
        end_idx = len(text_list) - 1

    # Drawing the browser
    w = init_win(max_height, width + 2, 3, 3, title, 0)
    w.attron(curses.A_REVERSE)
    w.move(1, 0 + width + 1)
    w.addch(curses.ACS_UARROW)
    w.move(max_height - 2, 0 + width + 1)
    w.addch(curses.ACS_DARROW)

    w.attron(curses.A_NORMAL)

    for i in range(2,max_height - 2):
        w.move(i, 0 + width + 1)
        w.addch(curses.ACS_CKBOARD)

    # Populating
    row = 2
    for i in range(start_idx, end_idx):
        w.addstr(row, 1, text_list[i], curses.color_pair(_PAIR_WINDOW_BG))
        row += 1

    # TODO: Action keys.
    w.getch()

    # Closing the browser
    del_win(w)
