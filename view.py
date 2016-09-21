from __future__ import print_function
from collections import deque


def __write_separator(length):
    print('|', end='')
    i = 0
    while i < length:
        print('-', end='')
        i += 1
    print('|')


def syntax_error(request):
    print('Syntax error in request "{0}"'.format(request))


def unknown_command(command):
    print('Unknown command "{0}"'.format(command))


def unknown_table(table_name):
    print('Unknown table "{0}"'.format(table_name))


def arguments_mismatch(arguments, table_columns):
    print('Arguments_mismatch "{0}" with "{1}"'.format(arguments, table_columns))


def show_table(table):
    table_columns = table["COLUMNS"]
    table_content = table["CONTENT"]

    if len(table_content) > 0:
        column_length = deque()
        columns_count = len(table_columns)

        for index in xrange(columns_count):
            max_length = len(table_columns[index])

            for row in table_content:
                row_length = len(str(row[index]))
                if row_length > max_length:
                    max_length = row_length

            column_length.append(max_length + 3)

        table_length = sum(column_length) + columns_count - 1

        __write_separator(table_length)

        print('|', end='')
        for index, column in enumerate(table_columns):
            formatter = "%{0}s|".format(column_length[index])
            print(formatter % format(column), end='')
        print()

        __write_separator(table_length)

        for row in table_content:
            print('|', end='')
            for index, column in enumerate(row):
                formatter = "%{0}s|".format(column_length[index])
                print(formatter % str(column), end='')
            print()

        __write_separator(table_length)
