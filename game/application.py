import pygame

from custom_logging.logging import get_logger


logger = get_logger('game')


class Application(object):
    def __init__(self, os, opened_by, memory):
        self.os = os
        self.opened_by = opened_by

        self.memory = memory # In MBs

        self.event_queue = []
        self.current_event = None
        self.modifiers = [False, False, False] # Ctrl, Shift, Alt

        logger.debug(f'Started a {self.__class__.__name__} Instance requested by OS with username {opened_by.username} ({opened_by.system.IP}).')

    async def event_handler(self):
        if len(self.event_queue) < 1:
            self.current_event = None
            return

        self.current_event = self.event_queue.pop(0)

        if self.current_event.type in (pygame.KEYDOWN, pygame.KEYUP):
            if self.current_event.key in (pygame.K_LALT, pygame.K_RALT):
                self.modifiers[2] = False if self.current_event.type == pygame.KEYUP else True
            elif self.current_event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                self.modifiers[1] = False if self.current_event.type == pygame.KEYUP else True
            elif self.current_event.key in (pygame.K_LCTRL, pygame.K_RCTRL):
                self.modifiers[0] = False if self.current_event.type == pygame.KEYUP else True

        if self.modifiers[2]:
            if self.current_event[0] == pygame.K_F4:
                await self.quit()

    async def graphics_handler(self):
        pass

    async def run(self):
        await self.event_handler()
        await self.graphics_handler()

    async def idle(self):
        pass

    async def input_event(self, event):
        self.event_queue.append(event)

    def quit(self):
        logger.debug(f'Quitting {self.__class__.__name__} Instance.')
        self.os.system.graphics.conn_pygame_graphics.pop_surface(self.surface)
        self.os.application_queue.remove(self)
        self.os.applications[self.__class__.__name__.upper()]['instances'].remove(self)
