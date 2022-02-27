from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from logging_module.custom_logging import get_logger
from utils.deserializer import deserialize_root_directory
from utils.serializer import serialize_root_directory 
if TYPE_CHECKING:
    from game.storage_system.directory import RootDir
    from game.operating_system import OperatingSystem


class InternalStorageMedium(object):
    """Class representing an internal storage medium"""
    
    def __init__(self, path = None) -> None:
        self.data: Optional[RootDir]

        if path:
            self.data = deserialize_root_directory(path)
        else:
            self.data = None
    
    def get_data(self) -> RootDir:
        """Returns the data stored in the storage media"""
        
        return self.data


class ExternalStorageMedium(object):
    """Class represting an external storage medium"""

    def __init__(self, name: str, root: RootDir, is_bootable: bool = False) -> None:
        self.name: str = name
        self.root: RootDir = root
        self.is_bootable = is_bootable

    def get_data(self) -> RootDir:
        """Returns the file system saved within the storage medium"""

        return self.root
