from typing import TYPE_CHECKING
from logging import Logger
from logging_module.custom_logging import get_logger
from game.storage_system.directory import RootDir
if TYPE_CHECKING:
    from game.system import System


class OperatingSystem(object):
    """Class representing an Operating System"""

    def __init__(self, system: System, root: RootDir) -> None:
        
        self.logger: Logger = get_logger('game')
        self.system: System = system
        self.root: RootDir = root

    def mainloop(self) -> None:
        """Main Loop of the Operating System"""

        pass
