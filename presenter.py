import weakref

from re import split


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
        arguments = split(r"\W+", request)

        arguments_count = len(arguments)

        if arguments_count < 1:
            return

        command = arguments[0].upper()

        if arguments_count > 2 and command == "SHOW":
            self.__show_table(arguments[1].upper())
        elif arguments_count > 4 and command == "INSERT":
            table_name = arguments[1].upper()

            if table_name == "CINEMAS":
                self.__insert_into_cinemas(arguments[2], arguments[3])
            elif arguments_count > 5 and table_name == "SESSIONS":
                self.__insert_into_sessions(arguments[2], arguments[3], arguments[4])
            else:
                self.view.unknown_table(table_name)

        elif arguments_count > 3 and command == "DELETE":
            self.__delete(arguments[1].upper(), arguments[2])
        elif command == "SELECT":
            self.__select()
        elif command == "EXIT":
            self.application.stop()
        else:
            self.view.unknown_command(command)

    def __show_table(self, table_name):
        if table_name == "CINEMAS":
            self.view.show_cinemas_table(self.model[table_name])
        elif table_name == "SESSIONS":
            self.view.show_sessions_table(self.model[table_name])
        else:
            self.view.unknown_table(table_name)

    def __insert_into_cinemas(self, name, location):
        pass

    def __insert_into_sessions(self, name, time, cinema_id):
        pass

    def __delete(self, table_name, entity_id):
        pass

    def __select(self):
        pass
