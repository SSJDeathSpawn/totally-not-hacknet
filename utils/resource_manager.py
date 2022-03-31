import logging
import os.path

from multiprocessing import Semaphore
from logging_module.custom_logging import get_logger
from collections.abc import Callable


def uses_resource(func: Callable, name: str, handles: bool) -> None:
    func.resource = name
    func.handles = handles
    return func


class ResourceManager(object):
    """The operating system's resource manager"""

    logger: logging.Logger = get_logger(__name__)
    resources: dict[str, Semaphore] = dict()
        
    @staticmethod
    def add_resource(name: str) -> str:
        """Adds a shared resource to manage"""

        ResourceManager.logger.debug(f'Adding new resource {name}')
        ResourceManager.resources[name] = Semaphore(1)
    
    @staticmethod
    def use_resource(func: Callable, *args, **kwargs) -> None:
        """Uses a resource"""

        if not getattr(func, 'resource') and not getattr(func, 'handles'):
            ResourceManager.logger.error('Function does not use any resource.')
            return

        sem: Semaphore = ResourceManager.resources.get(func.resource)
        if not sem:
            if os.path.exists(func.resource) or func.handles:
                ResourceManager.add_resource(func.resource)
            else:
                ResourceManager.logger.error(f'Resource {func.resource} does not exist. Ignoring request.')
                return

        ResourceManager._acquire_resource(func.resource)
        func(*args, **kwargs)
        ResourceManager._release_resource(func.resource)

    @staticmethod
    def _acquire_resource(name: str) -> None:
        """Acquire a resource"""

        sem: Semaphore = ResourceManager.resources.get(name)
        if sem:
            sem.acquire()
            
        # else:
        #     if os.path.exists(name):
        #         ResourceManager.add_resource(name)
        #     else:
        #         ResourceManager.logger.error(f'Resource {name} does not exist. Ignoring request.')
        #         return

    @staticmethod
    def _release_resource(name: str) -> None:
        """Release a resource"""

        sem: Semaphore = ResourceManager.resources.get(name)
        if sem:
            sem.release()

        # else:
        #     if os.path.exists(name):
        #         ResourceManager.add_resource(name)
        #     else:
        #         ResourceManager.logger.error(f'Resource {name} does not exist. Ignoring request.')
        #         return
        