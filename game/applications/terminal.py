from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Union
from game.applications.application import Application
from game.debug_constants import HOSTNAME
from graphics.conn_pygame_graphics import Surface
from graphics.text import Text, Section
from graphics.constants import UM_FNT_PT_FACTOR, TERMINAL_CURSOR_COLOR, TERMINAL_FONT_SIZE, TERMINAL_CONTENT_COLOR, TITLEBAR_DEFAULT_HEIGHT, CODE_FORMATTING
if TYPE_CHECKING:
    from game.command import Response
    from game.storage_system.directory import Directory
    from game.operating_system import OperatingSystem

import pygame


class Terminal(Application):
    """Class representing the terminal"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None) -> None:
        super().__init__(host, opened_by)

        self.surface: Surface = self.host.system.graphics.get_app_surface(800, 600, [150, 150])

        self.font_size = TERMINAL_FONT_SIZE

        self.current_dir: Directory = self.host.root
        self.stdin: str = ''
        self.content: str = self.get_new_line()
        self.personal_backlog = self.host.command_backlog + ['']
        self.new_commands = len(self.personal_backlog)
        self.backlog_alteration = dict()
        self.pointer = -1
        
        self.text: Text = Text(self.content + self.stdin, TERMINAL_CONTENT_COLOR, 'regular', self.font_size, (0, TITLEBAR_DEFAULT_HEIGHT + 0), self.surface.get_width(), self.surface.get_height())

        self.processed_text: list[Section] = self.text.get_processed_text()

        self.cur_pos: int = 0  # Relative to the start of stdin

        self.cursor = pygame.Surface((self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]), pygame.SRCALPHA)
        self.cursor.fill(TERMINAL_CURSOR_COLOR)
        self.cursor.set_alpha(0)


    # Helpers

    def set_cursor_alpha(self) -> None:
        """Sets the alpha of the cursor to give a cursor effect"""

        t_half = 500  # in ticks
        val = lambda x: 1 - pow(1 - x, 4)
        pass_val = lambda x: (t_half - abs(x % (2 * t_half) - t_half)) / t_half
        alpha = 155 * val(pass_val(pygame.time.get_ticks()))
        self.cursor.set_alpha(alpha) 

    # Main

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_app_surface(self.surface)

        for section in self.processed_text:
            self.graphics.conn_pygame_graphics.render_text(section.style, self.text.font_size, section.text, section.color, section.pos, surface=self.surface)
        
    def events_handler(self) -> None:
        super().events_handler()

        for event in self.events:
            if event.type == pygame.TEXTINPUT:
                self.stdin += event.text
                self.personal_backlog[self.pointer] = self.stdin 
                self.update_cur_pos(1)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.stdin = self.stdin[:-1]
                    self.update_cur_pos(-1)

                if event.key == pygame.K_RETURN:
                    self.execute_command(self.stdin)
                    self.content += self.get_new_line()
                    self.stdin = ''
                    self.personal_backlog.append('')
                
                if event.key == pygame.K_UP:
                    if abs(self.pointer) < len(self.personal_backlog):
                        self.pointer -= 1
                    #Else annoying sound
                    self.stdin = self.personal_backlog[self.pointer]
                
                if event.key == pygame.K_DOWN:
                    if self.pointer < -1:
                        self.pointer += 1
                    #Else annoying sound
                    self.stdin = self.personal_backlog[self.pointer]
            
            if event.type in [pygame.TEXTINPUT, pygame.KEYDOWN]:
                self.text.update_text(self.content + self.stdin, True)
                self.processed_text = self.text.get_processed_text()
                
    def update_cur_pos(self, amt: int) -> None:
        """Update the cursor position relative to stdin"""
        
        if (self.cur_pos == 0 and amt < 0) or (self.cur_pos == len(self.stdin) and amt > 0):
            # Annoying Sound Effect in future
            return
            
        self.cur_pos += amt

    def get_new_line(self) -> str:
        """Returns a new terminal line"""

        return CODE_FORMATTING['GREEN'] + HOSTNAME + CODE_FORMATTING['RESET'] + ':' + CODE_FORMATTING['BLUE'] + self.current_dir.get_path() + CODE_FORMATTING['RESET'] + '$ '

    def execute_command(self, command: str) -> None:
        """Executes a terminal command and returns a Response object"""

        args = command.split(' ')
        name = args[0].lower()
        self.logger.info('reaching here')
        args = args[1:]
        self.logger.info('yeah')

        response = self.host.execute_command(self, name, args)

        self.content += self.stdin + '\n' 
        if response.stdout: 
            self.content += response.stdout + '\n'
        if response.stderr:
            self.content += response.stderr + '\n'
    
    def quit(self, ) -> None:
        self.host.command_backlog += self.personal_backlog[self.new_commands:]
        super().quit()
