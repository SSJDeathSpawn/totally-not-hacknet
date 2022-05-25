from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from logging import Logger

from logging_module import get_logger


class LoggingException(Exception):
    def __init__(self, message: str) -> None:
        self.logger: Logger = get_logger('exception')
        self.message: str = message
        self.logger.error(f'{self.__class__}: {self.message}')
