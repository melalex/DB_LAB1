class Application(object):

    class __Application(object):

        def __init__(self):
            self.isRunning = True
            self.controller = None

        def run(self):
            while self.isRunning:
                pass

        def stop(self):
            self.isRunning = False

    instance = None

    def __new__(cls, *args, **kwargs):
        if not Application.instance:
            Application.instance = Application.__Application()
        return Application.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name, value):
        return setattr(self.instance, name, value)
