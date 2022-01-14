#!/usr/bin/env python3
#
# CurTools
#
# By Pablo Niklas <pablo _dot_ niklas _at_ gmail _dot_ com>
#

import curses
import re
import string
import textwrap
from curses import ascii

from typing import List

# from var_dump import var_dump

STATUSBAR_PREFIX = " StatusBar | "

# Color pair constants. Curses doesn't have them =(
_pair_pointer = 1
_PAIR_SCREEN_BG = _pair_pointer

_pair_pointer += 1
_PAIR_WINDOW_BG_LOWER = _pair_pointer
_pair_pointer += 1
_PAIR_WINDOW_BG_UPPER = _pair_pointer

_pair_pointer += 1
_PAIR_WINDOW_TITLE = _pair_pointer

_pair_pointer += 1
_PAIR_INPUT_FIELD = _pair_pointer

_pair_pointer += 1
_PAIR_WINDOW_SHADOW = _pair_pointer

_pair_pointer += 1
_PAIR_WINDOW_HELPER = _pair_pointer

_pair_pointer += 1
_PAIR_ITEM_SELECTED = _pair_pointer
_pair_pointer += 1
_PAIR_HOTKEY_SELECTED = _pair_pointer
_pair_pointer += 1
_PAIR_HOTKEY_UNSELECTED = _pair_pointer
_pair_pointer += 1
_PAIR_ITEM_UNSELECTED = _pair_pointer

_pair_pointer += 1
_PAIR_ERROR_WINDOW = _pair_pointer

# Input types
INPUT_TYPE_ALPHANUMERIC = 0
INPUT_TYPE_NUMERIC = 1
INPUT_TYPE_ALPHABETIC = 2


def curses_init(scr: curses.window) -> curses.window:
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
    curses.init_pair(_PAIR_WINDOW_BG_LOWER, curses.COLOR_BLACK, curses.COLOR_WHITE)
    # curses.init_pair(_PAIR_WINDOW_BG_UPPER, curses.COLOR_WHITE, curses.COLOR_WHITE)

    # Window shadow
    curses.init_pair(_PAIR_WINDOW_SHADOW, curses.COLOR_WHITE, curses.COLOR_BLACK)

    # Window title
    curses.init_pair(_PAIR_WINDOW_TITLE, curses.COLOR_RED, curses.COLOR_WHITE)

    # Input type field
    curses.init_pair(_PAIR_INPUT_FIELD, curses.COLOR_WHITE, curses.COLOR_BLUE)

    # Menu Items
    curses.init_pair(_PAIR_ITEM_SELECTED, curses.COLOR_BLACK, curses.COLOR_GREEN)
    curses.init_pair(_PAIR_ITEM_UNSELECTED, curses.COLOR_BLACK, curses.COLOR_WHITE)
    curses.init_pair(_PAIR_HOTKEY_SELECTED, curses.COLOR_RED, curses.COLOR_GREEN)
    curses.init_pair(_PAIR_HOTKEY_UNSELECTED, curses.COLOR_RED, curses.COLOR_WHITE)

    # Error Windows color
    curses.init_pair(_PAIR_ERROR_WINDOW, curses.COLOR_WHITE, curses.COLOR_RED)

    curses.init_pair(_PAIR_WINDOW_HELPER, curses.COLOR_BLACK, curses.COLOR_GREEN)

    scr.bkgd(curses.color_pair(_PAIR_SCREEN_BG))
    scr.clear()
    scr.bkgdset(' ')
    scr.bkgd(curses.color_pair(_PAIR_SCREEN_BG))
    scr.refresh()

    return scr


def curses_end():
    """Ends curses environment"""
    curses.endwin()


def _popup(s: curses.window, color: curses, title: str, txt: str):
    mh, mw = s.getmaxyx()
    w = len(txt) + 6

    if w < 30:
        w = 30

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)
    wininfo = init_win(h, w, wx, wy, title, color)
    wininfo.addstr(3, 3, txt)
    wininfo.getch()
    end_win(wininfo)


def info_win(s: curses.window, txt: str):
    """Creates an info window

    Args:
        s (curses) : Curses scrren object.
        txt (string) : Text to be displayed.

    """
    color = _PAIR_WINDOW_BG_LOWER
    title = "Info Window"
    _popup(s, color, title, txt)


