from __future__ import annotations
from typing import Union, TYPE_CHECKING, Optional, Any
from exceptions.storage_system import StorageUnitError
from game.storage_system.constants import INVALID_CHARACTERS
if TYPE_CHECKING:
    from game.storage_system.directory import Directory


class StorageUnit(object):
    """Class representing a storage unit in the virtual file system"""

    def __init__(self, parent: Directory, name: str, contents: Union[str, bytes, list[StorageUnit]]) -> None:

        self._validate_parent(parent)
        self.parent: Directory = parent

        self._validate_name(name)
        self.set_name(name)

        self._validate_contents(contents)
        self.contents: Union[str, bytes, list[StorageUnit]] = contents

        self.metadata: dict[str, Any] = {}

    # Getters

    def get_parent(self) -> Optional[Directory]:
        """Returns the storage unit's parent"""

        return self.parent

    def get_name(self) -> str:
        """Returns the storage unit's name"""

        return self.name

    def get_contents(self) -> Union[str, bytes, list[StorageUnit]]:
        """Returns the storage unit's contents"""

        return self.contents

    # Setters

    def set_parent(self, parent: Directory) -> None:
        """Sets the storage unit's parent"""

        self._validate_parent(parent)
        self.parent = parent

    def set_name(self, name: str) -> None:
        """Sets the storage unit's name"""

        self._validate_name(name)
        self.name = name

    def set_contents(self, contents: Union[str, bytes, list[StorageUnit]]) -> None:
        """Sets the storage unit's contents"""

        self._validate_contents(contents)
        self.contents = contents

    # Validation

    def _validate_parent(self, parent: Directory) -> None:
        """Checks if the parent is valid"""

        from game.storage_system.directory import Directory

        if not isinstance(parent, Directory):
            raise StorageUnitError('Storage unit\'s parent needs to be of type Directory.')
    
    def _validate_name(self, name: str) -> None:
        """Checks if the name is valid"""

        if not isinstance(name, str):
            raise StorageUnitError('Storage unit\'s name needs to be of type str.')

        if len(name) < 1:
            raise StorageUnitError('Storage unit\'s name needs to be atleast 1 character long.')

        if len(name) > 50:
            raise StorageUnitError('Storage unit\'s name can only be atmost 50 character long.')

        for letter in name:
            if letter in INVALID_CHARACTERS:
                raise StorageUnitError(f'Storage unit\'s name cannot have any of the following characters -> {INVALID_CHARACTERS}')

    def _validate_contents(self, contents: Union[str, bytes, list[StorageUnit]]) -> None:
        """Checks if the contents are valid"""

        if not (isinstance(contents, str) or isinstance(contents, bytes) or isinstance(contents, list)):
            raise StorageUnitError('Storage unit\'s contents need to be of one of the following types -> str, bytes, list[StorageUnit]')

    # Magic functions

    def __str__(self) -> str:
        
        return self.get_path()
