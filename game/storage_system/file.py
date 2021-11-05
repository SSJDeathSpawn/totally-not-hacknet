from custom_logging.logging import get_logger
from utils import id_generator
from game.storage_system.storage_unit import StorageUnit
from exceptions.storage_system import *


logger = get_logger('game')


class File(StorageUnit):
    """Class representing a file in the virtual file system.

    This class represents a file in the virtual file system, and it inherits from StorageUnit.
    It needs to have a name, contents and a parent.

    Attributes:
        SUID -- ID of the file.
        name -- string representing the name of the file.
        contents -- represent the contents of the file.
        parent -- Directory which the file belongs to.
    """

    def __init__(self, name, contents, parent):
        """Initializes the file using name, contents and a parent.
        
        Arguments:
            name -- string representing the name of the file.
            contents -- represent the contents of the file.
            parent -- Directory which the file belongs to.
        """
        
        super().__init__(f'FILE-{id_generator.generate_id()}', name, contents, parent)

    def set_name(self, name):
        """Splits name into filename and extension and stores them."""

        self._validate_name(name)
        namesplit = name.split('.')
        self.filename = namesplit[0] if len(namesplit) == 1 else '.'.join(namesplit[0:-1])
        self.extension = None if len(namesplit) == 1 else namesplit[-1]

        logger.debug(f'Setting name for {self.__class__.__name__} with id {self.SUID} to "{name}"')

    def replace(self, old, new, count=None):
        """Replaces a part of the contents with something else.
        
        Arguments:
            old -- The part of the contents you wish to replace.
            new -- What you want to replace it with.
            count -- (optional) how many of old to replace with new.
        """

        if isinstance(self.get_contents(), bytes):
            raise TypeError('Cannot replace contents of a byte file.')
        if not (isinstance(old, str) and isinstance(new, str)):
            raise TypeError('Both arguments need to be of type str.', old, new)

        self.contents = self.contents.replace(old, new, count) if count else self.get_contents().replace(old, new)
        logger.debug(f'Replaced "{old}" with "{new}" in the contents of {self.__class__.__name__} with id {self.SUID}.')

    def get_name(self):
        """Returns the name of the file."""

        return f'{self.filename}.{self.extension}' if self.extension else self.filename

    def _validate_contents(self, contents):
        """Raises appropriate exception if file contents are of invalid type."""

        super()._validate_contents(contents)
        if isinstance(contents, list):
            raise FileContentsError(contents, 'File contents need to be of type str or bytes.')