def error_win(s: curses.window, txt: str):
    """Creates an error window

    Args:
        s (curses) : Curses scrren object.
        txt (string) : Text to be displayed.

    """
    color = _PAIR_ERROR_WINDOW
    title = "Error Window"
    _popup(s, color, title, txt)


def init_win(height: int, width: int, wx: int, wy: int, title: str = "",
             bgcolor: curses = _PAIR_WINDOW_BG_LOWER,
             border_type: int = 0) -> curses.window:
    """Creates a windows dialog.

    Args:
        height (int): Window height.
        width (int): Windows width.
        wx (int): x coor.
        wy (int): y coor.
        title (string): Title (could be empty).
        bgcolor (Curses.color): Background color.
        border_type (int): 0 for simple border, 1 for double border. Other values are ignored.

    Returns:
        curses: Curses screen object.
    """

    w = curses.newwin(height, width, wx, wy)

    if border_type == 0:
        w.box()
        # for x in range(0, width):
        #     w.move(0, x)
        #     w.addch(curses.ACS_HLINE)
        #
        # w.addstr(0, 5, "*",
        #          curses.color_pair(_PAIR_WINDOW_BG_UPPER) | curses.A_BOLD | curses.A_REVERSE)

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
        # w.border(chr(186), chr(186), chr(186), chr(186), chr(201), chr(187), chr(200), chr(188))

    w.bkgd(' ', curses.color_pair(bgcolor))

    # Shadow
    # https://stackoverflow.com/questions/17096352/ncurses-shadow-of-a-window
    # w.attron(_PAIR_WINDOW_SHADOW)
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
    #
    # w.attroff(_PAIR_WINDOW_SHADOW)

    if title != "":
        col = int((width - len(title) - 4) / 2)
        w.addstr(0, col, f'[ {title} ]', curses.A_REVERSE)

    return w


def end_win(w: curses.window):
    """Closes a curses window.

    Args:
        w (curses): curses window object.
    """
    w.bkgd(' ', curses.color_pair(_PAIR_SCREEN_BG))
    w.erase()
    w.refresh()
    del w


