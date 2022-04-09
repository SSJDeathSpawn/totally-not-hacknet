from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from logging_module.custom_logging import get_logger
from graphics.conn_pygame_graphics import ConnPygameGraphics, Surface
from graphics.constants import RESOLUTION, APPLICATION_MIN_HEIGHT, APPLICATION_MIN_WIDTH, TITLEBAR_1PX_DIMENSIONS, TITLEBAR_DEFAULT_HEIGHT, TITLEBAR_OPTIONS_PATH, TITLEBAR_OPTIONS_DIMENSIONS, TITLEBAR_1PX_PATH
if TYPE_CHECKING:
    from logging import Logger
    from game.system import System

import pygame


class Graphics(object):
    """System graphics layer"""

    def __init__(self, system: System, fullscreen: bool = False) -> None:
        self.logger: Logger = get_logger('graphics')
        self.system: System = system

        self.conn_pygame_graphics: ConnPygameGraphics = ConnPygameGraphics(*RESOLUTION, 'Totally Not Hacknet', fullscreen=fullscreen)

    def render_surfaces(self):
        """Blits all surfaces on to the original surface"""

        self.conn_pygame_graphics.main()

    def remove_surface(self, surface: Surface) -> None:
        """Removes the given surface from the render queue"""

        self.logger.debug('Removing surface')
        self.conn_pygame_graphics.remove_surface(surface)
            
    def swap_surfaces(self, surface: Surface) -> Surface:
        """Swaps the application surface with the conn_pygame_graphics surface"""

        rendered_surface = self.conn_pygame_graphics.get_surface_by_id(surface.ID)
        index = self.conn_pygame_graphics.render_queue.index(rendered_surface)

        self.conn_pygame_graphics.render_queue[index] = surface
        # self.logger.debug(f'ORIGINAL -> {id(surface)} FAKE -> {id(rendered_surface)}')

        rendered_surface.pos = surface.pos.copy()
        
        return rendered_surface

    def draw_image(self, surface: Surface, name: str, pos: tuple[int, int] = (0, 0), dimensions: Optional[tuple[int, int]] = None) -> None:  # Subject to change

        if not dimensions:
            self.conn_pygame_graphics.blit_image(pos, name, 0, 0, surface)

        else:
            self.conn_pygame_graphics.blit_image(pos, name, dimensions[0], dimensions[1], surface)

    def draw_desktop_icon(self) -> None:  # Subject to change
        pass
    
    def get_surface(self, width: int, height: int, pos: list[int, int], push: bool = True) -> Surface:
        """Returns a surface"""

        surface = Surface((width, height), pos)
        if push:
            self.conn_pygame_graphics.push_surface(surface)
        return surface

    def get_app_surface(self, width: int, height: int, pos: list[int ,int]) -> Optional[Surface]:
        """Returns a surface with the titlebar in it or nothing if width or height is too small"""

        if width < APPLICATION_MIN_WIDTH or height < APPLICATION_MIN_HEIGHT:
            return None

        padding = 0
        surface = self.get_surface(width, height, pos, False)
        self.conn_pygame_graphics.blit_image((0, 0), TITLEBAR_1PX_PATH, width, TITLEBAR_DEFAULT_HEIGHT, surface)

        options_width = int(TITLEBAR_OPTIONS_DIMENSIONS[0]/TITLEBAR_OPTIONS_DIMENSIONS[1] * TITLEBAR_DEFAULT_HEIGHT)
        options_pos = (width-options_width-padding,0)

        self.conn_pygame_graphics.blit_image(options_pos, TITLEBAR_OPTIONS_PATH, options_width, TITLEBAR_DEFAULT_HEIGHT, surface)

        self.conn_pygame_graphics.push_surface(surface)

        return surface
            

    def clear_surface(self, surface: Surface, area: Optional[tuple[int, int, int, int]]=None):  # x, y, width, height
        """Clears a given surface"""

        if not area:
            surface.fill(pygame.Color('black'))

        else:
            surface.fill(pygame.Color('black'), pygame.Rect(*area))
        

    def clear_app_surface(self, surface: Surface):
        """Clears everything on a given surface except for the title bar"""

        self.clear_surface(surface, (0, TITLEBAR_DEFAULT_HEIGHT, surface.get_width(), surface.get_height() - TITLEBAR_DEFAULT_HEIGHT))
