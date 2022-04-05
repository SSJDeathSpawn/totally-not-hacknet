from __future__ import annotations
from sys import stderr
from typing import TYPE_CHECKING
from game.command import Response
from exceptions.storage_system import PathError
from game.storage_system.directory import Directory
from logging_module.custom_logging import get_logger

if TYPE_CHECKING:
    from game.applications.application import Application
    from game.operating_system import OperatingSystem
    import logging


logger: logging.Logger = get_logger(__name__)

"""
0 - ran to completion
1 - catchall for general errors
127 - command not found
130 - control - c
"""

# Helpers

def process_args(args: list) -> tuple[list[str], list[str], str]:
    """Processes command arguments"""
    
    # Flags
    flags = list(filter(lambda arg: arg.startswith('-') and not arg.startswith('--') and arg != '-', args))
    args = list(filter(lambda arg: arg not in flags, args))
    flags = ''.join(map(lambda arg: arg[1:], flags)).split()

    # Special Flags
    special_flags = list(filter(lambda arg: arg.startswith('--'), args))
    args = list(filter(lambda arg: arg not in special_flags, args))
    special_flags = list(map(lambda arg: arg[2:], special_flags))

    return (flags, special_flags, args)    


# Commmands

def ls(app: Application, *args) -> Response:
    """List command"""

    flags, _, args = process_args(args)
    
    recursive = 'R' in flags

    if args:
        try:
            directories = list(map(lambda arg: app.host.get_directory_by_path(arg), args))
        except PathError:
            return Response(1, '', f'Cannot access \'{args[0]}\'. No such file or directory')
    else:
        directories = [app.current_dir]

    stdout = ''

    def recurse(directories: list[Directory]) -> None:
        nonlocal stdout
        for directory in directories:
            stdout += directory.get_name() + ':\n'
            stdout += '\t'.join(directory.get_contents())

        stdout += '\n\n'
        
        dirs = list(filter(lambda su: isinstance(su, Directory), directory.get_contents()))
        for directory in dirs:
            recurse(directory)

    if recursive:
        recurse(directories)
    
    elif len(args) > 1:    
        for directory in directories:
            stdout += directory.get_name() + ':\n'
            stdout += '\t'.join(directory.get_contents()) + '\n'
    
    else:
        logger.debug(directories)
        stdout = '\t'.join(sorted(list(map(lambda su: su.get_name(), directories[0].get_contents()))))
        logger.debug('complete')
    
    return Response(0, stdout=stdout, stderr='')
    

def cd(os: OperatingSystem, *args) -> Response:
    """Change directory command"""

    _, _, args = process_args(args)