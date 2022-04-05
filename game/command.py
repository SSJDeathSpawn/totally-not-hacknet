from __future__ import annotations
from typing import TYPE_CHECKING, Optional
from collections.abc import Callable

if TYPE_CHECKING:
    from game.applications.application import Application


class Response(object):
    """Template for a command response"""

    def __init__(self, status: int, stdout: Optional[str]='', stderr: Optional[str]='') -> None:
        self.status = status
        self.stdout = stdout
        self.stderr = stderr

class Command(object):
    """Class representing a command in the Operating System"""

    def __init__(self, name: str, func: Callable[[Application, list[str]], Response], man_entry: str='') -> None:
        self.name = name
        self.func = func
        self.man_entry = man_entry

    def __call__(self, app: Application, *args) -> Response:
        return self.func(app, *args)
