from utils.general_utils import generate_network_id, generate_host_id


class Router(object):
    """Class representing a router"""

    def __init__(self) -> None:
        """Normal constructor"""

        self.network_id = generate_network_id()
        self.conn_comps = {}

    def __init__(self, **kwargs) -> None:
        """Constructor to be used when loading from save file"""

        for i in kwargs:
            self.__setattr__(i, kwargs[i])

    def join(self, os):
        """Adds an OS to the network"""

        self.conn_comps[os] = self.network_id + "." + generate_host_id(self.network_id)

    def is_connected(self, os):
        """Checks if an OS is part of the network"""

        return os in self.conn_comps 


class Internet(object):
    """Class representing the Internet"""

    # Network ID, Router
    conn_networks = {} 
    
    # Name, IP Address
    domain_names = {}

    @staticmethod
    def add_router(network_id: str, router: Router):
        """Adds a router to the internet"""

        Internet.conn_networks[network_id] = router

    @staticmethod
    def add_domain(name: str, ip_address: str):
        """Adds a domain to the internet"""

        Internet.domain_names[ip_address] = name
