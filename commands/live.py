from __future__ import annotations

from typing import TYPE_CHECKING

import time
import pickle
import pygame

from game.command import Response, Command
from game.storage_system import RootDir, Directory, File
from game.operating_system import OperatingSystem
from game.applications import Desktop, Terminal, Explorer
from logging_module import get_logger
from commands.basic import process_args
from game.constants import DEFAULT_ROOTDIR_PATH, GET_INPUT, INPUT_RECEIVED
from utils import serialize_root_directory
from commands.basic import *

if TYPE_CHECKING:
    from logging import Logger
    from game.applications import Application

logger: Logger = get_logger(__name__)


def install_os(app: Application, *args) -> Response | None:
    """Installs the OS on the system"""
    
    app.printf('Enter your username: ')  

    pygame.event.post(pygame.event.Event(GET_INPUT, password=False))
    
    while not (events:=pygame.event.get(INPUT_RECEIVED)):
        pass
    print(events)
    username = events[0].input

    app.printf('Enter your password: ')

    pygame.event.post(pygame.event.Event(GET_INPUT, password=True))
    
    while not (events:= pygame.event.get(INPUT_RECEIVED)):
        pass
    password = events[0].input

    app.printf('Confirm password: ')
    
    pygame.event.post(pygame.event.Event(GET_INPUT, password=True))
    
    while not (events:= pygame.event.get(INPUT_RECEIVED)):
        pass
    confirm = events[0].input

    if password != confirm:
        return Response(1, None, 'Password does not match. Try again.')

    app.printf('\nInstalling OS.')
    
    # Creating an pickling the OS
    os = OperatingSystem(RootDir(), username, password)

    os.startup_apps = {
        Desktop: False,
        Terminal: False,
        Explorer: False
    }

    os.commands = {
        'ls': Command('ls', ls, ''),
        'cd': Command('cd', cd, ''),
        'exit': Command('exit', exit_, ''),
        'cat': Command('cat', cat, ''),
        'mkdir': Command('mkdir', mkdir, ''),
        'touch': Command('touch', touch, ''),
        'mv': Command('mv', mv, ''),
        'clear': Command('clear', clear, ''),
        'reboot': Command('reboot', reboot, ''),
        'shutdown': Command('shutdown', shutdown, '')
        
        # TODO: Put man entires as constants later on
    }
    
    pickled_os: bytes = pickle.dumps(os)
    length = len(pickled_os)
    int_pickled_os = int.from_bytes(pickled_os, 'big')


    app.printf('.')

    # Creating the Root Directory
    root = RootDir()
    system_folder = Directory(root, 'system', [])
    system_file = File(system_folder, 'system.bin', contents=str(int_pickled_os))
    system_file.metadata['length'] = length
    system_folder.add(system_file)
    root.add(system_folder)
    

    app.printf('.')

    # Serialize into JSON
    serialize_root_directory(root, DEFAULT_ROOTDIR_PATH)

    app.printf('\n\nSUCCESS!')

    return Response(0, '\nOS has been installed. Please reboot.', None)
