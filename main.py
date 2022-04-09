#!venv/bin/python3

from logging_module.custom_logging import get_logger
from game.system import System

import sys, getopt


logger = get_logger(__name__)

argument_list: list[str] = sys.argv[1:]
options: str = ''
long_options: list[str] = ['fullscreen=']


def main():

    fullscreen: bool = False

    arguments, _ = getopt.getopt(argument_list, options, long_options)
    for arg, val in arguments:
        if arg in ('--fullscreen') and val in ('true'):
            fullscreen = True

    logger.info('Hi! Starting Computer System')
    system = System('AsyncXeno', 4096, fullscreen=fullscreen)
    system.run_os()
    logger.info('Bye!')


if __name__ == '__main__':
    main()
