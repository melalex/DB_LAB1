import pickle
import application
import presenter

from os.path import isfile
from my_time import Time


FILE_NAME = "cinemas.meldb"

if isfile(FILE_NAME):
    dataBaseFile = open(FILE_NAME, 'rb')
    dataBase = pickle.load(dataBaseFile)
    dataBaseFile.close()
else:
    cinemas_columns = ("id", "name", "address")
    cinemas_columns_types = (int, str, str)
    cinemas_table = {"COLUMNS": cinemas_columns, "COLUMNS_TYPES": cinemas_columns_types, "CONTENT": list()}
    sessions_columns = ("id", "name", "time", "cinema_id")
    sessions_columns_types = (int, str, Time, int)
    sessions_table = {"COLUMNS": sessions_columns, "COLUMNS_TYPES": sessions_columns_types, "CONTENT": list()}
    dataBase = {"cinemas": cinemas_table, "sessions": sessions_table}

presenter = presenter.Presenter()
presenter.model = dataBase

app = application.Application()

app.presenter = presenter

app.run()

dataBaseFile = open(FILE_NAME, 'wb')
pickle.dump(dataBase, dataBaseFile)
dataBaseFile.close()
