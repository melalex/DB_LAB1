
class View(object):

    def show_table(self, table):
        pass

    def syntax_error(self, request):
        print 'Syntax error in request "{0}"'.format(request)

    def unknown_command(self, command):
        print 'Unknown command "{0}"'.format(command)

    def unknown_table(self, table_name):
        print 'Unknown table "{0}"'.format(table_name)

    def arguments_mismatch(self, arguments, table_columns):
        print 'Arguments_mismatch "({0})" with "{1}"'.format(arguments, table_columns)
