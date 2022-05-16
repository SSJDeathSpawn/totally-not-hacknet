from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from game.applications.application import Application

DEFAULT_ROOTDIR_PATH: str = 'res/game/root.json'

FPS = 120

# Applications
APPLICATIONS: dict[str, Application] = {

}

# DEBUG
HOSTNAME: str = 'hackerman'

# User events
DIRECTORY_CHANGE: pygame.event.Event = pygame.USEREVENT + 1
