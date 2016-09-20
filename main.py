import pickle
import application
import presenter
import view

from os.path import isfile

FILE_NAME = "cinemas.meldb"

if isfile(FILE_NAME):
    dataBaseFile = open(FILE_NAME, 'rb')
    dataBase = pickle.load(dataBaseFile)
    dataBaseFile.close()
else:
    dataBase = {'CINEMAS': list(), 'SESSIONS': list()}

presenter = presenter.Presenter()
view = view.View()

presenter.view = view
presenter.model = dataBase

app = application.Application()

app.presenter = presenter

app.run()

dataBaseFile = open(FILE_NAME, 'wb')
pickle.dump(dataBase, dataBaseFile)
dataBaseFile.close()
