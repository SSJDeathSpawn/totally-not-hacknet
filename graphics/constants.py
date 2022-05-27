from typing import Union, Type

from game.storage_system.storage_unit import StorageUnit
from game.storage_system.file import File
from game.storage_system.directory import Directory

# Colors
WHITE: tuple[int, int, int, int] = (255, 255, 255, 255)
BETTER_WHITE: tuple[int, int, int, int] = (215, 215, 215, 255)
BLACK: tuple[int, int, int, int] = (0, 0, 0, 255)
RED: tuple[int, int, int, int] = (255, 0, 0, 0)

# Title Bar
TITLEBAR_OPTIONS_PATH: str = 'application/titlebar_options.png'
TITLEBAR_OPTIONS_DIMENSIONS: tuple[int, int] = (2, 1)  # width, height

TITLEBAR_1PX_PATH: str = 'application/titlebar_1px.png'
TITLEBAR_1PX_DIMENSIONS: tuple[int, int] = (1, 4)  # width, height

TITLEBAR_DEFAULT_HEIGHT: int = 30

# General
RESOLUTION: tuple[int, int] = (1366, 768) 

APPLICATION_MIN_WIDTH = 100
APPLICATION_MIN_HEIGHT = 100

# Formatting

CODE_FORMATTING: dict[str, str] = {

    'BLACK': '⸸{c:black}',
    'RED': '⸸{c:red}',
    'GREEN': '⸸{c:green}',
    'YELLOW': '⸸{c:yellow}',
    'BLUE': '⸸{c:blue}',
    'CYAN': '⸸{c:cyan}',
    'MAGENTA': '⸸{c:magenta}',
    'WHITE': '⸸{c:white}',
    'RESET': '⸸{c:reset}⸸{s:reset}',
    'REGULAR': '⸸{s:regular}',
    'BOLD': '⸸{s:bold}',
    'ITALIC': '⸸{s:italic}',
    'BOLD_ITALIC': '⸸{s:bold-italic}',

    'COLOR_RESET': '⸸{c:reset}',
    'STYLE_RESET': '⸸{s:reset}'

}

TEXT_CODES: dict[str, Union[tuple[int, int, int], str]] = {

    '⸸{c:black}': (0, 0, 0), 
    '⸸{c:red}': (255, 0, 0), 
    '⸸{c:green}': (0, 255, 0), 
    '⸸{c:yellow}': (255, 255, 0), 
    '⸸{c:blue}': (0, 0, 255), 
    '⸸{c:magenta}': (255, 0, 255), 
    '⸸{c:cyan}': (0, 255, 255), 
    '⸸{c:white}': (255, 255, 255),
    
    '⸸{s:regular}': 'regular', 
    '⸸{s:bold}': 'bold', 
    '⸸{s:italic}': 'italic',
    '⸸{s:bold-italic}': 'bolditalic'
    
}

TEXT_ESCAPE_CHAR: str = '⸸'

UM_FNT_PT_FACTOR: tuple[float, float] = (1 / 2, 1)  # Ubuntu Mono Font size point conversion factors
IBM_FNT_PT_FACTOR: tuple[float, float] = (3 / 5, 1)  # IBM Plex Mono Font size point conversion factors

# Fonts
# DEFAULT_REGULAR_FONT: str = 'res/fonts/regular.ttf'
# DEFAULT_ITALIC_FONT: str = 'res/fonts/italic.ttf'
# DEFAULT_BOLD_FONT: str = 'res/fonts/bold.ttf'
# DEFAULT_BOLDITALIC_FONT: str = 'res/fonts/bolditalic.ttf'

DEFAULT_REGULAR_FONT: str = 'res/fonts/IBMregular.ttf'
DEFAULT_ITALIC_FONT: str = 'res/fonts/IBMitalic.ttf'
DEFAULT_BOLD_FONT: str = 'res/fonts/IBMbold.ttf'
DEFAULT_BOLDITALIC_FONT: str = 'res/fonts/IBMbolditalic.ttf'

# Images
IMAGE_PATH: str = 'res/images/'
DESKTOP_BACKGROUND_PATH: str = 'desktop/background.png'

# Applications
WINDOW_OUTLINE_COLOR: tuple[int, int, int, int] = (65, 65, 65, 255)

SCROLLBAR_WIDTH: int = 15

# Message Box
MESSAGE_BOX_DIMENSIONS: tuple[int, int] = (320, 160)
MESSAGE_BOX_PADDING: tuple[int, int] = (10, 10)
MESSAGE_BOX_FONT_SIZE: int = 20
MESSAGE_BOX_TEXT_COLOR: tuple[int, int, int, int] = (255, 46, 99, 255)
MESSAGE_BOX_BGCOLOR: tuple[int, int, int, int] = (30, 30, 30, 250)
MESSAGE_BOX_OUTLINE_COLOR: tuple[int, int, int, int] = (65, 65, 65, 255)
MESSAGE_BOX_TIME: int = 3

# TTy
TTY_FONT_SIZE: int = 20
TTY_TEXT_PADDING: tuple[int, int] = (3, 3)

# Terminal
TERMINAL_CURSOR_COLOR: tuple[int, int, int] = (255,255, 255, 255)
TERMINAL_COLOR_CODES = {
    '⸸{c:kaliblue}': (48, 102, 196),
    '⸸{c:kaliorange}': (242, 132, 26)
}
TERMINAL_COLOR_FORMATTING: dict[str, str] = {
    'KALI-BLUE': '⸸{c:kaliblue}', 
    'KALI-ORANGE': '⸸{c:kaliorange}'
}
TERMINAL_CONTENT_COLOR: tuple[int, int, int, int] = (255, 255, 255, 255)
TERMINAL_BGCOLOR: tuple[int, int, int, int] = (15, 15, 15, 217)
TERMINAL_FONT_SIZE: int = 20

# Explorer
FILE_ICON_PATH: str = 'explorer/file.png'
FILE_ICON_SELECTED_PATH: str = 'explorer/file_selected.png'
FOLDER_ICON_PATH: str = 'explorer/folder.png'
FOLDER_ICON_SELECTED_PATH: str = 'explorer/folder_selected.png'
SU_ICON_DIMENSIONS: tuple[int, int] = (42, 42)
SU_ICON_LABEL_FNT_SIZE: int = 12

EXPLORER_BGCOLOR: tuple[int, int, int, int] = (20, 20, 20, 252)
EXPLORER_TEXT_COLOR: tuple[int, int, int, int] = (255, 115, 255, 255)
EXPLORER_SCROLLBAR_COLOR: tuple[int, int, int, int] = (30, 30, 30, 255)
EXPLORER_CWD_FONT_SIZE: int = 17
ICON_PADDING: tuple[int, int, int, int] = (20, 20, 20, 20)

PATH_FROM_CLASS: dict[Type[StorageUnit], dict[bool, str]] = {
    File: {
        True: FILE_ICON_SELECTED_PATH,
        False: FILE_ICON_PATH
    },
    Directory: {
        True: FOLDER_ICON_SELECTED_PATH,
        False: FOLDER_ICON_PATH
    }
}
