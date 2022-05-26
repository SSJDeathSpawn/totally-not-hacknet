from game import OperatingSystem, BOOT_MEDIA_ROOTDIR_PATH, Command
from game.storage_system import RootDir
from game.applications import TeleTypeWriter
from utils import deserialize_root_directory
from commands.basic import *
from commands import install_os
from pickle import dumps, loads


progenitor: OperatingSystem = OperatingSystem(RootDir())
progenitor.startup_apps = {
    TeleTypeWriter: False
}
progenitor.commands = {
    'ls': Command('ls', ls, ''),
    'cd': Command('cd', cd, ''),
    'exit': Command('exit', exit_, ''),
    'cat': Command('cat', cat, ''),
    'mkdir': Command('mkdir', mkdir, ''),
    'touch': Command('touch', touch, ''),
    'mv': Command('mv', mv, ''),
    'clear': Command('clear', clear, ''),
    'install': Command('install', install_os, ''),
    'reboot': Command('reboot', reboot, '')
}

progenitor: bytes = dumps(progenitor)
s = len(progenitor)
print(s)
progenitor = int.from_bytes(progenitor, 'big')
print(progenitor)
progenitor = progenitor.to_bytes(s, 'big')
progenitor = loads(progenitor)

print(progenitor)

# progenitor = bytes(progenitor, 'utf-8')
# print(progenitor)
# progenitor = loads(progenitor)
# print(progenitor)