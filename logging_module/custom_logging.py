import logging
import logging.config


class CustomFormatter(logging.Formatter):
    """Custom Formatter for Colored Logs"""

    dimmed: str = '\033[2;37m'
    green: str = '\033[0;32m'
    yellow: str = '\033[0;33m'
    red: str = '\033[0;31m'
    bold_red: str = '\033[1;31m'
    reset: str = '\033[0;37m'
    
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS: dict = {
        logging.DEBUG: dimmed + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record) -> str:
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)


# Configuring Logging
try:
    logging.config.fileConfig('logging_module/logging.conf')
except FileNotFoundError:
    print('Directory \'logs/\' not found in Current Working Directory. Exiting.')
    exit()

# Adding Colors to Console Logs
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(fmt=CustomFormatter())
logging.root.addHandler(stream_handler)


def get_logger(name: str) -> logging.Logger:
    """Returns a Logger object with the given name"""

    return logging.getLogger(name)
