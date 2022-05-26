#!venv/bin/python3

import cProfile, pstats
import sys, getopt
import io

from logging_module.custom_logging import get_logger
from game.system import System

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
    System('Ziphernet Kilog 2000', 4096, fullscreen=fullscreen)
    logger.info('Bye!')


if __name__ == '__main__':
    profiler = cProfile.Profile()

    profiler.enable()
    main()
    profiler.disable()
    
    s = io.StringIO()
    stats = pstats.Stats(profiler, stream=s).sort_stats('cumtime')
    stats.print_stats()
    
    with open('logs/profiler.log', 'w+') as f:
        for index, line in enumerate(s.getvalue().split('\n')):
            f.write(f'{line}\n' if (index < 5) or ('method' in line and 'built-in' not in line) else '')
