from __future__ import annotations
from typing import TYPE_CHECKING, Optional, Type
from logging_module.custom_logging import get_logger
from graphics.conn_pygame_graphics import ConnPygameGraphics, Surface
from graphics.constants import RESOLUTION, APPLICATION_MIN_HEIGHT, APPLICATION_MIN_WIDTH, TITLEBAR_1PX_DIMENSIONS, TITLEBAR_DEFAULT_HEIGHT, TITLEBAR_OPTIONS_PATH, TITLEBAR_OPTIONS_DIMENSIONS, TITLEBAR_1PX_PATH, UM_FNT_PT_FACTOR, WHITE
if TYPE_CHECKING:
    from logging import Logger
    from game.system import System
    from game.storage_system.storage_unit import StorageUnit

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
            

    def clear_surface(self, surface: Surface, color: tuple[int, int, int, int], area: Optional[tuple[int, int, int, int]]=None):  # x, y, width, height
        """Clears a given surface"""

        if not area:
            surface.fill(color)

        else:
            surface.fill(color, pygame.Rect(*area))
        

    def clear_app_surface(self, surface: Surface, color: tuple[int, int, int, int]):
        """Clears everything on a given surface except for the title bar"""

        self.clear_surface(surface, color, (0, TITLEBAR_DEFAULT_HEIGHT, surface.get_width(), surface.get_height() - TITLEBAR_DEFAULT_HEIGHT))

    def draw_explorer_icons(self, surface: Surface, icons: dict[str, tuple[str, bool]], icon_dims: tuple[int, int], padding: tuple[int, int, int, int], fontsize: int, textcolor: tuple[int, int, int, int]=WHITE):
        """Draws the icons in the explorer window
         
        Args:
            padding: top, right, bottom, left
        """

        max_per_row = surface.get_width() // (icon_dims[0] + padding[1] + padding[3])

        row_width = max_per_row * (icon_dims[0] + padding[1] + padding[3])

        x_margin = surface.get_width() - row_width          

        for index, icon in enumerate(icons.items()):
            x_cell = index % max_per_row
            y_cell = index // max_per_row

            x = (x_margin / 2) + (padding[1] + padding[3] + icon_dims[0]) * x_cell + padding[1]
            y = (padding[2] + padding[0] + icon_dims[1]) * y_cell + padding[0]

            if 0 < y < surface.get_height():
                self.conn_pygame_graphics.blit_image((x, y), icon[1][0], width=icon_dims[0], height=icon_dims[1], surface=surface)

        for index, icon in enumerate(icons.items()):
            x_cell = index % max_per_row
            y_cell = index // max_per_row

            x = (x_margin / 2) + (padding[1] + padding[3] + icon_dims[0]) * x_cell + padding[1]
            y = (padding[2] + padding[0] + icon_dims[1]) * y_cell + padding[0] + icon_dims[1] + ((20 - fontsize) // 2)

            text = icon[0]
            char_width = fontsize * UM_FNT_PT_FACTOR[0]
            max_chars = int(icon_dims[0] // char_width)

            color = textcolor if icon[1][1] else WHITE

            if len(text) <= max_chars:
                x += ((max_chars - len(text)) * char_width) / 2
                self.conn_pygame_graphics.render_text('regular', fontsize, text, color, (x, y), surface=surface)
                continue

            if not icon[1][1]:
                text = text[:max_chars - 2]
                text += '..'
                self.conn_pygame_graphics.render_text('regular', fontsize, text, color, (x, y), surface=surface)
                continue

            if icon[1][1]:
                text_objs = text.split(' ')
                i = 0
                while i < len(text_objs):
                    if '-' in text_objs[i]:
                        temp = text_objs[i]
                        text_objs[i] = temp[:temp.index('-') + 1]
                        text_objs.insert(i+1, temp[temp.index('-') + 1:])
                    i += 1
                    
                final_ver = []

                i=1
                for index, text_obj in enumerate(text_objs):
                    if i > 1:
                        i -= 1
                        continue
                    while len(' '.join(text_objs[index:index+i])) <= max_chars:
                        i+=1
                    if len(text_obj) > max_chars:
                        chunks, chunk_size = len(text_obj), max_chars
                        final_ver.extend([text_obj[j:j+chunk_size] for j in range(0, chunks, chunk_size)])
                    else:
                        final_ver += text_objs[index:index+i]
                    
                for index, line in enumerate(final_ver):
                    self.conn_pygame_graphics.render_text('regular', fontsize, line, color, (x, y + (index * fontsize * UM_FNT_PT_FACTOR[1])), surface=surface)
