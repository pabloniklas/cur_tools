#!/usr/bin/env python3
#
# CurTools
#
# By Pablo Niklas <pablo _dot_ niklas _at_ gmail _dot_ com>
#

import curses
import re
# import time
import string
import textwrap
from curses import ascii

# from var_dump import var_dump

_STATUSBAR_PREFIX = " StatusBar | "

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
_PAIR_ITEM_SELECTED = _pair_pointer
_pair_pointer += 1
_PAIR_HOTKEY_SELECTED = _pair_pointer
_pair_pointer += 1
_PAIR_HOTKEY_UNSELECTED = _pair_pointer
_pair_pointer += 1
_PAIR_ITEM_UNSELECTED = _pair_pointer

_pair_pointer += 1
_PAIR_ERROR_WINDOW = _pair_pointer


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

    scr.bkgd(curses.color_pair(_PAIR_SCREEN_BG))
    scr.clear()
    scr.bkgdset(' ')
    scr.bkgd(curses.color_pair(_PAIR_SCREEN_BG))
    scr.refresh()

    return scr


def curses_end():
    """Ends curses environment"""
    curses.endwin()


def _popup(s: curses.window, color: curses, title: string, txt: string):
    mh, mw = s.getmaxyx()
    w = len(txt) + 6

    if w < 30:
        w = 30

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)
    wininfo: curses.window = init_win(h, w, wx, wy, title, color)
    wininfo.addstr(3, 3, txt)
    wininfo.getch()
    end_win(wininfo)


def info_win(s: curses.window, txt: string):
    """Creates an info window

    Args:
        s (curses) : Curses scrren object.
        txt (string) : Text to be displayed.

    """
    color = _PAIR_WINDOW_BG_LOWER
    title = "Info Window"
    _popup(s, color, title, txt)


def error_win(s: curses.window, txt: string):
    """Creates an error window

    Args:
        s (curses) : Curses scrren object.
        txt (string) : Text to be displayed.

    """
    color = _PAIR_ERROR_WINDOW
    title = "Error Window"
    _popup(s, color, title, txt)


