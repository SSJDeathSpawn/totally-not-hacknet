from typing import TYPE_CHECKING, Optional
from collections.abc import Callable

if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


class Response(object):
    """Template for a command response"""

    def __init__(self, status: int, stdout: Optional[str]='', stderr: Optional[str]='') -> None:
        self.status = status
        self.stdout = stdout
        self.stderr = stderr

class Command(object):
    """Class representing a command in the Operating System"""

    def __init__(self, name: str, func: Callable[[OperatingSystem, list[str]], Response], man_entry: str='') -> None:
        self.name = name
        self.func = func
        self.man_entry = man_entry

    def __call__(self, os: OperatingSystem, *args) -> Response:
        return self.func(os, *args)
