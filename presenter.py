import weakref
import re
import view
import my_time

from collections import deque


class Presenter(object):
    __SHOW_COMMAND = re.compile(r'^SHOW (\w+)$', re.IGNORECASE)
    __INSERT_COMMAND = re.compile(r'^INSERT (\w+)\((.+)\)$', re.IGNORECASE)
    __DELETE_COMMAND = re.compile(r'^DELETE (\w+)\(([\d,]+)\)$', re.IGNORECASE)
    __SELECT_COMMAND = re.compile(r'^SELECT (\w+)\(([\d,]+)\)$', re.IGNORECASE)
    __FUNCTION_COMMAND = re.compile(r'^FUNCTION$', re.IGNORECASE)
    __EXIT_COMMAND = re.compile(r'^EXIT$', re.IGNORECASE)

    def __init__(self):
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
        disassembled_request = Presenter.__SHOW_COMMAND.match(request)
        if disassembled_request:
            table_name = disassembled_request.group(1)
            self.__show_table(table_name)
            return

        disassembled_request = Presenter.__INSERT_COMMAND.match(request)
        if disassembled_request:
            table_name = disassembled_request.group(1)
            values = disassembled_request.group(2).split(',')
            self.__insert_into_table(table_name, values)
            return

        disassembled_request = Presenter.__SELECT_COMMAND.match(request)
        if disassembled_request:
            table_name = disassembled_request.group(1)
            values = [int(entity_id.strip()) for entity_id in disassembled_request.group(2).split(',')]
            self.__select(table_name, values)
            return

        disassembled_request = Presenter.__DELETE_COMMAND.match(request)
        if disassembled_request:
            table_name = disassembled_request.group(1)
            values = [int(entity_id.strip()) for entity_id in disassembled_request.group(2).split(',')]
            self.__delete(table_name, values)
            return

        if Presenter.__FUNCTION_COMMAND.match(request):
            self.__function()
            return

        if Presenter.__EXIT_COMMAND.match(request):
            self.application.stop()
            return

        view.syntax_error(request)

    def __show_table(self, table_name):
        if table_name in self.model:
            view.show_table(self.model[table_name])
        else:
            view.unknown_table(table_name)

    def __insert_into_table(self, table_name, values_list):
        if table_name in self.model:
            table = self.model[table_name]
            types = table["COLUMNS_TYPES"]
            content = table["CONTENT"]
            columns = table["COLUMNS"]

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
                    view.arguments_mismatch(values_list, columns)
            else:
                view.arguments_mismatch(values_list, columns)
        else:
            view.unknown_table(table_name)

    def __select(self, table_name, entity_ids):
        if table_name in self.model:
            table = self.model[table_name]
            types = table["COLUMNS_TYPES"]
            columns = table["COLUMNS"]
            content = [row for row in table["CONTENT"] if row[0] in entity_ids]

            table = {"COLUMNS": columns, "COLUMNS_TYPES": types, "CONTENT": content}

            view.show_table(table)
        else:
            view.unknown_table(table_name)

    def __delete(self, table_name, entity_ids):
        if table_name in self.model:
            table = self.model[table_name]
            table["CONTENT"] = [row for row in table["CONTENT"] if row[0] not in entity_ids]

            if table_name.lower() == "cinemas":
                table = self.model["sessions"]
                table["CONTENT"] = [row for row in table["CONTENT"] if row[-1] not in entity_ids]
        else:
            view.unknown_table(table_name)

    def __function(self):
        content = self.model["sessions"]["CONTENT"]
        clock = my_time.Time("18:00")
        entity_ids = [row[-1] for row in content if row[-2] >= clock]
        self.__select("cinemas", entity_ids)
