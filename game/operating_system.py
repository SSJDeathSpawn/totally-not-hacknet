from custom_logging.logging import get_logger
from game.application import Application


logger = get_logger('game')


class OperatingSystem(object):
    async def __init__(self, system):
        self.system = system

        self.applications = {
            'APPLICATION': {
                'class': Application,
                'instances': []
            }
        }

    async def initialize(self):
        # start terminal app

        # prompt for username and password

        pass

    def start_application(self, name, os):
        app = self.applications[name]['class'](self, os)
        self.applications[name]['instances'].append(app)
        return app

    def open_terminal(self, os):
        # terminal = Terminal(self, os)
        # self.active_terminals.append(terminal)
        # return terminal
        pass

    def start(self):
        self.main_terminal = self.open_terminal(self)
        # while True:
        #     self.main_terminal.stdout('Input username: ')
        #     username = await self.main_terminal.stdin()
        #     self.main_terminal.stdout('Input password: ')
        #     password = await self.main_terminal.stdin(hidden=True)

        #     if username != self.username: 
        #         self.main_terminal.stdout('Invalid username')
        #         continue

        #     if password != self.password:
        #         self.main_terminal.stdout('Wrong password')
        #         continue
