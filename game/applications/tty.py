from __future__ import annotations

from typing import TYPE_CHECKING
from threading import Thread

import pygame

from game.applications.application import Application
from graphics import RESOLUTION, TTY_FONT_SIZE, BETTER_WHITE, WHITE, BLACK, UM_FNT_PT_FACTOR, TTY_TEXT_PADDING
from graphics import Text, Section
if TYPE_CHECKING:
    from game.storage_system import Directory
    from game import OperatingSystem    


class TeleTypeWriter(Application):
    """Tele TYpe writer"""

    def __init__(self, host: OperatingSystem, opened_by: OperatingSystem | None = None) -> None:
        super().__init__(host, opened_by)

        self.surface = self.host.graphics.get_surface(RESOLUTION[0] * 9/10, RESOLUTION[1] * 9/10, [RESOLUTION[0] * 1/20, RESOLUTION[1] * 1/20])

        self.font_size = TTY_FONT_SIZE

        
        # # self.current_dir: Directory = self.host.root.get_su_by_name('root')
        self.current_dir: Directory = self.host.root

        self.stdin: str = ''
        self.content: str = self.get_new_line()
        
        self.personal_backlog: list[str] = self.host.command_backlog + ['']
        self.new_commands_start: int = len(self.personal_backlog) - 1
        self.pointer = -1
        
        self.text: Text = Text(self.content + self.stdin, WHITE, 'regular', self.font_size, TTY_TEXT_PADDING, self.surface.get_width(), self.surface.get_height(), TTY_TEXT_PADDING)

        self.processed_text: list[Section] = self.text.get_processed_text()

        self.cur_pos: int = 0  # Relative to the start of stdin

        self.cursor = pygame.Surface((self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]), pygame.SRCALPHA)
        self.cursor.fill(BETTER_WHITE)

        self.env_var = dict()
        self.max_lines: int = ((self.surface.get_height()) // (self.font_size * UM_FNT_PT_FACTOR[1])) - 1
        self.bottom_line = 0
        self.running_command: Thread | None = None
        self.hide_input: bool = False
    
    # Helpers

    @property
    def eff_surf_width(self) -> float:
        """Returns effective surface width"""

        font_size = self.font_size * UM_FNT_PT_FACTOR[0], self.font_size * UM_FNT_PT_FACTOR[1]

        return ((self.surface.get_width() - self.text.start[0] - self.text.end_padding[0]) // font_size[0]) * font_size[0]

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

    def quit(self) -> None:
        """Shuts down the system"""
        
        #TODO: Change after implementing proper shutdown
        super().quit()
        self.host.send_shutdown_signal()

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:

        self.graphics.clear_surface(self.surface, BLACK)

        for section in self.processed_text:
            if self.surface.get_height() >= section.pos[1] >= 0:
                self.graphics.conn_pygame_graphics.render_text(section.style, self.text.font_size, section.text, section.color, section.pos, surface=self.surface)

        self.surface.blit(self.cursor, self.get_cursor_rend_pos())
        self.graphics.draw_outline(self.surface)

    def events_handler(self) -> None:

        if self.running_command and not self.running_command.is_alive():
            try:
                self.running_command.start()
                self.stdin = ''
                self.cur_pos = 0
                self.update_text()
            except RuntimeError:
                self.running_command = None
                
        for event in self.events:

            if event.type == pygame.TEXTINPUT:
                raw_stdin = Text.get_uncoded_text(self.stdin)
                raw_stdin = raw_stdin[:self.cur_pos] + event.text + raw_stdin[self.cur_pos:]
                self.stdin = raw_stdin

                self.personal_backlog[self.pointer] = self.stdin
                self.update_cur_pos(1)
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if self.cur_pos > 0:
                        raw_stdin = Text.get_uncoded_text(self.stdin)
                        raw_stdin = raw_stdin[:self.cur_pos - 1] + raw_stdin[self.cur_pos:]

                        self.stdin = raw_stdin

                    # Else annoying sound
                    self.update_cur_pos(-1)

                if self.running_command is None:
                    if event.key == pygame.K_RETURN:
                        raw_stdin = Text.get_uncoded_text(self.stdin)
                        self.running_command = Thread(target=self.execute_command, args=(raw_stdin,))

                        # backlog
                        if self.stdin in self.personal_backlog[:self.pointer]:
                            self.personal_backlog.remove(self.stdin)
                        if self.stdin:    
                            self.personal_backlog.append('')

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
            
            if event.type in [pygame.TEXTINPUT, pygame.KEYDOWN]:
                self.update_text(event)

    def printf(self, text: str) -> None:
        """Print text in the terminal"""

        self.content += text
        self.update_text()

    def get_input(self, hide: bool=False) -> str:
        """Gets user Input"""

        self.hide_input = hide

        listening = True
        while listening:
            for event in self.events:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    stdin = '•' * len(self.stdin) if self.hide_input else self.stdin
                    self.content += stdin + '\n'

                    output = self.stdin

                    self.stdin = ''
                    stdin = '•' * len(self.stdin) if self.hide_input else self.stdin
                    self.cur_pos = 0
                    self.hide_input = False 

                    event_to_remove = event
                    listening = False
            
        self.events.remove(event_to_remove)    
        return output

    def update_text(self, event=None) -> None:
        """Updates text"""
        
        stdin = '•' * len(self.stdin) if self.hide_input else self.stdin
        self.text.update_text(self.content + stdin, True)

        if event:
            if event.type == pygame.TEXTINPUT or event.key not in [pygame.K_PAGEDOWN, pygame.K_PAGEUP]:
                if self.get_number_of_lines() >= self.max_lines:
                    self.bottom_line = self.get_number_of_lines()
                else:
                    self.bottom_line = 0

        if self.get_number_of_lines() > self.max_lines:
            self.text.update_starting_pos((TTY_TEXT_PADDING[0], TTY_TEXT_PADDING[1] - (self.text.font_size * UM_FNT_PT_FACTOR[1] * (self.bottom_line - self.max_lines))))
        else:
            self.text.update_starting_pos(TTY_TEXT_PADDING)

        self.processed_text = self.text.get_processed_text()

    def update_cur_pos(self, amt: int) -> None:
        """Update the cursor position relative to stdin"""
        
        if (self.cur_pos == 0 and amt < 0) or (self.cur_pos == len(Text.get_uncoded_text(self.stdin)) and amt > 0):
            # Annoying Sound Effect in future
            return
            
        self.cur_pos += amt
                  
    def get_new_line(self) -> str:
        """Returns a new terminal line"""

        return self.host.username + ':' + self.current_dir.get_path() + '$ '

    def execute_command(self, command: str) -> None:
        """Executes a terminal command and returns a Response object"""

        if command == '':
            self.content += '\n'
        
        else:
            args = command.split(' ')
            name = args[0]
            args = args[1:]

            self.content += self.stdin + '\n'

            response = self.host.execute_command(self, name, args)
            
            if response.stdout: 
                self.content += response.stdout + '\n'
            if response.stderr:
                self.content += response.stderr + '\n'  

        self.content += self.get_new_line()
        self.update_text()