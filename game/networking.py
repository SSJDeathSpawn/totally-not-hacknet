from __future__ import annotations
from utils.general_utils import generate_network_id, generate_host_id
from utils.resource_manager import ResourceManager
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from game.operating_system import OperatingSystem


class Router(object):
    """Class representing a router"""

    def __init__(self, **kwargs) -> None:
        if len(kwargs) == 0:
            self.network_id: str = generate_network_id()
            self.conn_comps: dict[str, OperatingSystem] = {}
        else:
            for i in kwargs:
                self.__setattr__(i, kwargs[i])

        Internet.add_router(self.network_id, self)

    def get_device(self, host_id: str) -> OperatingSystem | None:
        """Returns a device by host ID"""

        return self.conn_comps.get(host_id)

    def join(self, os: OperatingSystem) -> None:
        """Adds an OS to the network"""
        
        host_id = generate_host_id(self.network_id)
        if not host_id:
            return

        self.conn_comps[host_id] = os

    def is_connected(self, os: OperatingSystem) -> bool:
        """Checks if an OS is part of the network"""

        return os in self.conn_comps


class Internet(object):
    """Class representing the Internet"""

    conn_networks: dict[str, Router] = {}  # Network ID, Router
    domain_names: dict[str, str] = {}  # Name, IP Address

    @staticmethod
    def add_router(network_id: str, router: Router) -> None:
        """Adds a router to the internet"""

        Internet.conn_networks[network_id] = router

    @staticmethod
    def get_router(network_id: str) -> Router | None:
        """Returns a router with given network ID"""

        return Internet.conn_networks.get(network_id, None)
        
    @staticmethod
    def add_domain(name: str, ip_address: str) -> None:
        """Adds a domain to the internet"""

        Internet.domain_names[ip_address] = name
        
    @staticmethod
    def dns_parse(name: str) -> str | None:
        """Returns IP address for the given domain """
        
        return Internet.domain_names.get(name, None)
