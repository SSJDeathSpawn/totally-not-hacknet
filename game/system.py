import pygame
import asyncio

from custom_logging.logging import get_logger
from utils.id_generator import generate_id
from utils.ip_generator import generate_ip
from game.graphics import Graphics


logger = get_logger('game')


class System(object):
    def __init__(self, owner: str, memory: int, graphics):
        self.ID = f'SYSTEM-{generate_id()}'
        self.IP = generate_ip()

        self.owner = owner
        self.memory = memory
        self.graphics = graphics

        self.bootable_media = None
        self.os = None

        self.outputs = {
            'scan': 'Scanning for Bootable Media...',
            'found': 'Bootable Media found...',
            'not_found': 'Bootable Media not found...'
        }

        self.surface = self.graphics.draw_system_borders()

        logger.debug(f'Initialized System with ID {self.ID} and IP {self.IP}.')

    def event_handler(self):
        events = pygame.event.get()

        for event in events:
            if event.type == pygame.QUIT:
                logger.info('Exiting Application...')
                pygame.quit()
                exit()
                
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                for application in self.os.application_queue:
                    application.quit()

        for application in self.os.application_queue:
            application.event_queue += events


    def graphics_handler(self):
        self.graphics.conn_pygame_graphics.main()

    async def run_loops(self):
        logger.info('Starting System Processes...')
        await asyncio.gather(self.os.run_main_loop(), self.system_loop())

    async def system_loop(self):
        logger.info('Starting Main Loop...')
        while True:
            await asyncio.sleep(0)
            self.event_handler()
            self.graphics_handler()

    async def install_os(self):
        if not self.bootable_media:
            logger.critical('No bootable media. How did this even happen?')
            exit()
        await self.bootable_media.install(self)
        logger.info('Operating System Installed Successfully.')

    def output(self, message):
        pass
