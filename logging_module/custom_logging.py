from __future__ import annotations

import os
import logging
import logging.config
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from logging import LogRecord

from dotenv import load_dotenv


class CustomFormatter(logging.Formatter):
    """Custom Formatter for Colored Logs"""

    cyan: str = '\033[0;36m'
    green: str = '\033[0;32m'
    yellow: str = '\033[0;33m'
    red: str = '\033[0;31m'
    bold_red: str = '\033[1;31m'
    reset: str = '\033[0;37m'
    
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS: dict[int, str] = {
        logging.DEBUG: cyan + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self: CustomFormatter, record: LogRecord) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


load_dotenv()

try:
    if int(os.getenv('DEBUG')):
        # Configuring Logging
        try:
            logging.config.fileConfig('logging_module/logging.conf')
        except FileNotFoundError:
            print('Couldn\'t initialize logging. Make sure you have a logs directory in your working directory.\n(You are seeing this message because DEBUG is set to true. Set it to false if you want to ignore logging.)')
            exit()

        # Adding Colors to Console Logs
        stream_handler: logging.Handler = logging.StreamHandler()
        stream_handler.setFormatter(fmt=CustomFormatter())
        logging.root.addHandler(stream_handler)

except (TypeError, ValueError):
    print('A valid DEBUG env variable was not found. Ignoring custom logging.')


def get_logger(name: str) -> logging.Logger:
    """Returns a Logger object with the given name"""

    return logging.getLogger(name)