def _menu_hotkey_option(choices: List[str]) -> List[str]:
    """INTERNAL - Given a list of options, returns a list of the hotkeys for every option.

    Args:
        choices (List[str]): The list of choices.

    Returns:
        List[str]: The list of hotkeys for every option.
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


def status_bar(stdscr: curses.window, intxt: str):
    """Creates a status bar for informational purposes.

    Args:
        stdscr (curses): Curses screen object.
        intxt (str): Text to be displayed.
    """
    height, width = stdscr.getmaxyx()

    txt = STATUSBAR_PREFIX

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

    stdscr.addstr(height - 1, 0, txt, curses.color_pair(_PAIR_WINDOW_BG_LOWER))
    stdscr.addstr(height - 1, len(txt) - 1, " " *
                  (width - len(txt)), curses.color_pair(_PAIR_WINDOW_BG_LOWER))
    stdscr.refresh()


def _menu_option_refresh(window_menu: curses.window, row: List[int], max_length: int,
                         choice: List[str], hotkey_list: List[str],
                         word_color: int, hotkey_color: int):
    """INTERNAL - Refresh the menu option

    Args:
        window_menu (curses.window): Curses window object.
        row (int): Row number.
        max_length (int): Options max length
        choice [str]: Menu option to be written.
        hotkey_list [str]: Hotkey inside the option.
        word_color (int): Color combination of the option.
        hotkey_color (int): Color combination of the hotkey.

    Returns:
        None.
    """
    window_menu.addstr(row + 1,
                       1,
                       " " + choice[0].ljust(max_length + 1),
                       curses.color_pair(word_color))

    window_menu.addstr(row + 1,
                       hotkey_list[row][2] + 2,
                       choice[0][hotkey_list[row][2]:hotkey_list[row][2] + 1],
                       curses.color_pair(hotkey_color))


def vertical_menu(stdscr: curses.window, choices: List[str], wx: int, wy: int) -> int:
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
    for choice in choices:
        if len(choice[0]) > max_length:
            max_length = len(choice[0])

    max_length += 2

    # Discovering the hotkeys
    hotkey_list = _menu_hotkey_option(choices)

    # Creating a new list to keep the code simple
    hotkeys = []
    for h in hotkey_list:
        hotkeys.append(h[1])

    # Drawing the window
    window_menu: curses.window = init_win(len(choices) + 2, max_length + 4, wx, wy)

    # Printing the choices of the submenu
    row = 0
    for choice in choices:

        parent_choice = choice

        if len(choice) == 3:  # Submenu
            parent_choice[0] = choice[0].ljust(max_length-1)+ ">"

        # First option selected
        if row == 0:
            _menu_option_refresh(window_menu, row, max_length, parent_choice, hotkey_list,
                                 _PAIR_ITEM_SELECTED, _PAIR_HOTKEY_SELECTED)

        else:
            _menu_option_refresh(window_menu, row, max_length, parent_choice, hotkey_list,
                                 _PAIR_ITEM_UNSELECTED, _PAIR_HOTKEY_UNSELECTED)

        row += 1


    window_menu.refresh()

    # Submenu main cycle.
    highlight_option = 0

    _menu_option_refresh(window_menu, highlight_option, max_length,
                         choices[highlight_option],
                         hotkey_list,
                         _PAIR_ITEM_SELECTED, _PAIR_HOTKEY_SELECTED)

    status_bar(stdscr, choices[highlight_option][1])

    pressed = window_menu.getch()
    while pressed != 67 and \
            pressed != 68 and \
            pressed != curses.ascii.NL:

        # Jump to the option if it's hotkey is pressed.
        if chr(pressed).upper() in hotkeys:
            old_highlight_option = highlight_option

            highlight_option = _search_in_list(hotkey_list, chr(pressed), 0) - 1

            _menu_option_refresh(window_menu, old_highlight_option, max_length,
                                 choices[old_highlight_option],
                                 hotkey_list,
                                 _PAIR_ITEM_UNSELECTED, _PAIR_HOTKEY_UNSELECTED)

            status_bar(stdscr, choices[highlight_option][1])

        elif pressed == 66:  # curses.KEY_DOWN:

            _menu_option_refresh(window_menu, highlight_option, max_length,
                                 choices[highlight_option],
                                 hotkey_list,
                                 _PAIR_ITEM_UNSELECTED, _PAIR_HOTKEY_UNSELECTED)

            status_bar(stdscr, choices[highlight_option][1])

            highlight_option += 1

            if highlight_option >= len(choices) - 1:
                highlight_option = 0

        elif pressed == 65:  # curses.KEY_UP:
            _menu_option_refresh(window_menu, highlight_option, max_length,
                                 choices[highlight_option],
                                 hotkey_list,
                                 _PAIR_ITEM_UNSELECTED, _PAIR_HOTKEY_UNSELECTED)

            status_bar(stdscr, choices[highlight_option][1])

            highlight_option -= 1

            if highlight_option < 0:
                highlight_option = len(choices) - 1

        # Draw the new option
        _menu_option_refresh(window_menu, highlight_option, max_length,
                             choices[highlight_option],
                             hotkey_list,
                             _PAIR_ITEM_SELECTED, _PAIR_HOTKEY_SELECTED)

        status_bar(stdscr, choices[highlight_option][1])

        window_menu.refresh()
        pressed = window_menu.getch()

    if pressed == 67:
        end_win(window_menu)
        return -10
    elif pressed == 68:
        end_win(window_menu)
        return -11
    else:
        if len(choices[highlight_option]) == 2:
            end_win(window_menu)
            return highlight_option + 1
        else:   # submenu
            second_choices = choices[highlight_option][2]
            second_choice = vertical_menu(stdscr, second_choices, wx + row - 1,
                                          wy + max_length + 4)
            end_win(window_menu)

            return second_choice


def _search_in_list(my_list: List[str], key: str, idx: int = 0) -> int:
    """INTERNAL - Search a string in a list of arrays.

    Args:
        my_list (list): The list.
        key (string): The string to be searched in the list.
        idx (int):

    Returns:
        int: location of the string.
    """
    x = 0

    for item in my_list:
        if item[idx] == key.lower() or item[idx] == key.upper():
            return x
        else:
            x = x + 1

    return x


def menu_bar(stdscr: curses.window, options_dict: dict) -> tuple:
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
    hotkey_list = _menu_hotkey_option(menubar_options)
    idx = 0
    for opc in menubar_options:
        stdscr.addstr(0, col, " " + opc + " ", curses.color_pair(_PAIR_WINDOW_BG_LOWER))
        stdscr.addstr(
            0, col + hotkey_list[idx][2] + 1, hotkey_list[idx][1], curses.color_pair(_PAIR_WINDOW_TITLE))

        col += len(opc) + 2
        idx += 1
        list_cols.append(col)

    stdscr.addstr(0, col, " " * (width - col), curses.color_pair(_PAIR_WINDOW_BG_LOWER))
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
            idx = 0

        _idx = menubar_options[idx]

        # Calling the vertical menu
        submenu_options = options_dict[_idx]
        submenu_choice = vertical_menu(
            stdscr, submenu_options, 1, list_cols[idx])

        while (submenu_choice == -10) or \
                (submenu_choice == -11) or \
                (submenu_choice == -1):

            # Going to the right
            if submenu_choice == -10:
                if idx < len(menubar_options) - 1:
                    idx += 1

            # Going to the left
            elif submenu_choice == -11:
                if idx > 0:
                    idx -= 1

            # Enter
            elif 0 <= submenu_choice < len(submenu_options):
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
            submenu_choice = vertical_menu(
                stdscr, submenu_options, 1, list_cols[idx])
    else:
        info_win(stdscr, f"Char '{key}' not found in list {hotkey_list}")

    return idx + 1, submenu_choice


def _simple_field_input_type(w: curses.window, input_type: str, field_x: int,
                             field_y: int, cursor_offset: int,
                             length: int, key: curses.ascii, value: str,
                             hidden: bool = False) -> tuple:
    """INTERNAL - Logic behind the input field.

    Args:
        w (curses.window): A curses window object.
        input_type (string): Boolean validation expression
        field_x (int): x coordinate.
        field_y (int): y coordinate.
        cursor_offset: Cursor position inside the field.
        length (int): Field length.
        key (curses.ascii): The key pressed.
        value (string) : The data in the field.
        hidden (bool): If True, print "*" instead of char.

    Returns:
        The tuple [cursor_offset, value]
    """

    w.move(field_x, field_y + cursor_offset)
    if eval(input_type) and cursor_offset < length:
        if hidden:
            w.addch(curses.ACS_BULLET)
        else:
            w.addch(key)
        value += chr(key)
        cursor_offset += 1
    elif key in [ord('\b'), 127,
                 curses.ascii.BS,
                 curses.KEY_BACKSPACE
                 ]:
        value = value[:len(value) - 1]
        if cursor_offset > 0:
            cursor_offset -= 1
            w.move(field_x, field_y + cursor_offset)
            w.addch(" ")

    return cursor_offset, value


def input_box(s: curses.window, label: str,
              length: int, help="", type: int = 0, hidden: bool = False) -> str:
    """Provides a simple input box

    Args:
        s (curses.windows): A curses window object.
        label (string): Field label.
        length (int): Field length.
        help (string): Field help.
        type (int): Field type:
            INPUT_TYPE_ALPHANUMERIC
            INPUT_TYPE_NUMERIC
            INPUT_TYPE_ALPHABETIC
        hidden (bool): True means to hide the chars

    Returns:
        value (string)
    """

    w = length + len(label) + 10

    mh, mw = s.getmaxyx()

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)

    win_input: curses.window = init_win(h, w, wx, wy, "Input Box")

    value = simple_input_text_field(s, win_input, 3, 3, label, length, help, type, hidden)

    end_win(win_input)

    return value


def simple_input_text_field(s: curses.window, w: curses.window, x: int, y: int, label: str,
                            length: int, help="", type: int = 0, hidden: bool = False) -> str:
    """Creates a text field input.

    Args:
        s (curses.window): Curses screen object.
        w (curses.window): Curses window object.
        x (int): row.
        y (int): col.
        label (string): Field label.
        length (int): Length of the input field.
        help (string): Help text.
        type (int): Field type.
            INPUT_TYPE_ALPHANUMERIC
            INPUT_TYPE_NUMERIC
            INPUT_TYPE_ALPHABETIC

    Returns:
        String: The value of the input.
    """

    value = ""

    status_bar(s, help)

    # Label
    w.addstr(x, y, label + ":", curses.color_pair(_PAIR_WINDOW_BG_LOWER))

    # Draw the gap
    field_y = y + len(label) + 2
    field_x = x
    w.addstr(field_x, field_y, ' '.ljust(length + 1), curses.color_pair(_PAIR_INPUT_FIELD))

    # Main cycle.
    curses.curs_set(1)  # make cursor visible
    curses.echo(False)
    w.nodelay(True)
    key = w.getch()
    cursor_offset = 0
    w.move(field_x, field_y + cursor_offset)
    w.attron(curses.color_pair(_PAIR_INPUT_FIELD))

    while key != curses.ascii.NL and key != curses.ascii.ESC:

        bool_expr_type = False
        if type == 0:
            bool_expr_type = "curses.ascii.isalnum(key) or curses.ascii.isblank(key)"
        elif type == 1:
            bool_expr_type = "curses.ascii.isdigit(key)"
        elif type == 2:
            bool_expr_type = "curses.ascii.isalpha(key)"

        w.move(field_x, field_y + cursor_offset)
        cursor_offset, value = _simple_field_input_type(w, bool_expr_type,
                                                        field_x, field_y,
                                                        cursor_offset, length, key, value,
                                                        hidden)
        w.refresh()
        key = w.getch()

        # TODO: Insert

    # Cancel Input when ESC is pressed
    if key == curses.ascii.ESC:
        value = ""

    curses.curs_set(0)  # make cursor invisible
    end_win(w)

    return value


def text_justification(text: str, width: int) -> List[str]:
    """Justifity a text inside the desired width.

    Args:
        text (string): Text to be justified
        width (int): Width of the justification.

    Returns:
        list[str]: list of rows for the justied text.
    """

    current_cursor = 0
    ulist = []

    # Split the text into a list
    while current_cursor < len(text) - 1:

        end_cursor = current_cursor + width - 1
        if end_cursor > len(text) - 1:
            end_cursor = len(text) - 1

        aux = text[current_cursor:end_cursor + 1]

        # Truncate only where a space is detected
        while aux[end_cursor - current_cursor] != " " \
                and end_cursor > current_cursor:  # last line space detected
            end_cursor -= 1

        if end_cursor == current_cursor:  # big word detected
            end_cursor = current_cursor + width
            if end_cursor > len(text) - 1:
                end_cursor = len(text) - 1

        aux = text[current_cursor:end_cursor] \
            .strip() \
            .ljust(width)  # up to the last space within width

        ulist.append(aux)  # up to the last space within width
        current_cursor = end_cursor

    jlist = []
    for uitem in ulist:
        jlist.append(align_string(uitem, width))

    return jlist


def _items_len(thelist) -> int:
    return sum([len(x) for x in thelist])


# https://code.activestate.com/recipes/414870-align-text-string-using-spaces-between-words-to-fi/
def align_string(s: str, width: int, last_paragraph_line: int = 0) -> str:
    """Align string to specified width.

    Args:
        s (str): string
        width (int): width
        last_paragraph_line (int): To indicate if it's the last line.

    Returns:
        Justified line
    """

    # detect and save leading whitespace
    lead_re = re.compile(r'(^\s+)(.*)$')
    m = lead_re.match(s)
    if m is None:
        left, right, w = '', s, width
    else:
        left, right, w = m.group(1), m.group(2), width - len(m.group(1))

    items = right.split()

    # add required space to each words, exclude last item
    for i in range(len(items) - 1):
        items[i] += ' '

    if not last_paragraph_line:
        # number of spaces to add
        left_count = w - _items_len(items)
        while left_count > 0 and len(items) > 1:
            for i in range(len(items) - 1):
                items[i] += ' '
                left_count -= 1
                if left_count < 1:
                    break

    res = left + ''.join(items)
    return res


def align_paragraph(paragraph: List[str], width: int, debug=0) -> List[str]:
    """Align paragraph to a specific width.

    Args:
        paragraph (list): list of lines
        width (int): width
        debug (bool):

    Returns:
        List[str]: List of paragraph lines
    """

    lines = list()
    if type(paragraph) == type(lines):
        lines.extend(paragraph)
    elif type(paragraph) == type(''):
        lines.append(paragraph)
    elif type(paragraph) == type(tuple()):
        lines.extend(list(paragraph))
    else:
        raise TypeError('Unsopported paragraph type: %r' % type(paragraph))

    flatten_para = ' '.join(lines)

    splitted = textwrap.wrap(flatten_para, width)
    if debug:
        print('textwrap:\n%s\n' % '\n'.join(splitted))

    wrapped = list()
    while len(splitted) > 0:
        line = splitted.pop(0)
        if len(splitted) == 0:
            last_paragraph_line = 1
        else:
            last_paragraph_line = 0
        aligned = align_string(line, width, last_paragraph_line)
        wrapped.append(aligned)

    return wrapped


def _text_browser_refresh(w: curses.window, start_idx: int,
                          end_idx: int, text_list: List[str]):
    row = 2
    for i in range(start_idx, end_idx):
        w.addstr(row, 2, text_list[i], curses.color_pair(_PAIR_WINDOW_BG_LOWER))
        row += 1

    w.refresh()


def _text_browser_refresh_bar(w: curses.window, start_idx: int, height: int, scale: int, width: int):
    """INTERNAL - Browser of the refresh bar

    w (curses.window): Curses window object
    start_idx (int): Index stat
    height (int): Height of the window
    scale (int): Scale (length)
    width (int): Width of the window

    """
    if start_idx > 0:
        w.move(start_idx + 1, 0 + width + 3)
        w.addch(curses.ACS_DIAMOND)

    for i in range(start_idx + 1, scale + start_idx - 1):
        w.move(i + 1, 0 + width + 3)
        w.addch(curses.ACS_CKBOARD)

    if scale + start_idx < height - 2:
        w.move(scale + start_idx, 0 + width + 3)
        w.addch(curses.ACS_DIAMOND)

    w.refresh()


def text_browser(s: curses.window, title: str, text: str, width: int = 50, height: int = 20):
    """Text Browsing

    Args:
        s (Curses.window): Curses screen object.
        title (string): Title of the window.
        text (string): Text to be browsed.
        width (int): width of the browser.
        height (int): height of the browser.
    """

    status_bar(s, "Browsing text.")

    text_list = text_justification(text, width)
    text_list[len(text_list) - 1] = text_list[len(text_list) - 1].ljust(width)
    # text_list.append(" ".ljust(width))

    num_rows = len(text_list)

    start_idx = 0
    end_idx = start_idx + height - 1 - 2

    if end_idx > num_rows:
        end_idx = num_rows - 1

    # Drawing the browser
    w: curses.window = init_win(height + 2, width + 4, 3, 3, title,
                                _PAIR_WINDOW_BG_LOWER, 0)
    w.attron(curses.A_REVERSE)
    w.move(1, 0 + width + 3)
    w.addch(curses.ACS_UARROW)
    w.move(height - 2, 0 + width + 3)
    w.addch(curses.ACS_DARROW)

    w.attron(curses.A_NORMAL)

    # Draw the right bar
    for i in range(2, height - 2):
        w.move(i, 0 + width + 3)
        w.addch(curses.ACS_DIAMOND)

    # Draw the box on the right bar
    max_length = height - 4
    scale = int(max_length / num_rows * (height - 2)) - 1

    if num_rows > max_length:
        _text_browser_refresh_bar(w, start_idx, height, scale, width)

    w.addstr(height + 1, 2, "<ESC> Exit /// Up/Down to browse".center(width),
             curses.color_pair(_PAIR_WINDOW_HELPER))

    # Populating
    _text_browser_refresh(w, start_idx, end_idx, text_list)

    pressed = s.getch()
    s.nodelay(True)
    while pressed != curses.ascii.ESC:

        if pressed == curses.KEY_DOWN:  # curses.KEY_DOWN: 66
            if start_idx > 0:
                start_idx -= 1
                end_idx -= 1

        if pressed == curses.KEY_UP:  # curses.KEY_UP: 65
            if end_idx < len(text_list):
                start_idx += 1
                end_idx += 1

        _text_browser_refresh(w, start_idx, end_idx, text_list)

        if num_rows > max_length:
            _text_browser_refresh_bar(w, start_idx, height, scale, width)

        pressed = s.getch()

    # Closing the browser
    end_win(w)
