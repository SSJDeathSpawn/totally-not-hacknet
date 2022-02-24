from typing import Union


IMAGE_PATH: str = 'res/images/'

TITLEBAR_OPTIONS_PATH: str = 'titlebar_options.png' 
TITLEBAR_OPTIONS_RATIO: tuple[int, int] = (2, 1)  # width to height

TITLEBAR_1PX_PATH: str = 'titlebar_1px.png'
TITLEBAR_1PX_RATIO: tuple[int, int] = (1, 4)  # width to height

RESOLUTION: tuple[int, int] = (1366, 768) 

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
