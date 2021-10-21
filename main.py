import json
import asyncio

from custom_logging.logging import get_logger
from graphics.conn_pygame_graphics import ConnPygameGraphics
from game.system import System
from game.graphics import Graphics
from game.bootable_media import BootableMedia

DEBUG = False
logger = get_logger('root')


def setup():
	with open('data/generated_ids.json', 'w') as f:
		json.dump([], f, indent=4)
	with open('data/generated_ips.json', 'w') as f:
		json.dump([], f, indent=4)


async def main():
	logger.info('Setting things up...')
	setup()

	logger.info('Starting Application...')
	system = System('Xeno', 256, Graphics(ConnPygameGraphics(1080, 720, 'Totally Not Hacknet')))
	system.bootable_media = BootableMedia()
	await system.install_os()
	await system.run_loops()


if __name__ == "__main__":
	asyncio.run(main())
