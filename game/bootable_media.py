from custom_logging.logging import get_logger
from game.operating_system import OperatingSystem


logger = get_logger('game')


class BootableMedia(object):
	@staticmethod
	async def install(system):
		system.os = OperatingSystem(system)
		await system.os.initialize()
