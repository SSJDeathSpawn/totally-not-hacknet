from logging import Logger
from os import times_result
import pygame
from pygame import surface
from pygame.constants import KEYDOWN
from pygame.math import enable_swizzling

from custom_logging.logging import get_logger
from game.application import Application
from game.constants import titlebar_height
from game.storage_system.file import File


logger = get_logger('game')


class AuthenticFile(Application):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 30)

		self.bg_colour = (25, 25, 25)
		self.starting_size = (720, 480)
		
		self.title = 'Authentic File'

		self.file_icon_path = '/images/icons/file_icon.png'
		self.folder_icon_path = '/images/icons/folder_icon.png'

		self.storage_units = dict.fromkeys(self.current_dir.get_contents(), False)

		self.icon_dimensions = [64, 64]
		self.space = [10, 8]

		self.scroll = 0
		self.ctrl = False

	async def run(self):
		logger.warn(self.timer_running)
		await super().run()
		updated = self.current_dir.get_contents()
		for unit in updated:
			if unit not in self.storage_units:
				self.storage_units[unit] = False

	async def event_handler(self):
		await super().event_handler()
		if not self.current_event: return

		if self.current_event.type == pygame.KEYDOWN:
			if self.current_event.key == pygame.K_DOWN:
				self.scroll += 1
			if self.current_event.key == pygame.K_UP:
				self.scroll -= 1

			if self.current_event.key == pygame.K_BACKSPACE:
				if self.current_dir.get_parent(): self.current_dir = self.current_dir.get_parent()

			limit = self.surface.get_width() // (self.icon_dimensions[0] + 2 * (self.space[0]))
			new_surface_height = ((self.icon_dimensions[1] + (3 * self.space[1])) * ((len(self.storage_units.keys()) // limit) + 2))
			self.scroll = min(max(self.scroll, 0), 0 if new_surface_height < self.surface.get_height() - titlebar_height else (new_surface_height - self.surface.get_height() + titlebar_height) // (self.icon_dimensions[1] + 3 * self.space[1]) + 1)

		if self.current_event.type == pygame.MOUSEBUTTONDOWN and self.current_event.button==1:
			surface_units_range = ((self.surface.pos[0], self.surface.pos[1] + titlebar_height), (self.surface.pos[0] + self.surface.get_width(), self.surface.pos[1] + self.surface.get_height()))

			if all([i < k < j for i,j,k in zip(surface_units_range[0],surface_units_range[1],self.current_event.pos)]):
				offset = (self.current_event.pos[0] - surface_units_range[0][0], self.current_event.pos[1] - surface_units_range[0][1])

				limit_hor = self.surface.get_width() // (self.icon_dimensions[0] + (2 * self.space[0]))
				# limit_ver = (self.surface.get_height() - titlebar_height) // (self.icon_dimensions[1] + (3 * self.space[1])) 

				col, row = offset[0] // (self.icon_dimensions[0] + (2 * self.space[0])), offset[1] // (self.icon_dimensions[1] + (3 * self.space[1])) + self.scroll
				index = int(row * limit_hor + col)

				if index > len(self.storage_units) - 1:
					self.storage_units = dict.fromkeys(self.current_dir.get_contents(), False) 

				else:
					if not (pygame.key.get_mods() & pygame.KMOD_CTRL): 
						for unit in self.storage_units:
							if unit != list(self.storage_units.keys())[index]:
								self.storage_units[unit] = False

						if not self.storage_units[list(self.storage_units.keys())[index]]:
							self.storage_units[list(self.storage_units.keys())[index]] = True
						
						else:
							if self.timer_running:
								self.open(list(self.storage_units.keys())[index])
			
					else:
						self.storage_units[list(self.storage_units.keys())[index]] = not self.storage_units[list(self.storage_units.keys())[index]]

		await self.event_handler()

	async def graphics_handler(self):
		await super().graphics_handler()
		self.os.system.graphics.display_explorer_icons(self.surface, self.storage_units, self.icon_dimensions, self.space, self.scroll, self.file_icon_path, self.folder_icon_path)

	def open(self, unit):
		if isinstance(unit, File): logger.warn('WORK IN PROGRESS')
		else: 
			self.current_dir = unit
			self.scroll = 0
			self.storage_units = dict.fromkeys(self.current_dir.get_contents(), False)
