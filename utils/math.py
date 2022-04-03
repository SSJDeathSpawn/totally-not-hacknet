import logging

from logging_module.custom_logging import get_logger


logger: logging.Logger = get_logger(__name__)


def between(point: tuple[int, int], corner_tl: tuple[int, int], corner_br: tuple[int, int]) -> bool:
    """Returns True if a point is between two corner points (top left and bottom right)"""
    
    return corner_tl[0] <= point[0] <= corner_br[0] and corner_tl[1] <= point[1] <= corner_br[1]


def clamp(val: int, min_val: int, max_val: int) ->  int:
    """Restricts the value to the given range"""
    
    return max(min(val, max_val), min_val)