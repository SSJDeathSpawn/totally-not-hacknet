from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame

from game.applications.application import Application
from game.storage_system.directory import Directory
from game.storage_system.storage_unit import StorageUnit
from graphics.conn_pygame_graphics import Surface
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


class Explorer(Application):
    """Class representing the file explorer"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):
        super().__init__(host, opened_by)

        self.surface: Surface = self.host.system.graphics.get_app_surface(800, 600, [200, 200])
        self.current_dir: Directory = self.host.root

        self.scroll: int = 0
        self.storage_units: dict[StorageUnit, bool] = dict.fromkeys(self.current_dir.get_contents(), False)

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_app_surface(self.surface)

    def events_handler(self) -> None:
        super().events_handler()

        for event in self.events:
            pass
