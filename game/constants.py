from __future__ import annotations
from typing import TYPE_CHECKING

import pygame

if TYPE_CHECKING:
    from game.applications.application import Application

DEFAULT_ROOTDIR_PATH: str = 'res/game/root.json'
BOOT_MEDIA_ROOTDIR_PATH: str = 'res/game/boot_media_root.json'

FPS = 60

# Applications
APPLICATIONS: dict[str, Application] = {

}

# DEBUG
HOSTNAME: str = 'hackerman'

# User events
DIRECTORY_CHANGE: pygame.event.Event = pygame.USEREVENT + 1
GET_INPUT: pygame.event.Event = pygame.USEREVENT + 2
INPUT_RECEIVED: pygame.event.Event = pygame.USEREVENT + 3
