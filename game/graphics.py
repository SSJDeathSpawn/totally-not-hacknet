from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from logging_module.custom_logging import get_logger
from graphics.conn_pygame_graphics import ConnPygameGraphics, Surface
from graphics.constants import RESOLUTION
if TYPE_CHECKING:
    from logging import Logger
    from game.system import System

import pygame


class Graphics(object):
    """System graphics layer"""

    def __init__(self, system: System) -> None:
        self.logger: Logger = get_logger('graphics')
        self.system: System = system

        self.conn_pygame_graphics: ConnPygameGraphics = ConnPygameGraphics(*RESOLUTION, 'Totally Not Hacknet')

    def render_surfaces(self):
        """Blits all surfaces on to the original surface"""

        self.conn_pygame_graphics.main()

    def draw_image(self, surface: Surface, name: str, pos: tuple[int, int] = (0, 0), dimensions: Optional[tuple[int, int]] = None) -> None:  # Subject to change

        if not dimensions:
            self.conn_pygame_graphics.blit_image(pos, name, 0, 0, surface)

        else:
            self.conn_pygame_graphics.blit_image(pos, name, dimensions[0], dimensions[1], surface)

    def draw_desktop_icon(self) -> None:  # Subject to change
        pass

    def get_surface(self, width: int, height: int, pos: list[int, int]) -> Surface:
        """Returns a surface"""

        surface = Surface((width, height), pos)
        self.conn_pygame_graphics.push_surface(surface)
        return surface

    @staticmethod
    def clear_surface(surface: Surface, area: Optional[tuple[int, int, int, int]]=None):  # x, y, width, height
        """Clears a given surface"""

        surface.fill(pygame.Color('black'))
        # Do area stuff
