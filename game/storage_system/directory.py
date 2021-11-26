from custom_logging.logging import get_logger
from utils import id_generator
from exceptions.storage_system import *
from game.storage_system.storage_unit import StorageUnit


logger = get_logger('game')


class Directory(StorageUnit):
    """Directory of a file system.

    This class represents a directory in the virtual file system, and inherits from StorageUnit.
    This class can store other Storage Units.

    Attributes:
        SUID -- ID of the directory.
        name -- string representing the name of the directory.
        contents -- list containing the contents of the directory. 
        parent -- Directory which this directory belongs to. 
    """
    
    def __init__(self, name, contents, parent):
        """InitializeS the directory using a name, contents and a parent.
        
        Arguments:
            name -- name of the directory.
            contents -- contents of the directory.
            parent -- parent of the directory.
        """

        super().__init__(f'DIR-{id_generator.generate_id()}', name, contents, parent)

    def bfs(self, depth = 0):
        """Returns the contents of the directory in tree format"""

        bfsstr = ''
        
        for su in self.get_contents():
            bfsstr += '\n'
            bfsstr += ('|    ' * depth)
            bfsstr += ('| -- ')
            bfsstr += su.get_name()
        
            if isinstance(su, Directory):
                bfsstr += su.bfs(depth + 1)
            
        return bfsstr if depth != 0 else bfsstr[1:]

    def has_su(self, su):
        """Checks if a storage unit belongs to this directory or any of its sub directories."""

        for content in self.get_contents():
            if content == su:
                return True
            if isinstance(content, Directory):
                if content.has_su(su):
                    return True
        
        return False

    def add(self, su):
        """Adds a storage unit to the contents of the directory"""

        self._validate_directory_element(su)
        self.contents.append(su)
        if su.parent and su.parent != self:
            su.parent.delete(su.get_name())
        su.set_parent(self)

        logger.debug(f'Added {su.__class__.__name__} with ID {su.get_id()} and name {su.get_name()} to {self.__class__.__name__} with ID {self.SUID}')

    def delete(self, su_name):
        """Deleted a storage unit from the contents of the directory"""

        su = self.get_su_by_name(su_name)
        if su:
            self.contents.remove(su)
            su.set_parent(None)

            logger.debug(f'Deleted {su.__class__.__name__} with ID {su.get_id()} and name {su.get_name()} from {self.__class__.__name__} with ID {self.SUID}')
        else:
            logger.warning(f'No SU with name {su_name} in contents of {self.__class__.__name__} with ID {self.SUID}')

    def get_path(self):
        """Returns the Directory's absolute path"""

        return f'{self.parent.get_path()}{self.get_name()}/'

    def get_su_by_name(self, su_name):
        """Returns SU with the given name from contents."""

        elements = list(filter(lambda su: su.get_name() == su_name, self.contents))
        if len(elements) > 0:
            return elements[0]
        return

    def set_contents(self, contents):
        """Set contents fot the directory."""

        self._validate_contents(contents)
        self.contents = contents

        logger.debug(f'Set contents for {self.__class__.__name__} with id {self.SUID}')

    def _validate_contents(self, contents):
        """Raises approprite exception if directory contents are of invalid type."""

        if not isinstance(contents, list):
            raise DirectoryContentsError(contents, 'Contents need to be of type list')
        
        for element in contents:
            self._validate_directory_element(element)

    def _validate_directory_element(self, su):
        """Raises appropriate exception if directory element is invalid"""

        if not isinstance(su, StorageUnit):
            raise DirectoryElementError(su, 'Element needs to be of type StorageUnit')

        if su.get_name() in [s.get_name() for s in self.contents]:
            raise DirectoryElementError(su, 'Directory cannot have duplicate elements')


class RootDir(Directory):
    """Class representing the Root Directory.

    This class represents the root directory in the virtual file system.
    It doesn't have a name or a parent.
    """

    def __init__(self, contents):
        """Initializes the root directory using contents."""
        
        super().__init__('', contents, None)

    def get_path(self):
        """Returns path of the root dir"""

        return '/'

    def _validate_name(self, name):
        """Raises exception if there is a name."""

        if name != "":
            raise RootDirName(name, 'Cannot assign a name to root directory.')
    
    def _validate_parent(self, parent):
        """Raises exception if there is a parent."""

        if parent:
            raise RootDirParent(parent, 'Cannot assign a parent to root directory.')
