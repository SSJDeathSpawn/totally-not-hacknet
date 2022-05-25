from game import OperatingSystem, BOOT_MEDIA_ROOTDIR_PATH, Command
from utils import deserialize_root_directory
from commands.basic import *
from pickle import dumps


progenitor: OperatingSystem = OperatingSystem(deserialize_root_directory(BOOT_MEDIA_ROOTDIR_PATH))
progenitor.startup_apps = {
    "": False
}
progenitor.commands = {
    'ls': Command('ls', ls, ''),
    'cd': Command('cd', cd, ''),
    'exit': Command('exit', exit_, ''),
    'cat': Command('cat', cat, ''),
    'mkdir': Command('mkdir', mkdir, ''),
    'touch': Command('touch', touch, ''),
    'mv': Command('mv', mv, ''),
    'clear': Command('clear', clear, '')
}

progenitor: bytes = dumps(progenitor)
