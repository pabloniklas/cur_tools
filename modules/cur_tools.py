#!/usr/bin/env python3
#
# CurTools
#
# By Pablo Niklas <pablo _dot_ niklas _at_ gmail _dot_ com>
#

import curses
import re
import os
import string
import textwrap
from curses import ascii

from typing import List
import calendar
import datetime
import copy


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

# ASCI Graphics
CHAR_LOW_GRAY = "░"
CHAR_MEDIUM_GRAY = "▒"
CHAR_HIGH_GRAY = "▓"

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


def _popup(s: curses.window, color: curses, title: string, txt: string):
    mh, mw = s.getmaxyx()
    w = len(txt) + 6

    if w < 30:
        w = 30

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)
    wininfo,shadow = init_win(h, w, wx, wy, title, color)
    wininfo.addstr(3, 3, txt)
    wininfo.getch()
    end_win(wininfo,shadow)


def info_win(s: curses.window, txt: string):
    """Creates an info window

    Args:
        s (curses) : Curses screen object.
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

def confirm_dialog(s: curses.window, message: string):
    """Show a confirmation dialog.

    Args:
        s (curses.window): Curses screen object.
        message (string): Message to be displayed.

    Returns:
        _type_: Return value
    """
    height, width = 7, 50
    start_y, start_x = (s.getmaxyx()[0] - height) // 2, (s.getmaxyx()[1] - width) // 2
    win = curses.newwin(height, width, start_y, start_x)
    win.box()
    win.addstr(2, 2, message)
    win.addstr(4, 2, "[Y] Sí    [N] No")
    win.refresh()
    while True:
        key = win.getch()
        if key in [ord('y'), ord('Y')]:
            return True
        elif key in [ord('n'), ord('N')]:
            return False

def file_selector(s: curses.window, start_path="."):
    """Show a file selector dialog.

    Args:
        s (curses.window): Curses screen object.
        start_path (str, optional): Initial path. Defaults to ".".

    Returns:
        _type_: Return value
    """
    current_path = os.path.abspath(start_path)
    while True:
        files = os.listdir(current_path)
        files.insert(0, "..")  # Para navegar al directorio padre
        selected = vertical_menu(s, files, 0, 0)
        chosen = files[selected]
        new_path = os.path.join(current_path, chosen)
        if os.path.isdir(new_path):
            current_path = os.path.abspath(new_path)
        else:
            return new_path

def progress_bar_create(s:curses.window, max_value: int, title: str = "Progress") -> curses.window:
    """
    Create a progress bar window.

    Args:
        stdscr: Standard screen object provided by curses.wrapper.
        max_value (int): The maximum value of the progress bar.
        title (str): Title for the progress bar (default: "Progress").

    Returns:
        A curses window object representing the progress bar.
    """
    height, width = 3, 50
    start_y, start_x = (s.getmaxyx()[0] // 2) - 1, (s.getmaxyx()[1] - width) // 2

    win = init_win(height, width, start_x, start_y, title)

    progress_label = f"0/{max_value}"
    bar_width = width - len(progress_label) - 4
    win.addstr(1, 2, f"[{' ' * bar_width}] {progress_label}")
    win.refresh()

    return win

def progress_bar_update(s: curses.window, current_value: int, max_value: int) -> None:
    """
    Update the progress bar with the current value.

    Args:
        win (curses.window): The progress bar window.
        current_value (int): The current progress value.
        max_value (int): The maximum progress value.
    """
    width = s.getmaxyx()[1] - 10
    progress = int((current_value / max_value) * width)
    bar = CHAR_MEDIUM_GRAY * progress + " " * (width - progress)

    s.addstr(1, 2, f"[{bar}]")
    s.refresh()

def progress_bar_close(win: curses.window) -> None:
    """
    Close and clear the progress bar window.

    Args:
        win (curses.window): The progress bar window to close.
    """
    win.clear()
    win.refresh()

def input_box(s: curses.window, label: str,
              length: int, help="", type: int = 0, hidden: bool = False) -> str:
    """
    Provides a simple input box.

    Args:
        s (curses.window): A curses window object.
        label (str): Field label.
        length (int): Field length.
        help (str): Field help.
        type (int): Field type:
            0 - INPUT_TYPE_ALPHANUMERIC
            1 - INPUT_TYPE_NUMERIC
            2 - INPUT_TYPE_ALPHABETIC
        hidden (bool): True means to hide the chars.

    Returns:
        str: The value of the input.
    """
    w = length + len(label) + 10

    mh, mw = s.getmaxyx()

    h = 7
    wx = int((mh - h) / 2)
    wy = int((mw - w) / 2)

    win_input, sha_input = init_win(h, w, wx, wy, "Input Box")

    value = simple_input_text_field(s, win_input, 3, 3, label, length, help, type, hidden)

    end_win(win_input, sha_input)

    return value


def simple_input_text_field(s: curses.window, w: curses.window, x: int, y: int, label: str,
                            length: int, help="", type: int = 0, hidden: bool = False) -> str:
    """
    Creates a text field input.

    Args:
        s (curses.window): Curses screen object.
        w (curses.window): Curses window object.
        x (int): Row position.
        y (int): Column position.
        label (str): Field label.
        length (int): Length of the input field.
        help (str): Help text.
        type (int): Field type (0-Alphanumeric, 1-Numeric, 2-Alphabetic).
        hidden (bool): True if the input should be hidden.

    Returns:
        str: The value of the input.
    """
    value = ""
    status_bar(s, help)

    # Label
    w.addstr(x, y, label + ":", curses.color_pair(_PAIR_WINDOW_BG_LOWER))

    # Draw the gap
    field_y = y + len(label) + 2
    field_x = x
    w.addstr(field_x, field_y, ' '.ljust(length), curses.color_pair(_PAIR_INPUT_FIELD))

    # Main input cycle
    curses.curs_set(1)
    w.nodelay(False)
    cursor_offset = 0
    while True:
        w.move(field_x, field_y + cursor_offset)
        w.refresh()
        key = w.getch()

        if key in (curses.ascii.NL, curses.ascii.ESC):  # Enter or ESC
            break
        elif key == curses.ascii.DEL or key == 127:  # Backspace
            if cursor_offset > 0:
                cursor_offset -= 1
                value = value[:cursor_offset] + value[cursor_offset + 1:]
                w.addstr(field_x, field_y + cursor_offset, ' ')
        elif key == curses.KEY_LEFT:  # Move cursor left
            if cursor_offset > 0:
                cursor_offset -= 1
        elif key == curses.KEY_RIGHT:  # Move cursor right
            if cursor_offset < len(value):
                cursor_offset += 1
        elif len(value) < length and valid_input(key, type):
            # Insert character
            char = chr(key)
            value = value[:cursor_offset] + char + value[cursor_offset:]
            cursor_offset += 1

        # Redraw the input field
        display_value = ''.join(['*' if hidden else c for c in value])
        w.addstr(field_x, field_y, display_value.ljust(length), curses.color_pair(_PAIR_INPUT_FIELD))

    # Handle ESC key to cancel input
    if key == curses.ascii.ESC:
        value = ""

    curses.curs_set(0)
    return value


def valid_input(key: int, input_type: int) -> bool:
    """
    Validates the input based on type.

    Args:
        key (int): The key pressed.
        input_type (int): The input type (0-Alphanumeric, 1-Numeric, 2-Alphabetic).

    Returns:
        bool: True if the key is valid, False otherwise.
    """
    char = chr(key)
    if input_type == 0:  # Alphanumeric
        return char.isalnum() or char.isspace()
    elif input_type == 1:  # Numeric
        return char.isdigit()
    elif input_type == 2:  # Alphabetic
        return char.isalpha()
    return False

        
def multi_select_menu(s: curses.window, options:List[str], title="Selecciona opciones:"):
    """Show a multi select menu dialog.

    Args:
        s (curses.window): Curses screen object.
        options (List[str]): Options list.
        title (str, optional): Title message. Defaults to "Selecciona opciones:".

    Returns:
        _type_: Choices list
    """
    selected = [False] * len(options)
    current_index = 0

    while True:
        s.clear()
        s.addstr(0, 0, title)
        for i, option in enumerate(options):
            marker = "[X]" if selected[i] else "[ ]"
            if i == current_index:
                s.addstr(i + 1, 0, f"{marker} {option}", curses.A_REVERSE)
            else:
                s.addstr(i + 1, 0, f"{marker} {option}")
        s.addstr(len(options) + 2, 0, "Presiona Espacio para seleccionar, Enter para confirmar.")
        s.refresh()

        key = s.getch()
        if key == curses.KEY_UP:
            current_index = (current_index - 1) % len(options)
        elif key == curses.KEY_DOWN:
            current_index = (current_index + 1) % len(options)
        elif key == ord(' '):  # Espacio para seleccionar/deseleccionar
            selected[current_index] = not selected[current_index]
        elif key == 10:  # Enter para confirmar
            return [options[i] for i, sel in enumerate(selected) if sel]

def calendar_widget(s: curses.window):
    """Show a calendar widget.

    Args:
        s (curses.window): Curses screen object.

    Returns:
        _type_: Date.
    """
    today = datetime.date.today()
    current_year, current_month = today.year, today.month
    selected_day = today.day

    while True:
        s.clear()
        display_calendar(s, current_year, current_month, selected_day)
        s.addstr(10, 0, "Usa las flechas para moverte, Enter para seleccionar.")
        s.refresh()

        key = s.getch()
        selected_day = update_selected_day(key, current_year, current_month, selected_day)
        if key == 10:  # Enter
            return datetime.date(current_year, current_month, selected_day)


def display_calendar(s: curses.window, year: int, month: int, selected_day: int):
    """Display the calendar on the screen.

    Args:
        s (curses.window): Curses screen object.
        year (int): Year to display.
        month (int): Month to display.
        selected_day (int): Currently selected day.
    """
    cal = calendar.monthcalendar(year, month)
    s.addstr(0, 0, f"{calendar.month_name[month]} {year}")
    for week in cal:
        for day in week:
            if day == 0:
                s.addstr("   ")  # Día vacío
            elif day == selected_day:
                s.addstr(f"[{day:2}]", curses.A_REVERSE)
            else:
                s.addstr(f" {day:2} ")
        s.addstr("\n")


def update_selected_day(key: int, year: int, month: int, selected_day: int) -> int:
    """Update the selected day based on the key pressed.

    Args:
        key (int): Key pressed.
        year (int): Current year.
        month (int): Current month.
        selected_day (int): Currently selected day.

    Returns:
        int: Updated selected day.
    """
    if key == curses.KEY_LEFT:
        return max(1, selected_day - 1)
    elif key == curses.KEY_RIGHT:
        return min(calendar.monthrange(year, month)[1], selected_day + 1)
    elif key == curses.KEY_UP:
        return max(1, selected_day - 7)
    elif key == curses.KEY_DOWN:
        return min(calendar.monthrange(year, month)[1], selected_day + 7)
    return selected_day

def bar_chart(s: curses.window, data:List[int], title="Gráfico de barras"):
    """Show a bar chart.

    Args:
        s (curses.window): Curses screen object.
        data (List[int]): Data list.
        title (str, optional): Title message. Defaults to "Gráfico de barras".
    """
    max_value = max(data.values())
    max_width = s.getmaxyx()[1] - 20

    s.clear()
    s.addstr(0, 0, title)
    for i, (label, value) in enumerate(data.items()):
        bar_length = int((value / max_value) * max_width)
        s.addstr(i + 2, 0, f"{label:15}: {'#' * bar_length} ({value})")
    s.addstr(len(data) + 3, 0, "Presiona cualquier tecla para salir.")
    s.refresh()
    s.getch()

def table_viewer(s: curses.window, data, col_width=15):
    """Show a table viewer.

    Args:
        s (curses.window): Curses screen object.
        data (_type_): Data list.
        col_width (int, optional): Column width. Defaults to 15.
    """
    rows, cols = len(data), len(data[0])
    top, left = 0, 0

    while True:
        s.clear()
        for r in range(min(rows - top, s.getmaxyx()[0] - 2)):
            for c in range(min(cols - left, s.getmaxyx()[1] // col_width)):
                s.addstr(r, c * col_width, f"{data[top + r][left + c]:<{col_width}}")
        s.addstr(s.getmaxyx()[0] - 1, 0, "Usa las flechas para moverte, Q para salir.")
        s.refresh()

        key = s.getch()
        if key == curses.KEY_UP and top > 0:
            top -= 1
        elif key == curses.KEY_DOWN and top < rows - 1:
            top += 1
        elif key == curses.KEY_LEFT and left > 0:
            left -= 1
        elif key == curses.KEY_RIGHT and left < cols - 1:
            left += 1
        elif key in [ord('q'), ord('Q')]:
            break

def show_notification(s: curses.window, message:string, duration=2):
    """Show a notification.

    Args:
        s (curses.window): Curses screen object.
        message (string): Message to be displayed.
        duration (int, optional): Duration in seconds. Defaults to 2.
    """
    height, width = 3, len(message) + 4
    start_y, start_x = (s.getmaxyx()[0] - height) // 2, (s.getmaxyx()[1] - width) // 2
    win = curses.newwin(height, width, start_y, start_x)
    win.box()
    win.addstr(1, 2, message)
    win.refresh()
    curses.napms(duration * 1000)
    win.clear()


def simple_text_editor(s: curses.window, filename="untitled.txt"):
    """Simple text editor.

    Args:
        s (curses.window): Curses screen object.
        filename (str, optional): File name. Defaults to "untitled.txt".
    """
    curses.curs_set(1)
    text = []
    cursor_y, cursor_x = 0, 0

    while True:
        s.clear()
        s.addstr(0, 0, f"Archivo: {filename}  |  F2: Guardar  |  F10: Salir", curses.A_REVERSE)
        for i, line in enumerate(text):
            s.addstr(i + 1, 0, line)
        s.move(cursor_y + 1, cursor_x)
        s.refresh()

        key = s.getch()
        if key in [curses.KEY_F10]:  # Salir
            break
        elif key in [curses.KEY_F2]:  # Guardar
            with open(filename, 'w') as file:
                file.write('\n'.join(text))
        elif key in [curses.KEY_BACKSPACE, 127]:
            if cursor_x > 0:
                text[cursor_y] = text[cursor_y][:cursor_x - 1] + text[cursor_y][cursor_x:]
                cursor_x -= 1
            elif cursor_y > 0:
                cursor_x = len(text[cursor_y - 1])
                text[cursor_y - 1] += text.pop(cursor_y)
                cursor_y -= 1
        elif key == curses.KEY_DOWN:
            cursor_y = min(cursor_y + 1, len(text) - 1)
        elif key == curses.KEY_UP:
            cursor_y = max(0, cursor_y - 1)
        elif key == curses.KEY_LEFT:
            cursor_x = max(0, cursor_x - 1)
        elif key == curses.KEY_RIGHT:
            cursor_x = min(len(text[cursor_y]), cursor_x + 1)
        elif key in [10, 13]:  # Enter
            text.insert(cursor_y + 1, text[cursor_y][cursor_x:])
            text[cursor_y] = text[cursor_y][:cursor_x]
            cursor_y += 1
            cursor_x = 0
        else:
            if len(text) <= cursor_y:
                text.append("")
            text[cursor_y] = text[cursor_y][:cursor_x] + chr(key) + text[cursor_y][cursor_x:]
            cursor_x += 1


def init_win(height: int, width: int, wx: int, wy: int, title: str = "",
             bgcolor: curses = _PAIR_WINDOW_BG_LOWER,
             border_type: int = 0) -> tuple[curses.window,curses.window]:
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

    w.bkgd(' ', curses.color_pair(bgcolor))

    # Create shadow effect
    s = curses.newwin(height, width, wx + 1, wy + 2)
    s.bkgd(" ", curses.A_DIM)  # Shadow background
    s.refresh()
    
    w.refresh()

    if title != "":
        col = int((width - len(title) - 4) / 2)
        w.addstr(0, col, f'[ {title} ]', curses.A_REVERSE)

    return w,s

def end_win(w: curses.window, s: curses.window):
    """Closes a curses window.

    Args:
        w (curses): curses window object.
        s (curses): curses window object.
    """
    w.bkgd(' ', curses.color_pair(_PAIR_SCREEN_BG))
    w.erase()
    w.refresh()
    
    s.bkgd(' ', curses.color_pair(_PAIR_SCREEN_BG))
    s.erase()
    s.refresh()
    
    del w,s


def _menu_hotkey_option(choices: list) -> List[str]:
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
    window_menu, shadow_menu = init_win(len(choices) + 2, max_length + 4, wx, wy)

    # Printing the choices of the submenu
    row = 0
    for choice in choices:

        parent_choice = choice.copy()   # tipos mutables se pasan por referencia con "=". Ojo.

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


    shadow_menu.refresh()
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
        end_win(window_menu, shadow_menu)
        return -10
    elif pressed == 68:
        end_win(window_menu, shadow_menu)
        return -11
    else:
        if len(choices[highlight_option]) == 2:
            end_win(window_menu, shadow_menu)
            return highlight_option + 1
        else:   # submenu
            second_choices = choices[highlight_option][2]
            second_choice = vertical_menu(stdscr, second_choices, wx + row - 1,
                                          wy + max_length + 4)
            end_win(window_menu, shadow_menu)

            return second_choice

def _search_in_list(my_list: list, key: string, idx: int = 0) -> int:
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
        tuple [cursor_offset, value]
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


def text_justification(text: string, width: int) -> List[str]:
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
def align_string(s: string, width: int, last_paragraph_line: int = 0) -> str:
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


def align_paragraph(paragraph, width, debug=0) -> List[str]:
    """Align paragraph to a specific width.

    Args:
        paragraph (list): list of lines
        width (int): width
        debug (bool):

    Returns:
        List of paragraph lines
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
                          end_idx: int, text_list: list):
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


def text_browser(s: curses.window, title: string, text: string, width: int = 50, height: int = 20):
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
    w,s = init_win(height + 2, width + 4, 3, 3, title,
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
    end_win(w,s)
