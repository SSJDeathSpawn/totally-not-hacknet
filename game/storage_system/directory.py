from __future__ import annotations
from logging import Logger
from typing import Optional
from exceptions.storage_system import DirectoryError, RootDirError
from game.storage_system.storage_unit import StorageUnit
from logging_module.custom_logging import get_logger


#dict2dir
#...
#return Directory()

class Directory(StorageUnit):
    """Class representing a directory in the virtual file system"""

    def __init__(self, parent: StorageUnit, name: str, contents: list[StorageUnit]) -> None:

        super().__init__(parent, name, contents)

        self.logger: Logger = get_logger('game')

    # Getters

    def get_path(self) -> str:
        """Returns the directory's absolute path"""
        
        return f'{self.parent.get_path()}{self.get_name()}/'

    def get_su_by_name(self, name: str) -> Optional[StorageUnit]:
        """Returns SU with the given name from contents"""

        elements = list(filter(lambda su: su.get_name() == name, self.contents))

        if len(elements) == 0:
            return None

        return elements[0]

    # Setters

    def set_contents(self, contents: list[StorageUnit]) -> None:
        """Sets the contents of a directory"""

        self._validate_contents(contents)
        self.contents = contents

    # Operations

    def add(self, su: StorageUnit) -> None:
        """Adds a storage unit to the contents"""

        self._validate_directory_element(su)

        if self.get_su_by_name(su.get_name()) is not None:
            raise DirectoryError('Directory cannot have more than 1 storage units with the same name')

        self.contents.append(su)

    def delete(self, su: StorageUnit) -> None:
        """Deletes a storage unit from the contents"""

        try:
            self.contents.remove(su)
        except ValueError:
            self.logger.warning('Given storage unit is not a child. Ignoring delete request')

    # Validation

    def _validate_contents(self, contents: list[StorageUnit]) -> None:
        "Checks if the contents are valid"

        if not isinstance(contents, list):
            raise DirectoryError("Directory contents need to be of type list")

        for element in contents:
            self._validate_directory_element(element)

        for element in contents:
            if len(list(filter(lambda su: su.get_name() == element.get_name(), contents))) > 1:
                raise DirectoryError('Directory cannot have more than 1 storage units with the same name')

    def _validate_directory_element(self, element: StorageUnit) -> None:
        """Checks if the directory element is valid"""

        if not isinstance(element, StorageUnit):
            raise DirectoryError("Units in the directory need to be of type StorageUnit")


class RootDir(Directory):
    """Class representing the root directory in the virtual file system"""

    def __init__(self, contents: list[StorageUnit]) -> None:

        super().__init__(None, '', contents)

    # Getters
    
    def get_path(self) -> str:
        """Returns the path of the root directory"""

        return '/'

    # Validation

    def _validate_name(self, name: str) -> None:
        """Checks if the name is valid"""

        if name != "":
            raise RootDirError('Root directory cannot have a name')

    def _validate_parent(self, parent: None) -> None:
        """Checks if the parent is valid"""

        if parent is not None:
            raise RootDirError('Root directory cannot have a parent')
