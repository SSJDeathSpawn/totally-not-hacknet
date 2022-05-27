from __future__ import annotations
from typing import Optional, TYPE_CHECKING
from logging import Logger

from logging_module.custom_logging import get_logger
from game.storage_system.directory import Directory, RootDir
from game.storage_system.file import File
from exceptions.ser_des import DeserializationError
from utils.validator import validate_root_dir_contents
if TYPE_CHECKING:
    from game.storage_system.storage_unit import StorageUnit

import json


logger: Logger = get_logger(__name__)

def deserialize_root_directory(path: str) -> Optional[RootDir]:
    """Converts a JSON file (path given) into a RootDir object"""

    try:
        with open(path, 'r') as f:
            root_dir_contents = json.load(f) 

    except FileNotFoundError:
        raise DeserializationError(f'JSON file path ({path}) not found. Cannot deserialize')

    validate_root_dir_contents(root_dir_contents)

    root = RootDir([])

    for content in root_dir_contents:
        if isinstance(content.get('contents'), list):
            root.add(__dict2dir(content, root))
        elif isinstance(content.get('contents'), str):
            root.add(__dict2file(content, root))

    return root


def __dict2dir(dir_dict: dict[str, list[StorageUnit]], parent: Directory) -> Directory:
    """Converts a dictionary into a Directory object with the given parent"""

    new_dir = Directory(parent, dir_dict.get('name'), [])
    
    contents = []
    
    for content in dir_dict.get('contents'):  
        if not isinstance(content.get('contents'), list):
            contents.append(__dict2file(content, new_dir))
        else:
            contents.append(__dict2dir(content, new_dir))
            
    new_dir.set_contents(contents)

    for key in dir_dict.keys():
        if key not in ['contents', 'name']:
            new_dir.metadata[key] = dir_dict.get(key)
    
    return new_dir


def __dict2file(file_dict: dict[str, str], parent: Directory) -> File:
    """Converts a dictionary into a File object"""

    new_file = File(parent, file_dict.get('name'), file_dict.get('contents')) # FIXME: Make this ^^ work. Convert to 0's and 1s but in string
    
    for key in file_dict.keys():
        if key not in ['contents', 'name']:
            new_file.metadata[key] = file_dict.get(key)
    
    #if file_dict.get('name').split('.')[-1] in ss_consts.BINARY_EXTS:
    return new_file
    #else:
    #    return File(parent, file_dict.get('name'), file_dict.get('contents'))
