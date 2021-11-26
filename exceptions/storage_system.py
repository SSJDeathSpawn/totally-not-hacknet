class SUPathError(Exception):
    """Exception raised for errors related to SU Paths.

    Attributes:
        path -- invalid path which caused this error
        message -- explaination of the error
    """

    def __init__(self, path, message='Path is Invalid.'):
        self.path = path
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.path} -> {self.message}'


class SUNameError(Exception):
    """Exception raised for errors while setting SU names.

    Attributes:
        name -- invalid name which caused the error
        message -- explanation of the error
    """

    def __init__(self, name, message='Name is Invalid.'):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} -> {self.message}'


class SUParentError(Exception):
    """Exception raised for errors while setting SU parents.

    Attributes:
        parent -- invalid parent which caused the error
        message -- explanation of the error
    """

    def __init__(self, parent, message='Parent is Invalid.'):
        self.parent = parent
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.parent} -> {self.message}'


class SUContentsError(Exception):
    """Exception raised for errors while setting SU contents.

    Attributes:
        contents -- invalid contents which caused the error
        message -- explanation of the error
    """

    def __init__(self, contents, message='Contents are Invalid.'):
        self.contents = contents
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class FileContentsError(Exception):
    """Exception raised for errors while setting File contents.

    Attributes:
        contents -- invalid contents which caused the error
        message -- explanation of the error
    """

    def __init__(self, contents, message='Contents are Invalid.'):
        self.contents = contents
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message


class DirectoryContentsError(Exception):
    """Exception raised for errors while setting Directory contents.

    Attributes:
        contents -- invalid contents which caused the error
        message -- explanation of the error
    """

    def __init__(self, contents, message='Contents are Invalid.'):
        self.contents = contents
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message

class DirectoryElementError(Exception):
    """Exception raised for errors while setting Directory Elements.

    Attributes:
        element -- invalid element which caused the error
        message -- explanation of the error
    """

    def __init__(self, element, message='Element is Invalid.'):
        self.element = element
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.element} -> {self.message}'


class RootDirName(Exception):
    """Exception raised for errors while setting RootDir names.

    Attributes:
        name -- invalid name which caused the error
        message -- explanation of the error
    """

    def __init__(self, name, message='Cannot set a name.'):
        self.name = name
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} -> {self.message}'


class RootDirParent(Exception):
    """Exception raised for errors while setting RootDir parents.

    Attributes:
        parent -- invalid parent which caused the error
        message -- explanation of the error
    """

    def __init__(self, parent, message='Parent needs to be of type None.'):
        self.parent = parent
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.parent} -> {self.message}'
