from __future__ import annotations
from typing import TYPE_CHECKING
from game.applications.application import MasterApplication
from graphics.conn_pygame_graphics import Surface
from graphics.constants import DESKTOP_BACKGROUND_PATH, RESOLUTION
from typing import Optional
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


class Desktop(MasterApplication):
    """Class representing the desktop"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):
        super().__init__(host, opened_by)

        self.surface: Surface = self.graphics.get_surface(*RESOLUTION, [0, 0])

    def graphics_handler(self) -> None:
        super().graphics_handler()
        self.graphics.draw_image(self.copy_surface, DESKTOP_BACKGROUND_PATH, (0, 0))
        self.surface.blit(self.copy_surface, (0, 0))

    def events_handler(self) -> None:
        super().events_handler()
