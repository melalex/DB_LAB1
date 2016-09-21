import weakref
import re
import view

from collections import deque


class Presenter(object):
    __SHOW_COMMAND = r"SHOW "
    __INSERT_COMMAND = r"INSERT "
    __DELETE_COMMAND = r"DELETE "
    __SELECT_COMMAND = r"SELECT"
    __EXIT_COMMAND = r"EXIT"

    def __init__(self):
        self._view = None
        self._model = None
        self._application = None

    @property
    def model(self):
        return self._model

    @property
    def application(self):
        return self._application

    @model.setter
    def model(self, value):
        self._model = value

    @application.setter
    def application(self, value):
        ref = weakref.ref(value)
        self._application = ref()

    def make_request(self, request):
        if re.match(self.__SHOW_COMMAND, request, re.IGNORECASE):
            table_name_regex = re.compile(r'\w+', re.IGNORECASE)
            table_name = table_name_regex.match(request, len(self.__SHOW_COMMAND))
            if table_name:
                self.__show_table(table_name.group(0))
            else:
                view.syntax_error(request)
        elif re.match(self.__INSERT_COMMAND, request, re.IGNORECASE):
            table_name_regex = re.compile(r'\w+', re.IGNORECASE)
            table_name = table_name_regex.match(request, len(self.__INSERT_COMMAND))
            values = re.search(r'\(.+\)', request)
            if table_name and values:
                self.__insert_into_table(table_name.group(0), values.group(0))
            else:
                view.syntax_error(request)
        elif re.match(self.__DELETE_COMMAND, request, re.IGNORECASE):
            table_name_regex = re.compile(r'\w+', re.IGNORECASE)
            table_name = table_name_regex.match(request, len(self.__DELETE_COMMAND))
            entity_id = re.search(r'\([\d]+\)', request)
            if table_name and entity_id:
                self.__insert_into_table(table_name.group(0), entity_id.group(0))
            else:
                view.syntax_error(request)
        elif re.match(self.__SELECT_COMMAND, request, re.IGNORECASE):
            self.__select()
        elif re.match(self.__EXIT_COMMAND, request, re.IGNORECASE):
            self.application.stop()
        else:
            command = re.match(r'\w+', request)
            if command:
                view.unknown_command(command.group(0))

    def __show_table(self, table_name):
        if table_name in self.model:
            view.show_table(self.model[table_name])
        else:
            view.unknown_command(table_name)

    def __insert_into_table(self, table_name, values):
        if table_name in self.model:
            table = self.model[table_name]
            types = table["COLUMNS_TYPES"]
            content = table["CONTENT"]
            columns = table["COLUMNS"]
            values = values.translate(None, "()")
            values_list = values.split(",")

            if len(types) - 1 == len(values_list):
                try:
                    row = deque()

                    if len(content) > 0:
                        row.append(content[-1][0] + 1)
                    else:
                        row.append(1)

                    for index, value in enumerate(values_list):
                        row.append(types[index + 1](value.strip()))

                    content.append(row)
                except ValueError:
                    view.arguments_mismatch(values, columns)
            else:
                view.arguments_mismatch(values, columns)
        else:
            view.unknown_table(table_name)

    def __delete(self, table_name, entity_id):
        print table_name
        print entity_id

    def __select(self):
        pass
