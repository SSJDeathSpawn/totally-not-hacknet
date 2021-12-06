from custom_logging.logging import get_logger
from game.application import Application


logger = get_logger('game')


class AuthenticFile(Application):
	def __init__(self, os, opened_by):
		super().__init__(os, opened_by, 30)

		self.bg_colour = (25, 25, 25)
		self.starting_size = (720, 480)
		
		self.title = 'Authentic File'

		self.file_icon_path = 'images/icons/file_icon.png'
		self.folder_icon_path = 'images/icons/folder_icon.png'

		self.storage_units = dict.fromkeys(self.current_dir.get_contents(), False)

		self.scroll = 0

	async def event_handler(self):
		await super().event_handler()
		if not self.current_event: return

		await self.event_handler()

	async def graphics_handler(self):
		await super().graphics_handler()

		self.os.system.graphics.display_explorer_icons(self.surface, self.storage_units, [40, 40], [10, 20], self.scroll, self.file_icon_path, self.folder_icon_path)
