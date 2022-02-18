from typing import Optional, Union
from exceptions.storage_system import FileError
from game.storage_system.storage_unit import StorageUnit
from game.storage_system.directory import Directory


class File(StorageUnit):
    """Class representing a file in the virtual file system"""

    def __init__(self, parent: Directory, name: str, contents: Union[str, bytes]) -> None:

        self.filename: str
        self.extension: Optional[str]

        super().__init__(parent, name, contents)

    # Getters

    def get_name(self) -> str:
        """Returns the file's name"""

        if self.extension:
            return f'{self.filename}.{self.extension}'

        else:
            return self.filename

    def get_path(self) -> str:
        """Returns the file's absolute path"""
        
        return f'{self.parent.get_path()}{self.get_name()}'
        
    # Setters

    def set_name(self, name: str) -> None:
        """Splits name into filename and extension and stores them"""

        self._validate_name(name)

        namesplit = name.split('.')
        
        if len(namesplit) < 2:
            self.filename = namesplit[0]
            self.extension = None

        else:
            self.filename = '.'.join(namesplit[:-1])
            self.extension = namesplit[-1]
        
    # Validation

    def _validate_contents(self, contents: Union[str, bytes]) -> None:
        """Checks if the contents are valid"""
        
        super()._validate_contents(contents)

        if isinstance(contents, list):
            raise FileError('File\'s contents need to be of one of the following types -> str, bytes')
