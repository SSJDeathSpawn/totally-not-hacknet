from typing import Union

# Title Bar

TITLEBAR_OPTIONS_PATH: str = 'application/titlebar_options.png'
TITLEBAR_OPTIONS_DIMENSIONS: tuple[int, int] = (2, 1)  # width, height

TITLEBAR_1PX_PATH: str = 'application/titlebar_1px.png'
TITLEBAR_1PX_DIMENSIONS: tuple[int, int] = (1, 4)  # width, height

TITLEBAR_DEFAULT_HEIGHT: int = 30

RESOLUTION: tuple[int, int] = (1366, 768) 

APPLICATION_MIN_WIDTH = 100
APPLICATION_MIN_HEIGHT = 100

# File Explorer Color Pallete

EXP_BACKGROUND: tuple[int, int, int] = (22, 0, 64)

# Formatting

CODE_FORMATTING: dict[str, str] = {

    'BLACK': '⸸{c:black}',
    'RED': '⸸{c:red}',
    'GREEN': '⸸{c:green}',
    'YELLOW': '⸸{c:yellow}',
    'BLUE': '⸸{c:blue}',
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
    '⸸{s:bold-italic}': 'bold-italic'
    
}

TEXT_ESCAPE_CHAR: str = '⸸'

FONTSIZE_WIDTH_HEIGHT_RATIO: tuple[int, int, int] = ()


# Images
IMAGE_PATH: str = 'res/images/'
DESKTOP_BACKGROUND_PATH = 'desktop/background.jpg'
