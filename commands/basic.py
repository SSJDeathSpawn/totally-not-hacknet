from __future__ import annotations

import re
import itertools
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import logging

from game.command import Response
from game.storage_system.directory import Directory
from game.storage_system.file import File
from exceptions.storage_system import PathError, FileError
from logging_module.custom_logging import get_logger
if TYPE_CHECKING:
    from game.applications.application import Application


logger: logging.Logger = get_logger(__name__)

# Helpers

def process_args(args: list) -> tuple[list[str], list[str], str]:
    """Processes command arguments"""
    
    # Flags
    flags = list(filter(lambda arg: arg.startswith('-') and not arg.startswith('--') and arg != '-', args))
    args = list(filter(lambda arg: arg not in flags, args))
    flags = list(''.join(list(map(lambda arg: arg[1:], flags))))

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


def exit_(app: Application, *args) -> Response:
    """Quits the application"""

    app.quit()
    return Response(0, stdout=None, stderr=None)


def cat(app: Application, *args) -> Response:
    """Displays the contents of a file"""

    _, _, args = process_args(args)

    try:
        su = app.host.get_su_by_path(args[0], app.current_dir)
    except PathError as e:
        return Response(1, stdout=None, stderr=f'cat: {e}')
    except IndexError:
        return Response(1, stdout=None, strerr=f'cat: command takes 1 file argument')
        
    if not isinstance(su, File):
        return Response(1, stdout=None, stderr=f'cat: not a directory: {args[0]}')
    
    contents = bytes.decode(su.get_contents(), 'ascii') if type(su.get_contents()) == bytes else su.get_contents()  # Add this to the man string

    return Response(0, stdout=contents, stderr=None)


def mkdir(app: Application, *args) -> Response:
    """Makes new directory"""

    flags, _, args = process_args(args)

    logger.debug(flags)

    stdout = ''

    for arg in args:
        if app.host.path_exists(arg, app.current_dir):
            return Response(1, stdout=None, stderr=f'mkdir cannot create directory \'{arg}\': Directory exists')
        
    if 'p' not in flags:
        for arg in args:
            if '/' in arg:
                if not app.host.path_exists('/'.join(arg.split('/')[:-1]), app.current_dir):
                    return Response(1, stdout=None, stderr=f'mkdir: cannot create directory \'{arg}\': No such file or directory')
            else:
                su = app.current_dir

            su.add(Directory(su, arg.split('/')[-1], []))
            if 'v' in flags: 
                if stdout != '':
                    stdout += '\n'
                stdout += f'mkdir: created directory \'{arg}\''
                
    else:
        for arg in args:
            last_dir = '/'.join(arg.split('/')[:-1])
            while True:
                if '/' in last_dir:
                    if not app.host.path_exists(last_dir, app.current_dir):
                        last_dir = '/'.join(last_dir.split('/')[:-1])
                    else:
                        break
                else:
                    su = app.current_dir
                    break

            while last_dir != arg:
                logger.debug(last_dir)
                logger.debug(arg)
                logger.debug(len(last_dir))
                logger.debug(arg[len(last_dir)+1:].split('/')[0])
                logger.debug(su.get_path())

                su.add(Directory(su, last_dir.split('/')[-1], []))

                if 'v' in flags: 
                    if stdout != '':
                        stdout += '\n'
                    stdout += f'mkdir: created directory \'{arg}\''
                    
                su = app.host.get_su_by_path(last_dir, app.current_dir)
                last_dir = last_dir + '/' + arg[len(last_dir)+1:].split('/')[0]
                
            su.add(Directory(su, last_dir.split('/')[-1], []))

    return Response(0, stdout=None if stdout == '' else stdout, stderr=None)


def touch(app: Application, *args) -> Response:
    """Touches into my soul and rips it out"""
    
    _, _, args = process_args(args)

    for arg in args:
        if '/' in arg:
            if not app.host.path_exists('/'.join(arg.split('/')[:-1]), app.current_dir):
                return Response(1, stdout=None, stderr=f'touch: cannot touch {arg}: No such file or directory')
            else:
                logger.info('I reached here.')
                su = app.host.get_su_by_path('/'.join(arg.split('/')[:-1]), app.current_dir)
        else:
            su = app.current_dir 

        name = arg.split('/')[-1]

        pattern = re.compile(r'\{([1-9]+|[a-z])\.\.([0-9]+|[a-z])\}')  # {letter/number..letter/number}

        a = pattern.split(name)

        #No magic
        if len(a) == 1:
            su.add(File(su, arg.split('/')[-1], ''))

        # Magic {letter/number..letter/number stuff}
        else:
            un_changed = a[::3]
            inputs = [(a[i - 2], a[i -1]) for i in range(3, len(a), 3)]

            index = 0
            while index < len(inputs):
                i = inputs[index]

                if not (str.isdigit(i[0]) and str.isdigit(i[1])) and not (str.islower(i[0]) and str.islower(i[1])) and not (str.isupper(i[0]) and str.isupper(i[1])):
                    print(un_changed, index)
                    new = un_changed[index] + '{' + f'{i[0]}..{i[1]}' + '}' + (un_changed[index+1] if index < len(inputs) - 1 else '')
                    un_changed[index] = new
                    un_changed.pop(index+1)
                    inputs.pop(index)
                    print(un_changed)
                    index -= 1
                index +=1

            iterables = []
            for i in inputs:
                if (str.isdigit(i[0]) and str.isdigit(i[1])) or (str.islower(i[0]) and str.islower(i[1])) or (str.isupper(i[0]) and str.isupper(i[1])):
                    iterables.append(list(map(lambda num: chr(num), list(range(ord(i[0]), ord(i[1])+1)))))

            cartesian_product = list(itertools.product(*iterables, repeat=1))

            for combination in cartesian_product:
                try:
                    su.add(File(su, ''.join(i+j for i,j in zip(un_changed, combination)), ''))
                except FileError:
                    pass

    return Response(0, stdout=None, stderr=None)


def mv(app: Application, *args) -> Response:
    """Move command"""
    
    flags, _, args = process_args(args)
    stderr = ''
    rename = None


    try:    
        if len(args) <= 1:
            return Response(1, stdout=None, stderr=f'mv: missing destination file operand after {args[0]}')

        try:
            output_dir = app.host.get_su_by_path(args[-1], app.current_dir)
        except PathError:
            if (len(args) > 2):
                return Response(1, stdout=None, stderr=f'mv: target {args[-1]} is not a directory')
            else:
                output_dir = app.host.get_su_by_path('/'.join(args[-1].split('/')[:-1]), app.current_dir)
                rename = args[-1].split('/')[:-1]
        
        for arg in args[:-1]:
            if not app.host.path_exists(arg, app.current_dir):
                stderr += f'mv: cannot stat {arg}: No such file or directory'

            else:
                su = app.host.get_su_by_path(arg, app.current_dir)
                if rename:
                    su.set_name(rename)
                    
                app.host.move_to_new_dir(su, output_dir)
                
    except Exception as e:
        logger.error(e)

    return Response(0 if not stderr else 1, stdout=None, stderr=None if not stderr else stderr)

def clear(app: Application, *args) -> Response:
    """Clears the window text"""

    app.content = ''
    return Response(0, stdout=None, stderr=None)
