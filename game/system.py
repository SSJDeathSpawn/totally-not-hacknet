from __future__ import annotations
from game.storage_media import ExternalStorageMedium, InternalStorageMedium
from game.operating_system import OperatingSystem
from game.constants import DEFAULT_ROOTDIR_PATH
from logging_module.custom_logging import get_logger
from utils.general_utils import generate_id
from utils.deserializer import deserialize_root_directory
from game.graphics import Graphics
from game.constants import FPS
from typing import TYPE_CHECKING, Optional
if TYPE_CHECKING:
    from game.networking import Router

import pygame, pygame.key


class System(object):
    """Class representing a Computer System"""

    def __init__(self, owner: str, ram: int):
        self.logger = get_logger('game')
        
        self.ID: str = f'SYSTEM-{generate_id()}'

        self.network: Router

        self.owner: str = owner
        self.ram: int = ram
        self.clock = pygame.time.Clock()

        self.running: bool = True
        
        self.internal_storage_media: InternalStorageMedium = InternalStorageMedium()
        self.external_storage_media: Optional[ExternalStorageMedium] = None

        self.os: OperatingSystem = OperatingSystem(self, deserialize_root_directory(DEFAULT_ROOTDIR_PATH))
        self.graphics = Graphics(self)

        pygame.key.set_repeat(500, 200)

        self.logger.debug(f'Initialized System with ID {self.ID}')

    # def handle_boot(self) -> bool:
    #     """Handles boot"""
        
    #     if self.internal_storage_media.data and self.internal_storage_media.data.get_su_by_name('system'):
    #         # TODO: Encrypting and decrypting  
    #         # self.os = pickle.load(self.decipher(internal_storage_media.data.get_su_by_name('system').get_su_by_name('system.dat').get_contents()))(system, internal_storage_media.data)
    #         return True

    #     elif self.external_storage_media and self.external_storage_media.is_bootable:
    #         # TODO: Encrypting and decrypting  
    #         # self.os = pickle.load(self.decipher(external_storage_media.data.get_su_by_name('system').get_su_by_name('system.dat').get_contents()))(system, external_storage_media.data)
    #         return True

        # else:
        #     self.logger.critical('No Operating System found')
        #     return False

    def event_handler(self) -> None:
        """Handles pygame events"""

        pass

    def graphics_handler(self):
        """Handles graphics"""

        pass

    def run_os(self):
        """Runs the operating system installed"""
        if self.os:
            self.os.main_loop(self.clock, FPS)

    # def install_os(self):
    #     """Installs an Operating System on the system"""
    #
    #     if not self.bootable_media:
    #         self.logger.critical('No bootable media. How did this even happen?')
    #         exit()
    #     self.bootable_media.install(self)
    #     self.logger.info('Operating System Installed Successfully.')
