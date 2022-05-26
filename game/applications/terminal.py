from __future__ import annotations

import math
from typing import Optional, TYPE_CHECKING

import pygame

from game.applications.application import Application
from game.debug_constants import HOSTNAME
from graphics.conn_pygame_graphics import Surface
from graphics.text import Text, Section
from graphics.constants import UM_FNT_PT_FACTOR, TERMINAL_CURSOR_COLOR, TERMINAL_FONT_SIZE, TERMINAL_CONTENT_COLOR, TITLEBAR_DEFAULT_HEIGHT, CODE_FORMATTING, TERMINAL_COLOR_CODES, TERMINAL_BGCOLOR, TERMINAL_COLOR_FORMATTING
if TYPE_CHECKING:
    from game.command import Response
    from game.storage_system.directory import Directory
    from game.operating_system import OperatingSystem


class Terminal(Application):
    """Class representing the terminal"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None) -> None:
        super().__init__(host, opened_by)

        self.surface: Surface = self.graphics.get_app_surface(800, 600, [150, 150])

        self.font_size = TERMINAL_FONT_SIZE

        self.current_dir: Directory = self.host.root
        self.stdin: str = ''
        self.content: str = self.get_new_line()
        self.personal_backlog: list[str] = self.host.command_backlog + ['']
        self.new_commands_start: int = len(self.personal_backlog) - 1
        self.pointer = -1
        
        self.text: Text = Text(self.content + self.stdin, TERMINAL_CONTENT_COLOR, 'regular', self.font_size, (5, TITLEBAR_DEFAULT_HEIGHT + 5), self.surface.get_width(), self.surface.get_height(), (5, 5), additional_colors = TERMINAL_COLOR_CODES)

        self.processed_text: list[Section] = self.text.get_processed_text()

        self.cur_pos: int = 0  # Relative to the start of stdin
        self.max_lines: int = ((self.surface.get_height() - TITLEBAR_DEFAULT_HEIGHT) // self.font_size * UM_FNT_PT_FACTOR[1]) - 1

        self.cursor = pygame.Surface((self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]), pygame.SRCALPHA)
        self.cursor.fill(TERMINAL_CURSOR_COLOR)
        self.cursor.set_alpha(155)

        self.env_var = dict()
        self.bottom_line = 0

    # Helpers

    @property
    def eff_surf_width(self) -> float:
        """Returns effective surface width"""

        font_size = self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]

        return ((self.surface.get_width() - self.text.start[0] - self.text.end_padding[0]) // font_size[0]) * font_size[0]

    def set_cursor_alpha(self) -> None:
        """Sets the alpha of the cursor to give a cursor effect"""

        t_half = 600  # in ticks
        val = lambda x: math.sin((x * math.pi) / 2)
        alpha = 155 * val((pygame.time.get_ticks()/t_half) % 2)
        self.cursor.set_alpha(alpha)

    def get_number_of_lines(self) -> int:
        """Returns the number of lines in the terminal (excludes current line)"""

        font_size = self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]
        
        content_raw = Text.get_uncoded_text(self.content)

        new_lines = -1
        for line in content_raw.split('\n'):
            new_lines += ((len(line) * font_size[0]) // self.eff_surf_width)
            new_lines += 1

        input_contrib = (len(content_raw.split('\n')[-1]) % (self.eff_surf_width // font_size[0]) + self.cur_pos) // (self.eff_surf_width // font_size[0])
        new_lines += input_contrib

        return new_lines

    def get_cursor_rend_pos(self) -> tuple[int, int]:
        """Gets the cursor position at the current point of time"""

        font_size = self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]
        content = len(Text.get_uncoded_text(self.content).split('\n')[-1])

        x = self.text.start[0] + (((content + self.cur_pos) * font_size[0]) % (self.eff_surf_width))
        y = self.text.start[1] + self.get_number_of_lines() * font_size[1]

        return x, y

    def get_input(self) -> str:
        """Gets input from the terminal"""

        pass
       
    def intellisense(self, word: str) ->  str:
        """Returns the appropriate color for the first first in stdin"""

        if word in self.host.commands.keys():
            return CODE_FORMATTING['CYAN']

        elif word.startswith('./'):
            if word[2:] in list(map(lambda su: su.get_name(), self.current_dir.get_contents())):
                return CODE_FORMATTING['CYAN']

        return CODE_FORMATTING['RED']

    # Main

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_app_surface(self.surface, TERMINAL_BGCOLOR)

        for section in self.processed_text:
            if self.surface.get_height() - 5 > section.pos[1] >= 5 + TITLEBAR_DEFAULT_HEIGHT:    
                self.graphics.conn_pygame_graphics.render_text(section.style, self.text.font_size, section.text, section.color, section.pos, surface=self.surface)

        self.set_cursor_alpha()
        self.surface.blit(self.cursor, self.get_cursor_rend_pos())

        self.graphics.draw_outlines(self.surface)
        
    def events_handler(self) -> None:
        super().events_handler()

        for event in self.events:
            if event.type == pygame.TEXTINPUT:
                raw_stdin = Text.get_uncoded_text(self.stdin)
                raw_stdin = raw_stdin[:self.cur_pos] + event.text + raw_stdin[self.cur_pos:]

                try: 
                    self.stdin = self.intellisense(raw_stdin.split(' ')[0]) + raw_stdin.split(' ')[0] + CODE_FORMATTING['RESET'] + (' ' if ' ' in raw_stdin else '') + ' '.join(raw_stdin.split(' ')[1:])
                except Exception as e:
                    self.logger.error(e)

                self.personal_backlog[self.pointer] = self.stdin
                self.update_cur_pos(1)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.cur_pos > 0:
                        raw_stdin = Text.get_uncoded_text(self.stdin)
                        raw_stdin = raw_stdin[:self.cur_pos - 1] + raw_stdin[self.cur_pos:]

                        self.stdin = self.intellisense(raw_stdin.split(' ')[0]) + raw_stdin.split(' ')[0] + CODE_FORMATTING['RESET'] + (' ' if ' ' in raw_stdin else '') + ' '.join(raw_stdin.split(' ')[1:])

                    # Else annoying sound
                    self.update_cur_pos(-1)

                if event.key == pygame.K_RETURN:
                    raw_stdin = Text.get_uncoded_text(self.stdin)
                    self.execute_command(raw_stdin)
                    self.content += self.get_new_line()

                    # backlog
                    if self.stdin in self.personal_backlog[:self.pointer]:
                        self.personal_backlog.remove(self.stdin)
                    if self.stdin:    
                        self.personal_backlog.append('')

                    self.stdin = ''
                    self.cur_pos = 0
                
                if event.key == pygame.K_UP:
                    if abs(self.pointer) < len(self.personal_backlog):
                        self.pointer -= 1
                    # Else annoying sound
                    self.stdin = self.personal_backlog[self.pointer]
                    self.cur_pos = len(Text.get_uncoded_text(self.stdin))
                
                if event.key == pygame.K_DOWN:
                    if self.pointer < -1:
                        self.pointer += 1
                    # Else annoying sound
                    self.stdin = self.personal_backlog[self.pointer]
                    self.cur_pos = len(Text.get_uncoded_text(self.stdin))
                
                if event.key == pygame.K_LEFT:
                    self.update_cur_pos(-1)

                if event.key == pygame.K_RIGHT:
                    self.update_cur_pos(1) 
                
                if self.get_number_of_lines() >= self.max_lines:
                    if event.key == pygame.K_PAGEUP:
                        self.bottom_line = max(min(self.bottom_line - 1, self.get_number_of_lines()), self.max_lines)

                    if event.key == pygame.K_PAGEDOWN:
                        self.bottom_line = max(min(self.bottom_line + 1, self.get_number_of_lines()), self.max_lines)
            
            if event.type in [pygame.TEXTINPUT, pygame.KEYDOWN]:
                self.text.update_text(self.content + self.stdin, True)

                if event.type == pygame.TEXTINPUT or event.key not in [pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
                    if self.get_number_of_lines() >= self.max_lines:
                        self.bottom_line = self.get_number_of_lines()
                    else:
                        self.bottom_line = 0

                if self.get_number_of_lines() > self.max_lines:
                    self.text.update_starting_pos((5, TITLEBAR_DEFAULT_HEIGHT + 5 - (self.text.font_size * UM_FNT_PT_FACTOR[1] * (self.bottom_line - self.max_lines))))
                else:
                    self.text.update_starting_pos((5 , TITLEBAR_DEFAULT_HEIGHT + 5))

                self.processed_text = self.text.get_processed_text()
                
    def update_cur_pos(self, amt: int) -> None:
        """Update the cursor position relative to stdin"""
        
        if (self.cur_pos == 0 and amt < 0) or (self.cur_pos == len(Text.get_uncoded_text(self.stdin)) and amt > 0):
            # Annoying Sound Effect in future
            return
            
        self.cur_pos += amt

    def get_new_line(self) -> str:
        """Returns a new terminal line"""

        return TERMINAL_COLOR_FORMATTING['KALI-BLUE'] + '┌──[' + TERMINAL_COLOR_FORMATTING['KALI-ORANGE'] + HOSTNAME + TERMINAL_COLOR_FORMATTING['KALI-BLUE'] + ']─[' + CODE_FORMATTING['RESET'] + self.current_dir.get_path() + TERMINAL_COLOR_FORMATTING['KALI-BLUE'] + ']\n' + '└────' + TERMINAL_COLOR_FORMATTING['KALI-ORANGE'] + '$ ' + CODE_FORMATTING['RESET']

    def execute_command(self, command: str) -> None:
        """Executes a terminal command and returns a Response object"""

        if command == '':
            self.content += '\n'
            return

        args = command.split(' ')
        name = args[0]
        args = args[1:]

        self.content += self.stdin + '\n'

        response = self.host.execute_command(self, name, args)
        
        if response.stdout: 
            self.content += response.stdout + '\n'
        if response.stderr:
            self.content += CODE_FORMATTING['RED'] + response.stderr + '\n'
    
    def quit(self) -> None:
        """Quits the terminal"""

        self.host.command_backlog += self.personal_backlog[self.new_commands_start:]
        super().quit()
