from __future__ import annotations
from logging_module.custom_logging import get_logger
from utils.general_utils import generate_id
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.networking import Router

logger = get_logger('game')


class System(object):
    def __init__(self, owner: str, memory: int, graphics):
        self.ID: str = f'SYSTEM-{generate_id()}'

        self.network: Router

        self.owner: str = owner
        self.memory: int = memory

        self.running: bool = True
        
        # TODO: self.graphics = graphics
        
        # TODO: self.bootable_media = None
        
        # TODO: self.os = None

        # TODO: self.surface = self.graphics.get_system_surface()

        # TODO: self.graphics.outline_surface(self.surface, 'green', 1)

        logger.debug(f'Initialized System with ID {self.ID}.')

    def event_handler(self) -> None:
        """Handles pygame events"""

        pass

    def graphics_handler(self):
        """Handles graphics"""

        pass

    def install_os(self):
        """Installs an Operating System on the system"""

        if not self.bootable_media:
            logger.critical('No bootable media. How did this even happen?')
            exit()
        self.bootable_media.install(self)
        logger.info('Operating System Installed Successfully.')
