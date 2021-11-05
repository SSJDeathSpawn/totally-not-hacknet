from custom_logging.logging import get_logger
from exceptions.storage_system import *


logger = get_logger('game')


class StorageUnit(object):
    """Storage unit of a file system.

    This class represents a storage unit of the virtual file system.
    This class cannot be used on it's own.
    It can be used either as a File or a Directory.

    Attributes:
        SUID -- ID of the storage unit.
        name -- string representing the name of the storage unit.
        contents -- the contents of the storage unit. 
        parent -- Directory which the storage unit belongs to.       
    """

    def __init__(self, suid, name, contents, parent):
        """Initializes StorageUnit using name, contents and a parent.
        
        Arguments:
            suid -- ID of the storage unit.
            name -- name of the storage unit.
            contents -- contents of the storage unit.
            parent -- Directory which the storage unity belongs to.
        """

        self.SUID = suid

        self.set_name(name)
        self.set_parent(parent)
        self.set_contents(contents)

        logger.debug(f'Initialized {self.__class__.__name__} with id {self.SUID}.')

    def __str__(self):
        return self.get_name()

    def set_name(self, name):
        """Sets the name attribute of the class"""
        
        self._validate_name(name)
        self.name = name

        logger.debug(f'Set name for {self.__class__.__name__} with id {self.SUID} to {name}.')

    def set_parent(self, parent):
        """Sets the parent attribute of the class"""

        self._validate_parent(parent)
        self.parent = parent

        logger.debug(f'Set parent for {self.__class__.__name__} with id {self.SUID} to {parent}')

    def set_contents(self, contents):
        """Sets the contents attribute of the class"""
        
        self._validate_contents(contents)
        self.contents = contents

        logger.debug(f'Modified contents for {self.__class__.__name__} with id {self.SUID}.')

    def get_id(self):
        """Returns the SUID"""

        return self.SUID

    def get_name(self):
        """Returns the SU's name"""

        return self.name

    def get_parent(self):
        """Returns the SU's parent"""

        return self.parent

    def get_contents(self):
        """Returns the SU's contents"""

        return self.contents

    def get_path(self):
        """Returns the SU's absolute path"""

        return f'{self.parent.get_path()}{self.get_name()}'

    def _validate_name(self, name):
        """Raises appropriate exception if name is invalid."""

        if not isinstance(name, str):
            raise SUNameError(name, 'Name needs to be of type string')

        if len(name) < 1:
            raise SUNameError(name, 'Name cannot be empty')

        if len(name) > 50:
            raise SUNameError(name, 'Name is too long')

        for letter in name:
            if letter in ['<', '>', ':', '"', '/', '\\', '|', '?', '*', ' ']:
                raise SUNameError(name, f'Name cannot contain {letter}')
    
    def _validate_parent(self, parent):
        """Raises appropriate exception if parent is invalid."""

        from game.storage_system.directory import Directory
        if parent:
            if not isinstance(parent, Directory):
                raise SUParentError(parent, 'Parent needs to be of type Directory')

    def _validate_contents(self, contents):
        """Validates contents."""
    
        if not (isinstance(contents, str) or isinstance(contents, bytes) or isinstance(contents, list)):
            raise SUContentsError(contents, 'Contents are not of a valid type')
