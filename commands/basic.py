from __future__ import annotations
from sys import stderr
from typing import TYPE_CHECKING
from game.command import Response
from exceptions.storage_system import PathError
from game.storage_system.directory import Directory
from game.storage_system.file import File
from logging_module.custom_logging import get_logger

if TYPE_CHECKING:
    from game.applications.application import Application
    import logging


logger: logging.Logger = get_logger(__name__)

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
            directories = list(map(lambda arg: app.host.get_su_by_path(arg, app.current_dir), args))
        except PathError:
            return Response(1, '', f'ls: cannot access \'{args[0]}\'. No such file or directory')
    else:
        directories = [app.current_dir]

    stdout = ''

    def recurse(directories: list[Directory]) -> None:
        nonlocal stdout
        for directory in directories:
            stdout += directory.get_path() + ':\n'
            stdout += '\t'.join(list(map(lambda su: su.get_name(), directory.get_contents())))

            stdout += '\n\n'
            
            dirs = list(filter(lambda su: isinstance(su, Directory), directory.get_contents()))
            recurse(dirs)

    if recursive:
        recurse(directories)
    
    elif len(args) > 1:    
        for directory in directories:
            stdout += directory.get_name() + ':\n'
            stdout += '\t'.join(directory.get_contents()) + '\n'
    
    else:
        stdout = '\t'.join(sorted(list(map(lambda su: su.get_name(), directories[0].get_contents()))))
    
    return Response(0, stdout=stdout, stderr='')
    

def cd(app: Application, *args) -> Response:
    """Change directory command"""

    _, _, args = process_args(args)

    if len(args) > 1:
        return Response(1, stdout='', stderr=f'cd: too many arguments')

    if args[0] == '-' and 'OLDPWD' in app.env_var:
        app.current_dir, app.env_var['OLDPWD'] = app.env_var['OLDPWD'], app.current_dir
        return Response(0, stdout=None, stderr=None)

    try:
        old_dir = app.current_dir
        su = app.host.get_su_by_path(args[0], app.current_dir)
        if not isinstance(su, Directory):
            return Response(1, stdout=None, stderr=f'cd: not a directory: {args[0]}')
        app.current_dir = su
        app.env_var['OLDPWD'] = old_dir

    except PathError as e:
        return Response(1, stdout=None, stderr=f'cd: {e}')
    
    return Response(0, stdout=None, stderr=None)


def exit(app: Application, *args) -> Response:
    """Quits the application"""

    app.quit()
    return Response(0, stdout=None, stderr=None)


def cat(app: Application, *args) -> Response:

    _, _, args = process_args(args)

    try:
        su = app.host.get_su_by_path(args[0], app.current_dir)
    except PathError as e:
        return Response(1, stdout=None, stderr='cat: {e}')
        
    if not isinstance(su, File):
        return Response(1, stdout=None, stderr='cat: not a directory: {args[0]}')
    
    contents = bytes.decode(su.get_contents(), 'ascii') if type(su.get_contents()) == bytes else su.get_contents()  # Add this to the man string

    return Response(0, stdout=contents, stderr=None)