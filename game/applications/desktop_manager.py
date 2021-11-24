import pygame
import math

from custom_logging.logging import get_logger
from game.application import MasterApplication
from graphics.conn_pygame_graphics import Surface


logger = get_logger('game')


class DesktopManager(MasterApplication):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 50)
		#After filesystems have been implemented, make the OS add the User/Desktop applications in here 
		self.icons = [Icon("Terminal", "/images/icons/term_icon.png", 'TERMINAL')]
		#The list of indices of the icons that are selected 
		self.selected = set()
		self.icon_size = (150, 150)
		self.icon_limit_row = 3
		self.icon_background_render = Surface((100,100), (0,0))
		self.icon_background_render.fill((27, 63, 181, 100))

	async def event_handler(self):
		if len(self.event_queue) < 1:
			self.current_event = None
			return
			
		self.current_event = self.event_queue.pop(0)

		if self.current_event.type==pygame.MOUSEBUTTONDOWN and self.current_event.button==1:
			if self.application_queue:
				popindex = None
				if (not (self.application_queue[0].surface.pos[0] < self.current_event.pos[0] < self.application_queue[0].surface.pos[0] + self.application_queue[0].surface.get_width() and self.application_queue[0].surface.pos[1] < self.current_event.pos[1] < self.application_queue[0].surface.pos[1] + self.application_queue[0].surface.get_height())):
					for index, application in enumerate(self.application_queue[1:], start=1):
						if (application.surface.pos[0] < self.current_event.pos[0] < application.surface.pos[0] + application.surface.get_width() and application.surface.pos[1] < self.current_event.pos[1] < application.surface.pos[1] + application.surface.get_height()):
							popindex = index
							break
				if popindex: 
					app = self.application_queue.pop(popindex)
					self.application_queue.insert(0, app)
					self.os.system.graphics.conn_pygame_graphics.select_surface(app.surface)
					popindex = None

			predicate = self.current_event.pos[0] <= (len(self.icons)//self.icon_limit_row)*self.icon_size[0] and self.current_event.pos[1] <= self.icon_limit_row*self.icon_size[1] or \
				(len(self.icons)//self.icon_limit_row)*self.icon_size[0] < self.current_event.pos[0] <= math.ceil(len(self.icons)/self.icon_limit_row)*self.icon_size[0] and self.current_event.pos[1] <= (len(self.icons) % self.icon_limit_row)*self.icon_size[1]
			if predicate:
				selected_x = self.current_event.pos[0] // self.icon_size[0] 
				selected_y = self.current_event.pos[1] // self.icon_size[1] 
				select_index = selected_x + selected_y*self.icon_limit_row
				self.selected=self.selected.union({select_index})
			else:
				self.selected = set()

		if self.selected and self.current_event.type==pygame.KEYDOWN and self.current_event.key==pygame.K_RETURN:
			for i in self.selected:
				self.icons[i].open(self)
			self.selected = set()
			return

		if self.application_queue:
			self.application_queue[0].event_queue += [self.current_event]

		await self.event_handler()

	async def graphics_handler(self):
		#TODO: Remove once desktop images are a thing
		self.os.system.graphics.fill(self.surface, (0, 0, 0))
		x,y=0,0
		for index, icon in enumerate(self.icons):
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
		self.sel_render=None

	def render_icon(self, pos, desktop_manager, selected):
		if not self.render:
			self.render = desktop_manager.os.system.graphics.rendered_icon(self.path, self.name, (255,255,255), 16, 0, width=60, height=60)
		if not self.sel_render:
			self.sel_render = desktop_manager.icon_background_render.copy()
			rect = self.render.get_rect()
			rect.center = (self.sel_render.get_width()/2, self.sel_render.get_height()/2)
			self.sel_render.blit(self.render, rect)
		temp = self.render if not selected else self.sel_render
		temp_rect = temp.get_rect()
		temp_rect.topleft = pos
		desktop_manager.surface.blit(temp, temp_rect)

	def open(self, desktop_manager):
		desktop_manager.os.start_application(self.reg_name, desktop_manager.os, master_app=desktop_manager)