def init_win(height: int, width: int, wx: int, wy: int, title: str = "", bgcolor: curses = _PAIR_WINDOW_BG_LOWER,
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


def status_bar(stdscr: curses.window, intxt: str):
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

    stdscr.addstr(height - 1, 0, txt, curses.color_pair(_PAIR_WINDOW_BG_LOWER))
    stdscr.addstr(height - 1, len(txt) - 1, " " *
                  (width - len(txt)), curses.color_pair(_PAIR_WINDOW_BG_LOWER))
    stdscr.refresh()


def _menu_option_refresh(window_menu: curses.window, row: [int], max_length: int,
                         choice: [str], hotkey_list: [str],
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
    window_menu.addstr(row + 2,
                       1,
                       " " + choice[0].ljust(max_length + 1),
                       curses.color_pair(word_color))

    window_menu.addstr(row + 2,
                       hotkey_list[row][2] + 2,
                       choice[0][hotkey_list[row][2]:hotkey_list[row][2] + 1],
                       curses.color_pair(hotkey_color))


def vertical_menu(stdscr: curses.window, choices: list, wx: int, wy: int) -> int:
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

    # Discovering the hotkeys
    hotkey_list = _curses_menu_hotkey_option(choices)

    # Drawing the window
    window_menu: curses.window = init_win(len(choices) + 3, max_length + 4, wx, wy)

    # Printing the choices of the submenu
    row = 0
    for choice in choices:

        # First option selected
        if row == 0:
            _menu_option_refresh(window_menu, row, max_length, choice, hotkey_list,
                                 _PAIR_ITEM_SELECTED, _PAIR_HOTKEY_SELECTED)

        else:
            _menu_option_refresh(window_menu, row, max_length, choice, hotkey_list,
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

        # curses_status_bar(stdscr, "STATUS BAR | pressed: {}".format(pressed))

        # getch(): 001000010 = 66
        # curses.KEY_DOWN: 100000010 = 258

        if pressed == 66:  # curses.KEY_DOWN:

            _menu_option_refresh(window_menu, highlight_option, max_length,
                                 choices[highlight_option],
                                 hotkey_list,
                                 _PAIR_ITEM_UNSELECTED, _PAIR_HOTKEY_UNSELECTED)

            status_bar(stdscr, choices[highlight_option][1])

            highlight_option += 1

            if highlight_option >= len(choices) - 1:
                highlight_option = len(choices) - 1

        # getch(): 001000001 = 65
        # curses.KEY_UP: 100000011 = 259

        if pressed == 65:  # curses.KEY_UP:
            _menu_option_refresh(window_menu, highlight_option, max_length,
                                 choices[highlight_option],
                                 hotkey_list,
                                 _PAIR_ITEM_UNSELECTED, _PAIR_HOTKEY_UNSELECTED)

            status_bar(stdscr, choices[highlight_option][1])

            highlight_option -= 1

            if highlight_option < 0:
                highlight_option = 0

        # Draw the new option
        _menu_option_refresh(window_menu, highlight_option, max_length,
                             choices[highlight_option],
                             hotkey_list,
                             _PAIR_ITEM_SELECTED, _PAIR_HOTKEY_SELECTED)

        status_bar(stdscr, choices[highlight_option][1])

        window_menu.refresh()
        pressed = window_menu.getch()

    end_win(window_menu)

    if pressed == 67:
        return -10
    elif pressed == 68:
        return -11
    else:
        return highlight_option + 1


def _search_in_list(my_list: list, key: string, idx: int) -> int:
    """INTERNAL - Search a string in a list of arrays.

    Args:
        my_list (list): The list.
        key (string): The string to be searched in the list.
        idx (int): 

    Returns:
        int: [description]
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
    hotkey_list = _curses_menu_hotkey_option(menubar_options)
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
            pass

        _idx = menubar_options[idx]

        # Calling the vertical menu
        submenu_options = options_dict[_idx]
        submenu_choice = vertical_menu(
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


def _field_input_type(w: curses.window, input_type: str, field_x: int,
                      field_y: int, cursor_offset: int,
                      length: int, key: curses.ascii, value: str) -> [int, str]:
    """Logic behind the input field.

    Args:
        w (curses.window): A curses window object.
        input_type (string): Boolean validation expression
        field_x (int): x coordinate.
        field_y (int): y coordinate.
        cursor_offset: Cursor position inside the field.
        length (int): Field length.
        key (curses.ascii): The key pressed.
        value: The data in the field.

    Returns:
        The tuple [cursor_offset, value]
    """

    w.move(field_x, field_y + cursor_offset)
    if eval(input_type) and cursor_offset < length:
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


def input_text_field(s: curses.window, w: curses.window, x: int, y: int, label: string,
                     length: int, help="", type: int = 0) -> string:
    """Creates a text field input.

    Args:
        s (curses.window): Curses screen object.
        w (curses.window): Curses window object.
        x (int): row.
        y (int): col.
        label (string): text
        length (int): max length of the text field
        help (string): Help text.
        type (int): Type of validation:
                0 => Alphanumeric only.
                1 => Numeric only.
                2 => Alphabetic only.

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

    # Main cicle.
    curses.curs_set(1)  # make cursor visible
    curses.echo(False)
    w.nodelay(True)
    key = w.getch()
    cursor_offset = 0
    w.move(field_x, field_y + cursor_offset)
    w.attron(curses.color_pair(_PAIR_INPUT_FIELD))

    while key != curses.ascii.NL and key != curses.ascii.ESC:

        if type == 0:
            bool_expr_type = "curses.ascii.isalnum(key)"
        elif type == 1:
            bool_expr_type = "curses.ascii.isdigit(key)"
        elif type == 2:
            bool_expr_type = "curses.ascii.isalpha(key)"

        w.move(field_x, field_y + cursor_offset)
        cursor_offset, value = _field_input_type(w, bool_expr_type,
                                                 field_x, field_y,
                                                 cursor_offset, length, key, value)
        w.refresh()
        key = w.getch()

    # Cancel Input when ESC is pressed
    if key == curses.ascii.ESC:
        value = ""

    curses.curs_set(0)  # make cursor invisible
    end_win(w)

    return value


def text_justification(text: string, width: int) -> list:
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


def _items_len(thelist):
    return sum([len(x) for x in thelist])


# https://code.activestate.com/recipes/414870-align-text-string-using-spaces-between-words-to-fi/
def align_string(s, width, last_paragraph_line=0):
    '''
    align string to specified width
    '''
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


def align_paragraph(paragraph, width, debug=0):
    '''
    align paragraph to specified width,
    returns list of paragraph lines
    '''
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

    if debug:
        print('textwrap & align_string:\n%s\n' % '\n'.join(wrapped))

    return wrapped


def text_browser(s: curses.window, title: string, text: string):
    """Browsing text

    Args:
        s (Curses.window): Curses screen object.
        title (string): Title of thw window.
        text (string): Text to be browsed.
    """

    status_bar(s, "Browsing text.")

    width = 50
    max_height = 20
    text_list = text_justification(text, width)

    start_idx = 0
    end_idx = start_idx + max_height - 1 - 2

    if end_idx > len(text_list):
        end_idx = len(text_list) - 1

    # Drawing the browser
    w: curses.window = init_win(max_height, width + 4, 3, 3, title, _PAIR_WINDOW_BG_LOWER, 0)
    w.attron(curses.A_REVERSE)
    w.move(1, 0 + width + 3)
    w.addch(curses.ACS_UARROW)
    w.move(max_height - 2, 0 + width + 3)
    w.addch(curses.ACS_DARROW)

    w.attron(curses.A_NORMAL)

    for i in range(2, max_height - 2):
        w.move(i, 0 + width + 3)
        w.addch(curses.ACS_CKBOARD)

    # Populating
    row = 2
    for i in range(start_idx, end_idx):
        w.addstr(row, 2, text_list[i], curses.color_pair(_PAIR_WINDOW_BG_LOWER))
        row += 1

    # TODO: Action keys
    pressed = w.getch()
    while pressed != 67 and \
            pressed != 68 and \
            pressed != curses.ascii.NL and \
            pressed != curses.ascii.ESC:

        if pressed == 66:  # curses.KEY_DOWN:
            pass

        if pressed == 65:  # curses.KEY_UP:
            pass

        w.refresh()
        pressed = w.getch()

    # Closing the browser
    end_win(w)
