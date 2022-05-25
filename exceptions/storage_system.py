from exceptions.better_exception import LoggingException


class StorageUnitError(LoggingException):
    pass

class FileError(LoggingException):
    pass

class DirectoryError(LoggingException):
    pass

class RootDirError(LoggingException):
    pass

class PathError(LoggingException):
    pass
