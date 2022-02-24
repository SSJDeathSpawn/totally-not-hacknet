from __future__ import annotations
from typing import TYPE_CHECKING
from logging_module.custom_logging import get_logger
from utils.deserializer import deserialize_root_directory
from utils.serializer import serialize_root_directory 
if TYPE_CHECKING:
    from game.storage_system.directory import RootDir
    from game.operating_system import OperatingSystem


class InternalStorageMedium(object):
    """Class representing an internal storage medium"""
    
    def __init__(self, path) -> None:
        self.data: RootDir = deserialize_root_directory(path)
    
    def get_data(self) -> RootDir:
        """Returns the data stored in the storage media"""
        return self.data


class ExternalStorageMedium(object):
    """Class represting an external storage medium"""

    def __init__(self, root: RootDir) -> None:
        self.root: RootDir = root

    def get_data(self) -> RootDir:
        """Returns the file system saved within the storage medium"""

        return self.root
