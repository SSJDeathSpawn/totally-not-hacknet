class TerminalCommandError(Exception):
    """Exception raised for errors with Terminal Commands.

    Attributes:
        command -- command which caused the error
        message -- explanation of the error
    """

    def __init__(self, command, message='Command is Invalid.'):
        self.command = command
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.name} -> {self.message}'
