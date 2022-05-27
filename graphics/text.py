import re

from logging import Logger
from typing import Optional, Union

from logging_module.custom_logging import get_logger
from graphics.constants import TEXT_CODES, CODE_FORMATTING, TEXT_ESCAPE_CHAR, IBM_FNT_PT_FACTOR


class Section(object):
    """A section of text"""

    def __init__(self, text: str, color: tuple[int, int, int], style: str, pos: tuple[int, int]) -> None:
        
        self.text: str = text
        self.color: tuple[int, int, int] = color
        self.style: str = style
        self.pos: tuple[int, int] = pos

    def __str__(self) -> str:
        return f'Text -> {self.text}\nColor -> {self.color}\nStyle -> {self.style}\nPos -> {self.pos}\n'
    
    def __repr__(self) -> str:
        return self.__str__()


class Text(object):
    """The class handling all text rendering shenanigans"""

    def __init__(self, string: str, color: tuple[int, int, int], style: str, font_size: int, start: tuple[int, int], width: int, height: int, end_padding: tuple[int, int], fn_ptr_factor: Optional[tuple[int, int]] = IBM_FNT_PT_FACTOR, additional_colors: Optional[dict[str, tuple[int, int, int]]] = None) -> None:
        
        self.logger: Logger = get_logger('graphics')
        
        self.string: str = string
        self.processed_text: list[Section]

        self.starting_color: tuple[int, int, int] = color
        self.starting_style: str = style
        self.font_size: int = font_size

        self.start: tuple[int, int] = start
        self.end_padding: tuple[int, int] = end_padding
        self.width: int = width - self.end_padding[0]
        self.height: int = height - self.end_padding[0]

        self.fn_ptr_factor = fn_ptr_factor

        self.escape_codes: dict[str, Union[tuple[int, int, int], str]] = TEXT_CODES
        self.escape_codes.update({
            CODE_FORMATTING.get('COLOR_RESET'): self.starting_color, 
            CODE_FORMATTING.get('STYLE_RESET'): self.starting_style
        })

        if additional_colors: 
            self.escape_codes.update(additional_colors)
        
        self.escape_pattern: re.Pattern = re.compile('(' + TEXT_ESCAPE_CHAR + '\{(?:c|s):[a-z-]+\})')
        Text.escape_pattern: re.Pattern = self.escape_pattern

        self.process_text()

    #Helper

    @staticmethod
    def get_uncoded_text(string: str) -> str:
        """Returns the string without escape codes"""

        return ''.join(re.split(Text.escape_pattern, string)[::2])
        

    # Getters
    
    def get_raw_text(self, with_escape_codes: bool = False) -> str:
        """Returns the raw text"""

        if with_escape_codes:
            return self.string

        else:
            return ''.join(re.split(self.escape_pattern, self.string)[::2])

    def get_processed_text(self) -> list[Section]:
        """Returns the processed text"""

        return self.processed

    # Setters

    def set_width(self, new_width: int) -> None:
        """Updates the width of the Text object. Used while scaling the window"""

        self.width = new_width

        self.process_text()

    def set_height(self, new_height: int) -> None:
        """Updates the height of the Text object. Used while scaling the window"""

        self.height = new_height

        self.process_text()

    def update_text(self, string: str, new: bool = False) -> None:
        """Updates text"""

        if new:
            self.string = string
        else:
            self.string += string
            
        self.process_text()

    def update_color(self, new_color: tuple[int, int, int]) -> None:
        """Updates color"""
        
        self.starting_color = new_color
        self.escape_codes['COLOR_RESET'] = new_color

        self.process_text()

    def update_style(self, new_style: str) -> None:
        """Updates style"""

        self.starting_style = new_style
        self.escape_codes['STYLE_RESET'] = new_style

        self.process_text()

    def update_width(self, new_width: int) -> None:
        """Updates width"""

        self.width = new_width

        self.process_text()

    def update_height(self, new_height: int) -> None:
        """Updates height"""

        self.height = new_height

        self.process_text()

    def update_starting_pos(self, new_start: tuple[int, int]) -> None:
        """Updates starting position"""

        self.start = new_start

        self.process_text()

    # Processing

    def remove_codes(self, base_split: list[str]) -> list[str]:
        """"""
        
        string = []
        code_to_index = {}
        width = int(self.font_size * self.fn_ptr_factor[0])

        for s in base_split:
            code_to_index = {}
            matches = self.escape_pattern.finditer(s)
            s_split = self.escape_pattern.split(s)
            codes = s_split[1::2] if len(s_split) > 1 else s_split
            for item in matches:
                code_to_index[item.start(0)] = codes.pop(0)

            temp = ''.join(s_split[::2])

            i = 1
            while True:
                if len(temp) > ((self.width - self.start[0]) // width) * i + i - 1:
                    temp = temp[:((self.width - self.start[0]) // width) * i + i - 1] + '\n' + temp[((self.width - self.start[0]) // width) * i + i - 1:]
                    i += 1
                else: 
                    break

            # map_len = list(map(lambda s: len(s) > (self.width-self.start[0]) // width, temp))
            # while any(map_len):
            #     index = map_len.index(True)
            #     new = [string[index][i:i + (self.width-self.start[0]) // width] for i in range(0, len(temp[index]), (self.width-self.start[0]) // width)]
            #     i += len(new) - 1
            #     temp[index] = new[0]
            #     for s in new[1::-1]:
            #         temp.insert(index + 1, s)
            #     map_len = list(map(lambda s: len(s) > self.width // width, te)) 

            for i in code_to_index:
                original = i
                altered = original + temp[:i].count('\n')

                temp = temp[:altered] + code_to_index[i] + temp[altered:]

            string.append(temp)

        return string

    def partial_process_atrribs(self, strings: list[str], color: tuple[int, int, int], style: str, pos: list[int, int], codes: list[str], width: int, height: int) -> list[Section]:
        """Returns a semi-processed list of Sections (not accounting lines)"""

        semi_processed = []

        for string in strings:
            if len(string) > 0:
                splitstring = string.split('\n')

                if len(splitstring) > 1:
                    for part in splitstring:
                        semi_processed.append(Section(part, color, style, pos))

                        pos = [self.start[0], pos[1] + height]

                    pos[1] -= height   
                else:
                    semi_processed.append(Section(splitstring[0], color, style, pos))

                pos = [pos[0] + len(splitstring[-1]) * (width), pos[1]]
                        
            if codes:
                code = codes.pop(0)
                if code[2] == 'c':
                    color = self.escape_codes.get(code, color)

                else:
                    style = self.escape_codes.get(code, style)

        return semi_processed

    def process_text(self) -> None:
        """Internally processes the string. Use self.processed for results"""

        color = self.starting_color
        style = self.starting_style
        fontsize = self.font_size

        height = int(fontsize * self.fn_ptr_factor[1])
        width = int(fontsize * self.fn_ptr_factor[0])
        
        base = self.string.split('\n')
        string = self.remove_codes(base)  

        #self.logger.info(string)

        string = '\n'.join(string)
   
        self.processed = []
        
        pos = list(self.start)

        groups = self.escape_pattern.split(string)

        strings = groups[::2]
        codes = groups[1::2] if len(groups) > 1 else []

        semi_processed = self.partial_process_atrribs(strings, color, style, pos, codes, width, height)

        # Fully process attributes (account for lines)
        
        number_of_lines = 1
        pos = self.start[1]
        for group in semi_processed:
            if group.pos[1] != pos:
                pos = group.pos[1]
                number_of_lines += 1

        push = None

        index_to_start = 0

        if number_of_lines > self.start[1] + self.height:
            count = 1
            pos = self.start[1]
            for index, group in enumerate(semi_processed):
                if group.pos[1] != pos:
                    count += 1
                    pos = group.pos[1]
                    if count > number_of_lines - (self.start[1] + self.height):
                        push = number_of_lines - (self.start[1] + self.height)
                        index_to_start = index
                        break

        if not push: push = 0

        truncated = semi_processed[index_to_start:]
        
        self.processed = [Section(group.text, group.color, group.style, (group.pos[0], group.pos[1] - (height * push))) for group in truncated]
