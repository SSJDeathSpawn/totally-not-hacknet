from custom_logging.logging import get_logger
from game.applications.terminal import Terminal


logger = get_logger('game')


class OperatingSystem(object):
    def __init__(self, system):
        self.system = system
        self.memory_being_used = 0

        self.applications = {
            'TERMINAL': {
                'class': Terminal,
                'instances': []
            }
        }

        self.application_queue = []

    async def run_main_loop(self):
        await self.application_queue[0].run()
        for application in self.application_queue[1:]:
            await application.idle()

    async def initialize(self):
        self.start_application('TERMINAL', self)

        # prompt for username and password

        pass

    def start_application(self, name, os):
        app = self.applications[name]['class'](self, os)
        if app.memory + self.memory_being_used > self.system.memory:
            raise Exception() # MAKE AND RAISE CUSTOM EXCEPTION WHICH WILL BE HANDLED OUTSIDE
        self.applications[name]['instances'].append(app)
        self.application_queue.append(app)
        return app
