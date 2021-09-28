from custom_logging.logging import get_logger
from utils.id_generator import generate_id
from utils.ip_generator import generate_ip
from game.operating_system import OperatingSystem


logger = get_logger('game')


class System(object):
    def __init__(self, owner: str, memory: int):
        self.ID = f'SYSTEM-{generate_id(4)}'
        self.IP = generate_ip()

        self.owner = owner
        self.memory = memory

        self.bootable_media = None
        self.os = None

        self.outputs = {
            'scan': 'Scanning for Bootable Media...',
            'found': 'Bootable Media found...',
            'not_found': 'Bootable Media not found...'
        }

        logger.debug(f'Initialized System with ID {self.ID} and IP {self.IP}.')

    async def install_os(self):
        if not self.bootable_media:
            logger.critical('No bootable media. How did this even happen?')
            exit()
        await self.bootable_media.install(self)

    async def start(self):
        self.os.start()

    def output(self, message):
        pass
