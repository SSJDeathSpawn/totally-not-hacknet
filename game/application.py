from custom_logging.logging import get_logger


logger = get_logger('game')


class Application(object):
    def __init__(self, os, opened_by):
        self.os = os
        self.opened_by = opened_by
