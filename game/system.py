from __future__ import annotations

import pickle

from game.storage_media import ExternalStorageMedium, InternalStorageMedium
from game.operating_system import OperatingSystem
from game.constants import DEFAULT_ROOTDIR_PATH
from logging_module.custom_logging import get_logger
from utils.general_utils import generate_id
from utils.deserializer import deserialize_root_directory
from game.graphics import Graphics
from game.constants import FPS, BOOT_MEDIA_ROOTDIR_PATH, DEFAULT_ROOTDIR_PATH
from typing import TYPE_CHECKING, Optional
from game.networking import Router

import pygame, pygame.key


class System(object):
    """Class representing a Computer System"""

    def __init__(self, owner: str, ram: int, fullscreen: bool = False):
        self.logger = get_logger('game')
        
        self.ID: str = f'SYSTEM-{generate_id()}'

        self.network: Router = Router()

        self.owner: str = owner
        self.ram: int = ram
        self.clock = pygame.time.Clock()

        self.running: bool = True
        
        self.internal_storage_media: InternalStorageMedium = InternalStorageMedium(DEFAULT_ROOTDIR_PATH)
        self.external_storage_media: Optional[ExternalStorageMedium] = ExternalStorageMedium('TOTALLY NOT HACKNET v0.0.1', BOOT_MEDIA_ROOTDIR_PATH, is_bootable=True)

        self.graphics = Graphics(self, fullscreen=fullscreen)
        # self.os: OperatingSystem = OperatingSystem(deserialize_root_directory(DEFAULT_ROOTDIR_PATH))
        # self.os: OperatingSystem = OperatingSystem(deserialize_root_directory(self.external_storage_media.get_data()))

        if not self.handle_boot():
            return

        pygame.key.set_repeat(200, 40)

        self.logger.debug(f'Initialized System with ID {self.ID}')

        self.run_os()

    
    @property
    def os(self) -> OperatingSystem:
        return self._os

    @os.setter
    def os(self, __value) -> None:
        self._os = __value
        self._os.graphics = self.graphics
        # Other system attribs

    def reboot(self) -> bool:
        """Reboots the system"""

        self.os.send_shutdown_signal()
        self.handle_boot()

    def handle_boot(self) -> bool:
        """Handles boot"""

        self.internal_storage_media = InternalStorageMedium(DEFAULT_ROOTDIR_PATH)
        
        if self.internal_storage_media.root and self.internal_storage_media.root.get_su_by_name('system'):
            self.logger.info('Loading Operating System from Internal Storage Media')

            root = self.internal_storage_media.get_data()
            try:
                os_file = root.get_su_by_name('system').get_su_by_name('system.bin')
            except AttributeError:
                self.logger.critical('Internal OS corrupted.')
            else:
                os = int(os_file.get_contents()).to_bytes(os_file.metadata['length'], 'big')
                os = pickle.loads(os)
                os.root = root
                os.reboot = self.reboot

                self.os = os

                return True

        if self.external_storage_media and self.external_storage_media.is_bootable:
            self.logger.info('Trying to boot from external storage media.')

            root = self.external_storage_media.get_data()
            try:
                progenitor_os_file = root.get_su_by_name('system').get_su_by_name('system.bin')
            except AttributeError:
                self.logger.critical('Game is unplayable, external boot medium corrupted.')
                return False
            
            progenitor = int(progenitor_os_file.get_contents()).to_bytes(progenitor_os_file.metadata['length'], 'big')
            progenitor = pickle.loads(progenitor)
            progenitor.root = root
            progenitor.reboot = self.reboot

            self.os = progenitor
            
            return True

        else:
            self.logger.critical('No Operating System found')
            return False

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

    def install_os(self):
        """Installs an Operating System on the system"""
    
        if not self.bootable_media:
            self.logger.critical('No bootable media. How did this even happen?')
            exit()
        self.bootable_media.install(self)
        self.logger.info('Operating System Installed Successfully.')
