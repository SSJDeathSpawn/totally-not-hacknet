import pygame

from custom_logging.logging import get_logger
from game.application import Application
from graphics.conn_pygame_graphics import Surface


logger = get_logger('game')


class Terminal(Application):
    def __init__(self, os, opened_by):
        super().__init__(os, opened_by, 50)

        self.surface = self.os.system.graphics.draw_application_window(540, 360, (0, 255, 0), 'TERMINAL')

        self.commands = {
            'pwd': self.pwd
        }

        self.content = f'{self.new_line()}'
        self.stdin = ''

    def new_line(self):
        pass

    def update_content(self, new):
        self.content += new
        if self.content.count('\n') > 300: self.content = '\n'.join(self.content.split('\n')[-300:])

    async def event_handler(self):
        await super().event_handler()

        if not self.current_event: return

        if self.current_event.type == pygame.KEYDOWN and self.current_event.key == pygame.K_RETURN:
            await self.run_command(self.stdin)
            self.stdin = ''
            self.update_content('\n')

        if self.current_event.type == pygame.TEXTINPUT:
            self.stdin += self.current_event.text
            self.update_content(self.current_event.text)

    async def graphics_handler(self):
        await super().graphics_handler()

        self.os.system.graphics.fill_application_window((0, 255, 0))
        

    async def run_command(self, stdin):
        args = stdin.split(' ')
        cmd = args.pop(0)
        await self.commands[cmd](args)

    async def pwd(self, args):
        pass
