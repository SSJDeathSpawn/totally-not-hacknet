from __future__ import annotations
from typing import Optional
from utils import deserialize_root_directory
from game.storage_system import RootDir


class InternalStorageMedium(object):
    """Class representing an internal storage medium"""
    
    def __init__(self, path = None) -> None:
        self.root: Optional[RootDir]

        if path:
            self.root = deserialize_root_directory(path)
        else:
            self.root = None

    def set_data(self, data: RootDir) -> None:
        """Sets the root directory"""

        self.root = data
            
    def get_data(self) -> RootDir | None:
        """Returns the data stored in the storage media"""
        
        return self.root


class ExternalStorageMedium(object):
    """Class represting an external storage medium"""

    def __init__(self, name: str, root: RootDir | str, is_bootable: bool = False) -> None:
        self.name: str = name

        if isinstance(root, str):
            self.root = deserialize_root_directory(root)
        elif isinstance(root, RootDir):
            self.root: RootDir = root
            
        self.is_bootable = is_bootable

    def get_data(self) -> RootDir:
        """Returns the file system saved within the storage medium"""

        return self.root
