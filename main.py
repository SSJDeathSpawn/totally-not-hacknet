#!venv/bin/python3

from logging_module.custom_logging import get_logger
from game.system import System


logger = get_logger(__name__)


def main():
    logger.info('Hi! Starting Computer System')
    system = System('AsyncXeno', 4096)
    system.run_os()
    logger.info('Bye!')


if __name__ == '__main__':
    main()
