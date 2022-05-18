from __future__ import annotations

from typing import Optional, TYPE_CHECKING

import pygame

from game.applications.application import Application
from game.storage_system.directory import Directory
from game.storage_system.storage_unit import StorageUnit
from game.constants import DIRECTORY_CHANGE
from graphics.conn_pygame_graphics import Surface
from graphics.constants import SU_ICON_DIMENSIONS, SU_ICON_LABEL_FNT_SIZE, PATH_FROM_CLASS, EXPLORER_BGCOLOR, EXPLORER_TEXT_COLOR, ICON_PADDING, TITLEBAR_DEFAULT_HEIGHT, EXPLORER_SCROLLBAR_COLOR
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
        self.ctrl: bool = False

        # TEMPORARY PLS REMOVE
        self.storage_units[self.host.get_su_by_path('/hello.txt', self.current_dir)] = True
        self.storage_units[self.host.get_su_by_path('/homewdqujdhqwkjdhqwiudhqwuidqhwuiqdwu', self.current_dir)] = True

        self.update_surface()

    @property
    def icon_block_height(self: Explorer) -> int:
        """Returns the height of one icon block"""

        return ICON_PADDING[0] + SU_ICON_DIMENSIONS[1] + ICON_PADDING[2]

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

    def get_icon_index(self, pos: tuple[int, int]) -> Optional[int]:
        """Returns the icon index on a position if it's pointing to a valid icon index"""

        pos = [pos[0] - self.surface.pos[0] - ICON_PADDING[3], pos[1] - self.surface.pos[1] - TITLEBAR_DEFAULT_HEIGHT]

        x = pos[0] // self.icon_block_width
        y = pos[1] // self.icon_block_height

        index = y * self.max_cols + x

        try:
            list(self.storage_units.items())[index]
            return index
        except IndexError:
            return None

    def get_selected(self) -> None:
        """Returns the dictionary of selected Storage Units"""

        return dict(list(filter(lambda su: su[1], list(self.storage_units.items()))))

    def deselect_all(self, exc_index: int) -> None:
        """Deselects all Storage Units"""

        units = list(dict.fromkeys(self.current_dir.get_contents(), False).items())
        units[exc_index] = list(self.storage_units.items())[exc_index]
        self.storage_units = dict(units)
        self.update_surface()
        
    def invert_selection(self, index: int) -> None:
        """Select a Storage Unit at given index"""

        units = list(self.storage_units.items())
        item = units[index][0], not units[index][1]
        units[index] = item
        self.storage_units = dict(units)

        self.update_surface()
        
    def update_surface(self) -> None:
        """Updates the cached surface"""

        self.check_for_change()

        self.cached_surface.fill(EXPLORER_BGCOLOR)
        org_icons = {su.get_name(): (PATH_FROM_CLASS[type(su)][selected], selected) for su, selected in self.storage_units.items()}
        
        mod_icons = dict(list(org_icons.items())[(self.max_cols * self.scroll):(self.max_icons + (self.max_cols * (self.scroll+1)))])

        self.graphics.draw_explorer_icons(self.cached_surface, dict(mod_icons), SU_ICON_DIMENSIONS, ICON_PADDING, SU_ICON_LABEL_FNT_SIZE, self.scroll, self.max_scroll, self.current_dir.get_path(), textcolor=EXPLORER_TEXT_COLOR, scrollbar_color=EXPLORER_SCROLLBAR_COLOR)

    def check_for_change(self) -> None:
        """Checks for changes in the current directory and updates the dictionary while keeping the previous selected values"""

        new_units = dict.fromkeys(self.current_dir.get_contents(), False)
        if new_units != self.storage_units:
            for unit in new_units.keys():
                if unit in self.storage_units.keys():
                    new_units[unit] = self.storage_units[unit]
        self.storage_units = new_units

    @Application.graphics_wrapper
    def graphics_handler(self) -> None:
        self.graphics.clear_app_surface(self.surface, EXPLORER_BGCOLOR)

        self.surface.blit(self.cached_surface, self.cached_surface.pos)

        self.graphics.draw_outlines(self.surface)

    def events_handler(self) -> None:
        super().events_handler()

        for event in self.events:
            if event.type == DIRECTORY_CHANGE:
                event.path == self.current_dir.get_path() and self.update_surface()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEDOWN:
                    self.scroll = min(self.max_scroll, self.scroll + 1)
                    self.update_surface()

                if event.key == pygame.K_PAGEUP:
                    self.scroll = max(self.scroll - 1, 0)
                    self.update_surface()

                if event.key == pygame.K_BACKSPACE:
                    if self.current_dir.get_parent():
                        self.current_dir = self.current_dir.get_parent()
                        self.update_surface()

                if event.key == pygame.K_RETURN:
                    selected = list(self.get_selected().keys())
                    if len(selected) == 1:
                        if isinstance(selected[0], Directory):
                            self.current_dir = selected[0]
                            self.update_surface()
                
                if event.key == pygame.K_p:
                    self.current_dir.delete(self.host.get_su_by_path('hello.txt', self.current_dir))

                if event.key == pygame.K_LCTRL:
                    self.ctrl = True

            if event.type == pygame.KEYUP and event.key == pygame.K_LCTRL:
                self.ctrl = False

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:

                    icon_index = self.get_icon_index(pygame.mouse.get_pos())

                    if icon_index != None:
                        if self.ctrl:
                            self.invert_selection(icon_index)

                        else:
                            self.deselect_all(icon_index)
                            self.invert_selection(icon_index)

                    else:
                        self.deselect_all(-1)
