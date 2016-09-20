import weakref


class Presenter(object):

    def __init__(self):
        self._view = None
        self._model = None
        self._application = None

    @property
    def view(self):
        return self._view

    @property
    def model(self):
        return self._model

    @property
    def application(self):
        return self._application

    @view.setter
    def view(self, value):
        self._view = value

    @model.setter
    def model(self, value):
        self._model = value

    @application.setter
    def application(self, value):
        self._application = weakref.ref(value)

    def make_request(self, request):
        pass
