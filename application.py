class Application(object):

    def __init__(self):
        self.isRunning = True
        self._presenter = None

    def run(self):
        while self.isRunning:
            pass

    def stop(self):
        self.isRunning = False

    @property
    def presenter(self):
        return self._presenter

    @presenter.setter
    def presenter(self, value):
        self._presenter = value
        value.application = self
