from sys import stderr
from typing import TYPE_CHECKING
from game.command import Response
from __future__ import annotations
from exceptions.storage_system import PathError
from game.storage_system.directory import Directory

if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


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
    flags = list(filter(lambda arg: arg.startswith('-') and not arg.startswith('--') and arg != '-'), args)
    args = list(filter(lambda arg: arg not in flags, args))
    flags = ''.join(map(lambda arg: arg[1:], flags)).split()

    # Special Flags
    special_flags = list(filter(lambda arg: arg.startswith('--'), args))
    args = list(filter(lambda arg: arg not in special_flags, args))
    special_flags = list(map(lambda arg: arg[2:], special_flags))

    return (flags, special_flags, args)    


# Commands

def ls(os: OperatingSystem, *args) -> Response:
    """List command"""

    flags, _, args = process_args(args)

    # TODO: Add hidden folders
    recursive = 'R' in flags

    if args:
        try:
            directories = list(map(lambda arg: os.get_directory_by_path(arg), args))
        except PathError:
            return Response(1, '', f'Cannot access \'{args[0]}\'. No such file or directory')
    else:
        directories = [os.selected.app.current_dir]

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
        stdout = '\t'.join(directories[0].get_contents().sort(key=lambda x: x.get_name())) + '\n'
    
    return Response(0, stdout=stdout, stderr=None)


def cd(os: OperatingSystem, *args) -> Response:
    """Change directory command"""

    flags, special_flags, args = process_args(args)