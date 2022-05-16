from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame

from game.applications.application import Application
from game.storage_system.directory import Directory
from game.storage_system.storage_unit import StorageUnit
from game.constants import DIRECTORY_CHANGE
from graphics.conn_pygame_graphics import Surface
from graphics.constants import SU_ICON_DIMENSIONS, SU_ICON_LABEL_FNT_SIZE, PATH_FROM_CLASS, EXPLORER_BGCOLOR, EXPLORER_TEXT_COLOR, ICON_PADDING, TITLEBAR_DEFAULT_HEIGHT
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


class Explorer(Application):
    """Class representing the file explorer"""

    def __init__(self, host: OperatingSystem, opened_by: Optional[OperatingSystem] = None):
        super().__init__(host, opened_by)

        self.surface: Surface = self.host.system.graphics.get_app_surface(800, 600, [200, 200])
        self.cached_surface: Surface = Surface((800, 600-TITLEBAR_DEFAULT_HEIGHT), (0, TITLEBAR_DEFAULT_HEIGHT))
        self.current_dir: Directory = self.host.root
        
        self.scroll: int = 0
        self.storage_units: dict[StorageUnit, bool] = dict.fromkeys(self.current_dir.get_contents(), False)
        self.storage_units[self.host.get_su_by_path('/hello.txt', self.current_dir)] = True
        self.storage_units[self.host.get_su_by_path('/homewdqujdhqwkjdhqwiudhqwuidqhwuiqdwu', self.current_dir)] = True
        self.update_surface()

    @property
    def icon_block_height(self: Explorer) -> int:
        """Returns the height of one icon block"""

        return ICON_PADDING[0] + SU_ICON_DIMENSIONS[1] + SU_ICON_LABEL_FNT_SIZE + ICON_PADDING[2]

    @property
    def icon_block_width(self: Explorer) -> int:
        """Returns the width of one icon block"""

        return ICON_PADDING[3] + SU_ICON_DIMENSIONS[0] + ICON_PADDING[1]

    @property
    def max_cols(self: Explorer) -> int:
        """Returns maximum number of icons possible in one row"""

        return int(self.surface.get_width() // self.icon_block_width)

    @property
    def max_rows(self: Explorer) -> int:
        """Returns the maximum number of rows possible on the surface"""

        return int(self.surface.get_height() // self.icon_block_height)

    @property
    def max_icons(self: Explorer) -> int:
        """Returns the maximum number of icons possible on the surface"""

        return int(self.max_cols * self.max_rows)
    
    @property
    def max_scroll(self: Explorer) -> int:
        """Returns the maximum scroll amount"""
        
        num_icons = len(self.storage_units.items())
        rows = num_icons // self.max_cols + 1
        return max(0, rows-self.max_rows)

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_app_surface(self.surface, EXPLORER_BGCOLOR)

        self.surface.blit(self.cached_surface, self.cached_surface.pos)
    
    def update_surface(self) -> None:
        """Updates the cached surface"""

        self.storage_units = dict.fromkeys(self.current_dir.get_contents(), False)

        self.cached_surface.fill(EXPLORER_BGCOLOR)
        org_icons = {su.get_name(): (PATH_FROM_CLASS[type(su)][selected], selected) for su, selected in self.storage_units.items()}
        
        mod_icons = dict(list(org_icons.items())[(self.max_cols * self.scroll):(self.max_icons + (self.max_cols * (self.scroll+1)))])

        self.graphics.draw_explorer_icons(self.cached_surface, dict(mod_icons), SU_ICON_DIMENSIONS, ICON_PADDING, SU_ICON_LABEL_FNT_SIZE, textcolor=EXPLORER_TEXT_COLOR)

    def events_handler(self) -> None:
        super().events_handler()

        for event in self.events:
            if event.type == DIRECTORY_CHANGE:
                event.path == self.current_dir.get_path() and self.update_surface()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    self.scroll = min(self.max_scroll, self.scroll + 1)
                    self.logger.info(f'max = {self.max_scroll}, scroll = {self.scroll}')
                    self.update_surface()

                if event.key == pygame.K_PAGEUP:
                    self.scroll = max(self.scroll - 1, 0)
                    self.logger.info(f'scroll = {self.scroll}')
                    self.update_surface()

                if event.key == pygame.K_BACKSPACE:
                    if self.current_dir.get_parent():
                        self.current_dir = self.current_dir.get_parent()
                        self.update_surface()
                
                if event.key == pygame.K_p:
                    self.current_dir.delete(self.host.get_su_by_path('hello.txt', self.current_dir))
