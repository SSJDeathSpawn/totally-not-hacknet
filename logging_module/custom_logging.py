import logging
import logging.config


class CustomFormatter(logging.Formatter):
    """Custom Formatter for Colored Logs"""

    dimmed = '\033[2;37m'
    green = '\033[0;32m'
    yellow = '\033[0;33m'
    red = '\033[0;31m'
    bold_red = '\033[1;31m'
    reset = '\033[0;37m'
    
    format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"

    FORMATS = {
        logging.DEBUG: dimmed + format + reset,
        logging.INFO: green + format + reset,
        logging.WARNING: yellow + format + reset,
        logging.ERROR: red + format + reset,
        logging.CRITICAL: bold_red + format + reset
    }

    def format(self, record):
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


def get_logger(name: str):
    """Returns a Logger object with the given name"""

    return logging.getLogger(name)
