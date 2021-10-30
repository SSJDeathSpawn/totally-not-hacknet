import logging
import pygame
from pygame.constants import MOUSEBUTTONDOWN
import math

from custom_logging.logging import get_logger
from game.application import Application
from graphics.conn_pygame_graphics import Surface


logger = get_logger('game')


class DesktopManager(Application):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 50)
		#After filesystems have been implemented, make the OS add the User/Desktop applications in here 
		self.icons = [Icon("Terminal", "/images/icons/term_icon.png", 'TERMINAL')]
		logger.debug(type(self.icons[0]))
		#The list of indices of the icons that are selected 
		self.selected = set()
		self.starting_size=(self.os.system.graphics.conn_pygame_graphics.win.get_width(), self.os.system.graphics.conn_pygame_graphics.win.get_height())
		self.bg_colour = (0,0,0)
		self.fg_colour = (255, 255, 255)
		self.icon_size = (150, 150)
		self.icon_limit_row = 3
		self.titlebar=False

	async def event_handler(self):
		if len(self.event_queue) < 1:
			self.current_event = None
			return
		
		self.current_event = self.event_queue.pop(0)
		if self.current_event.type==pygame.MOUSEBUTTONDOWN and self.current_event.button==1:
			predicate = self.current_event.pos[0] <= (len(self.icons)//self.icon_limit_row)*self.icon_size[0] and self.current_event.pos[1] <= self.icon_limit_row*self.icon_size[1] or \
				(len(self.icons)//self.icon_limit_row)*self.icon_size[0] < self.current_event.pos[0] <= math.ceil(len(self.icons)/self.icon_limit_row)*self.icon_size[0] and self.current_event.pos[1] <= (len(self.icons) % self.icon_limit_row)*self.icon_size[1]
			if predicate:
				selected_x = self.current_event.pos[0] // self.icon_size[0] 
				selected_y = self.current_event.pos[1] // self.icon_size[1] 
				select_index = selected_x + selected_y*self.icon_limit_row
				logger.debug(select_index)
			self.selected=self.selected.union({select_index})
		await self.event_handler()

	async def graphics_handler(self):
		x,y=0,0
		for index, icon in enumerate(self.icons):
			#logger.debug(f"{index}, {self.selected}")
			icon.render_icon((x+10,y+10), self, index in self.selected)
			y+=self.icon_size[1]
			if y > self.icon_limit_row*self.icon_size[1]:
				y=0
				x+=self.icon_size[0]

class Icon(object):
	def __init__(self, name, path_to_icon, reg_name):
		self.name = name
		self.path = path_to_icon
		self.reg_name = reg_name
		self.render = None 

	def render_icon(self, pos, desktop_manager, selected):
		if not self.render:
			self.render = desktop_manager.os.system.graphics.rendered_icon(self.path, self.name, (255,255,255), 20, 10, width=80, height=70)
		temp = self.render if not selected else desktop_manager.os.system.graphics.outline_surface(self.render, (250, 200, 100), 5)
		temp_rect = temp.get_rect()
		temp_rect.topleft = pos
		desktop_manager.surface.blit(temp, temp_rect)


	def open(self, os):
		os.start_application(self.reg_name, os)

